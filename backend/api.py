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
    from .retrieval import LocalWikiRetriever, slugify
except ImportError:  # pragma: no cover - direct script execution fallback
    from retrieval import LocalWikiRetriever, slugify

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT / "frontend"
DEFAULT_WIKI_DIR = ROOT / "backend" / "wiki"
DEFAULT_FEEDBACK_LOG = ROOT / "backend" / "feedback.jsonl"


class RASCALApp:
    """Small route-aware app for serving the static UI and demo endpoints."""

    def __init__(
        self,
        *,
        wiki_dir: Path | None = None,
        feedback_log: Path | None = None,
    ) -> None:
        self.wiki_dir = wiki_dir or DEFAULT_WIKI_DIR
        self.feedback_log = feedback_log or DEFAULT_FEEDBACK_LOG
        self.retriever = LocalWikiRetriever(self.wiki_dir, repo_root=ROOT)
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
            ("POST", "/ask"): self.ask,
            ("POST", "/feedback"): self.feedback,
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
        event = {
            "id": datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f"),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "rating": body.get("rating"),
            "question": body.get("question"),
            "comment": body.get("comment", ""),
            "cited_docs": body.get("cited_docs", []),
        }
        self._append_jsonl(self.feedback_log, event)
        return self._json_response({"ok": True, "message": "Feedback recorded locally.", "event": event})

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

    def _json_response(self, payload: dict[str, Any]) -> tuple[int, str, dict[str, str], bytes]:
        body = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json", "Content-Length": str(len(body))}
        return HTTPStatus.OK, "OK", headers, body

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

    def _append_jsonl(self, path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("ab") as handle:
            line = json.dumps(payload, ensure_ascii=False).encode("utf-8") + b"\n"
            handle.write(line)

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
