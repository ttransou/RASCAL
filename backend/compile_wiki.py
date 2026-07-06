"""Primary implementation for the wiki compilation pipeline.

This module contains the actual ingest-and-compile workflow. The
backend/wiki_compiler.py entry point is a thin compatibility wrapper that
calls this implementation.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List

try:
    from .ingest import ingest as run_ingest
except ImportError:  # pragma: no cover - direct script execution fallback
    from ingest import ingest as run_ingest


def _document_title(path: str) -> str:
    return Path(path).stem.replace(" ", "-")


def _slugify(title: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", title).strip("-").lower()
    return slug or "page"


def compile_wiki(
    docs: Iterable[Dict[str, Any]],
    metadata_overrides: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    """Compile structured wiki pages from extracted documents.

    Each page contains a Markdown body, a title, and the source path.
    Metadata overrides are used when present to enrich the page summary,
    key points, and relationship sections.
    """
    metadata_overrides = metadata_overrides or {"documents": {}}
    document_metadata = metadata_overrides.get("documents", {})

    pages: List[Dict[str, Any]] = []
    for doc in docs:
        title = _document_title(str(doc.get("path", "untitled")))
        body = str(doc.get("text", ""))
        override = document_metadata.get(title) or document_metadata.get(Path(str(doc.get("path", ""))).stem)

        lines: List[str] = [f"# {title}", ""]
        if override:
            summary = override.get("summary")
            if summary:
                lines.extend([summary, ""])

            key_points = override.get("key_points") or []
            if key_points:
                lines.append("## Key Points")
                lines.extend(f"- {point}" for point in key_points)
                lines.append("")

            relationships = override.get("relationships") or {}
            if relationships:
                lines.append("## Relationships")
                for relation_name, related_items in relationships.items():
                    if related_items:
                        joined = ", ".join(str(item) for item in related_items)
                        lines.append(f"- **{relation_name}**: {joined}")
                lines.append("")

        lines.append("## Source Extract")
        lines.append("")
        lines.append(body)

        pages.append(
            {
                "title": title,
                "path": str(doc.get("path", "")),
                "markdown": "\n".join(lines).strip() + "\n",
            }
        )

    return {"pages": pages}


def compile_wiki_from_files(
    documents_path: str | Path,
    metadata_path: str | Path | None = None,
) -> Dict[str, Any]:
    """Load JSON documents and metadata overrides, then compile wiki pages."""
    documents_path = Path(documents_path)
    docs: List[Dict[str, Any]] = []

    if documents_path.is_dir():
        for document_file in sorted(documents_path.rglob("*.json")):
            try:
                payload = json.loads(document_file.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue

            if isinstance(payload, list):
                docs.extend(payload)
            elif isinstance(payload, dict):
                docs.append(payload)
    elif documents_path.exists():
        payload = json.loads(documents_path.read_text(encoding="utf-8"))
        if isinstance(payload, list):
            docs.extend(payload)
        elif isinstance(payload, dict):
            docs.append(payload)

    metadata_overrides = None
    if metadata_path is not None:
        metadata_path = Path(metadata_path)
        if metadata_path.exists():
            metadata_overrides = json.loads(metadata_path.read_text(encoding="utf-8"))

    return compile_wiki(docs, metadata_overrides)


def write_wiki_pages(result: Dict[str, Any], output_dir: str | Path) -> List[Path]:
    """Write compiled wiki pages to Markdown files in the supplied directory."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    written_paths: List[Path] = []
    for page in result.get("pages", []):
        title = str(page.get("title", "page"))
        slug = _slugify(title)
        page_path = output_dir / f"{slug}.md"
        page_path.write_text(page.get("markdown", ""), encoding="utf-8")
        written_paths.append(page_path)

    index_path = output_dir / "index.md"
    index_lines = ["# Wiki Index", ""]
    for page in result.get("pages", []):
        title = str(page.get("title", "page"))
        slug = _slugify(title)
        index_lines.append(f"- [{title}]({slug}.md)")
    index_path.write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    return written_paths


def resolve_output_path(path: str | Path | None) -> Path | None:
    if path is None:
        return None
    if isinstance(path, Path) and path.is_absolute():
        return path
    return (Path(__file__).resolve().parent.parent / Path(path)).resolve()


def main() -> None:
    parser = argparse.ArgumentParser(description="Ingest documents and compile them into wiki Markdown pages.")
    parser.add_argument("source", type=Path, help="File or directory to ingest")
    parser.add_argument(
        "--metadata",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "metadata_overrides.json",
        help="Path to metadata_overrides.json",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path(__file__).resolve().parent / "json",
        help="Directory for per-document JSON output",
    )
    parser.add_argument(
        "--wiki-root",
        type=Path,
        default=Path(__file__).resolve().parent / "wiki",
        help="Directory for generated Markdown wiki pages",
    )
    args = parser.parse_args()

    args.metadata = resolve_output_path(args.metadata)
    args.output_root = resolve_output_path(args.output_root)
    args.wiki_root = resolve_output_path(args.wiki_root)

    documents = run_ingest(args.source, output_root=args.output_root)
    metadata_overrides = None
    if args.metadata.exists():
        metadata_overrides = json.loads(args.metadata.read_text(encoding="utf-8"))

    result = compile_wiki(documents, metadata_overrides)
    written_pages = write_wiki_pages(result, args.wiki_root)

    print(f"Created {len(written_pages)} wiki page(s) in {args.wiki_root}")


if __name__ == "__main__":
    main()
