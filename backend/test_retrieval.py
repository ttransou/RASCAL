import tempfile
import unittest
from pathlib import Path

from backend.retrieval import LocalWikiRetriever, retrieve, slugify
from backend.source_map import SourceUrlMap


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
        (self.wiki_dir / "reviewed-policy.md").write_text(
            "\n".join(
                [
                    "# Reviewed Policy",
                    "",
                    "Reviewed relationship summary.",
                    "",
                    "## Relationships",
                    '- **depends_on**: {"confidence": 0.92, "human_reviewed": true, "provenance": "curator", "target": "Policy A", "weight": 0.88}',
                    "",
                    "## Source Extract",
                    "",
                    "Reviewed dependency details.",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        (self.wiki_dir / "index.md").write_text("# Wiki Index\n", encoding="utf-8")
        source_map = SourceUrlMap()
        source_map.by_doc_id = {"policy-a": "https://example.org/policy-a"}
        self.retriever = LocalWikiRetriever(self.wiki_dir, repo_root=self.root, source_url_map=source_map)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_slugify_keeps_file_safe_ids(self) -> None:
        self.assertEqual(slugify("Analysis: Approval!"), "analysis-approval")

    def test_load_documents_reads_markdown_metadata(self) -> None:
        docs = self.retriever.load_documents()

        self.assertEqual(len(docs), 2)
        self.assertEqual(docs[0]["title"], "Policy A")
        self.assertEqual(docs[0]["key_points"], ["Approval requires evidence"])
        self.assertEqual([edge["target"] for edge in docs[0]["relationships"]["requires"]], ["Procedure B", "Source C"])
        self.assertEqual(docs[0]["relationships"]["requires"][0]["weight"], 0.5)
        self.assertFalse(docs[0]["relationships"]["requires"][0]["human_reviewed"])
        self.assertEqual(docs[0]["source_url"], "https://example.org/policy-a")

    def test_retrieve_ranks_matching_documents(self) -> None:
        results = self.retriever.retrieve("approval evidence")

        self.assertEqual(results[0]["doc_id"], "policy-a")
        self.assertGreater(results[0]["combined_score"], 0)
        self.assertIn("evidence", results[0]["excerpt"].lower())
        self.assertEqual(results[0]["source_url"], "https://example.org/policy-a")

    def test_graph_payload_uses_relationships(self) -> None:
        payload = self.retriever.graph_payload()

        policy_edge = next(edge for edge in payload["edges"] if edge["from"] == "policy-a")
        reviewed_edge = next(edge for edge in payload["edges"] if edge["from"] == "reviewed-policy")
        self.assertEqual((policy_edge["to"], policy_edge["type"]), ("procedure-b", "requires"))
        self.assertEqual(policy_edge["weight"], 0.5)
        self.assertEqual(policy_edge["confidence"], 0.5)
        self.assertEqual(policy_edge["review_state"], "provisional")
        self.assertEqual((reviewed_edge["to"], reviewed_edge["type"]), ("policy-a", "depends_on"))
        self.assertEqual(reviewed_edge["weight"], 0.88)
        self.assertEqual(reviewed_edge["confidence"], 0.92)
        self.assertTrue(reviewed_edge["human_reviewed"])
        self.assertEqual(reviewed_edge["provenance"], "curator")

    def test_compatibility_retrieve_function_accepts_wiki_dir(self) -> None:
        results = retrieve("approval", wiki_dir=self.wiki_dir)

        self.assertEqual(results[0]["id"], "policy-a")


if __name__ == "__main__":
    unittest.main()
