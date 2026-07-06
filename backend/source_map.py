"""Source URL mapping for local citation traceability."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class SourceUrlMap:
    """Resolves canonical source URLs by document id, source file, or title."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path
        self.by_doc_id: dict[str, str] = {}
        self.by_source_file: dict[str, str] = {}
        self.by_title: dict[str, str] = {}
        if path is not None:
            self.load(path)

    def load(self, path: Path) -> None:
        if not path.exists():
            return
        payload = json.loads(path.read_text(encoding="utf-8"))
        self.by_doc_id = self._clean_mapping(payload.get("by_doc_id", {}))
        self.by_source_file = self._clean_mapping(payload.get("by_source_file", {}))
        self.by_title = self._clean_mapping(payload.get("by_title", {}))

    def resolve(self, *, doc_id: str = "", source_file: str = "", title: str = "") -> str:
        candidates = [
            (self.by_doc_id, doc_id),
            (self.by_source_file, source_file),
            (self.by_source_file, Path(source_file).name if source_file else ""),
            (self.by_title, title),
        ]
        for mapping, key in candidates:
            if not key:
                continue
            value = mapping.get(key) or mapping.get(key.lower())
            if value:
                return value
        return ""

    def _clean_mapping(self, payload: Any) -> dict[str, str]:
        if not isinstance(payload, dict):
            return {}
        mapping: dict[str, str] = {}
        for key, value in payload.items():
            if not isinstance(key, str) or not isinstance(value, str):
                continue
            mapping[key] = value
            mapping[key.lower()] = value
        return mapping
