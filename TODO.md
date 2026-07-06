# RASCAL TODO

This file tracks implementation work and documentation updates so the repo stays aligned with actual behavior.

## Current Focus
- [ ] Keep documentation aligned with implemented code paths and runtime behavior
- [ ] Update relevant README/documentation/TODO entries in the same change as implementation work
- [ ] Continue simplifying the stack toward a local-first, provider-open baseline
- [ ] Review and reframe residual Azure-specific assumptions as optional enterprise adapters where not required

## In Progress
- [ ] README consistency pass against implemented backend and frontend routes/scripts

## Highest Priority Reimplementation
These items are documented as core RASCAL behavior in `README.md` and `documentation/`, but the current branch only has scaffold/demo implementations or placeholders.

- [x] Reimplement real wiki-backed API behavior: make `/wiki_index`, `/wiki/{page_id}`, `/ask`, `/graph_map_data`, `/feedback`, and `/wiki` read from and write to actual local artifacts instead of hardcoded demo payloads.
- [x] Reimplement the retrieval layer: replace `backend/retrieval.py` placeholder behavior with local wiki/document retrieval, ranking, trace generation, and citation payload assembly.
- [x] Reimplement feedback and write-back persistence: store feedback events, persist saved analysis/wiki draft pages, refresh the wiki catalog after write-back, and ensure written pages can re-enter retrieval.
- [x] Reimplement remaining Curator Space backend routes: add `/feedback-propose-wiki`, `/triage_audit`, `/wiki_freshness`, `/lint/document`, `/cascade_status`, `/query_telemetry_summary`, `/graph_analytics_summary`, and `/wiki_mark_reviewed` or downgrade docs until those routes exist.
- [x] Fix and wire source traceability: make `config/source_url_map.json` valid JSON, load it in backend responses, and surface canonical source URLs in citations/UI.
- [x] Reimplement relationship metadata and HITL edge semantics: support rich relationship objects with `target`, `weight`, `confidence`, `human_reviewed`, and `provenance`, including default strength rules and reviewed-vs-provisional behavior.

## Environment Reliability
- [x] Install and verify ingestion dependencies in project `.venv`
- [ ] Add an explicit docs note: run backend Python commands with `/workspaces/RASCAL/.venv/bin/python` (or activate `.venv`) to avoid missing-package errors

## Next Up
- [ ] Audit all docs in documentation/ for references to non-existent scripts, files, and endpoints
- [ ] Create a single "source of truth" run path in docs (ingest -> compile -> serve)
- [ ] Add a lightweight changelog section in README for major behavior changes

## Originally Implemented Enhancement Reconciliation
These items are marked "originally implemented" in `documentation/FUTURE-ENHANCEMENTS.md`, but this branch needs verification or reimplementation before the docs can claim them as current behavior.

- [ ] Curation operations dashboard: restore live feedback review data, status filtering, cited-document pills, triage outcomes, wiki draft proposal flow, override-needed/resolved handling, and curator audit trail. Current branch only serves a scaffolded `/feedback-review` page and accepts `/feedback` without persistence.
- [ ] Knowledge quality and freshness tracking: restore freshness metadata, document-sidebar freshness display, live wiki-health panel, Mark Reviewed actions, curator notes, telemetry-driven recommendations, and graph analytics summaries. Current branch has static copy only.
- [ ] Stale-page detection: restore explicit freshness states/reason codes, policy controls, source-change probing hooks, and optional remediation queueing.
- [ ] Policy expiry/sunset tracking: restore expiry/expiring-soon signals, configurable expiry policies, UI triage cues, and scheduled remediation hooks.
- [ ] In-app source document viewer: restore citation actions, `/source_doc/{doc_id}`, source-artifact indexing, and structured rendering for processed source documents. Current branch only opens wiki preview modals.
- [ ] Citation action styling normalization: restore and verify consistent citation action controls after the source viewer/citation actions are back in place.
- [ ] Local-mode answer fallback hardening: replace local demo/excerpt-style fallback behavior with answer-first fallback structure and add regression coverage.
- [ ] Graph contract + schema dictionary foundation: restore `GRAPH_CONTRACT.md`/schema dictionary coverage, strict timestamp and temporal-window validation, and schema-version checks across write surfaces.
- [ ] Structured validation flags for ingest diagnostics: restore stable validation warning codes, warning-code definitions, smoke aggregation, and optional CI thresholds.
- [ ] Idempotent upsert semantics for node/edge writes: restore deterministic graph edge storage identity/partitioning and add repeated-ingest regression tests.
- [ ] Retrieval guardrails baseline: restore configurable retrieval/answer guardrails, timeout fallback behavior, and evaluation coverage.
- [ ] Deterministic tie-break retrieval ranking: restore stable tie-break ordering across local/cloud retrieval paths and verify provenance/review priority.
- [ ] Robust no-result fallback hierarchy: restore clarify/re-query/insufficient-evidence fallback stages and add metrics for fallback-stage hit rates.

## Stack-Open Adaptation
- [x] Inventory Azure-specific references in code and docs
- [x] Define minimal local-first baseline with zero cloud-provider lock-in
- [x] Document provider-open architecture tiers and adapter boundaries
- [ ] Classify remaining provider references as one of:
  - core baseline
  - open-tool adapter
  - enterprise adapter
  - legacy/stale
- [ ] Propose code abstraction points for provider-specific services
- [ ] Document migration notes for optional provider integrations

## Documentation Reality Checklist
- [ ] Every implementation change updates the relevant docs in the same pass
- [ ] Every command in docs points to an existing script
- [ ] Every referenced file path exists in this branch
- [ ] Endpoint tables match implemented routes
- [ ] Output directories in docs match real outputs
- [ ] Frontend docs references point to existing files

## Nice-to-Have
- [ ] Add CONTRIBUTING guide for documentation update expectations
- [ ] Add a small "How to update TODO" section for consistency

## Notes
- Treat this TODO as a living file.
- Prefer small, verified updates and check off items only after code + docs are both validated.
