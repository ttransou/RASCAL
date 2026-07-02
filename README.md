# RASCAL 🃏
### Retrieval Augmented Semantic Calibrated Active Learning

T. Transou - June 2026 - 🚧 Active Development 🚧


**Conceptual lineage:** This repo was originally an Azure-stack iteration of Andrej Karpathy's LLM Wiki gist. It follows the same wiki-first grounding idea, but adapts it to an Azure-oriented runtime, pipeline, and retrieval pattern. It is also directionally aligned with retrieval-and-structuring research, such as RAS (Retrieval-And-Structuring for Knowledge-Intensive LLM Generation), particularly in its emphasis on structured intermediate knowledge over flat passage-only retrieval.

RASCAL is a lightweight, wiki-first framework for building grounded assistants over **bounded, curated document corpora** with transparent retrieval and traceable citations.

**Basic Premise:** Instead of forcing the model to rediscover raw documents for every question, this repo compiles source material into a persistent wiki-shaped knowledge layer that can be reviewed, curated, and reused.

**Purpose:** This repository is the reusable Azure-stack baseline for that pattern. It is intentionally framework-only and does not ship bundled domain data. Any raw/sources markdown belongs to the source corpus you bring into the framework, not to the framework itself. The goal is to provide the extraction pipeline, wiki compilation flow, retrieval surface, and UI/API scaffolding needed to turn a curated corpus into an explainable assistant.

**Customization by design:** you are not locked into predefined taxonomies or relationship types. For each corpus, you define the document types, relationship semantics, and metadata structures that reflect your domain's actual knowledge model. In short, JSON config files, not code. Whether you ingest policy/compliance documents, technical specifications, operational procedures, or the complete works of Seneca the Younger, the framework adapts to your ontology, not the other way around.

For teams that need standards-based semantic interoperability, optional SPARQL/ontology support is positioned as a domain-specific extension path (see Future Enhancements) rather than part of the domain-agnostic baseline.

**How this differs from traditional RAG:** In a standard RAG setup, the system retrieves chunks from raw files at query time and synthesizes an answer on demand. In this framework, raw files are first transformed into structured artifacts and compiled into a maintained wiki representation. Retrieval and answering happen against that persistent layer, while source documents remain available for traceability.

This also aligns with recent evidence that retrieval-only pipelines are often insufficient for harder domain tasks unless paired with stronger knowledge organization and reasoning structures. (Wang et al., 2025).

**Compounding Loop:** Validated answers can be written back to the wiki, so useful outputs become reusable knowledge pages rather than one-time responses.

> "This is the key difference: the wiki is a persistent, compounding artifact."
> -- Andrej Karpathy, LLM Wiki (cited in References)

This follows the same high-level idea described in Karpathy's LLM Wiki gist: the knowledge base is a compounding artifact, not just a transient retrieval target. Here, that idea is implemented for bounded corpora (previously enterprise-level) with explicit ingestion, deterministic compilation paths, and Azure-oriented runtime patterns.


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
The implementation is intentionally bounded; it is not designed as a general agent framework or a model-agnostic chatbot.
- No Claude usage: this repo does not use Claude models in pipeline or runtime behavior. When Claude becomes more affordable for organizations and individual users, it may be a consideration for RASCAL.
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
- **Document type taxonomy** in `metadata_definitions.json` where you can rename or expand types to fit your domain
- **Relationship/edge type registry** in `metadata_definitions.json` where you declare which relationship types exist in your domain and their semantics, weight defaults, and confidence thresholds.
- **Metadata enrichment rules** in `metadata_overrides.json` where you curate document summaries, key points, and relationships specific to your context.
- **Fallback answers and response templates** in `config/fallback_qa.json` and `config/fallback_templates.json` where you inject domain-specific knowledge and phrasing.

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

The SCORECARD.md includes:
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
- Template config (`config/fallback_qa.json`, `config/fallback_templates.json`, `config/source_url_map.json`, the last may not be applicable to your corpus)
- Metadata taxonomy seed file (`metadata_definitions.json`)
- Schema placeholder docs (`config/schema/SCHEMA.md`)
- Empty metadata stubs (`metadata_overrides.json` with "documents":{})
- Environment template (`.env.example`)
- Placeholder directories (`raw/.gitkeep`)

RASCAL does not contain source documents, compiled wiki output, or domain-specific fallback answers.


## Human Curation Layer - The Two Required Files ✌
RASCAL is entirely automated EXCEPT for two JSON files that require human curation 🧠:
- `metadata_overrides.json` - enriches extracted metadata (summary, key points, relationships)
- `config/source_url_map.json` - Maps internal doc IDs to source location by URL and external validation (could be optional)
🧠 Required before production: complete both files with dataset-specific values and reviewer ownership.

Everything else is automated:
- Document extraction (`process_raw_sources.py`) → JSON
- Wiki compilation (`wiki_compiler.py`) → Markddown + index
- Retrieval, citation, tracing →  API Endpoints


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
- document-level HITL reviewed linkage (semantic tier strengths)
- per-link HITL reviewed override with explicit weight/confidence
🧠 **Customization point:** replace all example document keys, relationship targets, and confidence semantics with your domain-specific curated values.

```json
{
  "documents":{
    "doc_id_or_title":{
      "summary":"Human-written summary of this document's purpose and scope.",
      "key_points":[
        "Point 1: What users must understand.",
        "Point 2: Critical rule or constraint.",
      ],
      "relationships":[
      "requires":["ref_to_prerequisite_doc"],
      "depends_on":["ref_to_parent_policy"],
      "related_to":["ref_to_sibling_concept"]
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
- simple string form (backward compatible):
  - "requires": ["doc_b", "doc_c"]
- rich object form (recommended for curation-aware graph edges):
  - "requires": [{"target":"doc_b","weight":0.95, "confidence": 1.0, "human_reviewed":true, "provenance":"curated"}]
When object form is used, ingestion preserves link-level metadata on the edge record (weight, confidence, human_reviewed, provenance, optional labels, and dates).

If simple string form is used, RASCAL defaults apply by relationship type:
- `requires`: strongest defaults (weight=1.0, confidence=0.95)
- `depends_on`: medium defaults (weight=0.8, confidence=0.8)
- `related_to`: lowest defaults (weight=0.6, confidence=0.65)
Per-link object value always overrides these defaults.

HITL gating behavior:
- before HITL review, relationship links are treated as provisional and stored with neutral strength (weight=0.5, confidence=0.5)
- After HITL review is marked complete ("human_reviewed": true at document override level, or per-link), semantic tier strengths are applied automatically.
- custom per-link weight/confidence are only honored after HITL review (document-level or per-link)

Framework requirement for all adopters:
- Each team must define its own dataset policy for what qualifies as `requires`, `depends_on`, and `related_to`
- Each team must define HITL ownership (who reviews, approval criteria, and escalation path)
- Each team must define when document-level review is allowed vs per-link review only.
- Each team must define confidence/weight override rules for their domain
- These choices should be recorded in `metadata_overrides.json` under `curation_policy` before product onboarding.


## Source URL Map Structure
```json
{
  "by_doc_id":{
    "doc_id", "http://wwww.whatever.com/../document.docx"
  },
    "by_source_file":{
      "filename.docx":"http://www.whatever.com/../filename.docx"
  },
    "by_title":{
      "Document Title":"http://www.whatever.com/../document.docx"
  }
}
```

🧠 **Customization point:** map each real source document to its canonical system-of-record URL.
How to fill it in:
- map each document's internal ID, filename, or title to its source URL
- users see the source URL in the frontend (example: "View in Sharepoint/Drive" link)
- All three indexes point to the same upstream documents and pick whichever keys make sense for your corpus.


## Configuration and Customization Surfaces
**This section defines where you inject domain knowledge.**

RASCAL carefully distinguishes between framework infrastructures (the code and structure that remain constant across deployments) and domain customization (the vocabularies, definitions, and business/schema rules that change with each corpus).

For enterprise reuse, it helps to separate what you must provide to get the framework running from what you may customize to adapt it to a new domain, operating model, or UI.


## Required to Run vs. Optional to Customize
| Surface                                   | Required to run?                                           | When it becomes required                                               | Why it exists                                                                            |
| ----------------------------------------- | ---------------------------------------------------------- | ---------------------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| Source documents in `raw/`                  | Yes                                                        | Any real pipeline run                                                  | The framework need a corpus to extract and compile                                       |
| `metadata_overrides.json`                   | Yes for a proper corpus run                                | Before treating the wiki as curated knowledge                          | Human summaries, key points, and relationships are part of the framework’s quality model |
| `config/source_url_map.json`                | Yes for production-like traceability                       | Before expecting source links in citations/UI                          | Preserves traceability back to authoritative source systems                              |
| `metadata_definitions.json`                 | Yes for metadata synthesis workflows                       | Before relying on normalized document types                            | Defines your taxonomy and must be curated for domain-fit                                 |
| Python environment + requirements.txt     | Yes                                                        | Always                                                                 | Needed for the parser, API, and local runtime                                            |
| Azure Open AI env vers                    | Only for `--wiki-mode llm` or non-simulated chat synthesis | When using Azure-backed LLM paths                                      | Enables LLM completion, embeddings, and chat synthesis                                   |
| Cosmose env vers                          | Only for ingestion/cloud mode                              | When omitting `--skip-ingest` or running cloud-backed retrieval        | Enables graph ingestion and cloud-mode date access                                       |
| metadata_definitions.json                 | No                                                         | Only when changing or extending the default type taxonomy              | Adjusts the document classification vocabulary                                           |
| `config/fallback_qa.json`                   | No                                                         | When you want tailored low-evidence or pre-corpus answers              | Lets you inject domain-specific fallback behavior                                        |
| `config/fallback_template.json`             | No                                                         | When you want to tune the assistant wording and clarification behavior | Lets you alter response template without code changes                                    |
| `frontend/*` branding and tab mapping       | No                                                         | When white-labeling or adapting the UI to a new corpus                 | Supports reuse across teams and domains                                                  |
| Pipeline flags in `backend/run_pipeline.py` | No                                                         | When changing flow, directories, or deployment mode                    | Makes the same framework reusable across local and cloud workflows                       |


## Minimum Required to Run Locally
For the smallest credible local run, you need only:
- dependencies installed from requirements.txt
- a few source files in `raw/`
- curated `metadata_overrides.json`
- curated `config/source_url_map.json`
- scaffold mode pipeline run with `--skip-ingest`
- local API with `--local-mode`
Everything else in this section is about adaptation, enrichment, or alternate runtime paths.


## Optional Enterprise Customization
These are the main reuse levers when adapting RASCAL for another business unite, area, corpus, or product surface:
- taxonomy customization in `metadata_definitions.json`
- fallback and clarification behavior in `config/fallback_qa.json` and `config/fallback_templates.json`
- Azure development wiring in `.env`
- pipeline pathing and mode selection in `backend/run_pipeline.py`
- UI naming, category mapping, and external links in `frontend/app.js` and `frontend/index.html`


| File/Surface | What it controls | Typical customization |
| :---- | :---- | :---- |
| `metadata_definition.json` | Domain-specific taxonomy (document types, relationship/edge-types, term definitions) used throughout the pipeline | This is where you define your domain’s ontology – document types, relationship semantics, edge type registries, weight/confidence defaults, and term definitions for your corpus. Required customization point. |
| `metadata_overrides.json` | Per-document human curation and default metadata | Add summaries, key points, relationships, and final type overrides |
| `config/source_url_map.json` | Source-document links used in citations and UI | Point citations to SharePoint, Drive, etc., file portals, or document systems |
| `config/fallback_qa.json` | Domain-specific canned answers when no grounded wiki answer is available | Add starter FAQ behavior before you corpus is loaded |
| `config/fallback_templates.json` | Working templates for capability, clarification, and insufficient-context responses | Tune assistant tone and follow-up prompts without editing code |
| `.env/.env.example` | Azure OpenAI, Cosmos, and ingestion tuning knobs | Set deployments, endpoints, chunk sizing, and semantic break thresholds |
| `backend/run_pipeline.py` | End-to-end pipeline orchestration | Switch between wiki-first vs. legacy, scaffold vs. LLM, local vs. ingest-enabled runs |
| `frontend/app.js` \+ `frontend/FRONTEND-README.md` | UI labels, type-to-tab mapping, external files, and catalog behavior | Rebrand the UI, adapt type tabs, and expose richer metadata in the browser |


## What Each Surface Actually Does
**`metadata_definitions.json`**
- supplies the term definitions consumed by `synth_metadata.py`
- helps normalize extracted document types before wiki compilation
- is the right place to adapt RASCAL from policy-style corpora to a different domain taxonomy

**`config/fallback_qa.json` and `config/fallback_templates.json`**
- `fallback_qa.json` stores explicit fallback answers and clarifying questions
- `fallback_templates.json` stores reusable output phrasing for capability, clarification, and low-evidence responses
- These files let you customize assistant behavior safely without editing prompt logic in `graph_api.py/graph_chat.py`

**`.env` runtime controls**
- Azure chat path: ETC ETC
- Embedding path: ETC ETC
- Cloud graph path: ETC ETC
- Ingestion quality/cost tradeoffs: ETC ETC

**`backend/run_pipeline.py` orchestration switches**
- `--pipeline-mode wiki-first|legacy`: choose the newer integrated flow or the older multi-step flow
- `--wiki-mode skip|scaffold|llm`: skip wiki compilation, compile deterministically, or compile with Azure OpenAI assistance
- `--skip-ingest`: stay local and avoid Cosmos ingestion
- `health-url`: verify API health after pipeline completion
- Path flags such as `--raw-dir`, `--output-dir`, `--wiki-root`, and `wiki-dir` make it possible to re-point RASCAL at a different corpus layout with editing code

**Frontend customization**
- `frontend/app.js` controls type normalization, wiki tab behavior, external links, and model/catalog rendering
- `frontend/index.html` controls visible branding, labels, and the app shell layout
- `frontend/FRONTEND-README.md` already documents the UI-specific customization points in more detail


## Concept and Metadata Node Framework
This section defines how to add concept and metadata nodes in a way that is explainable, repeatable, and explicit about where human curation is required.

**Explainable Processing Contract**
Fro each ingested document, the system should produce a small processing trace:
- input document id/title
- extracted concept candidates
- emitted metadata nodes
- emitted edges (`mentions`, `defines`, `has_metadata`, etc.)
- curation status (`auto`, `reviewed`, `rejected`)
This keeps graph expansion auditable and helps reviewers understand why a node or edge exists.


## Auto vs Human Curation Boundaries
