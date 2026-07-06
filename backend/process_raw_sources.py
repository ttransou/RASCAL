"""Thin compatibility wrapper for the raw-source ingestion workflow.

This module intentionally delegates to backend.ingest.main so there is only
one implementation path for the ingestion pipeline.
"""
from __future__ import annotations

try:
    from backend.ingest import main as ingest_main
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback
    from ingest import main as ingest_main


if __name__ == "__main__":
    ingest_main()
