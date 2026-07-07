# Future Enhancements

The framework intentionally keeps the default operating model lightweight. The items below are optional maturity upgrades, not baseline requirements. Some will be added to a TODO to implement as development progresses. 

**Legend**

✅ - completed enhancement

🛠 - realistic short-term enhancement

👍 - nice-to-have enhancement

✨ - magical future enhancement


All enhancements are optional; however, the 🛠 realistic short-term enhancements will be implemented in the development process or judged optional and noted as such.



🛠 **Team governance and identity (optional):**
    
Add optional enterprise identity-provider authentication, role-based permissions (read, write, curate, admin), and curator workflow queues for teams that need stronger ownership, auditability, and controlled write-back. Not required for small teams or low-risk corpora; enable when complexity and governance needs increase.


🛠 **User-scoped session recap cache ("hot cache"):**
    
With user-level authentication enabled, maintain a short per-user recap at end-of-session boundaries to reduce repeat recap turns in the next session.
    
Attribution: concept inspiration from the community implementation: http://github.com/ScrapingArt/Karpathy-LLM-Wiki-Stack/tree/main ("hot cache" pattern).
    
Guardrails: human approval required before saving; skipped approval discards the draft; strict word limit; TTL/expiry with an explicit "starting over" notice after expiration; default overwrite behavior per user scope. 
    
Scope boundary: the recap cache is continuity-only and separate from canonical knowledge. This framework does not maintain transcript-style chat history; runtime context comes from retrieval and explicit, user-approved wiki write-back via canonical source workflows.


✨ **Multimodal image-heavy document ingestion (OCR + VLM, optional):**
    
Add OCR plus vision-language model processing for scanned/image-heavy PDFs and diagrams, with extracted visuals/figure references linked into wiki pages for click-to-view evidence.


🛠 **Curation operations dashboard (V1 baseline recovery target)**:
    
Target behavior: enrich negative feedback entries with `cited_docs` at capture time, and provide a triage dashboard (`/feedback-review`) that supports queue review, notes, and three outcomes: create Markdown wiki draft (`/feedback-propose-wiki`), flag override-needed, or mark resolved. Include status filtering, color-coded badges, cited-document pills, compact tooltips, and a Curator Audit Trail panel.


🛠 **Confidence-gated write-back proposals:**
    
Instead of fully manual write-back, answers that meet a quality threshold (e.g., a high grounding score and a sufficient citation count) are auto-proposed for write-back, but still require curator approval before the wiki is updated. This accelerates the compounding loop as good answers surface automatically rather than waiting for a curator to notice them, while keeping humans in the loop on every write.


🛠 **Knowledge quality and freshness tracking (V1 baseline recovery target):**
    
Target behavior: wiki pages expose freshness metadata (score/tier/stale reasons), freshness is visible in the document sidebar, FAQ includes explainability guidance, and Curator Space includes a live wiki-health panel plus one-click Mark Reviewed actions (with optional curator-note audit trail). Curator health should include telemetry-driven index recommendations and baseline graph analytics (`/query_telemetry_summary`, `/graph_analytics_summary`) with framework-level parameter defaults.


🛠 **Stale-page detection (V1 baseline recovery target):**
    
Target behavior: include explicit freshness states and reason codes (including source-vs-ingest-vs-review signals), configurable policy controls, and optional source-change probing hooks. Optional extension: automated re-run queueing and scheduled remediation workflows without a full rebuild.


🛠 **Conflict detection:**
    
Surface cases where two documents give contradictory answers to the same question (e.g., two versions of a policy disagree). Flag these pairs to curators before they reach users, so the knowledge base doesn't silently serve ambiguous or contradictory guidance.


🛠 **Policy expiry/sunset tracking (V1 baseline recovery target):**
    
Target behavior: freshness supports policy-expiry signals (including expiring-soon and expired states), configurable controls for expiry policies, and UI-visible expiry status cues for curator triage. Optional extension: scheduled remediation workflows (for example, auto-queueing expiring/expired policies for revalidation and refresh).


🛠 **Curation acceleration:**
    
Reduce the manual effort per feedback entry, e.g., by generating suggested edits from the LLM for the original Q&A pairs, applying one-click diffs to the relevant wiki page, and batch-triaging clusters of similar complaints. Keeps the curator queue draining faster than it fills.


✅ **AI-assisted curation suggestions (implemented, July 2026):**
    
The framework now includes an optional local NLP suggestion workflow via `backend/suggest_metadata.py` that drafts summary/key-point/entity/term suggestions from extracted JSON artifacts. Suggestions are output to a separate JSON file and are explicitly guardrailed as human-review-required (`do_not_auto_apply`, `human_review_required`) so curated metadata is never overwritten automatically.

Implemented details:
- model-profile selection for corpus/runtime context (`framework-default`, `lightweight`, `balanced`, `high-accuracy`)
- explicit model override support (`--model ...`)
- model availability check mode (`--check-models`) with deterministic fallback to `blank-en-sentencizer`
- local-first operation with no per-call API billing requirement for this feature

Optional follow-on work:
- corpus-level quality evaluation and heuristic tuning for suggestions
- organization-specific OSS/legal sign-off for selected model packages before production rollout


🛠 **Structured wiki diff on re-run:**
    
When source documents update and the pipeline re-runs, produce a per-page diff of what changed so curators review only the delta rather than the full page. Pairs naturally with stale-page detection; the queue item arrives with the diff already attached.


✨ **Federated AI service connectivity (API/MCP):**
   
Allow RASCAL to query approved internal AI services across teams or organizations through controlled API integrations and/or MCP tools, so external service outputs can enrich responses as advisory context. This is a governance-heavy direction and should be treated as its own PoC before any broad rollout.
    
Required guardrails: strict allowlists, role-based connector access, provenance tagging for each external result, policy-scoped routing, fail-closed behavior, and human approval before any write-back of externally sourced content into the canonical wiki knowledge.


✨ **Enterprise integration:**
   
Connectors to enterprise content systems (SharePoint, Confluence, ServiceNow) for automated source ingestion and push-back of curated wiki/pages; change-event webhooks to trigger incremental pipeline runs without manual intervention.
    
- SharePoint/Teams source sync: instead of manually placing files in `raw/`, auto-sync from the SharePoint or Teams library where documents already live and are maintained. The pipeline treats the library as the source of truth. New uploads and edits propagate automatically, and stale-page detection can compare against SharePoint's own version history rather than local file mod-dates.


👍 **Citation Export (Word/PDF):**
    
Generate a formatted answer + citations document for use in audits, formal handoffs, or presentations. Relevant for compliance domains where the answer needs to travel outside the UI. The report would include the question, answer, grounding status, cited source titles with URLS, and retrieval timestamp so recipients know exactly what the system knew and when.


👍 **SPARQL/ontology interoperability add-on (domain-specific):**
    
Keep the framework core domain-agnostic and lightweight, while allowing implementors to add RDF/OWL modeling and SPARQL query layers when their domain needs standards-based semantic interoperability, formal ontology alignment, or cross-graph federation. This should remain an extension path per implementation, not a baseline framework requirement.


👍 **Analytics and coverage:**
    
Surface corpus-level insights, which documents are never retrieved, which questions go unanswered ot return low-confidence answers, which wiki pages are most cited vs. never cited. Helps identify gaps to prioritize for authoring or re-ingestion rather than discovering them through user complaints.
   
- Query analytics view: add a lightweight dashboard showing most-queried concepts, most-cited documents, unanswered questions, and coverage gaps. Use local query telemetry artifacts and summary endpoints as the baseline source.


🛠 **In-app source document viewer (V1 baseline recovery target):**
    
Target behavior: citation cards in the chat panel offer three actions per cited document: open wiki entry, view source in-app, and source doc external link.
    
Target behavior: render processed source artifacts (headings, inline emphasis, and tables) from structured ingestion output. Add read-only API endpoint `GET /source_doc/{doc_id}` that resolves doc ID to a renderable payload.
   
The distinction between the two in-app views is intentional: the wiki model shows the curated, compiled knowledge layer; the source doc viewer shows what the original document actually says, so users can verify grounding without leaving the application.
    
To do: table of content/section jump for long documents, keyboard navigation between the two modals, deep-link support so a specific source document can be opened directly by URL.


🛠 **Citation action styling normalization (V1 baseline recovery target):**
   
The three citation actions (open wiki entry, view source, raw/source doc 🡕) should share one consistent button/link style system for typography, spacing, border treatment, and hover/focus behavior. This avoids mixed-control appearance in citation drawers and improves scannability for non-technical users.
    
Planned: optional visual differentiation by action intent (for example, neutral for in-app actions and subtle outbound accent for external-link actions) if product design later wants stronger affordance separation.


🛠 **Local-mode answer fallback hardening (V1 baseline recovery target):**
   
Target behavior: local retrieval mode does not return excerpt-only output as the primary response in normal question flows. The fallback returns a direct answer structure (Summary, Key Rules or Thresholds, Supporting Evidence) so framework behavior stays answer-first even when optional model-backed synthesis is disabled or unavailable.
   
Planned: add regression coverage to lock this behavior for framework starter projects and prevent reintroduction of excerpt-only answer templates.


🛠 **Graph contract + schema dictionary foundation (V1 baseline recovery target):**
   
Framework-level graph structure should be documented explicitly in GRAPH_CONTRACT.md (schema versioning policy, canonical ID/key rules, invariant, advisory-vs-strict enforcement model, and valid/invalid examples). A new code-side dictionary module `backend/graph_schema.py` centralizes schema constants used by validators and smoke checks (field sets, strength ranges/defaults, canonical edge keying).
   
Also, strict write-path validation should include ISO-8601 timestamp normalization/rejection and temporal ordering checks for edge windows (effective_date ⇐ depreciated_date).
    
Addition: add schema-version checks in more API write surfaces.


🛠 **Structured validation flags for ingest diagnostics (V1 baseline recovery target):**
    
Advisory/strict edge validation should emit stable machine-readable warning codes (for example: EDGE_MISSING_STRUCTURAL, EDGE_WEIGHT_CLAMPED, EDGE_DUPLICATE_SKIPPED) in `backend/graph_ingest.py`, with code definitions in `backend/graph_schema.py`. This enables cleaner telemetry aggregation and future dashboarding without changing existing validation semantics.
   
Additionally: aggregate warning-code counts in smoke output and add optional per-code thresholds in CI.
    
    
🛠 **Idempotent upsert semantics for node/edge writes (V1 baseline recovery target):**
   
Target behavior: graph ingest uses deterministic edge storage identity and partitioning (edge_storage_id, edge_partition_key) derived from canonical logic edge keys, and normalizes write-path identifiers before upsert. Re-running ingestion with equivalent input converges to stable graph storage identities instead of drifting due to formatting differences.
    
Additionally, add a repeated-ingest regression test harness to automatically assert stable counts/IDs across back-to-back runs.


🛠 **Retrieval guardrails baseline (V1 baseline recovery target):**
    
Target behavior: the /ask path applies explicit guardrails for retrieval and response shaping: top_k/keyword_k ceilings, seed-id and neighbor fan-out caps, traversal depth limit, request timeout budget, and context/answer size ceilings. Guardrails are configurable via ASK/* environment variables and include safe timeout fallback behavior when the budget is exceeded before synthesis.
    
Additionally, add a deterministic evaluation set and compare quality/latency before vs after guardrail tuning.


🛠 **Deterministic tie-break retrieval ranking (V1 baseline recovery target):**
   
Target behavior: retrieval ranking resolves ties deterministically using stable priority order: human_reviewed first, curated provenance/status second, then numeric relevance scores (combined_score, vector_score, keyword_score) and stable ID fields. This applies to local and adapter-backed retrieval paths to reduce ranking jitter among equivalent-score candidates.
    
Additionally, enrich source artifacts with stronger review/provenance coverage so tie-break priority has a broader effect beyond score-level ordering.


🛠 **Robust no-result fallback hierarchy (V1 baseline recovery target):**
   
Target behavior: /ask uses staged fallback behavior in local wiki, local chunk, and adapter-backed retrieval paths: (1) clarify when query intent is ambiguous, (2) run one targeted re-query pass using signal-heavy query terms when grounding is weak/no-match, and (3) return explicit insufficient-evidence guidance if grounding remains weak after retry. This reduces attempts at weakly grounded answers while preserving actionable next-step prompts for users.
    
Additionally, add evaluation-set metrics for fallback-stage hit rates (clarify, requery, insufficient) to tune thresholds.
