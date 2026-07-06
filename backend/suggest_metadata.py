"""Optional spaCy-powered metadata suggestion spike.

This script generates *suggestions* from ingested JSON artifacts and writes them
into a separate output file. It does not modify metadata_overrides.json.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import spacy


MODEL_PROFILES: dict[str, str] = {
    "framework-default": "en_core_web_sm",
    "lightweight": "en_core_web_sm",
    "balanced": "en_core_web_md",
    "high-accuracy": "en_core_web_lg",
}


def profile_guide() -> dict[str, str]:
    return {
        "framework-default": "Keeps baseline lightweight and broadly compatible.",
        "lightweight": "Fastest startup/runtime for constrained environments.",
        "balanced": "Recommended for richer entity/term extraction in most corpora.",
        "high-accuracy": "Higher quality at greater memory/runtime cost.",
    }


def resolve_model(model_profile: str, explicit_model: str | None) -> tuple[str, str]:
    if explicit_model and explicit_model.strip():
        return explicit_model.strip(), "explicit"
    return MODEL_PROFILES.get(model_profile, MODEL_PROFILES["framework-default"]), model_profile


def load_docs(path: Path) -> list[dict[str, Any]]:
    docs: list[dict[str, Any]] = []

    if path.is_dir():
        for item in sorted(path.rglob("*.json")):
            try:
                payload = json.loads(item.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue

            if isinstance(payload, list):
                docs.extend(x for x in payload if isinstance(x, dict))
            elif isinstance(payload, dict):
                docs.append(payload)
        return docs

    if path.exists():
        payload = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            docs.extend(x for x in payload if isinstance(x, dict))
        elif isinstance(payload, dict):
            docs.append(payload)

    return docs


def load_nlp(model: str) -> tuple[Any, bool]:
    try:
        return spacy.load(model), True
    except OSError:
        nlp = spacy.blank("en")
        if "sentencizer" not in nlp.pipe_names:
            nlp.add_pipe("sentencizer")
        return nlp, False


def can_load_model(model: str) -> bool:
    try:
        spacy.load(model)
        return True
    except OSError:
        return False


def build_model_availability_report(explicit_model: str | None = None) -> dict[str, Any]:
    profiles = {
        profile: {
            "model": model,
            "available": can_load_model(model),
        }
        for profile, model in MODEL_PROFILES.items()
    }

    explicit: dict[str, Any] | None = None
    if explicit_model and explicit_model.strip():
        explicit = {
            "model": explicit_model.strip(),
            "available": can_load_model(explicit_model.strip()),
        }

    return {
        "note": "Model availability check for local spaCy runtime.",
        "profiles": profiles,
        "explicit_model": explicit,
        "fallback": "blank-en-sentencizer",
    }


def clean_sentence(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text


def suggest_summary(sentences: list[str]) -> str:
    for sent in sentences:
        candidate = clean_sentence(sent)
        if len(candidate) >= 40:
            return candidate[:280]
    return clean_sentence(sentences[0])[:280] if sentences else ""


def sentence_score(sentence: str, entities: set[str]) -> int:
    score = 0
    lowered = sentence.lower()
    score += min(len(sentence) // 40, 5)
    score += sum(2 for ent in entities if ent.lower() in lowered)
    if any(token in lowered for token in ("must", "required", "shall", "should", "not")):
        score += 2
    return score


def suggest_key_points(sentences: list[str], entities: set[str], max_points: int) -> list[str]:
    ranked = sorted(
        ((sentence_score(s, entities), clean_sentence(s)) for s in sentences if clean_sentence(s)),
        key=lambda x: x[0],
        reverse=True,
    )

    chosen: list[str] = []
    for _, sentence in ranked:
        if sentence not in chosen:
            chosen.append(sentence)
        if len(chosen) >= max_points:
            break
    return chosen


def top_terms(text: str, max_terms: int) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", text)
    stop = {
        "the", "and", "for", "that", "with", "from", "this", "are", "was", "were", "has", "have",
        "will", "into", "their", "your", "not", "you", "can", "all", "any", "but", "use", "using",
        "its", "our", "out", "one", "two", "three", "about", "also", "more", "such", "than",
    }
    filtered = [w.lower() for w in words if w.lower() not in stop]
    counts = Counter(filtered)
    return [term for term, _ in counts.most_common(max_terms)]


def doc_key_from_path(path: str) -> str:
    return Path(path).stem.replace(" ", "-")


def generate_suggestions(
    docs: list[dict[str, Any]],
    *,
    model: str,
    model_profile: str,
    model_source: str,
    max_points: int,
    max_entities: int,
    max_terms: int,
) -> dict[str, Any]:
    nlp, model_loaded = load_nlp(model)

    output: dict[str, Any] = {
        "note": "Suggestions only. Review manually before copying to metadata_overrides.json.",
        "spacy_model": model if model_loaded else "blank-en-sentencizer",
        "requested_model": model,
        "model_profile": model_profile,
        "model_selection_source": model_source,
        "model_profile_guide": profile_guide(),
        "documents": {},
    }

    for doc_item in docs:
        path = str(doc_item.get("path", ""))
        text = str(doc_item.get("text", "")).strip()
        if not text:
            continue

        parsed = nlp(text)
        sentences = [s.text.strip() for s in parsed.sents if s.text.strip()]
        entities = [ent.text.strip() for ent in getattr(parsed, "ents", []) if ent.text.strip()]

        entity_counts = Counter(entities)
        top_entities = [name for name, _ in entity_counts.most_common(max_entities)]

        key = doc_key_from_path(path) if path else f"doc_{len(output['documents']) + 1}"
        output["documents"][key] = {
            "source_path": path,
            "suggested": {
                "summary": suggest_summary(sentences),
                "key_points": suggest_key_points(sentences, set(top_entities), max_points),
                "entities": top_entities,
                "terms": top_terms(text, max_terms),
                "relationships": {
                    "requires": [],
                    "depends_on": [],
                    "related_to": [],
                },
            },
            "guardrails": {
                "human_review_required": True,
                "do_not_auto_apply": True,
            },
        }

    return output


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate metadata suggestions from ingested JSON docs.")
    parser.add_argument(
        "documents",
        type=Path,
        nargs="?",
        help="Path to ingested docs JSON (file or directory, e.g. backend/json)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent / "json" / "metadata_suggestions.json",
        help="Output file for suggestions (default: backend/json/metadata_suggestions.json)",
    )
    parser.add_argument(
        "--model-profile",
        choices=["framework-default", "lightweight", "balanced", "high-accuracy"],
        default="framework-default",
        help=(
            "Model profile for corpus context. "
            "Defaults to framework-default; overridden by --model when provided."
        ),
    )
    parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Explicit spaCy model name (overrides --model-profile when set)",
    )
    parser.add_argument(
        "--check-models",
        action="store_true",
        help="Print availability for profile models (and optional --model) then exit",
    )
    parser.add_argument("--max-points", type=int, default=5, help="Maximum suggested key points per doc")
    parser.add_argument("--max-entities", type=int, default=12, help="Maximum suggested entities per doc")
    parser.add_argument("--max-terms", type=int, default=12, help="Maximum suggested frequent terms per doc")
    args = parser.parse_args()

    if args.check_models:
        report = build_model_availability_report(args.model)
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return

    if args.documents is None:
        parser.error("the following arguments are required unless --check-models is used: documents")

    selected_model, model_source = resolve_model(args.model_profile, args.model)

    docs = load_docs(args.documents)
    result = generate_suggestions(
        docs,
        model=selected_model,
        model_profile=args.model_profile,
        model_source=model_source,
        max_points=max(1, args.max_points),
        max_entities=max(1, args.max_entities),
        max_terms=max(1, args.max_terms),
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    print(
        "Generated suggestions for "
        f"{len(result['documents'])} document(s): {args.output} "
        f"(requested model: {selected_model}, loaded: {result['spacy_model']})"
    )


if __name__ == "__main__":
    main()
