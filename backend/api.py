"""Lightweight local API for the RASCAL frontend shell.

This module provides a minimal app factory and a small built-in HTTP server so the
frontend can be exercised locally without requiring additional dependencies.
"""
from __future__ import annotations

import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
FRONTEND_DIR = ROOT / "frontend"


class RASCALApp:
    """Small route-aware app for serving the static UI and demo endpoints."""

    def __init__(self) -> None:
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
        payload = {
            "status": "healthy",
            "mode": "local",
            "grounding": "wiki-first",
            "summary": "A static demo shell is running with transparent trace-enabled UI.",
        }
        return self._json_response(payload)

    def wiki_index(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        payload = {
            "documents": [
                {
                    "id": "policy-handbook",
                    "title": "Policy Handbook",
                    "type": "policy",
                    "category": "policy",
                    "summary": "Core policy guidance for the knowledge base.",
                    "key_points": ["Human oversight", "Evidence-first response"],
                },
                {
                    "id": "review-workflow",
                    "title": "Review Workflow",
                    "type": "procedure",
                    "category": "concept",
                    "summary": "How answers are reviewed before they become reusable knowledge.",
                    "key_points": ["Trace review", "Feedback loop"],
                },
                {
                    "id": "source-map",
                    "title": "Primary Source Map",
                    "type": "primary-source",
                    "category": "primary-source",
                    "summary": "Links from this repo into the curated source corpus.",
                    "key_points": ["Source traceability", "Reference links"],
                },
            ]
        }
        return self._json_response(payload)

    def faq(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        return self._serve_file(FRONTEND_DIR / "faq.json", content_type="application/json")

    def graph_map_data(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        payload = {
            "nodes": [
                {"id": "doc-1", "label": "Policy Handbook", "group": "policy"},
                {"id": "doc-2", "label": "Review Workflow", "group": "concept"},
                {"id": "doc-3", "label": "Escalation Ladder", "group": "policy"},
            ],
            "edges": [
                {"from": "doc-1", "to": "doc-2", "type": "depends_on"},
                {"from": "doc-2", "to": "doc-3", "type": "related_to"},
            ],
        }
        return self._json_response(payload)

    def graph_map_page(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        return self._serve_file(FRONTEND_DIR / "graph_map.html")

    def feedback_review_page(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        return self._serve_file(FRONTEND_DIR / "feedback_review.html")

    def ask(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        body = self._read_json_body(request)
        question = (body or {}).get("question", "")
        payload = {
            "answer": f"A local demo answer for: {question}\n\nThis response is grounded in the curated wiki scaffold and shows why each claim is considered relevant.",
            "trace": {
                "summary": "The answer used a curated overview and cited wiki evidence.",
                "retrieved_docs": [
                    {
                        "doc_id": "policy-handbook",
                        "title": "Policy Handbook",
                        "type": "policy",
                        "combined_score": 0.94,
                        "excerpt": "The policy layer emphasizes transparent traceability and grounded answers.",
                        "source_file": "wiki/policy-handbook.md",
                    }
                ],
                "citations": [
                    {
                        "doc_id": "policy-handbook",
                        "type": "policy",
                        "confidence": "high",
                        "source_file": "wiki/policy-handbook.md",
                        "source_url": "https://example.org/policy-handbook",
                    }
                ],
            },
        }
        return self._json_response(payload)

    def feedback(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        return self._json_response({"ok": True, "message": "Feedback recorded locally for the demo shell."})

    def wiki(self, request: Any | None = None) -> tuple[int, str, dict[str, str], bytes]:
        body = self._read_json_body(request)
        title = (body or {}).get("title", "Analysis page")
        return self._json_response({"ok": True, "message": f"Saved a new wiki draft for {title}."})

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
        if path.startswith("/wiki/") and len(path.split("/")) > 2:
            page_id = path.split("/", 2)[2]
            return self._json_response({
                "title": page_id.replace("-", " ").title(),
                "summary": "This preview is served from the local demo backend.",
                "content": "# Preview\n\nThis page is intentionally scaffolded for the frontend experience.",
            })
        handler = self.routes.get((method, path))
        if handler is None:
            return HTTPStatus.NOT_FOUND, "Not Found", {"Content-Type": "text/plain"}, b"Not Found"
        return handler(request)

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
