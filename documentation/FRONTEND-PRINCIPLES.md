# Frontend Guide
This guide is part of the RASCAL Framework. For conceptual framing, refer to `/WHITEPAPER.md`.
This frontend is a static HTML/CSS/JS client designed for wiki-first transparency. It is intentionally simple to run and intentionally rich in explainability.

**Human Curation Marker**
Any line prefixed with 🧠 marks a required dataset/domain customization touchpoint.


## Files
- `index.html`: app shell, brand panel, chat panel, trace panel, wiki catalog viewport, FAQ viewport, model
- `app.js`: API orchestration, Markdown rendering, trace/citation rendering, catalog filtering, FAQ template rendering, feedback/write-back actions, theme mode handling
- `graph_map.html`: relationship map shell, filters, focus controls, map status, template-state note
- `graph_map.js`: graph fetch/render orchestration, filter logic, focus subgraph behavior, map state persistence, shared theme-mode sync
- `styles.css`: visual system, layout, responsiveness, component states
- `faq.json`: editable FAQ template source rendered in the in-app FAQ viewport
- `feedback_review.html`: standalone feedback inspection UI


## Required to Run vs. Optional to Customize
For reuse, it is useful to distinguish the minimum frontend contract from the parts intended for white-labeling or domain adaptation.

*Insert Mermaid Diagram*


## Required to Run
For the main chat UI to work as implemented, the frontend needs:
- `index.html`, `app.js`, and `styles.css` are served by the backend
- GET/ to serve the chat shell


## Design Intent
The UI is built around a different assumption than typical RAG chat interfaces.

In many RAG apps, users see a polished answer and a small source list. In RASCAL, users see the working surface of the system:
- Which wiki pages were retrieved
- why those pages were considered relevant (scores and excerpts)
- where each claim can be traced back (source links)
- How user feedback can directly improve the wiki

This reinforces the LLM Wiki model: the wiki is a maintained knowledge layer, not a hidden retrieval cache.


## Information Architecture
The interface has three persistent regions:
- left panel: identity, health status, navigation actions
- center panel: conversation, wiki documents viewport, and FAQ viewpoint
- right panel: retrieval trace, chunks, citations, and run-status metadata
This layout ensures that transparency data remains visible during question answering rather than being buried behind a secondary screen.


## Transparency Features
### 1) Wiki Trace Panel
The trace panel shows retrieval evidence used for each answer:
- retrieved wiki chunks
- per-chunk `combined_score`
- excerpt preview and page metadata
- citation cards with `doc_id`, `type`, `confidence`, `source_file`, and source URL
It also shows run metadata badges such as mode, grounding status, and table-related signals.

### 2) Wiki Documents Catalog
The catalog lets users browse what knowledge exists before they ask:
- category tabs (example: all, policies, concepts, primary sources)
- expand all/collapse all controls
- search toggle with inline search field
- text search across title, IDs, type, summary, key points, markdown
- GET/health for the health pill
- POST/ask for question answering
- GET/wiki_index with /wiki-index fallback for the wiki catalog
- GET/wiki/{page_id} for the wiki modal and internal page links
For optional surfaces to work, the backend must also provide:
- GET/graph-map and GET/graph_map_data for the relationship map
- POST/feedback, GET/feedback-data, and GET/feedback-review for the feedback workflow and review dashboard
- POST/feedback-triage, POST/feedback-propose-wiki, and GET/triage_audit for curator triage actions and audit visiblitiy
- GET/wiki_freshness, GET/lint/document, GET/cascade_status, GET/query_telemetry_summary, and GET/graph_analytics_summary for Curator Space health/analysis cards
- POST/wiki_mark_reviewed for one-click stale-page recertification from Curator Space
- POST/wiki for save-to-wiki behavior

### 🧠 Optional to Customize
🧠 These are the main frontend reuse levers:
- branding and visible copy in `index.html`
- category mapping, external links, and API behavior in `app.js`
- layout and visual identity in `style.css`
    - graph map interaction defaults in `graph_map.html` and `graph_map.js`
    - feedback review presentation in `feedback_review.html`

### Local UI State
The frontend persists a small amount of browser-local state with `localStorage`:
- main left panel collapsed/expanded state
- trace panel collapsed/expanded state
- theme mode (default|light|dark) via uiThemeMode
- relationship map filter, focus, and layout state
The relationship map reads the same uiThemeMode key, so contrast/theme behavior is consistent between the chat shell and map surface.
This is useful for operator workflows, but it also means that UI state can persist across page reloads during testing.
- expandable Markdown previews
- open wiki page action
- source document link when available
This is important for scope transparency: users can inspect corpus coverage directly.

### 2b) FAQ Viewport (template-backed)
The FAQ entry in the left panel opens in an in-app FAQ surface in the center viewport:
- content is loaded from `frontend/faq.json`
- sections and entries are intentionally editable for domain onboarding
- empty sections are supported to stage future content
This provides a starter framework for organization-specific guidance without changing backend routes.

### 3) Inline Answer Transparency
Answering rendering supports:
- headings, lists, tables, code, inline emphasis
- internal policy/document links formatted as buttons that open wiki pages
- external links rendered as external anchors
This reduces context switching and keeps answer exploration interactive.

### 4) Relationship Map Transparency
The relationship map provides users with a graph-style view of how the knowledge layer can be navigated.
This implemented map UI also supports:
- document-only vs full-structure presets
- node-group filters and edge-type filters
- focused subgraphs at 1-3 hops from a selected node
- persisted layout and filter state between reloads
Right now, that view is intentionally templated. Until a real corpus is ingested, the graph uses scaffolded example nodes and edges so the interaction model can be demonstrated without implying that the current graph reflects live source-document relationships.

🧠 Customization point: replace template node/edge assumptions with your curated relationship semantics before production release.

### 5) Feedback and Write-Back Loop (Core Capability)
This is not a nice-to-have feature. It is the primary mechanism that turns the assistant from a static Q&A interface into a compounding knowledge system.
Every assistant message supports:
- thumbs up/down rating
- optional comment capture on downvote
- save-to-wiki action after positive feedback
When to save-to-wiki is used, the answer is persisted as an analysis wiki page and re-enters the retrieval surface for future questions.


## Explicit Feedback → Write-Back Flow
1) users ask a question (POST/ask)
2) UI renders answer plus trace/citations
3) user evaluates quality:
    - thumbs down → POST/feedback with optional comment
    - thumbs up → POST/feedback and enable Save to Wiki
4) user clicks Save to Wiki → POST/wiki
5) API stores a new analysis wiki page linked to the source question and cited pages
6) Wiki catalog refreshes the UI
7) Future retrieval can select this newly created page
In short: good answers are promoted into reusable knowledge, and weak answers generate actionable feedback


## Why Feedback-to-Wiki Matters
In a conventional chatbot, feedback is often telemetry only. Here, feedback can mutate the knowledge layer:
1) user asks a question
2) The system retrieves wiki pages and synthesizes an answer
3) user validates quality with feedback
4) The high-value answer is written back to the wiki
5) Future retrieval can reuse this newly created page.

Benefits:
- higher recall for recurring questions
- explicit human validation before persistence
- clearer audit trail from curated sources to synthesized pages


## Why This is Extremely Important
Without write-back, each high-quality answer is ephemeral: it helps one user once and disappears. With write-back, validated answers become shared memory.

That has a direct product impact:
- less repeated synthesis for the same question classes
- faster convergence on high-value institutional knowledge
- clearer separation between "model-generated once" and "human-validated and retained"
- a practical path from daily usage to a stronger, curated  wiki
This feature is the operational bridge between assistant use and continuous knowledge base improvement.


## Operational Guidance
Treat feedback and write-back as an editorial workflow, not just UI clicks:
- review downvote comments regularly in `feedback_review.html`
- identify repeated failure themes (missing policy page, weak summary, wrong type tagging)
- curate source/metadata issues in upstream pipeline files
- promote only high-signal answers with Save to Wiki
- periodically review newly created analysis pages for consolidation or refinement
The healthiest deployments use this loop continuously, not occasionally.


## Type Taxonomy and Corpus Customization
Taxonomy should match domain language, not generic defaults.
Flow of type:
- extraction infers an initial type
- `metadata_overrides.json` can override/refine the type
- `wiki_compiler.py` uses type to bucket wiki pages
- `app.js` normalized type to UI tab categories

Examples of type sets by domain:
- compliance: policy, procedure, control, requirement, form
- healthcare: guideline, protocol, workflow, faq, checklist
- engineering: architecture, pattern, troubleshooting, tutorial, reference
- legal: contract, amendment, addendum, precedent, template
- finance: regulation, underwriting guideline, risk policy, rate schedule


## Customizing Type Mapping
To adapt tabs for a new corpus:
1) Set domain-appropriate type values in `metadata_overrides.json`
2) updated `normalizeWikiDocCategory` in `app.js`
3) align tab buttons in `index.html` with those mapped categories
4) optionally add category-specific badge styling in `style.css`


## Quick Customization Playbook
### Branding and Prompting
Edit `index.html` for:
- assistant name and subtitle
- navigation labels
- query placeholder text tuned to the corpus vocabulary

### External and Corpus Links
Edit `app.js` for:
- `docLink` behavior if you want the left-nav document action to do something other than open the in-app wiki catalog
- `mapLink.href`
- `faqLink` behavior (if you want a different FAQ experience than the in-app template viewport)
Note: in the current implementation, `docLink` intentionally opens the in-app wiki catalog rather than navigating to an external URL.

### Theme Mode
The left panel includes a compact single-button glyph toggle that cycles:
- default (follow system preference)
- light
- dark
Theme mode is persisted in `localStorage` under `uiThemeMode` and reused by `graph_map.html/graph_map.js` and `graph_map.js` to maintain cross-page context consistency.

### Richer Metadata in UI
If the backend includes additional fields (for example, approval status, owner, version):
- add fields to catalog and citation rendering in `app.js`
- style these fields in `styles.css`

### Multilingual Adpatation
For multi-region use, add a language selector and text dictionary in `app.js`, then swap static labels at render time. Retrieval and trace behavior can remain unchanged if API fields stay stable.


## White-Label Checklist
Use this as a short rollout checklist when reusing the frontend for a new corpus, business unit, area, or internal product/project.

### Branding
1) Update the assistant name, subtitle, and visible navigation labels in `index.html`
2) Replace placeholder external destinations such as `reqLink.href` in `app.js`
3) Adjust visual identity in `styles.css` if the deployment needs different colors, spacing, or typography.

### Taxonomy Remapping
1) Confirm the corpus type values you want surfaced in the UI
2) updated `normalizeWikiDocCategory` in `app.js` to map those types into the tab model
3) align the tab labels in `index.html` with the categories you actually expose
4) Add or adjust badge styling in `style.css` if the new categories need distinct visual treatment.

### Route Integration
1) Confirm the backend serves the required chat routes: /, /health, /ask, /wiki_index. and /wiki/{page_id}
2) If you are enabling the relationship map, verify /graph-map and /graph_map_data
3) If you are enabling operator review workflows, verify /feedback, /feedback-data, /feedback-reivew, /feedbac-triage, /feedback-propose-wiki, and /triage_audit
4) If you are enabling Curator Space health cards, verify /wiki_freshness, /lint/document, /cascade_status, /query_telemetry_summary, /graph_analytics_summary, and /wiki_marked_reviewed
5) Decide whether the left-nav document action should continue to open the in-app wiki catalog or be replaced with a specific destination.


## Feedback Review Surface
`feedback_review.html` provides lightweight operational visibility into:
- rating direction trends
- common complaint themes from comments
- repeated question/answer patterns
- potential wiki coverage gaps
- wiki freshness and state-page triage
- telemetry-driven index tuning priorities
- graph connectivity health (connectors, isolation, components)
Use this view to prioritize curation and decide what should be formalized as wiki content.

Current Curator Space UX notes:
- key guidance is intentionally moved into compact hover ❔ tips to reduce visual clutter while preserving operator instructions
- Top Index Recommendations includes a Copy tuning request action to hand off prioritized tuning work to engineering
- state-page rows include one-click Mark Reviewed actions (with an optional note) for fast recertification loops.

Operational route details:
- GET/feedback-review serves the review page
- GET/feedback-data supplies the negative feedback entries shown on that page
- POST/feedbac-triage updates triage status and curator note
- POST/feedback-propose-wiki generates markdown draft proposals from selected feedback entries
- GET/triage_audit returns recent curator actions for audit visibility
- GET/wiki_freshness, GET/link/document, GET/cascade_status, GET/query_telemetry_summary, and GET/graph_analytics_summary power the health/analytics cards.
- POST/wiki_mark_reviewed supports stale-page review recertification directly from the panel.


## Frontend API Expectations
The frontend expects these endpoints:
```
- GET/
- GET/graph-map	
- GET/graph_map_data	
- GET/health	
- POST/ask	
- GET/wiki_index	
- GET/wiki_freshness	
- GET/cascade_status	
- GET/query_telemetry_summary	
- GET/graph_analysis_summary	
- GET/wiki_/{page_id}	
- POST/wiki_mark_reviewed	
- GET/raw/{file_name}	
- GET/schema/document	
- GET/schema/lint	
- GET/lint/document	
- GET/graph_connection/explain	
- POST/feedback	
- POST/feedback-triage	
- POST/feedback-propose-wiki	
- GET/feedback-review	
- GET/feedback-data	
- GET/triage_audit	
- POST/wiki
```

For detailed response shapes and full pipeline context, see README.md


## Boundaries and Scope
This frontend is optimized for bounded, curated corpora. It intentionally prioritizes explainability and operator control over maximal UI abstraction.

If your use case requires high-frequency streaming ingest, heavy role-based workflow controls, or advanced analytics dashboards, treat this UI as a transparent baseline and extend accordingly.
