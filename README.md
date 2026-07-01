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


## Human Curation Marker
In the following repo (not just the README), any section labeled with 🧠 requires human customization for your dataset/domain before production use.


## Framework Branding and Philosophy
> **Retrieval Augmented Semantic Calibrated Active Learning**

This name reflects both the implementation and the philosophy:
- **Retrieval:** answers are grounded in bounded corpora, not open-domain speculation
- **Augmented:** AI amplifies curator judgment; it does not replace accounable human review
- **Semantic:** knowledge is structured through domain-specific document types, edge types, and metadata.
- **Calibrated:** trust is earned through traceability, confidence signals, and explicit human-in-the-loop gates.'
- **Active Learning:** feedback, triage, and write-back create a compounding loop where the system improves with use.


## Calibrated Trust as the Core Principle
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



## Manifesto!
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


## Out of Scope (To Avoid Confusion)
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


## Intended Audience
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


## Domain-driven Design: Build Your Own Taxonomies and Ontologies (or don't)
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

## Self-assessment: Is your domain a good fit?
Before bringing a dataset to RASCAL, use the AI KMS Domain Feasibility Scorecard to independently assess two dimensions:
- **Value:** How useful would AI-assisted retrieval be for this domain? (e.g., reuse frequency, retrieval pain, decision impact)
- **Readiness**: How suitable is the current content for AI use without excessive curation/pre-processing? (e.g., structural coherence, semantic clarity, documentation currency)
