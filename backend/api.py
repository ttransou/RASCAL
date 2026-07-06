"""Lightweight local API for the RASCAL frontend shell.

This module provides a minimal app factory and a small built-in HTTP server so the
frontend can be exercised locally without requiring additional dependencies.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

try:
    from .feedback_store import FeedbackStore
    from .retrieval import LocalWikiRetriever, slugify
    from .source_map import SourceUrlMap
except ImportError:  # pragma: no cover - direct script execution fallback
    from feedback_store import FeedbackStore
    from retrieval import LocalWikiRetriever, slugify
    from source_map import SourceUrlMap

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT / "frontend"
DEFAULT_WIKI_DIR = ROOT / "backend" / "wiki"
DEFAULT_FEEDBACK_LOG = ROOT / "backend" / "feedback.jsonl"
DEFAULT_SOURCE_MAP = ROOT / "config" / "source_url_map.json"


class RASCALApp:
    """Small route-aware app for serving the static UI and demo endpoints."""

    def __init__(
        self,
        *,
        wiki_dir: Path | None = None,
        feedback_log: Path | None = None,
        source_map_path: Path | None = None,
    ) -> None:
        self.wiki_dir = wiki_dir or DEFAULT_WIKI_DIR
        self.feedback_log = feedback_log or DEFAULT_FEEDBACK_LOG
        self.source_map_path = source_map_path or DEFAULT_SOURCE_MAP
        self.source_url_map = SourceUrlMap(self.source_map_path)
        self.retriever = LocalWikiRetriever(self.wiki_dir, repo_root=ROOT, source_url_map=self.source_url_map)
        self.feedback_store = FeedbackStore(self.feedback_log)
        self.routes: dict[tuple[str, str], Any] = self._register_routes()

    def _register_routes(self) -> dict[tuple[str, str], Any]:
        return {
            ("GET", "/"): self.index,
            ("GET", "/health"): self.health,
            ("GET", "/wiki_index"): self.wiki_index,
            ("GET", "/faq.json"): self.faq,
            ("GET", "/graph_map_data"): self.graph_map_data,
            ("GET", "/graph-map"): self.graph_map_page,
            ("GET", "/feedback-review"): self.feedback_review_page,
            ("GET", "/feedback-data"): self.feedback_data,
            ("GET", "/triage_audit"): self.triage_audit,
            ("GET", "/wiki_freshness"): self.wiki_freshness,
            ("GET", "/lint/document"): self.lint_document,
            ("GET", "/cascade_status"): self.cascade_status,
            ("GET", "/query_telemetry_summary"): self.query_telemetry_summary,
            ("GET", "/graph_analytics_summary"): self.graph_analytics_summary,
            ("POST", "/ask"): self.ask,
            ("POST", "/feedback"): self.feedback,
            ("POST", "/feedback-triage"): self.feedback_triage,
            ("POST", "/feedback-propose-wiki"): self.feedback_propose_wiki,
            ("POST", "/wiki_mark_reviewed"): self.wiki_mark_reviewed,
            ("POST", "/wiki"): self.wiki,
            ("GET", "/styles.css"): self.styles,
            ("GET", "/app.js"): self.app_js,
            ("GET", "/graph_map.js"): self.graph_map_js,
            ("GET", "/index.html"): self.index,
        }

    def index(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        return self._serve_file(FRONTEND_DIR / "index.html")

    def styles(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        return self._serve_file(FRONTEND_DIR / "styles.css", content_type="text/css")

    def app_js(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        return self._serve_file(FRONTEND_DIR / "app.js", content_type="application/javascript")

    def graph_map_js(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        return self._serve_file(FRONTEND_DIR / "graph_map.js", content_type="application/javascript")

    def health(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        docs = self.retriever.load_documents()
        payload = {
            "status": "healthy",
            "mode": "local",
            "grounding": "wiki-first",
            "summary": f"Local wiki API is running with {len(docs)} indexed wiki page(s).",
            "wiki_pages": len(docs),
        }
        return self._json_response(payload)

    def wiki_index(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        return self._json_response({"documents": self.retriever.load_documents()})

    def faq(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        return self._serve_file(FRONTEND_DIR / "faq.json", content_type="application/json")

    def graph_map_data(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        return self._json_response(self.retriever.graph_payload())

    def graph_map_page(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        return self._serve_file(FRONTEND_DIR / "graph_map.html")

    def feedback_review_page(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        return self._serve_file(FRONTEND_DIR / "feedback_review.html")

    def ask(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        body = self._read_json_body(request)
        question = (body or {}).get("question", "")
        retrieved_docs = self.retriever.retrieve(question)
        if not retrieved_docs:
            payload = {
                "answer": (
                    "## Summary\n\n"
                    "I could not find enough matching wiki evidence to answer from the local corpus.\n\n"
                    "## Supporting Evidence\n\n"
                    "- No compiled wiki pages matched the question."
                ),
                "trace": {
                    "summary": "No local wiki pages matched the question.",
                    "retrieved_docs": [],
                    "citations": [],
                },
            }
            return self._json_response(payload)

        citations = [
            {
                "doc_id": doc["id"],
                "title": doc["title"],
                "type": doc["type"],
                "confidence": "local-match",
                "source_file": doc["source_file"],
                "source_url": doc.get("source_url", ""),
            }
            for doc in retrieved_docs
        ]
        evidence_lines = [
            f"- {doc['title']}: {doc.get('excerpt') or doc.get('summary') or 'Matched local wiki content.'}"
            for doc in retrieved_docs
        ]
        payload = {
            "answer": (
                "## Summary\n\n"
                f"I found {len(retrieved_docs)} local wiki page(s) relevant to this question. "
                "The strongest matches are listed below so the answer remains inspectable.\n\n"
                "## Supporting Evidence\n\n"
                + "\n".join(evidence_lines)
            ),
            "trace": {
                "summary": "The answer used local compiled wiki pages ranked by lexical overlap.",
                "retrieved_docs": retrieved_docs,
                "citations": citations,
            },
        }
        return self._json_response(payload)

    def feedback(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        body = self._read_json_body(request)
        event = self.feedback_store.create(body)
        return self._json_response({"ok": True, "message": "Feedback recorded locally.", "event": event})

    def feedback_data(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        query = {}
        if request is not None:
            query = self._parse_query(request.path)
        events = self.feedback_store.list(status=query.get("status"), rating=query.get("rating"))
        return self._json_response({"events": events, "count": len(events)})

    def feedback_triage(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        body = self._read_json_body(request)
        feedback_id = str(body.get("id") or body.get("feedback_id") or "")
        status = str(body.get("status") or "")
        if not feedback_id or not status:
            return self._json_response({"ok": False, "message": "id and status are required."}, status=400)
        try:
            event = self.feedback_store.triage(
                feedback_id,
                status=status,
                curator_note=str(body.get("curator_note") or ""),
                linked_wiki_page=str(body.get("linked_wiki_page") or ""),
            )
        except ValueError as exc:
            return self._json_response({"ok": False, "message": str(exc)}, status=400)
        if event is None:
            return self._json_response({"ok": False, "message": "Feedback event not found."}, status=404)
        return self._json_response({"ok": True, "event": event})

    def feedback_propose_wiki(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        body = self._read_json_body(request)
        ids = [str(item) for item in body.get("ids", [])]
        events = self.feedback_store.list()
        selected = [event for event in events if not ids or event.get("id") in ids]
        if not selected:
            return self._json_response({"ok": False, "message": "No feedback events matched."}, status=404)

        title = str(body.get("title") or f"Feedback proposal {datetime.now(timezone.utc).strftime('%Y-%m-%d')}")
        lines = [f"# {title}", "", "## Feedback Signals", ""]
        for event in selected:
            lines.extend(
                [
                    f"- **Feedback ID**: {event.get('id')}",
                    f"  - Rating: {event.get('rating')}",
                    f"  - Question: {event.get('question')}",
                    f"  - Comment: {event.get('comment')}",
                ]
            )
        lines.extend(["", "## Draft Answer", "", "Curator should replace this section with a verified reusable answer."])
        proposal = {
            "title": title,
            "markdown": "\n".join(lines).strip() + "\n",
            "source_feedback_ids": [event.get("id") for event in selected],
        }
        return self._json_response({"ok": True, "proposal": proposal})

    def triage_audit(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        events = [
            event
            for event in self.feedback_store.list()
            if event.get("status") != "new" or event.get("curator_note") or event.get("linked_wiki_page")
        ]
        events.sort(key=lambda event: str(event.get("updated_at", "")), reverse=True)
        return self._json_response({"events": events, "count": len(events)})

    def wiki_freshness(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        reviews = self._load_review_metadata()
        pages = []
        now = datetime.now(timezone.utc)
        for doc in self.retriever.load_documents():
            path = self.wiki_dir / f"{doc['id']}.md"
            modified_at = datetime.fromtimestamp(path.stat().st_mtime, tz=timezone.utc) if path.exists() else now
            age_days = max((now - modified_at).days, 0)
            review = reviews.get(doc["id"], {})
            reviewed_at = review.get("reviewed_at", "")
            stale = age_days > 90 and not reviewed_at
            pages.append(
                {
                    "id": doc["id"],
                    "title": doc["title"],
                    "modified_at": modified_at.isoformat(),
                    "age_days": age_days,
                    "reviewed_at": reviewed_at,
                    "review_note": review.get("note", ""),
                    "freshness": "stale" if stale else "current",
                    "reasons": ["older_than_90_days"] if stale else [],
                }
            )
        return self._json_response({"pages": pages, "stale_count": sum(1 for page in pages if page["freshness"] == "stale")})

    def lint_document(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        query = self._parse_query(request.path) if request is not None else {}
        requested_id = query.get("id") or query.get("doc_id")
        docs = self.retriever.load_documents()
        if requested_id:
            docs = [doc for doc in docs if doc.get("id") == requested_id]
        results = []
        for doc in docs:
            errors = []
            warnings = []
            if not doc.get("title"):
                errors.append("missing_title")
            if not doc.get("summary"):
                warnings.append("missing_summary")
            if "## Source Extract" not in doc.get("markdown", ""):
                warnings.append("missing_source_extract_section")
            results.append({"id": doc.get("id"), "title": doc.get("title"), "errors": errors, "warnings": warnings})
        return self._json_response(
            {
                "documents": results,
                "error_count": sum(len(item["errors"]) for item in results),
                "warning_count": sum(len(item["warnings"]) for item in results),
            }
        )

    def cascade_status(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        return self._json_response(
            {
                "mode": "local",
                "available": False,
                "pending": 0,
                "message": "Cascade cleanup is not active in the local file-backed baseline.",
            }
        )

    def query_telemetry_summary(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        questions = [event.get("question", "") for event in self.feedback_store.list() if event.get("question")]
        terms: dict[str, int] = {}
        for question in questions:
            for token in question.lower().split():
                cleaned = "".join(ch for ch in token if ch.isalnum())
                if len(cleaned) < 3:
                    continue
                terms[cleaned] = terms.get(cleaned, 0) + 1
        top_terms = [{"term": term, "count": count} for term, count in sorted(terms.items(), key=lambda item: (-item[1], item[0]))[:10]]
        return self._json_response({"query_count": len(questions), "top_terms": top_terms})

    def graph_analytics_summary(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        graph = self.retriever.graph_payload()
        connected = {edge["from"] for edge in graph["edges"]} | {edge["to"] for edge in graph["edges"]}
        isolated = [node for node in graph["nodes"] if node["id"] not in connected]
        edge_types: dict[str, int] = {}
        for edge in graph["edges"]:
            edge_types[edge["type"]] = edge_types.get(edge["type"], 0) + 1
        return self._json_response(
            {
                "node_count": len(graph["nodes"]),
                "edge_count": len(graph["edges"]),
                "isolated_node_count": len(isolated),
                "edge_types": edge_types,
            }
        )

    def wiki_mark_reviewed(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        body = self._read_json_body(request)
        page_id = str(body.get("id") or body.get("page_id") or body.get("doc_id") or "")
        if not page_id:
            return self._json_response({"ok": False, "message": "id/page_id/doc_id is required."}, status=400)
        if self.retriever.get_page(page_id) is None:
            return self._json_response({"ok": False, "message": "Wiki page not found."}, status=404)
        reviews = self._load_review_metadata()
        reviews[page_id] = {
            "reviewed_at": datetime.now(timezone.utc).isoformat(),
            "note": str(body.get("note") or ""),
        }
        self._save_review_metadata(reviews)
        return self._json_response({"ok": True, "page_id": page_id, "review": reviews[page_id]})

    def wiki(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        body = self._read_json_body(request)
        title = (body or {}).get("title", "Analysis page")
        content = (body or {}).get("content", "")
        page = self._write_wiki_page(str(title), str(content), body)
        self.retriever.rewrite_index()
        return self._json_response(
            {
                "ok": True,
                "message": f"Saved a new wiki draft for {page['title']}.",
                "page": page,
            }
        )

    def _serve_file(self, path: Path, content_type: str = "text/html") -> tuple[int, str, dict[str, str], bytes]:
        body = path.read_bytes()
        headers = {"Content-Type": content_type, "Content-Length": str(len(body))}
        return HTTPStatus.OK, "OK", headers, body

    def _json_response(
        self,
        payload: dict[str, Any],
        *,
        status: int = HTTPStatus.OK,
    ) -> tuple[int, str, dict[str, str], bytes]:
        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json", "Content-Length": str(len(body))}
        try:
            reason = HTTPStatus(status).phrase
        except ValueError:
            reason = "OK"
        return status, reason, headers, body

    def _read_json_body(self, request: Any | None) -> dict[str, Any]:
        if request is None:
            return {}
        try:
            content_length = int(request.headers.get("Content-Length", "0"))
        except (TypeError, ValueError):
            content_length = 0
        if content_length <= 0:
            return {}
        raw = request.rfile.read(content_length).decode("utf-8")
        try:
            return json.loads(raw) if raw else {}
        except json.JSONDecodeError:
            return {}

    def _parse_query(self, path: str) -> dict[str, str]:
        parsed = urlparse(path)
        query: dict[str, str] = {}
        for part in parsed.query.split("&"):
            if not part:
                continue
            key, _, value = part.partition("=")
            query[unquote(key)] = unquote(value)
        return query

    def _review_metadata_path(self) -> Path:
        return self.wiki_dir / "review_metadata.json"

    def _load_review_metadata(self) -> dict[str, dict[str, str]]:
        path = self._review_metadata_path()
        if not path.exists():
            return {}
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
        return payload if isinstance(payload, dict) else {}

    def _save_review_metadata(self, payload: dict[str, dict[str, str]]) -> None:
        self.wiki_dir.mkdir(parents=True, exist_ok=True)
        self._review_metadata_path().write_text(json.dumps(payload, indent=2), encoding="utf-8")

    def dispatch(self, method: str, path: str, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        parsed_path = urlparse(path).path
        if parsed_path.startswith("/wiki/") and len(parsed_path.split("/")) > 2:
            page_id = unquote(parsed_path.split("/", 2)[2])
            page = self.retriever.get_page(page_id)
            if page is None:
                return HTTPStatus.NOT_FOUND, "Not Found", {"Content-Type": "text/plain"}, b"Wiki page not found"
            return self._json_response(page)
        handler = self.routes.get((method, parsed_path))
        if handler is None:
            return HTTPStatus.NOT_FOUND, "Not Found", {"Content-Type": "text/plain"}, b"Not Found"
        return handler(request)

    def _write_wiki_page(self, title: str, content: str, body: dict[str, Any]) -> dict[str, Any]:
        timestamp = datetime.now(timezone.utc)
        base_slug = slugify(title)
        slug = base_slug
        path = self.wiki_dir / f"{slug}.md"
        if path.exists():
            slug = f"{base_slug}-{timestamp.strftime('%Y%m%d%H%M%S')}"
            path = self.wiki_dir / f"{slug}.md"

        self.wiki_dir.mkdir(parents=True, exist_ok=True)
        lines = [
            f"# {title}",
            "",
            "## Metadata",
            f"- **type**: analysis",
            f"- **created_at**: {timestamp.isoformat()}",
        ]
        cited_docs = body.get("cited_docs") or body.get("citations") or []
        if cited_docs:
            lines.append(f"- **cited_docs**: {', '.join(str(doc) for doc in cited_docs)}")
        lines.extend(["", "## Source Extract", "", content.strip() or "No content provided."])
        path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")
        return {
            "id": slug,
            "title": title,
            "type": "analysis",
            "category": "concept",
            "source_file": str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else str(path),
        }

    def run(self, host: str = "127.0.0.1", port: int = 8000) -> None:
        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802
                self._dispatch()

            def do_POST(self) -> None:  # noqa: N802
                self._dispatch()

            def _dispatch(self) -> None:
                status_code, reason, headers, body = self.server.app.dispatch(self.command, self.path, self)  # type: ignore[attr-defined]
                self.send_response(status_code)
                self.send_header("Content-Type", headers.get("Content-Type", "text/plain"))
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
                return

        class Server(ThreadingHTTPServer):
            def __init__(self, server_address: tuple[str, int], handler_class: type[BaseHTTPRequestHandler]) -> None:
                super().__init__(server_address, handler_class)
                self.app = self.app  # type: ignore[attr-defined]

        server = ThreadingHTTPServer((host, port), Handler)
        server.app = self  # type: ignore[attr-defined]
        print(f"Serving RASCAL frontend at http://{host}:{port}")
        server.serve_forever()


def create_app() -> RASCALApp:
    return RASCALApp()


if __name__ == "__main__":
    create_app().run()
