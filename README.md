# RASCAL
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
