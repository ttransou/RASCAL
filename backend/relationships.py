"""Relationship normalization and HITL edge semantics.

The local runtime accepts a concise relationship shorthand for easy curation,
but normalizes every edge to a richer object before graph use.
"""
from __future__ import annotations

from typing import Any


DEFAULT_STRENGTHS: dict[str, dict[str, float]] = {
    "requires": {"weight": 1.0, "confidence": 0.95},
    "depends_on": {"weight": 0.8, "confidence": 0.8},
    "related_to": {"weight": 0.6, "confidence": 0.65},
}
PROVISIONAL_STRENGTH = {"weight": 0.5, "confidence": 0.5}


def clamp_score(value: Any, default: float) -> float:
    try:
        score = float(value)
    except (TypeError, ValueError):
        return default
    return round(min(max(score, 0.0), 1.0), 4)


def default_strength(relation_type: str, *, human_reviewed: bool) -> dict[str, float]:
    if not human_reviewed:
        return dict(PROVISIONAL_STRENGTH)
    return dict(DEFAULT_STRENGTHS.get(relation_type, {"weight": 0.7, "confidence": 0.7}))


def normalize_relationship(
    relation_type: str,
    item: Any,
    *,
    document_human_reviewed: bool = False,
    default_provenance: str = "metadata_overrides",
) -> dict[str, Any] | None:
    """Convert a string or object relationship item to a canonical edge."""

    if isinstance(item, dict):
        target = str(item.get("target") or item.get("id") or item.get("title") or "").strip()
        link_human_reviewed = bool(item.get("human_reviewed", document_human_reviewed))
        provenance = str(item.get("provenance") or default_provenance)
        explicit_weight = item.get("weight")
        explicit_confidence = item.get("confidence")
    else:
        target = str(item).strip()
        link_human_reviewed = bool(document_human_reviewed)
        provenance = default_provenance
        explicit_weight = None
        explicit_confidence = None

    if not target:
        return None

    strength = default_strength(relation_type, human_reviewed=link_human_reviewed)
    if link_human_reviewed:
        weight = clamp_score(explicit_weight, strength["weight"])
        confidence = clamp_score(explicit_confidence, strength["confidence"])
    else:
        weight = strength["weight"]
        confidence = strength["confidence"]

    return {
        "target": target,
        "weight": weight,
        "confidence": confidence,
        "human_reviewed": link_human_reviewed,
        "provenance": provenance,
        "review_state": "reviewed" if link_human_reviewed else "provisional",
    }


def normalize_relationships(
    relationships: dict[str, Any],
    *,
    document_human_reviewed: bool = False,
    default_provenance: str = "metadata_overrides",
) -> dict[str, list[dict[str, Any]]]:
    normalized: dict[str, list[dict[str, Any]]] = {}
    for relation_type, raw_items in relationships.items():
        items = raw_items if isinstance(raw_items, list) else [raw_items]
        edges = [
            edge
            for edge in (
                normalize_relationship(
                    str(relation_type),
                    item,
                    document_human_reviewed=document_human_reviewed,
                    default_provenance=default_provenance,
                )
                for item in items
            )
            if edge is not None
        ]
        if edges:
            normalized[str(relation_type)] = edges
    return normalized
