import tempfile
import unittest
from pathlib import Path

from backend.retrieval import LocalWikiRetriever, retrieve, slugify


class LocalWikiRetrieverTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.wiki_dir = self.root / "wiki"
        self.wiki_dir.mkdir()
        (self.wiki_dir / "policy-a.md").write_text(
            "\n".join(
                [
                    "# Policy A",
                    "",
                    "Approval policy summary.",
                    "",
                    "## Key Points",
                    "- Approval requires evidence",
                    "",
                    "## Relationships",
                    "- **requires**: Procedure B, Source C",
                    "",
                    "## Source Extract",
                    "",
                    "Evidence is required for approval.",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        (self.wiki_dir / "index.md").write_text("# Wiki Index\n", encoding="utf-8")
        self.retriever = LocalWikiRetriever(self.wiki_dir, repo_root=self.root)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_slugify_keeps_file_safe_ids(self) -> None:
        self.assertEqual(slugify("Analysis: Approval!"), "analysis-approval")

    def test_load_documents_reads_markdown_metadata(self) -> None:
        docs = self.retriever.load_documents()

        self.assertEqual(len(docs), 1)
        self.assertEqual(docs[0]["title"], "Policy A")
        self.assertEqual(docs[0]["key_points"], ["Approval requires evidence"])
        self.assertEqual(docs[0]["relationships"], {"requires": ["Procedure B", "Source C"]})

    def test_retrieve_ranks_matching_documents(self) -> None:
        results = self.retriever.retrieve("approval evidence")

        self.assertEqual(results[0]["doc_id"], "policy-a")
        self.assertGreater(results[0]["combined_score"], 0)
        self.assertIn("evidence", results[0]["excerpt"].lower())

    def test_graph_payload_uses_relationships(self) -> None:
        payload = self.retriever.graph_payload()

        self.assertEqual(
            payload["edges"],
            [
                {"from": "policy-a", "to": "procedure-b", "type": "requires"},
                {"from": "policy-a", "to": "source-c", "type": "requires"},
            ],
        )

    def test_compatibility_retrieve_function_accepts_wiki_dir(self) -> None:
        results = retrieve("approval", wiki_dir=self.wiki_dir)

        self.assertEqual(results[0]["id"], "policy-a")


if __name__ == "__main__":
    unittest.main()
