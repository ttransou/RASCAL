# Backend Guide

This folder contains the local-first backend runtime used by RASCAL.

## Core Scripts

- `backend/process_raw_sources.py`
	- Extract supported source documents into JSON artifacts.
- `backend/wiki_compiler.py`
	- Compile extracted JSON plus metadata overrides into wiki Markdown pages.
- `backend/api.py`
	- Serve the static frontend and local API endpoints.
- `backend/suggest_metadata.py`
	- Optional local metadata suggestion helper.

## Core Modules

- `backend/retrieval.py`
	- Local wiki retriever, ranking, wiki parsing, and graph payload helpers.
- `backend/relationships.py`
	- Relationship normalization and HITL edge semantics (`weight`, `confidence`, `provenance`, `human_reviewed`).
- `backend/feedback_store.py`
	- File-backed feedback persistence and triage workflow updates.
- `backend/source_map.py`
	- Source URL resolution for citation traceability.

## Local Run Path

Use the project virtual environment:

```bash
/workspaces/RASCAL/.venv/bin/python backend/process_raw_sources.py raw --output-root backend/json
/workspaces/RASCAL/.venv/bin/python backend/wiki_compiler.py raw --output-root backend/json --wiki-root backend/wiki
/workspaces/RASCAL/.venv/bin/python backend/api.py
```

## Tests

Backend tests currently include:

- `backend/test_api_wiki.py`
- `backend/test_compile_wiki.py`
- `backend/test_feedback_store.py`
- `backend/test_relationships.py`
- `backend/test_retrieval.py`
- `backend/test_source_map.py`
