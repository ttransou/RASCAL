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
