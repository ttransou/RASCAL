"""Local file-backed feedback workflow storage.

Feedback is operator workflow data, not canonical knowledge. Canonical knowledge
enters the wiki only through explicit write-back routes.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_STATUS = "new"
VALID_STATUSES = {"new", "reviewed", "proposed_wiki", "resolved"}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def feedback_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")


class FeedbackStore:
    """Append-friendly JSONL store with rewrite-on-triage updates."""

    def __init__(self, path: Path) -> None:
        self.path = path

    def create(self, payload: dict[str, Any]) -> dict[str, Any]:
        event = self.normalize_event(payload)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("ab") as handle:
            handle.write(json.dumps(event, ensure_ascii=False).encode("utf-8") + b"\n")
        return event

    def list(self, *, status: str | None = None, rating: str | None = None) -> list[dict[str, Any]]:
        events = self.read_all()
        if status:
            events = [event for event in events if event.get("status") == status]
        if rating:
            events = [event for event in events if event.get("rating") == rating]
        return events

    def triage(
        self,
        feedback_id_value: str,
        *,
        status: str,
        curator_note: str = "",
        linked_wiki_page: str = "",
    ) -> dict[str, Any] | None:
        if status not in VALID_STATUSES:
            raise ValueError(f"Unsupported feedback status: {status}")

        events = self.read_all()
        updated: dict[str, Any] | None = None
        for event in events:
            if event.get("id") != feedback_id_value:
                continue
            event["status"] = status
            event["curator_note"] = curator_note
            if linked_wiki_page:
                event["linked_wiki_page"] = linked_wiki_page
            event["updated_at"] = utc_now()
            updated = event

        if updated is None:
            return None

        self.write_all(events)
        return updated

    def read_all(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []

        events: list[dict[str, Any]] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            try:
                payload = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(payload, dict):
                events.append(self.normalize_event(payload, preserve_id=True))
        return events

    def write_all(self, events: list[dict[str, Any]]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        lines = [json.dumps(event, ensure_ascii=False) for event in events]
        self.path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")

    def normalize_event(self, payload: dict[str, Any], *, preserve_id: bool = False) -> dict[str, Any]:
        created_at = str(payload.get("created_at") or utc_now())
        event = {
            "id": str(payload.get("id") or feedback_id()) if preserve_id else feedback_id(),
            "created_at": created_at,
            "updated_at": str(payload.get("updated_at") or created_at),
            "rating": payload.get("rating"),
            "question": payload.get("question", ""),
            "answer": payload.get("answer", ""),
            "comment": payload.get("comment", ""),
            "cited_docs": payload.get("cited_docs", []),
            "trace": payload.get("trace", {}),
            "status": payload.get("status") or DEFAULT_STATUS,
            "curator_note": payload.get("curator_note", ""),
            "linked_wiki_page": payload.get("linked_wiki_page", ""),
        }
        if event["status"] not in VALID_STATUSES:
            event["status"] = DEFAULT_STATUS
        return event
