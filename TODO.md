# RASCAL TODO

This file tracks implementation work and documentation updates so the repo stays aligned with actual behavior.

## P0: Immediate Priorities (Now)
- [x] README consistency pass against implemented backend and frontend routes/scripts
- [ ] Keep documentation aligned with implemented code paths and runtime behavior
- [ ] Update relevant README/documentation/TODO entries in the same change as implementation work
- [ ] Audit all docs in documentation/ for references to non-existent scripts, files, and endpoints
- [ ] Create a single "source of truth" run path in docs (ingest -> compile -> serve)
- [x] Every command in docs points to an existing script
- [x] Endpoint tables match implemented routes
- [x] Frontend docs references point to existing files

## P1: Architecture and Runtime Gaps
Derived from `documentation/GRAPH-ARCHITECTURE.md` normalization on 2026-07-07.

- [ ] Add `GET /graph_connection_explain` with deterministic local traversal fallback and stable response contract.
- [ ] Add first-class chunk-node graph projection from compiled wiki artifacts (not only document + inferred concept targets).
- [ ] Add materialized path snapshot generation (`kind=path`) with recompute metadata and TTL/expiry policy.
- [ ] Add concept/metadata node ingestion pipeline (explicit entities, not only inferred relationship targets).
- [ ] Add query-shape telemetry for graph/retrieval operations and a summary endpoint for index/refinement decisions.
- [ ] Add temporal graph versioning baseline (`valid_from`, `valid_to`, `changed_utc`, `change_reason`) for document and edge changes.

## P1: V1 Baseline Recovery Queue (Code-Loss Parity)
These items represent known V1 capabilities that are not fully present in the current branch and should be restored or replaced to re-establish the intended baseline.

- [ ] Curation operations dashboard: restore live feedback review data, status filtering, cited-document pills, triage outcomes, wiki draft proposal flow, override-needed/resolved handling, and curator audit trail.
- [ ] Knowledge quality and freshness tracking: restore freshness metadata, document-sidebar freshness display, live wiki-health panel, Mark Reviewed actions, curator notes, telemetry-driven recommendations, and graph analytics summaries.
- [ ] Stale-page detection: restore explicit freshness states/reason codes, policy controls, source-change probing hooks, and optional remediation queueing.
- [ ] Policy expiry/sunset tracking: restore expiry/expiring-soon signals, configurable expiry policies, UI triage cues, and scheduled remediation hooks.
- [ ] In-app source document viewer: restore citation actions, `GET /source_doc/{doc_id}`, source-artifact indexing, and structured rendering for processed source documents.
- [ ] Citation action styling normalization: restore and verify consistent citation action controls after source-viewer restoration.
- [ ] Local-mode answer fallback hardening: replace excerpt-style fallback behavior with answer-first fallback structure and add regression coverage.
- [ ] Graph contract + schema dictionary foundation: add `GRAPH_CONTRACT.md` and schema dictionary coverage with timestamp and temporal-window validation.
- [ ] Structured validation flags for ingest diagnostics: add stable validation warning codes, warning-code definitions, smoke aggregation, and optional CI thresholds.
- [ ] Idempotent upsert semantics for node/edge writes: restore deterministic edge storage identity/partitioning and add repeated-ingest regression tests.
- [ ] Retrieval guardrails baseline: restore configurable retrieval/answer guardrails, timeout fallback behavior, and evaluation coverage.
- [ ] Deterministic tie-break retrieval ranking: restore stable tie-break ordering across retrieval paths and verify provenance/review priority.
- [ ] Robust no-result fallback hierarchy: restore clarify/re-query/insufficient-evidence fallback stages and add fallback-stage metrics.

## P2: V1 Adaptation Queue
- [ ] Ingest and adapt v1 document: "Telemetry-Driven Index Refinement"
- [ ] For each migrated v1 document, produce a provider-open rewrite that:
  - removes provider-specific hard dependencies
  - preserves transferable architecture patterns and rationale
  - maps cloud-specific components to optional adapter equivalents
  - clearly labels baseline (local-first) vs optional enterprise adapters
  - status:
    - Graph Data Architecture migrated + rewritten
    - Telemetry-Driven Index Refinement pending migration + rewrite

## P2: Stack-Open Adaptation
- [ ] Continue simplifying the stack toward a local-first, provider-open baseline
- [ ] Review and reframe residual provider-specific assumptions as optional enterprise adapters where not required
- [ ] Classify remaining provider references as one of:
  - core baseline
  - open-tool adapter
  - enterprise adapter
  - legacy/stale
- [ ] Propose code abstraction points for provider-specific services
- [ ] Document migration notes for optional provider integrations

## P3: Metadata Suggestion Follow-Through
- [ ] Complete organization-specific OSS/legal sign-off for spaCy + selected model packages before production
- [ ] Evaluate quality using a real corpus sample and decide whether to keep/extend suggestion heuristics
- [ ] Optionally validate profile outcomes with installed models in environments where model downloads are allowed

## P3: Documentation and Governance Hygiene
- [ ] Add a lightweight changelog section in README for major behavior changes
- [ ] Every implementation change updates the relevant docs in the same pass
- [ ] Every referenced file path exists in this branch
- [ ] Output directories in docs match real outputs
- [ ] Add CONTRIBUTING guide for documentation update expectations
- [ ] Add a small "How to update TODO" section for consistency

## Completed Milestones

### Core Reimplementation
- [x] Reimplement real wiki-backed API behavior: make `/wiki_index`, `/wiki/{page_id}`, `/ask`, `/graph_map_data`, `/feedback`, and `/wiki` read from and write to actual local artifacts instead of hardcoded demo payloads.
- [x] Reimplement the retrieval layer: replace `backend/retrieval.py` placeholder behavior with local wiki/document retrieval, ranking, trace generation, and citation payload assembly.
- [x] Reimplement feedback and write-back persistence: store feedback events, persist saved analysis/wiki draft pages, refresh the wiki catalog after write-back, and ensure written pages can re-enter retrieval.
- [x] Reimplement remaining Curator Space backend routes: add `/feedback-propose-wiki`, `/triage_audit`, `/wiki_freshness`, `/lint/document`, `/cascade_status`, `/query_telemetry_summary`, `/graph_analytics_summary`, and `/wiki_mark_reviewed` or downgrade docs until those routes exist.
- [x] Fix and wire source traceability: make `config/source_url_map.json` valid JSON, load it in backend responses, and surface canonical source URLs in citations/UI.
- [x] Reimplement relationship metadata and HITL edge semantics: support rich relationship objects with `target`, `weight`, `confidence`, `human_reviewed`, and `provenance`, including default strength rules and reviewed-vs-provisional behavior.

### Environment Reliability
- [x] Install and verify ingestion dependencies in project `.venv`
- [x] Add an explicit docs note: run backend Python commands with `/workspaces/RASCAL/.venv/bin/python` (or activate `.venv`) to avoid missing-package errors

### V1 Adaptation
- [x] Ingest and adapt v1 document: "Graph Data Architecture"

### Stack-Open Foundation
- [x] Inventory provider-specific references in code and docs
- [x] Define minimal local-first baseline with zero cloud-provider lock-in
- [x] Document provider-open architecture tiers and adapter boundaries

### Metadata Suggestion Baseline
- [x] Add optional spaCy-based metadata suggestion script (`backend/suggest_metadata.py`)
- [x] Ensure suggestions are written to a separate file and never auto-overwrite curated metadata
- [x] Add model-profile selection flag (`framework-default`, `lightweight`, `balanced`, `high-accuracy`) for implementor context tuning
- [x] Add model availability check mode (`--check-models`) for environment validation before suggestion runs
- [x] Verify spaCy library licensing metadata and usage assumptions for framework distribution
- [x] Verify spaCy model-package licensing metadata and confirm local cost expectations (no per-call API billing)
- [x] Capture licensing/cost guidance in README and docs for implementors

## Notes
- Treat this TODO as a living file.
- Prefer small, verified updates and check off items only after code + docs are both validated.
