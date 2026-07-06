# Stack-Open Architecture

RASCAL is moving toward a local-first, provider-open architecture.

This means the framework core should run without a cloud account, enterprise identity provider, hosted model endpoint, vector database, or managed graph database. Those systems can be valuable, but they are adapter choices rather than baseline requirements.

## Core Rule

The core runtime must work with local artifacts:
- source files in `raw/`
- extracted JSON in `backend/json/`
- compiled Markdown wiki pages in `backend/wiki/`
- deterministic retrieval in `backend/retrieval.py`
- API and static frontend from `backend/api.py` and `frontend/`
- file-backed feedback and write-back as the starter persistence model

If a feature cannot run without credentials, a cloud service, a proprietary SDK, or an enterprise control plane, it belongs behind an adapter boundary.

## Architecture Tiers

### 1. Framework Core

Always available and dependency-light:
- ingestion
- wiki compilation
- local retrieval
- trace and citation payloads
- feedback capture
- write-back to Markdown wiki pages
- static frontend
- local file-backed persistence

The core should prefer standard library behavior and small, portable dependencies.

### 2. Open Tool Adapters

Useful outside enterprise environments:
- local model servers such as Ollama, LM Studio, or other OpenAI-compatible endpoints
- local persistence through SQLite, DuckDB, JSONL, or plain files
- vector search through Chroma, Qdrant, LanceDB, or similar tools
- graph exploration through JSON graph files, NetworkX, Neo4j Community, or similar tools
- source movement through GitHub, Obsidian exports, Google Drive exports, or other user-controlled file workflows

These adapters should be optional and configured explicitly.

### 3. Enterprise Adapters

Useful when governance, identity, managed hosting, or existing document systems require them:
- Azure OpenAI or other approved hosted model providers
- Azure Blob or other object storage
- Cosmos DB, Azure AI Search, or other managed retrieval stores
- Entra ID or other identity providers
- SharePoint, Teams, Confluence, ServiceNow, or internal governed APIs

Enterprise adapters should not leak into core imports or quick-start requirements.

## Code Boundary Guidance

Core modules should not import provider-specific SDKs directly.

Preferred shape:
- `backend/retrieval.py` owns the local retrieval baseline.
- Future retrievers can live behind a retrieval boundary, for example `backend/retrievers/`.
- File-backed persistence should be the default before adding database adapters.
- Provider-specific configuration should be opt-in and fail closed when credentials are absent.
- Documentation should label provider paths as optional adapters, not required setup.

## Documentation Language

Use:
- local-first
- provider-open
- optional adapter
- enterprise adapter
- open-tool adapter
- no required cloud control plane
- no required model vendor

Avoid describing the framework baseline as Azure-centric, model-specific, or enterprise-only. It is accurate to say RASCAL began as an Azure-oriented experiment, but current framework direction is local-first and provider-open.
