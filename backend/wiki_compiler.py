"""Thin compatibility wrapper for the wiki compilation workflow.

This module intentionally delegates to backend.compile_wiki.main so there is
only one implementation path for the wiki pipeline.
"""
from __future__ import annotations

try:
    from backend.compile_wiki import main as compile_main
except ModuleNotFoundError:  # pragma: no cover - direct script execution fallback
    from compile_wiki import main as compile_main


if __name__ == "__main__":
    compile_main()
