# RASCAL 🃏
### Retrieval Augmented Semantic Calibrated Active Learning

T. Transou - June 2026 - 🚧 Active Development 🚧


**Conceptual lineage:** This repo began as an Azure-stack iteration of Andrej Karpathy's LLM Wiki gist. It now keeps the same wiki-first grounding idea while moving toward a **local-first, provider-open framework**: the baseline runs on local files, local Markdown wiki output, local JSON artifacts, and deterministic retrieval, while cloud, model, vector, graph, and enterprise systems remain optional adapters. It is also directionally aligned with retrieval-and-structuring research, such as RAS (Retrieval-And-Structuring for Knowledge-Intensive LLM Generation), particularly in its emphasis on structured intermediate knowledge over flat passage-only retrieval.

RASCAL is a lightweight, wiki-first framework for building grounded assistants over **bounded, curated document corpora** with transparent retrieval and traceable citations.

**Basic Premise:** Instead of forcing the model to rediscover raw documents for every question, this repo compiles source material into a persistent wiki-shaped knowledge layer that can be reviewed, curated, and reused.

**Purpose:** This repository is the reusable baseline for that pattern. It is intentionally framework-only and does not ship bundled domain data. Any raw/sources markdown belongs to the source corpus you bring into the framework, not to the framework itself. The goal is to provide the extraction pipeline, wiki compilation flow, retrieval surface, and UI/API scaffolding needed to turn a curated corpus into an explainable assistant without requiring a specific cloud provider, model vendor, vector database, or enterprise identity stack.

**Local-first and provider-open:** RASCAL's core should work with no cloud control plane:
- local source files in `raw/`
- local extraction artifacts in `backend/json/`
- local Markdown wiki pages in `backend/wiki/`
- local deterministic retrieval through `backend/retrieval.py`
- local API/frontend runtime through `backend/api.py` and `frontend/`
- local feedback/write-back artifacts as the starter persistence model

Provider integrations are allowed, but they are adapters rather than prerequisites. Useful open/local adapters may include SQLite or DuckDB for local persistence, Chroma/Qdrant/LanceDB for vector search, NetworkX or JSON graph files for graph exploration, Ollama/LM Studio/OpenAI-compatible local servers for optional synthesis, and GitHub/Obsidian/Google Drive export workflows for source movement. Enterprise adapters may include Azure OpenAI, Azure Blob, Cosmos DB, Entra ID, SharePoint, Teams, Confluence, or internal governed APIs.

**Customization by design:** you are not locked into predefined taxonomies or relationship types. For each corpus, you define the document types, relationship semantics, and metadata structures that reflect your domain's actual knowledge model. In short, JSON config files, not code. Whether you ingest policy/compliance documents, technical specifications, operational procedures, or the complete works of Seneca the Younger, the framework adapts to your ontology, not the other way around.

For teams that need standards-based semantic interoperability, optional SPARQL/ontology support is positioned as a domain-specific extension path (see Future Enhancements) rather than part of the domain-agnostic baseline.

**How this differs from traditional RAG:** In a standard RAG setup, the system retrieves chunks from raw files at query time and synthesizes an answer on demand. In this framework, raw files are first transformed into structured artifacts and compiled into a maintained wiki representation. Retrieval and answering happen against that persistent layer, while source documents remain available for traceability.

This also aligns with recent evidence that retrieval-only pipelines are often insufficient for harder domain tasks unless paired with stronger knowledge organization and reasoning structures. (Wang et al., 2025).

**Compounding Loop:** Validated answers can be written back to the wiki, so useful outputs become reusable knowledge pages rather than one-time responses.

> "This is the key difference: the wiki is a persistent, compounding artifact."
> -- Andrej Karpathy, LLM Wiki (cited in References)

This follows the same high-level idea described in Karpathy's LLM Wiki gist: the knowledge base is a compounding artifact, not just a transient retrieval target. Here, that idea is implemented for bounded corpora with explicit ingestion, deterministic compilation paths, and adapter-friendly runtime boundaries.


## Human Curation Marker 🧠
In the following repo (not just the README), any section labeled with 🧠 requires human customization for your dataset/domain before production use.


## Framework Branding and Philosophy 📜
> **Retrieval Augmented Semantic Calibrated Active Learning**

This name reflects both the implementation and the philosophy:
- **Retrieval:** answers are grounded in bounded corpora, not open-domain speculation
- **Augmented:** AI amplifies curator judgment; it does not replace accounable human review
- **Semantic:** knowledge is structured through domain-specific document types, edge types, and metadata.
- **Calibrated:** trust is earned through traceability, confidence signals, and explicit human-in-the-loop gates.'
- **Active Learning:** feedback, triage, and write-back create a compounding loop where the system improves with use.


## Calibrated Trust as the Core Principle 🤝
RASCAL is built around a practical trust posture:
- Show what the system knows, where it comes from, and how strongly responses are supported.
- Separate machine-extracted candidates from human-approved knowledge.
- Treat curation decisions as first-class system inputs, not post-hoc cleanup.
- Prefer transparent uncertainty over false confidence.
This posture aligns with trust-calibration research in AI-assisted decision systems and broader HCI literature on automation trust and miscalibration.

It also aligns with recent Human-Generative AI collaboration framing that defines collaboration as complementary human/AI work under explicit human oversight, where humans retain control of goals and boundaries while AI contributes bounded assistance or iterative support (Le et al., 2025, Sections 3.1.1-3.1.2)



## Framework Positioning
RASCAL is not trying to be a general-purpose autonomous agent stack.

It is a domain-grounded knowledge framework where:
- retrieval is bounded,
- outputs are reviewable,
- curation is operationalized,
- and quality compounds over time and use.
In short: the goal is not maximum autonomy; it is **maximum dependable usefulness** for real knowledge workflows.



## Manifesto! 🤜
RASCAL is a human-centered knowledge framework designed to support institutional memory, semantic retrieval, and governed knowledge evolution through constrained AI assistance. It is philosophically inspired by emerging LLM Wiki concepts while diverging architecturally from autonomous or heavily generative systems. RASCAL prioritizes provenance, ontology, metadata integrity, graph-based relationships, and human stewardship over unbounded probabilistic synthesis.

At its core, RASCAL treats AI not as an authoritative generator of institutional truth, but as a semantic mediation layer operating over structured, governed knowledge systems. Graph databases, semantic relationships, metadata schemas, taxonomies, and ontologies form the framework's persistent foundation, while natural-language interfaces enable users to interact with complex institutional knowledge in a more accessible and intuitive way. AI assists with retrieval, contextualization, semantic linkage, and relationship discovery, but human validation and stewardship remain critical to system operation and evolution.

RASCAL was developed in response to limitations observed in native RAG (Retrieval-Augmented Generation) implementations, especially in high-trust enterprise environments where probabilistic synthesis can introduce interpretive drift, hallucination, inconsistent outputs, and weakened provenance. Rather than emphasizing one-shot generated responses, RASCAL focuses on retrieval decisions, semantic continuity, explainability, calibrated trust, and persistent institutional coherence.

RASCAL assumes that meaningful knowledge systems require ongoing curation, governance, and contextual understanding. As authoritative data evolves, the semantic graph evolves alongside it through interaction, validation, and stewardship. The system therefore functions not merely as an AI chatbot or retrieval layer, but as living institutional knowledge infrastructure designed to preserve and strengthen organizational understanding over time.

The framework is especially applicable in environments where:
- provenance and auditability matter,
- institutional trust must be maintained,
- knowledge complexity exceeds simple keyword retrieval,
- Semantic relationships are operationally important,
- and AI systems must remain explainable, governable, and human-centered.

RASCAL does not reject AI, generation, or future agentic systems outright. Instead, it advocates calibrated trust, bounded probabilistic authority, and responsible human oversight as organizations integrate AI into sensitive knowledge environments. RASCAL reflects a simple belief: AI should augment human reasoning, stewardship, and institutional continuity rather than replace them.

With that philosophy in mind, the next section clarifies explicit boundaries to prevent misuse and expectation drift.


## Out of Scope (To Avoid Confusion) 😖
The implementation is intentionally bounded; it is not designed as a general agent framework or a general-purpose chatbot.
- No required named model vendor: the local-first baseline does not require Claude, OpenAI, Azure OpenAI, or any hosted LLM. Model-backed synthesis can be added later through optional adapters.
- No autonomous multi-agent orchestration: this is a single assistant, pipeline-driven system. The use of agents may be considered later, once the baseline MVP is proven and security concerns are analyzed.
- No open-domain assistant behavior: responses are grounded in a bounded, curated corpus with traceability.
- No chat-over-anything posture: ingestion and answer quality depend on structured artifacts plus human curation.
Essentially: start small, test, verify, then iterate and add features.


## Core feasibility premise
AI knowledge solutions are more feasible when applied to small, bounded, reviewable knowledge domains rather than broad, uncurated repositories.

RASCAL is best suited for:
- the scope is limited, and the owner of the data is identifiable
- the source content has at least moderate structure
- the knowledge has repeated operational and potential business/organizational value
- the content can be reviewed and improved incrementally

It is less suited to domains where content is highly fragmented, purely informational or personal, unbounded, or too costly to curate relative to expected value.


## What RASCAL is designed to explore
- Whether AI can make small knowledge domains more accessible without a large platform investment
- Whether a wiki-like format improves usability and discoverability over a static document repository
- Whether bounded enterprise datasets can support trustworthy retrieval
- Whether bounded humanities/science/abstracted datasets can support trustworthy AND explainable retrieval
- Whether knowledge can become more structured and reviewable over time through gradual curation

RASCAL is not intended to replace a full enterprise knowledge platform (not yet). It is a framework for evaluating feasibility and practical utility at a smaller scale ("tribal" or "niche" knowledge).


## Intended Audience 🎭
RASCAL is relevant for "stakeholders" interested in:
- bounded AI knowledge use cases within a specific team or function
- improving internal (tribal) knowledge accessibility and discoverability
- enterprise-safe experimentation using approved tooling
- academic-robust experimentation using approved tooling
- retrieval over document-based content
- practical AI applications that can be deployed, reviewed, and improved incrementally.

## Lessons from earlier experimentation
Experience in an organization while formulating RASCAL included work with more unstructured internal team knowledge (shared notes, informal support content, mixed operational comments) and showed that raw retrieval against messy repositories is not reliably effective. For example, a support team's internal OneNote KB fed into a naive RAG pipeline became a quagmire of nonsense, hallucination, and AI insanity. Even with more semi-structured data, naive RAG frameworks, in the developer's experience, were consistently hallucinatory, opaque, and confusing to others. See SCARAG for a response to RAG implementations.

All of this reinforced a key design principle for RASCAL:
> **Not all knowledge or data is equally ready for AI use.**

Anyone who has been developing alongside emerging AI tech knows the adage: Garbage in, garbage out. **DATA MATTERS**.

Source material in forms such as personal notes, screenshots, or ad hoc documentation may contain valuable knowledge, but is often not suitable for direct ingestion without significant transformation, curation, and pre-processing. RASCAL is better understood as a framework for **bounded AI knowledge experimentation**, not a universal ingestion solution, as RAG is generally treated. RAG is not a "magic AI hole" to throw data into. 😅


## A Demonstration narrative
When testing RASCAL against real data, a Credit and Risk team in the financial services sector had approximately 50 documents, including policies, procedures, directives, forms, and supporting reference material. The 50 documents, aka a dataset, were selected for their characteristics, initially favorable for RAG or other AI-assisted retrieval methods. The dataset was "structured" as. DOCX, .XLSX, and a single PDF. With a bounded scope and a clear domain, the dataset was a suitable benchmark for testing RASCAL. Ingestion, embedding, retrieval, response shape, and traceability proved to be, on its face, successful. The downside is that the developer lacked the domain expertise to assess accuracy, veracity, and trustworthiness. 


## Limitations
RASCAL does not assume that all data (academic/enterprise) is ready for AI consumption. Its usefulness depends heavily on the quality and boundedness of the source material.

Known constraints:
- unstructured or informal knowledge may require significant curation/pre-processing before ingestion produces reliable results
- AI retrieval usefulness depends directly on document quality, scope clarity, and reviewability
- broader organizational rollout would require a domain-specific feasibility assessment before committing

For this reason, RASCAL should be evaluated as a targeted approach for suitable domains, rather than as a general solution to all knowledge problems.


## Domain-driven Design: Build Your Own Taxonomies and Ontologies (or don't) 🤷
**This is a core strength of RASCAL.**

Unlike rigid, top-down knowledge platforms, RASCAL is designed for corpus operators to define their own domain vocabularies… taxonomies, relationship types, concept hierarchies, and metadata schemas… based on the actual data being ingested. **Note:** controlled vocabularies, taxonomies, etc., per domain do exist. Exercise best practices here.

RASCAL ships with sensible defaults (e.g., `requires`, `depends_on`, `related_to` relationships; policy, procedure, standard, required document types), but these are **templates, not constraints.**

When you bring a new corpus, you customize:
- **Metadata enrichment rules** in `metadata_overrides.json` where you curate document summaries, key points, and relationships specific to your context.
- **Source traceability mapping** in `config/source_url_map.json` where you maintain canonical links back to upstream systems.

This means:
- A credit/risk corpus uses relationships like `delegates_to`, `exempts`, `scoped_to`, not generic `related_to`
- A compliance corpus classifies documents by regulatory framework, authority level, and expiry date, not generic document types.
- A technical corpus structures relationships by implementation dependency, version compatibility, and depreciation chains, not generic relationships.
- A humanities/science based corpus structures relationships more specifically depending on context and source
- Each corpus reflects the actual semantics and decision-making patterns of its domain, not a one-size-fits-all ontology.

RASCAL provides the **extraction pipeline, graph layer, retrieval logic, and UI scaffolding**. You provide the domain knowledge.

The ontology-first stance is consistent with ontology-grounded retrieval directions that improve interoperability by making semantic structures explicit.


## Why this matters
Even where RASCAL is not feasible for every group, it demonstrates a credible and practical pattern:
- AI can be applied to small corpora/datasets across domains without a large platform investment
- A wiki format can improve usability and cross-document navigation over static repositories
- Bounded document sets are a realistic and achievable entry point
- Approved internal tooling can support supplementation without waiting for platform-level infrastructure.
This makes RASCAL useful both as a demonstration of what is possible and as a decision tool for identifying whether AI knowledge solutions may be viable for a given team or domain.

## Self-assessment: Is your domain a good fit? 🧩
Before bringing a dataset to RASCAL, use the AI KMS Domain Feasibility Scorecard to independently assess two dimensions:
- **Value:** How useful would AI-assisted retrieval be for this domain? (e.g., reuse frequency, retrieval pain, decision impact)
- **Readiness**: How suitable is the current content for AI use without excessive curation/pre-processing? (e.g., structural coherence, semantic clarity, documentation currency)

The `documentation/SCORECARD.md` includes:
- Five value dimensions to evaluate
- Five readiness dimensions to evaluate
- Scoring guidance for each (1-5 scale)
- Interpretations thresholds
- A combined assessment matrix
- Real-world scenario examples

Depending on your scoring, you can assign decision labels:
- **Direct AI KMS Candidate** - high value + high or moderate readiness, suitable for ingestions with normal preprocessing
- **AI-Assisted Transformation Candidate** - high value + low readiness, suitable only if AI helps convert messy content into a usable knowledge object first.
- **Selective Extraction Candidate** - high value + very low readiness: do not ingest broadly; extract only recurring issues, FAQs, procedures, or key patterns.
- **Not Currently Viable** - low value and/or very low readiness, curation cost likely too high for expected benefit.

What to bring when evaluating your domain:
- Scope and ownership
- Content structure
- Stability
- Retrieval pain today
- Consequence of poor access
- Review appetite


## Framework Scope
RASCAL as a framework intentionally contains:
- Pipeline and API source code (`backend/`, `frontend/`)
- Template config (`config/source_url_map.json`)
- Documentation in `documentation/` including scorecard and architecture notes
- Empty metadata stubs (`metadata_overrides.json` with "documents":{})
- Placeholder directory (`raw/`)

RASCAL does not contain source documents, compiled wiki output, or domain-specific fallback answers.


## Human Curation Layer - The Two Required Files ✌
RASCAL is entirely automated EXCEPT for two JSON files that require human curation 🧠:
- `metadata_overrides.json` - enriches extracted metadata (summary, key points, relationships)
- `config/source_url_map.json` - Maps internal doc IDs to source location by URL and external validation (could be optional)
🧠 Required before production: complete both files with dataset-specific values and reviewer ownership.

Everything else is automated:
- Document extraction (`backend/process_raw_sources.py`) → JSON
- Wiki compilation (`backend/wiki_compiler.py`) → Markdown + index
- Retrieval, citation, tracing →  API Endpoints


## Current Build Status and Workflow (V2-style)
This repository is currently being rebuilt around a working ingestion-to-wiki pipeline that reflects the README’s architecture in a pragmatic, version-2 form.

The current workflow is:
1. Put source files into the raw/ folder.
2. Run ingestion to extract text from supported document types into JSON artifacts.
3. Use curated metadata from metadata_overrides.json to enrich the extracted content.
4. Compile those artifacts into Markdown wiki pages under backend/wiki.

The code now follows this shape:
- backend/ingest.py — primary ingestion implementation
- backend/process_raw_sources.py — thin compatibility wrapper for the README-style entry point
- backend/compile_wiki.py — primary wiki compilation implementation
- backend/wiki_compiler.py — thin compatibility wrapper for the README-style entry point

Typical commands:
```bash
source .venv/bin/activate
python backend/process_raw_sources.py raw --output-root backend/json
python backend/wiki_compiler.py raw --output-root backend/json --wiki-root backend/wiki
```

This is intentionally a practical first-pass implementation of the README’s conceptual pipeline. As the project matures, the README and the code will be updated together to reflect the final architecture.

## Why Human Curation is Needed (Plain Language)
Automation gets you speed; 🧠 human curation gives you trust.

RASCAL can extract text, infer links, and build a useable knowledge graph automatically. But in many domains, correctness is not only about syntax. It is about meaning, intent, and sometimes risk. This is why human curation remains essential before treating outputs as trusted knowledge.

In practice, human curation is needed for three reasons:
- **Meaning accuracy:** extracted links can look reasonable but still be wrong for your domain
- **Accountability:** someone must own what is approved, rejected, or still provisional
- **Traceable decisions:** reviewers need to explain why a relationship or summary was accepted.

| Area                                                       | What Humans Decide                                  | Why It Matters                                        |
| ---------------------------------------------------------- | --------------------------------------------------- | ----------------------------------------------------- |
| `metadata_overrides.json` summaries/key points              | Final summary wording and top takeaways             | Prevents misleading or incomplete framing             |
| Relationship validation (`requires`, `depends_on`, `related_to`) | Whether an extracted relationship is truly valid    | Protect dependency chains from semantic errors        |
| Confidence and weight promotion                            | Which links deserve high-confidence status          | Separates verified knowledge from provisional signals |
| Concept naming and synonym merges                          | Canonical terms and merge/split choices             | Avoids ontology drift across teams/doc types          |
| `config/source_url_map.json` mapping                        | Canonical source-of-truth URLS/documents            | Keeps citations auditable and user-verifiable         |
| Curator review loop                                        | Which feedback should be written back into the wiki | Prevents low-quality or incorrect write-back          |

**Rule of Thumb**
- If it changes interpretation, risk, or policy meaning it needs 🧠 human review
- If it is a mechanical transformation (parse, compile, index, retrieve), automation is sufficient

**Human Curation and Governance Model**
For teams operationalizing this model, role clarity (owner, reviewer, curator, approver) is not optional; it is the control surface that keeps grounded retrieval from drifting into ungoverned synthesis.
> "Projects slip not because the model is weak, but because accountability is fuzzy."
> > *- Megan Leanda Berry, The Human Layer in GraphRAG*

$INSERT MERMAID DIAGRAM$


## Metadata Overrides Structure
See `metadata_overrides.json` for framework-ready example entries covering:
- unreviewed linkage (provisional strength)
- document-level HITL-reviewed linkage (semantic tier strengths)
- per-link HITL reviewed override with explicit weight/confidence
🧠 **Customization point:** replace all example document keys, relationship targets, and confidence semantics with your domain-specific curated values.

```json
{
  "documents": {
    "doc_id_or_title": {
      "summary": "Human-written summary of this document's purpose and scope.",
      "human_reviewed": false,
      "key_points": [
        "Point 1: What users must understand.",
        "Point 2: Critical rule or constraint."
      ],
      "relationships": {
        "requires": ["ref_to_prerequisite_doc"],
        "depends_on": ["ref_to_parent_policy"],
        "related_to": [
          {
            "target": "ref_to_sibling_concept",
            "weight": 0.6,
            "confidence": 0.65,
            "human_reviewed": true,
            "provenance": "curator"
          }
        ]
      }
    }
  }
}
```
**How to fill it in:**
- `summary`: 1-3 sentences answering "What does this document do?"
- `key_points`: Bullet list of 3-5 most important takeaways
- `relationships.requires`: docs that must be read/understood first
- `relationships.depends_on`: docs that this one supersedes or refines
- `relationships.related_to`: docs with tangential relevance
You can provide relationship links in either form:
- simple string form, which is backward compatible: `"requires": ["doc_b", "doc_c"]`
- rich object form, which is recommended for curation-aware graph edges: `"requires": [{"target": "doc_b", "weight": 0.95, "confidence": 1.0, "human_reviewed": true, "provenance": "curated"}]`
When object form is used, compilation preserves link-level metadata on the edge record: `target`, `weight`, `confidence`, `human_reviewed`, `provenance`, and `review_state`.

If simple string form is used, RASCAL defaults apply by relationship type:
- `requires`: strongest defaults (weight=1.0, confidence=0.95)
- `depends_on`: medium defaults (weight=0.8, confidence=0.8)
- `related_to`: lowest defaults (weight=0.6, confidence=0.65)
Per-link object value always overrides these defaults.

HITL gating behavior:
- before HITL review, relationship links are treated as provisional and stored with neutral strength (weight=0.5, confidence=0.5)
- After HITL review is marked complete ("human_reviewed": true at document override level, or per-link), semantic tier strengths are applied automatically.
- custom per-link weight/confidence are only honored after HITL review (document-level or per-link)
- `/graph_map_data` exposes these fields directly, and the graph UI renders reviewed edges as solid links and provisional edges as dashed links.

Framework requirement for all adopters:
- Each team must define its own dataset policy for what qualifies as `requires`, `depends_on`, and `related_to`
- Each team must define HITL ownership (who reviews, approval criteria, and escalation path)
- Each team must define when document-level review is allowed vs per-link review only.
- Each team must define confidence/weight override rules for their domain
- These choices should be recorded in `metadata_overrides.json` under `curation_policy` before product onboarding.


## Source URL Map Structure
```json
{
  "by_doc_id": {
    "doc_id_or_wiki_page_id": "https://example.org/source-system/document"
  },
  "by_source_file": {
    "filename-or-relative-path.ext": "https://example.org/source-system/document"
  },
  "by_title": {
    "Document Title": "https://example.org/source-system/document"
  }
}
```

🧠 **Customization point:** map each real source document to its canonical system-of-record URL.
How to fill it in:
- map each document's internal ID, filename, or title to its source URL
- users see the source URL in the frontend (example: "View in Sharepoint/Drive" link)
- All three indexes point to the same upstream documents and pick whichever keys make sense for your corpus.

Current local resolution order:
1. `by_doc_id` using the wiki page/document ID
2. `by_source_file` using the stored source file path
3. `by_source_file` using only the source filename
4. `by_title` using the wiki page title

Resolved URLs are included in wiki catalog records, wiki page payloads, retrieval trace citations, and frontend citation links.


## Configuration and Customization Surfaces
**This section defines where you inject domain knowledge.**

RASCAL carefully distinguishes between framework infrastructures (the code and structure that remain constant across deployments) and domain customization (the vocabularies, definitions, and business/schema rules that change with each corpus).

For reuse across local, open-tool, or enterprise environments, it helps to separate what you must provide to get the framework running from what you may customize to adapt it to a new domain, operating model, or UI.


## Required to Run vs. Optional to Customize
| Surface                                   | Required to run?                                           | When it becomes required                                               | Why it exists                                                                            |
| ----------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Source documents in `raw/`                  | Yes                                                        | Any real pipeline run                                                  | The framework need a corpus to extract and compile                                       |
| `metadata_overrides.json`                   | Yes for a proper corpus run                                | Before treating the wiki as curated knowledge                          | Human summaries, key points, and relationships are part of the framework’s quality model |
| `config/source_url_map.json`                | Yes for production-like traceability                       | Before expecting source links in citations/UI                          | Preserves traceability back to authoritative source systems                              |
| Python environment + requirements.txt     | Yes                                                        | Always                                                                 | Needed for the parser, API, and local runtime                                            |
| `frontend/*` branding and tab mapping       | No                                                         | When white-labeling or adapting the UI to a new corpus                 | Supports reuse across teams and domains                                                  |
| CLI flags in `backend/process_raw_sources.py` and `backend/compile_wiki.py` | No                                                         | When changing extraction/compile directories for your local workflow   | Lets you reuse the same framework across different corpus layouts                        |


## Minimum Required to Run Locally
For the smallest credible local run, you need only:
- dependencies installed from requirements.txt
- a few source files in `raw/`
- curated `metadata_overrides.json`
- curated `config/source_url_map.json`
- extraction and compilation runs using `backend/process_raw_sources.py` and `backend/wiki_compiler.py`
- local API using `python backend/api.py`
Everything else in this section is about adaptation, enrichment, or alternate runtime paths.


## Optional Provider and Product Customization
These are the main reuse levers when adapting RASCAL for another team, public/open-tool workflow, local lab environment, business unit, area, corpus, or product surface:
- metadata curation in `metadata_overrides.json`
- source traceability mapping in `config/source_url_map.json`
- ingestion/compilation pathing with `backend/process_raw_sources.py` and `backend/wiki_compiler.py`
- UI naming, category mapping, and external links in `frontend/app.js` and `frontend/index.html`


| File/Surface | What it controls | Typical customization |
| :---- | :---- | :---- |
| `metadata_overrides.json` | Per-document human curation and default metadata | Add summaries, key points, relationships, and final type overrides |
| `config/source_url_map.json` | Source-document links used in citations and UI | Point citations to local files, GitHub, Obsidian exports, Google Drive, SharePoint, Drive, file portals, or document systems |
| `backend/process_raw_sources.py` + `backend/wiki_compiler.py` | Ingestion and wiki compilation orchestration | Control source path, JSON output root, and wiki output root for local runs |
| `frontend/app.js` + `frontend/README.md` | UI labels, type-to-tab mapping, external files, and catalog behavior | Rebrand the UI, adapt type tabs, and expose richer metadata in the browser |


## What Each Surface Actually Does
**`metadata_overrides.json`**
- stores curated summaries, key points, and relationship hints that are merged during wiki compilation

**`config/source_url_map.json`**
- stores mappings from internal IDs/source file names/titles to canonical source URLs
- supports traceability when you surface source links in UI or downstream APIs

**Current ingestion/compilation CLI switches**
- `backend/process_raw_sources.py`: use the positional `source` argument and `--output-root` to control where extracted JSON is written
- `backend/wiki_compiler.py`: use the positional `source` argument plus `--output-root`, `--wiki-root`, and `--metadata` to control compilation inputs/outputs
- Use absolute or repo-relative paths to repoint RASCAL at a different corpus layout without editing code

**Frontend customization**
- `frontend/app.js` controls type normalization, wiki tab behavior, external links, and model/catalog rendering
- `frontend/index.html` controls visible branding, labels, and the app shell layout
- `frontend/README.md` documents frontend-specific setup and behavior


## Concept and Metadata Node Framework
This section defines how to add concept and metadata nodes in a way that is explainable, repeatable, and explicit about where human curation is required.

**Explainable Processing Contract**
For each ingested document, the system should produce a small processing trace:
- input document id/title
- extracted concept candidates
- emitted metadata nodes
- emitted edges (`mentions`, `defines`, `has_metadata`, etc.)
- curation status (`auto`, `reviewed`, `rejected`)
This keeps graph expansion auditable and helps reviewers understand why a node or edge exists.


## Auto vs Human Curation Boundaries

| Item | Auto-generated by framework | Human input needed | Why |
| :---- | :---- | :---- | :---- |
| Concept candidate extraction | Yes | No | Deterministic extraction from title/summary/key points/headings |
| Metadata node extraction (doc type, source file, tags) | Yes | No | Mechanical mapping from document fields |
| Concept canonical naming/synonym mergers | No | Yes | Domain language differs across teams and corpora |
| Concept-to-concept logical links (`implies`, `conflicts_with`) | Optional | Yes for production confidence | Requires domain interpretation |
| Edge confidence elevation to 1.0 | Optional | Yes | Marks verified truth, not just extracted signal |
| `Human_reviewed` flag | Optional | Yes | Explicit audit marker for verified relationships |


## Minimal Template to Include in `metadata_overrides.json`
Use this shape per document when you want concept/metadata support with optional HITL curation:
```json
{
  "documents": {
    "doc_id_or_title": {
      "summary": "Human-written summary of this document's purpose and scope.",
      "human_reviewed": false,
      "key_points": [
        "Point 1: What users must understand.",
        "Point 2: Critical rule or constraint."
      ],
      "relationships": {
        "requires": [],
        "depends_on": [],
        "related_to": []
      }
    }
  }
}
```


## HITL Workflow (Where, Why, What, How)
1. Where: After extraction and before promoting graph output to a trusted source
3. Why: Extracted concept links can be syntactically correct but semantically wrong for policy intent
4. What: Review concept names, merges/splits, and high-impact links used in dependency chains
5. How: Update status, `human_reviewed`, and confidence/weight in overrides, then re-run ingestion.


## Framework Rule of Thumb
- Framework default: produce usable graph output without human intervention
- Reliability mode (especially for enterprise): requires human review only for critical concept mappings and policy-chain edge.


## When Human-in-the-Loop (HITL) is Needed: Framework vs. Instance Level
This section clarifies where human judgment is required vs. where the framework is fully automated. Understanding this distinction prevents over-engineering at the framework level and clearly defines what each party (framework developer, corpus operator, domain expert) is responsible for.


## Framework Level: No HITL Required - Autonomous
The framework itself needs **zero human intervention** to operate. All of the following are automatic:

| Process | Automate By | Human Input? | Why |
| :---- | :---- | :---- | :---- |
| Document extraction (DOCX/XLSX/PDF, et al →JSON) | `backend/process_raw_sources.py` | NO | Framework handles supported source formats and writes JSON output |
| Wiki compilation | `backend/wiki_compiler.py` | No | Produces Markdown pages and an index markdown from extracted docs |
| Retrieval and serving | `backend/api.py` | No | Local demo endpoints work out-of-box |
| Citation-like trace payloads | `backend/api.py` | No | `/ask` returns demo trace and source payloads |
| Feedback capture | `backend/api.py` | No | `/feedback` captures local feedback events |

**Result:** Framework produces a valid, self-contained pseudo-graph and retrieval system without human judgment.


## Instance Level: Optional HITL for Enrichment, Optional Customization
When an operator uses the framework on a **specific corpus**, they have the option (not a requirement) to add human judgment. This is corpus-specific, not framework-level:

| Where | What | Optional? | When You’d Use it | Impact |
| :---- | :---- | :---- | :---- | :---- |
| Metadata curation | Summaries, key points, relationship in `metadata_overrides.json` | Yes | Before releasing the wiki as “curated knowledge” | Better initial retrieval; richer user context |
| Source link mapping | Document IDs →authoritative URLS in `config/source_url_map.json` | Yes | When users need to verify claims against source | Traceability \+ authority |
| Relationship validation | Mark extracted edges as `human_reviewed`: true after verification | Yes | When dependencies matter for compliance/policy chains | Enable high-confidence traversal queries |
| Relationship weighing | Adjust weight (0.0-1.0) to mark critical vs. weak dependencies | Yes | When some links are stronger than others (e.g., legal vs. informational) | Allows filtering to only strong paths |
| Confidence adjustment | Set confidence: 1.0 on verified edges; leave confidence on \< 1.0 on speculative ones | Yes | When distinguishing extracted-guess from curated-fact | Query filtering by minimum confidence |
| Fallback answers | Pre-write answers for common questions when corpus coverage is weak | Yes | During early rollout or for out-of-corpus questions | Graceful degradation; better user experience |
| UI customization | Rebrand, change tab labels, remap type categories in `frontend/` | Yes | When adapting RASCAL for a different business unit/domain space | Better fit to domain vocabulary |
| Feedback review | Read query logs and write verified answers back into wiki | Yes | When you want compounding loop (answers \+ wiki knowledge) | Continuously improving knowledge base |

**Key Point**: None of these are required for RASCAL to work. The framework is self-contained and autonomous. These are value-adds that an operator can choose to invest in.


## Where HITL Becomes Essential (Not Framework, but Operator Judgment)
Human hands are genuinely needed in only one place, and it's outside RASCAL.

**Domain knowledge verification**:
- The framework cannot verify if a relationship extracted from a policy/source document is *actually* correct in your organization.
- Example: RASCAL might extract "Policy A requires Policy B" from document text, but a legal or policy expert needs to confirm that this relationship is *intended* and *accurate* for your operating model
- If a relationship is wrong, the entire downstream dependency is tainted.

** How to handle this:**
1. Run RASCAL extraction (automatic, no review needed)
2. Operator reads extracted relationships and metadata
3. **Domain expert reviews and marks as verified** ← This is HITEL
4. Operator sets `human_reviewed`: true on verified relationships (optional but recommended for critical paths)
5. Users can then query with `min_confidence` filter to focus on verified chains.


## HITL Summary: Who Does What

| Role | Responsibility | HITL Required? | When |
| :---- | :---- | :---- | :---- |
| Framework Developer | Code, pipeline logic, schema | No | Framework is autonomous |
| Corpus Operator | Run pipeline, manage metadata, maintain mappings | Minimal | Just filling in `metadata_overrides.json` and `config/source_url_map.json` |
| Domain Expert | Verify extracted relationships are correct for your org/use case | Yes | Before making edges `human_reviewed`: true |
| Product Manager et al. | UI/UX customization, fallback answers | Optional | If you want a tailored experience |

**Typical workflow:**
1. Operator: Run framework extraction (automatic)
2. Domain Expert: Review relationships (HITL verification)
3. Operator: Mark verified edges with metadata (optional enrichment)
4. Users: Query with filters to focus on verified chains (automatic retrieval)


## Onboarding RASCAL
Use this sequence when onboarding RASCAL for a new corpus or internal product surface.

**1. Define the Operating Model**
Decide up front:
- Which document set is in scope for the first rollout
- whether the first deployment is local-only, open-tool backed, enterprise-backed, or some deliberate combination
- which teams will own metadata creation, source-link mapping, and frontend branding
This prevents RASCAL from being treated as a generic chatbot shell before the knowledge and ownership model are clear.

**2. Establish the Minimum Viable Corpus**
Start with a bounded, representative set of source documents in `raw/`
Recommended first pass:
- 20 to 60 representative documents.
- current approved versions only
- a mix of content styles where applicable
The goal is not maximum coverage on day one. The goal is a clean, reviewable first knowledge layer.

**3. Complete the Required Curation Layers**
Before presenting the system as a grounded assistant, complete:
- `metadata_overrides.json` for summaries, key points, relationships, and final type corrections
- `config/source_url_map.json` for source traceability back to the authoritative document system
These are the core human-controlled inputs that make the framework reusable and auditable.

**4. Choose the Runtime Path**
Pick one of these paths deliberately:
- local-first path: fastest for pipeline and UX validation; uses files, Markdown, local API, and deterministic retrieval
- open-tool path: use local or open services such as Ollama/LM Studio, SQLite/DuckDB, Chroma/Qdrant/LanceDB, or file/Git-based workflows when they fit your environment
- enterprise adapter path: use Azure, SharePoint, Entra ID, Cosmos DB, or other governed services only when those controls are needed
Do not casually mix these paths in documentation or handoffs. Different teams will care about different prerequisites.

**5. Align the Frontend to the Corpus**
Before wider rollout, verify that the UI reflects the corpus you loaded:
- branding and viable labels in `frontend/index.html`
- category mapping and external links in `frontend/app.js`
- frontend route contract and white-label checklist in `frontend/README.md`
This keeps the framework reusable across areas/units without implying that every deployment shares the same taxonomy or navigation model.

**6. Run an Operator Review Pass**
Before calling the deployment ready for users:
- run the pipeline end-to-end
- inspect wiki output quality
- ask representative questions in the UI
- confirm citations resolve to expected source links
- review feedback and write-back behavior
This is the practical gate between a technically running system and a trustworthy internal assistant.


## Optional Outputs
At the end of onboarding, you should have:
- a bounded starter corpus
- a curated metadata layer
- a validated source-link map
- a chosen runtime path with matching environment/configuration
- a frontend aligned to the target vocabulary
- two handoff documents kept current: this root README and `frontend/README.md`


## High-Level Architecture
This framework branch intentionally ships with no prebuilt wiki Markdown pages. The `backend/wiki/` content shown below is runtime-generated from your own corpus and should remain git-ignored

`raw/` → `backend/process_raw_sources.py` + `backend/json/*.json`  
↓  
`backend/wiki_compiler.py`  
↓  
`backend/wiki/*.md` + `backend/wiki/index.md`  
↓  
`backend/api.py` (serves frontend and demo endpoints)  
↓  
User asks a question  
↓  
demo retrieval flow → answer + trace-style payload

At step 1, `metadata_overrides.json` is merged during wiki compilation, and `config/source_url_map.json` is available for source traceability mapping.


## Data Objects and Terminology
To keep this README coherent, these terms are used consistently:
- Raw/source documents: original input files in `raw/` (ex: DOCX, XLSX, JSON, et al)
- JSON artifacts: extracted, structured intermediate files in `backend/json/`
- Wiki pages: compiled Markdown knowledge pages in `backend/wiki/`


## Canonical Type Field
Use types as the canonical document taxonomy field across pipeline stages.
- Extraction infers type
- Human curation can override/refine type in `metadata_overrides.json`
- Wiki compilation uses type to place pages into buckets and annotate metadata
- Frontend filters and tabs are mapped from type
If you have legacy payloads that expose `page_type`, treat them as compatibility aliases and normalize to the type in your API/serialization layer.


## How this Differs from the Original LLM Wiki Gist
The core idea is the same: build a wiki-shaped, grounded knowledge layer first, then answer questions from that curated representation instead of trating the model as the source of truth.

This repo differs in a few important ways:
- It is local-first and provider-open. The default runtime uses local files, Markdown, JSON artifacts, and deterministic retrieval; Azure and other cloud services are optional adapters.
- It is not designed around any named model vendor or autonomous multi-agent orchestration. The runtime is a single-assistant, pipeline-driven retrieval-and-answer flow.
- It uses an explicit extraction pipeline. Raw source documents are converted into structured JSON artifacts before wiki compilation, rather than assuming a single monolithic wiki-generation step.
- It keeps a human curation layer in the loop; `metadata_overrides.json` and `config/source_url_map.json` are first-class parts of the workflow, not incidental extras.
- It separates deterministic and LLM-assisted compilation. Scaffold mode gives a reproducible baseline; LLM mode is an optional enhancement, not the only path.
- It is designed for a variety of corpora in a variety of settings (academic or enterprise). The document model, relationships, traceability, and citation handking are optimized for a variety of document formats (policy, procedure, forms, analysis, primary sources)
- It exposes an application surface, not just a content artifact. The wiki is compiled into assets that are then served through API and frontend layers with retrieval trace and citations.
In short, this project is best understood as a local-first, provider-open implementation of an LLM Wiki pattern rather than a direct clone of the original gist.


## Data Flow Transparency
**Note:** This section reflects the code currently present in `backend/ingest.py`, `backend/compile_wiki.py`, and `backend/api.py`.

### Data Flow and Human Input Points
**Stage 1: Raw Source Documents (`raw/`)**
- Input formats supported by ingestion include: TXT, MD, HTML/HTM, XML, JSON, CSV, PDF, DOCX, PPTX, XLSX.

**Stage 2: Extract to JSON (`backend/process_raw_sources.py` → `backend/json/`)**
- Reads each supported file under the provided source path.
- Extracts text content and writes one JSON document per source file under `backend/json/`.

**Stage 3: Human Curation (`metadata_overrides.json` and `config/source_url_map.json`)**
- Update `metadata_overrides.json` to curate summaries, key points, and relationships.
- Update `config/source_url_map.json` to maintain source traceability mappings.

**Stage 4: Compile Wiki (`backend/wiki_compiler.py` → `backend/wiki/`)**
- Loads extracted docs and optional metadata overrides.
- Writes markdown pages into `backend/wiki/`.
- Writes `backend/wiki/index.md` as the generated wiki index.

**Stage 5: Serve UI and Endpoints (`backend/api.py`)**
- Serves frontend assets (`frontend/`) and demo endpoints such as `/health`, `/ask`, `/feedback`, and `/wiki_index`.
- Returns answer and trace-style payloads for local testing.


## Summary: Where Data Flows & Where Human Input Happens

| Stage | Input | Process | Output | Human Input? |
| :---- | :---- | :---- | :---- | :---- |
| 1 | User uploads files | Drop in `raw/` | .docx, .xlsx, .pdf | Upload |
| 2 | `raw/` files | Text extraction | `backend/json/*.json` | Automatic |
| 3 | JSON + overrides | Enrich metadata | `metadata_overrides.json` (edited) | REQUIRED for curated runs |
| 3b | JSON | Map source URLs | `config/source_url_map.json` (edited) | REQUIRED for traceability |
| 4 | JSON + overrides | Wiki compilation | `backend/wiki/*.md` + `backend/wiki/index.md` | Automatic |
| 5 | Wiki markdown | Serve UI/API | Local endpoints on `backend/api.py` | Automatic |


## End-to-end Workflow
This is the fastest way to understand how raw/source documents become answers users can inspect and improve.

*MERMAID DIAGRAM*


## Practical Walkthrough
1. Add a few representative raw source documents to `raw/`
2. Run extraction to produce JSON artifacts in `backend/json/`
3. curate `metadata_overrides.json` and `config/source_url_map.json`
4. compile wiki pages into `backend/wiki/` and `backend/wiki/index.md`
5. start API/UI and ask questions
6. inspect trace/citations in the frontend to validate grounding
7. use feedback: thumbs-down logs quality issues, thumbs up + save writes useful answers back to the wiki


## Quick Start
**Required to Run**
1) Install dependencies
``` bash
#create and activate an isolated environment for this project
python -m venv .venv
source .venv/bin/activate    # macOS/Linux

#install parser and local API dependencies
pip install -r requirements.txt
```

2) Add your source documents
Place .doc, .pdf, etc in `raw/`

3) Build local artifacts
```bash
python backend/process_raw_sources.py raw --output-root backend/json
python backend/wiki_compiler.py raw --output-root backend/json --wiki-root backend/wiki
```

This runs ingestion followed by wiki compilation using the current V2 entry points.

Common variations:
- replace `raw` with a specific file path to ingest a single document
- change `--output-root` if you want JSON artifacts outside `backend/json`
- change `--wiki-root` if you want compiled Markdown outside `backend/wiki`
- pass `--metadata` on `backend/wiki_compiler.py` to use a non-default metadata override file

4) Start the API
```bash
python backend/api.py
```

The local API serves the frontend shell and demo endpoints at port 8000 by default.

5) Open the app
Browse to http://127.0.0.1:8000

6) Open Curator Space (Feedback/Triage)
After the API is running, open Curator Space directly at:
- http://127.0.0.1:8000/feedback-review
You can also reach it from the main app shell (/) using the sidebar link labeled **Internal: Curator Space**. That entry intentionally opens in a new tab/window and is styled as a low-emphasis internal control rather than a primary end-user action.

What you can do there:
- review negative feedback queue entries
- triage to be `resolved`, `proposed_wiki`, or `proposed_override`
- create wiki drafts from feedback
- monitor wiki health (freshness + lint)
- review recent curator audit actions
If your goal is only to prove the framework works end-to-end locally, the six steps above are enough.


## Optional to Customize
After the framework is running, the most common customization steps are:
1. Curate `metadata_overrides.json` with domain-specific summaries, key points, and relationships.
2. Maintain source traceability in `config/source_url_map.json` for authoritative upstream links.
3. Repoint extraction and wiki output directories with `backend/process_raw_sources.py --output-root ...` and `backend/wiki_compiler.py --output-root ... --wiki-root ...` if your corpus layout differs from the default.
4. Rebrand the UI and adapt type tabs in `frontend/index.html` and `frontend/app.js` when reusing the framework for another team.


## Clone and Customize Handoff (No Bundled Data)
When stakeholders clone this framework, the fastest path is:
1. Add representative file types into `raw/`
2. Run `python backend/process_raw_sources.py raw --output-root backend/json` and then `python backend/wiki_compiler.py raw --output-root backend/json --wiki-root backend/wiki`
3. Curate `metadata_overrides.json` for summaries, key points, and relationships
4. Curate `config/source_url_map.json` for source traceability links.
5. Start local UI with `python backend/api.py` and review grounded answers/citations.
This sequence intentionally keeps onboarding lightweight for first-time adopters while preserving traceability and curation controls.


## Optional Provider Adapter Paths

The local-first path above is the baseline. Provider adapters are optional extensions for teams that need additional runtime capabilities.

Examples:
- local/open model adapter: use Ollama, LM Studio, or another OpenAI-compatible local endpoint for optional synthesis
- local persistence adapter: use SQLite, DuckDB, or file-backed JSONL for feedback, telemetry, and curator state
- vector adapter: use Chroma, Qdrant, LanceDB, Azure AI Search, or another vector backend behind the retrieval boundary
- graph adapter: use JSON graph files, NetworkX, Neo4j, Cosmos DB, or another graph-capable store behind the relationship boundary
- source-system adapter: sync from GitHub, Obsidian exports, Google Drive, SharePoint, Teams, Confluence, or another controlled source system

Adapter rule: the framework core must still run without the adapter. If an integration requires credentials, cloud resources, enterprise identity, or a managed service, it belongs behind a provider-specific boundary and should not be required for the quick start.


## Validation Checklist After a Build
- Note: this checklist applies after you run a local build using your own source corpus.
- `backend/json/` contains extracted `.json` files
- `backend/wiki/` contains generated `.md` pages and `backend/wiki/index.md`
- `metadata_overrides.json` has curated entries under documents
- `config/source_url_map.json` has URL mappings for docs you expect to cite
- `GET/health` returns healthy mode status once the API is running


## API Endpoints

| Endpoint | Description |
| :---- | :---- |
| `GET/` | Frontend shell |
| `GET/index.html` | Frontend shell HTML |
| `GET/styles.css` | Frontend stylesheet |
| `GET/app.js` | Frontend app script |
| `GET/graph_map.js` | Graph map script |
| `GET/faq.json` | FAQ payload for UI |
| `GET/graph-map` | Relationship map UI (currently templatized until corpus ingest) |
| `GET/graph_map_data` | Graph nodes/edges payload for visualization (currently scaffolded example data) |
| `GET/health` | Mode and service health |
| `POST/ask` | Demo answer with trace-style payload |
| `GET/wiki_index` | Wiki catalog for the documents sidebar |
| `GET/wiki/{page_id}` | Single wiki page payload (dynamic route) |
| `GET/feedback-review` | Curator space page |
| `GET/feedback-data` | Read local feedback events with optional `status` and `rating` query filters |
| `GET/triage_audit` | Read local triage actions derived from reviewed/proposed/resolved feedback events |
| `GET/wiki_freshness` | Local wiki freshness summary based on page modification and review metadata |
| `GET/lint/document` | Local wiki document lint summary for required structural fields |
| `GET/cascade_status` | Local cascade status placeholder; reports unavailable with zero pending work |
| `GET/query_telemetry_summary` | Local query/feedback term summary derived from feedback questions |
| `GET/graph_analytics_summary` | Local graph node/edge summary derived from compiled wiki relationships |
| `POST/feedback` | Record local feedback workflow event in `backend/feedback.jsonl` |
| `POST/feedback-triage` | Update local feedback status, curator note, and optional linked wiki page |
| `POST/feedback-propose-wiki` | Generate a Markdown wiki proposal draft from selected feedback events |
| `POST/wiki_mark_reviewed` | Mark a local wiki page reviewed in `backend/wiki/review_metadata.json` |
| `POST/wiki` | Create a Markdown wiki draft/analysis page and refresh the wiki index |

Feedback status values currently supported by the local file-backed workflow are `new`, `reviewed`, `proposed_wiki`, and `resolved`. Feedback is operator workflow data, not canonical knowledge. Durable knowledge changes happen through explicit wiki write-back.


## Curator Health in Plain Language (Non-Developer Guide)
RASCAL is meant to be understandable to more than just engineering teams. In Curator Space, the health panel answers one practical question:

**Can we trust the knowledge we are using to answer people right now?**

Use this quick translation:
- Stale Pages
  - What it means: content may be old or out of sync with source material
  - Why it matters: outdated policy/process content creates wrong answers.
  - What to do: prioritize review of stale pages first.
- Freshness Threshold
  - What it means: the review age limit (in days) before content is treated as needing attention.
  - Why it matters: sets your expected recertification cadence.
  - What to do: adjust the threshold only if your business/unit update cadence changes.
- Lint Errors/Lint Warnings
  - What it means: quality checks on structure, required fields, and linked references.
  - Why it matters: broken or inconsistent structure reduces retrieval quality.
  - What to do: resolve errors first, then warnings
- Cascade Pending
  - What it means: source items marked for deletion are still waiting for downstream cleanup
  - Why it matters: stale graph artifacts can keep old relationships visible
  - What to do: if the pending count grows, run/inspect the cascade worker flow
- Query Telemetry
  - What it means: how many real query events were observed for analysis
  - Why it matters: tells us what users actually ask, so indexing can be tuned to reality
  - What to do: review "Top Index Recommendations" and prioritize high-frequency field combinations.

Local demo note:
- In local-only mode, some cloud-back metrics (for example, cascade lifecycle) are shown as unavailable by design
- That is expected behavior in this framework and not an error.

Operational rule of thumb:
- If Freshness and Lint are healthy and telemetry recommendations are being reviewed regularly, answer quality should remain stable and explainable to non-developers.


## Response Schemas
*To be added*


## Frontend - Customization and Transparency
The frontend is a static, no-build-step HTML/CSS/JS application that is intentionally easy to adapt per corpus and use case.

At a high level, the UI provides:
- transparent answer grounding (trace, chunk visibility, citations)
- browsable wiki pages with type-based fitting
- feedback capture and write-back to wiki pages
- relationship map visualization of document links (graph view)
- a subtle internal navigation path to Curator Space (`/feedback-review`) from the main sidebar
In the relationship map view, users can:
- filter by node group and edge type
- focus on a selected node to view a 1-3 hop subgraph
- keep map settings/layout persisted across sessions
Framework-level frontend customizations are concentrated in:
- `frontend/index.html` for product naming, panel labels, and visible copy
- `frontend/app.js` for category mapping, external document links, and wiki catalog rendering
- `frontend/styles.css` for layout and visual treatment
- `frontend/README.md` for the UI-specific extension guide
At the moment, this map should be read as a template-based visualization layer. Because no real corpus has been ingested yet, the nodes and edges shown are scaffolded example relationships rather than live graph structures from source documents.


## Interaction Model (Important)
RASCAL is intentionally not a ChatGPT-style persistent chat product.
- There is no transcript-style cross-session chat memory ("hot caching" to be included)
- Answers are generated from current retrieval over the compiled wiki/source artifacts.
- Durable knowledge changes happen only through explicit write-back flows (for example, `POST /wiki` or curator-approved draft promotion)
- Operational logging can be added by downstream deployments, but logs are not treated as canonical wiki knowledge and are not a substitute for write-back.


 ## UI/UX Note: Curator Access Visibility
 Curator Space is intentionally discoverable but de-emphasized in the main UI. The sidebar includes an **Internal: Curator Space** link that opens `/feedback-review` in a new tab/window. This keeps curation workflows reachable for operators while avoiding prominence in the primary end-user chat flow.

 This pattern also keeps room for future role-based or environment-specific access controls without changing the core user journey.


 ## Critical Feature: Feedback and Write-Back
 This is an essential part of RASCAL's purpose.

 Without write-back, high-quality answers are one-time outputs. With write-back, validated answers become reusable wiki pages that improve future retrieval and coverage.

 This is the mechanism that turns the system into a compounding knowledge base instead of a stateless chat surface.

 *Mermaid Diagram?*

 Flow Highlights:
 - `POST /feedback` captures local feedback workflow events in `backend/feedback.jsonl`
 - `GET /feedback-data` reads feedback events for review and supports `status`/`rating` filters
 - `POST /feedback-triage` updates event status, curator note, and optional linked wiki page
 - `POST /feedback-propose-wiki` generates a Markdown proposal from selected feedback events
 - `GET /triage_audit` reports reviewed/proposed/resolved feedback actions
 - `GET /wiki_freshness`, `GET /lint/document`, `GET /query_telemetry_summary`, and `GET /graph_analytics_summary` expose local curator health signals
 - `POST /wiki_mark_reviewed` stores local review metadata in `backend/wiki/review_metadata.json`
 - Curator dashboard is served at `/feedback-review`
 - `POST /wiki` creates a Markdown wiki draft/analysis page and refreshes `backend/wiki/index.md`
 - Feedback logs are not canonical knowledge; explicit write-back is the boundary where reusable knowledge enters the wiki.
To keep the root README focused on the pipeline and runtime setup, detailed frontend documentation is now maintained in:
- `frontend/README.md`
That guide covers UI architecture, customization points, type taxonomy mapping, feedback review, and endpoint expectations.


## Key Directories
```
backend/    # API, retrieval, ingestion, pipeline scripts
frontend/    # Static HTML/CSS/JS client (no build step)
config/    # Source URL mapping and related runtime config
metadata_overrides.json    # Human curation layer for summaries/key points/relationships
raw/    # Source documents (user supplied, git-ignored in this branch)
backend/json/    # Generated extraction artifacts
backend/wiki/    # Generated markdown wiki output
```

## Framework Docs

- `documentation/README.md` - documentation index
- `documentation/STACK-OPEN-ARCHITECTURE.md` - local-first/provider-open architecture guidance and adapter boundaries
- `documentation/FRONTEND-PRINCIPLES.md` - frontend transparency, customization, and route expectations
- `documentation/SCORECARD.md` - domain fit and PoC readiness scorecard
- `documentation/FUTURE-ENHANCEMENTS.md` - optional maturity roadmap
- `documentation/WHITEPAPER.md` - conceptual framing and references


## Component Guides

*to be added*


## POC Scope
This repo intentionally prioritizes:
- transparency and grounded behavior
- deterministic local iteration
- simple, auditable architecture
It does not aim to be production-hardened by default.


## Corpora That Work Best
RASCAL performs best when the source corpus is:
- bounded and intentionally selected, not open-ended or continuously expanding wider than users can track
- policy/procedure heavy (requirements, directives, SOPs, controls, forms, primary sources, tech specs)
- semi-structured (clear headings, sections, tables, repeated document patterns)
- domain-consistent (shared terminology across documents)
- relatively stable (not changing daily)
- citation-sensitive (users need traceable source links)
- ingested deliberately by humans who decide what belongs in the wiki
Typical strong-fit domains:
- compliance and risk policy libraries
- operational procedures and playbooks
- internal governance frameworks
- corporate structures: finance, credit, underwriting; legal structures: policies, procedures; academic structures: primary sources, papers


## Corpora That Are a Weaker Fit (for this PoC)
These still can work, but usually need more preprocessing and curation:
- unbounded corpora that are expected to ingest everything automatically
- live telemetry, IoT (Internet of Things), event-stream, or operational signal data feeds
- mostly unstructured narratives with little section hierarchy
- scanned/image heavy files with poor OCR quality
- highly conflicting versions of the same policy without a clear source of truth
- fast-changing corpora where content is updated continuously throughout the day
- corpora where answers require heavy cross-document reasoning beyond direct grounding


## Recommended Number of Source Documents

| `Corpus Size` | `Recommendation for RASCAL PoC` | `Why` |
| :---- | :---- | :---- |
| `1 to 10 docs` | `Too small for meaningful retrieval evaluation` | `Better for parser smoke tests than assistant quality` |
| `20 to 75 docs` | `Best starting range` | `Fast iteration, easy human curation, clear signal on retrieval quality` |
| `75 to 250 docs` | `Strong PoC range` | `Realistic complexity while still manageable with manual metadata/URL curation` |
| `250 to 500 docs` | `Upper PoC range` | `Works, but requires disciplined curation and version control` |
| `500+ docs` | `Beyond comfortable PoC scope` | `Usually needs automation for metadata governance and source mapping` |

Practical guidance:
- If this is your first run, target 30 to 60 representative documents
- Include a mix of document patterns/types
- Avoid loading every historical version initially; prefer current approved documents
- Treat corpus expansion as a curation step: add documents intentionally, rebuild, then review the wiki output


## Why Corpus Size Matters
The core pipeline is automated, but quality still depends on human curation in:
- `metadata_overrides.json`
- `config/source_url_map.json`
This PoC assumes wiki ingestion is deliberate rather than ambient. Humans select which source documents to place in `raw/`, review the generated artifacts, and curate the metadata layer before treating the corpus as part of the assistant's knowledge base.

As corpus size grows, the effort to keep those two files complete and accurate increases as well. That is the main scaling limiter in this PoC, not extraction speed.



## Future Enhancements

*moved to its own documentation*


## References
**Where These References Connect in this README**
- Trust calibration and uncertainty posture:
  - Framework Branding and Philosophy → Calibrated Trust as the Core Principle
  - Manifesto (bounded probabilistic authority, explainability)
- Human governance and operating model:
  - Human Curation Layer → Human Curation and Governance Model
  - Future Enhancements → Team Governance and Identity
- Ontology and Structure-aware retrieval framing:
  - Feasibility and Fit → Domain-Driven Design: Build Your Own Taxonomies and Ontologies
  - Concept and Metadata Node Framework
- Knowledge-management fit and implementation constraints:
  - Feasibility and Fit (boundedness, readiness, reviewability)
  - PoC Scope and corpus-size guidance
 

## Citations
- Andrej Karpathy. LLM Wiki concept (wiki-first architecture)
- Pengchen Jiang et al. (2026). RAS: Retrieval-And-Structuring for Knowledge-Intensive LLM Generation
- Megan Leanda Berry. (2025). The Human Layer in GraphRAG: Roles, RACI, and the first 90 Days.
- Community implementation reference: ScrapingArt/Karpathy-LLM-Wiki-Stack
- FastAPI documentation
- Louafi, Bilal; Nessah, Dhamel; and Meheleain, Ridha. (2025). AI-Based Knowledge Management Systems: A Review of AI Techniques, Applications, and Challenges.
- Mojtaba, Rezasi. (2025). Artificial Intelligence in knowledge management: identifying and addressing the key implementation challenges.
- Amy Turner, Meena Kaushik, Mu-Ti Huang, and Srikar Varanasi. (2024). Calibrating Trust in AI-Assisted Decision Making.
- Magdalena Wischnewski, Nicole Kramer, and Emmanuel Muller. (2023). Measuring and Understanding Trust Calibrations for Automated Systems: A Survey of the State-of-the-Art and Future Directions.
- Kartik Sharma, Peeyush Kumar, Yunqig Li. (2024). OG-RAG: Ontology-Grounded Retrieval-Augmented Generation for Large Language Models
- Jinyu Wang, Jingjig Fu, Rui Wang, Lei Song, and Jiang Bian. (2025). PIKE-RAG: sPecialized KnowledgE and Rationale Augmented Generation.
- Ngoc Luyen Le, Marie-Helene Abel, and Bertrand Laforge. (2026). From Prompts to Context: An Ontology-Driven Framework for Human-Generative AI Collaboration.
