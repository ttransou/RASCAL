"""Local wiki retrieval primitives for the default RASCAL runtime.

This module intentionally uses deterministic file-backed retrieval. It gives the
framework a transparent baseline while leaving room for vector, graph, or cloud
retrievers to replace the same boundary later.
"""
from __future__ import annotations

import re
from pathlib import Path
from typing import Any


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9._-]+", "-", value).strip("-").lower()
    return slug or "page"


def tokenize(value: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9]+", value.lower())


class LocalWikiRetriever:
    """Loads compiled wiki Markdown and ranks pages by lexical overlap."""

    def __init__(self, wiki_dir: Path, *, repo_root: Path | None = None) -> None:
        self.wiki_dir = wiki_dir
        self.repo_root = repo_root

    def load_documents(self) -> list[dict[str, Any]]:
        if not self.wiki_dir.exists():
            return []

        documents: list[dict[str, Any]] = []
        for path in sorted(self.wiki_dir.glob("*.md")):
            if path.name == "index.md":
                continue
            content = path.read_text(encoding="utf-8", errors="ignore")
            documents.append(self.document_from_markdown(path, content))
        return documents

    def get_page(self, page_id: str) -> dict[str, Any] | None:
        path = self.wiki_dir / f"{slugify(page_id)}.md"
        if not path.exists():
            return None
        content = path.read_text(encoding="utf-8", errors="ignore")
        document = self.document_from_markdown(path, content)
        return {
            "id": document["id"],
            "title": document["title"],
            "summary": document["summary"],
            "type": document["type"],
            "content": content,
            "markdown": content,
            "source_file": document["source_file"],
        }

    def retrieve(self, query: str, top_k: int = 5) -> list[dict[str, Any]]:
        query_terms = tokenize(query)
        if not query_terms:
            return []

        scored: list[dict[str, Any]] = []
        for doc in self.load_documents():
            haystack = " ".join(
                [
                    doc.get("title", ""),
                    doc.get("summary", ""),
                    " ".join(doc.get("key_points", [])),
                    doc.get("markdown", ""),
                ]
            ).lower()
            score = sum(haystack.count(term) for term in query_terms)
            if score <= 0:
                continue
            scored.append(
                {
                    "doc_id": doc["id"],
                    "id": doc["id"],
                    "title": doc["title"],
                    "type": doc["type"],
                    "combined_score": round(score / max(len(query_terms), 1), 4),
                    "excerpt": self.best_excerpt(doc.get("markdown", ""), query_terms),
                    "summary": doc["summary"],
                    "source_file": doc["source_file"],
                }
            )

        scored.sort(key=lambda item: (-item["combined_score"], item["title"].lower(), item["id"]))
        return scored[:top_k]

    def graph_payload(self) -> dict[str, list[dict[str, str]]]:
        docs = self.load_documents()
        nodes_by_id = {
            doc["id"]: {"id": doc["id"], "label": doc["title"], "group": doc["category"]}
            for doc in docs
        }
        edges: list[dict[str, str]] = []
        for doc in docs:
            for relation_type, targets in doc.get("relationships", {}).items():
                for target in targets:
                    target_id = slugify(str(target))
                    nodes_by_id.setdefault(
                        target_id,
                        {
                            "id": target_id,
                            "label": str(target).replace("-", " ").title(),
                            "group": "concept",
                        },
                    )
                    edges.append({"from": doc["id"], "to": target_id, "type": relation_type})

        return {"nodes": list(nodes_by_id.values()), "edges": edges}

    def rewrite_index(self) -> None:
        docs = self.load_documents()
        self.wiki_dir.mkdir(parents=True, exist_ok=True)
        lines = ["# Wiki Index", ""]
        for doc in docs:
            lines.append(f"- [{doc['title']}]({doc['id']}.md)")
        (self.wiki_dir / "index.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def document_from_markdown(self, path: Path, content: str) -> dict[str, Any]:
        title = self.extract_title(path, content)
        summary = self.extract_summary(content)
        doc_type = self.infer_type(title, content)
        return {
            "id": path.stem,
            "title": title,
            "type": doc_type,
            "category": self.category_for_type(doc_type),
            "summary": summary,
            "key_points": self.extract_list_section(content, "Key Points"),
            "relationships": self.extract_relationships(content),
            "source_file": self.source_file(path),
            "markdown": content,
        }

    def source_file(self, path: Path) -> str:
        if self.repo_root is not None and path.is_relative_to(self.repo_root):
            return str(path.relative_to(self.repo_root))
        return str(path)

    def extract_title(self, path: Path, content: str) -> str:
        for line in content.splitlines():
            if line.startswith("# "):
                return line[2:].strip() or path.stem
        return path.stem.replace("-", " ").title()

    def extract_summary(self, content: str) -> str:
        lines = content.splitlines()
        after_title = False
        collected: list[str] = []
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("# "):
                after_title = True
                continue
            if not after_title or not stripped:
                continue
            if stripped.startswith("## "):
                break
            collected.append(stripped)
        if collected:
            return " ".join(collected)
        plain = [line.strip() for line in lines if line.strip() and not line.strip().startswith("#")]
        return plain[0] if plain else ""

    def extract_relationships(self, content: str) -> dict[str, list[str]]:
        relationships: dict[str, list[str]] = {}
        for item in self.extract_list_section(content, "Relationships"):
            match = re.match(r"\*\*(?P<name>[^*]+)\*\*:\s*(?P<targets>.+)", item)
            if not match:
                continue
            relation_name = match.group("name").strip()
            targets = [target.strip() for target in match.group("targets").split(",") if target.strip()]
            if targets:
                relationships[relation_name] = targets
        return relationships

    def extract_list_section(self, content: str, heading: str) -> list[str]:
        in_section = False
        items: list[str] = []
        for line in content.splitlines():
            stripped = line.strip()
            if stripped == f"## {heading}":
                in_section = True
                continue
            if in_section and stripped.startswith("## "):
                break
            if in_section and stripped.startswith("- "):
                items.append(stripped[2:].strip())
        return items

    def infer_type(self, title: str, content: str) -> str:
        lowered = f"{title}\n{content}".lower()
        metadata_match = re.search(r"- \*\*type\*\*:\s*(?P<type>[\w-]+)", content, flags=re.IGNORECASE)
        if metadata_match:
            return metadata_match.group("type").strip().lower()
        if "policy" in lowered:
            return "policy"
        if "source" in lowered or "reference" in lowered:
            return "primary-source"
        if "procedure" in lowered or "workflow" in lowered:
            return "procedure"
        return "concept"

    def category_for_type(self, doc_type: str) -> str:
        lowered = doc_type.lower()
        if "policy" in lowered:
            return "policy"
        if "source" in lowered or "reference" in lowered:
            return "primary-source"
        return "concept"

    def best_excerpt(self, markdown: str, query_terms: list[str], max_length: int = 220) -> str:
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", markdown) if part.strip()]
        best = ""
        best_score = -1
        for paragraph in paragraphs:
            lowered = paragraph.lower()
            score = sum(lowered.count(term) for term in query_terms)
            if score > best_score:
                best = paragraph
                best_score = score
        return best[:max_length].strip()


def retrieve(query: str, top_k: int = 5, *, wiki_dir: Path | None = None) -> list[dict[str, Any]]:
    """Compatibility helper for callers that want a single retrieval function."""
    default_wiki_dir = Path(__file__).resolve().parent / "wiki"
    return LocalWikiRetriever(wiki_dir or default_wiki_dir).retrieve(query, top_k=top_k)
