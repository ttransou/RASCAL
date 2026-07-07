# RASCAL Graph Architecture

This document defines a normalized, stack-neutral graph contract for RASCAL.

The baseline is local-first and file-backed. Optional adapters can project the same contracts into local/open tools or managed enterprise platforms, but the core architecture should remain portable.

## Goals

- Keep document relationships explicit and inspectable.
- Support grounded retrieval and graph exploration with deterministic local behavior.
- Preserve trust signals (`weight`, `confidence`, `provenance`, `human_reviewed`) in edge payloads.
- Keep Human-in-the-Loop (HITL) decisions clear and auditable.

## Current Runtime Baseline (Implemented)

The current branch already supports:

- Document nodes derived from compiled wiki Markdown in `backend/wiki/`.
- Relationship edge normalization in `backend/relationships.py`.
- Graph payload output via `GET /graph_map_data` from `backend/api.py`.
- Lightweight graph health summary via `GET /graph_analytics_summary`.
- Relationship trust fields:
  - `weight`
  - `confidence`
  - `provenance`
  - `human_reviewed`
  - `review_state`

## Data Model

### Node Types

1. Document node
- Source: compiled Markdown page in `backend/wiki/*.md`
- Required baseline fields:
  - `id`
  - `label` (title)
  - `group` (category)

2. Concept placeholder node
- Source: relationship targets that are not explicit wiki documents.
- Used for graph continuity in map views.
- Required baseline fields:
  - `id`
  - `label`
  - `group` = `concept`

### Edge Types

Baseline relation types are corpus-defined and not globally fixed. Common examples:

- `requires`
- `depends_on`
- `related_to`

Each normalized edge should include:

- `source` (in API payload as `from`)
- `target` (in API payload as `to`)
- `type`
- `weight` (0.0 to 1.0)
- `confidence` (0.0 to 1.0)
- `provenance` (for example: `wiki_markdown`, `metadata_overrides`, `curator`)
- `human_reviewed` (`true` or `false`)
- `review_state` (`reviewed` or `provisional`)

## HITL Boundary

Automatic steps:

1. Parse wiki pages.
2. Parse relationship metadata.
3. Normalize edge fields and defaults.
4. Publish graph payloads for UI and downstream use.

HITL steps:

1. Confirm or reject high-impact relationships.
2. Raise confidence to reviewed values only after curator verification.
3. Mark `human_reviewed=true` intentionally, not implicitly.

## API Contract (Baseline)

### `GET /graph_map_data`

Returns:

- `nodes`: array of graph nodes.
- `edges`: array of directed edges with trust metadata.

This endpoint is used by `frontend/graph_map.html` and `frontend/graph_map.js`.

### `GET /graph_analytics_summary`

Returns a lightweight summary:

- `node_count`
- `edge_count`
- `isolated_node_count`
- `edge_types` (counts by relation type)

## Query and Traversal Guidance

Current local baseline uses single-hop relationships from compiled artifacts and lightweight derived analytics.

Future traversal expansion should be staged:

1. Add deterministic local multi-hop traversal helper.
2. Add explain endpoint for connection/path reasoning.
3. Add optional adapter-backed acceleration only after baseline contracts and tests are stable.

## Contract Extensions (Planned)

The following are intentionally documented as planned, not current behavior:

- Chunk nodes as first-class graph entities.
- Concept and metadata nodes from structured ingestion pipelines.
- Materialized path snapshots with recompute metadata.
- Temporal graph versioning (`valid_from`, `valid_to`, change history).
- Extended analytics (centrality, cluster detection, drift snapshots).

## Documentation-to-Implementation Diff (As of 2026-07-07)

The architecture intent currently exceeds implementation in these areas:

- No dedicated `GET /graph_connection_explain` endpoint yet.
- No materialized path document generation yet.
- No first-class chunk-node graph ingestion in runtime graph payload.
- No concept/metadata extraction pipeline writing canonical graph entities.
- No temporal versioning contract implemented in runtime storage.
- No query-shape telemetry stream for index/refinement decisions.

These are tracked as implementation TODO items in `TODO.md`.

## Normalization Rules for Future Updates

When updating this file:

- Keep sections tagged as either `Implemented` or `Planned` to avoid capability drift.
- Use stack-neutral wording; do not require named providers in baseline sections.
- Keep endpoint names and paths synchronized with `backend/api.py`.
- Update `TODO.md` in the same change if this doc adds or removes planned capabilities.
