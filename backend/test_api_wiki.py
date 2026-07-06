import json
import tempfile
import unittest
from io import BytesIO
from pathlib import Path

from backend.api import RASCALApp


class FakeRequest:
    def __init__(self, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.headers = {"Content-Length": str(len(body))}
        self.rfile = BytesIO(body)


def decode_response(response: tuple[int, str, dict[str, str], bytes]) -> dict:
    return json.loads(response[3].decode("utf-8"))


class WikiBackedApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.wiki_dir = self.root / "wiki"
        self.feedback_log = self.root / "feedback.jsonl"
        self.wiki_dir.mkdir()
        (self.wiki_dir / "policy-a.md").write_text(
            "\n".join(
                [
                    "# Policy A",
                    "",
                    "A concise summary about approval thresholds.",
                    "",
                    "## Key Points",
                    "- Approval requires documented evidence",
                    "",
                    "## Relationships",
                    "- **requires**: Procedure B",
                    "",
                    "## Source Extract",
                    "",
                    "Approval thresholds require documented evidence and review.",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
        self.app = RASCALApp(wiki_dir=self.wiki_dir, feedback_log=self.feedback_log)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_wiki_index_reads_markdown_pages(self) -> None:
        payload = decode_response(self.app.dispatch("GET", "/wiki_index"))

        self.assertEqual(len(payload["documents"]), 1)
        self.assertEqual(payload["documents"][0]["id"], "policy-a")
        self.assertEqual(payload["documents"][0]["title"], "Policy A")
        self.assertIn("approval thresholds", payload["documents"][0]["summary"])

    def test_wiki_detail_reads_markdown_content(self) -> None:
        payload = decode_response(self.app.dispatch("GET", "/wiki/policy-a"))

        self.assertEqual(payload["title"], "Policy A")
        self.assertIn("## Source Extract", payload["content"])

    def test_ask_retrieves_local_wiki_evidence(self) -> None:
        response = self.app.dispatch(
            "POST",
            "/ask",
            FakeRequest({"question": "What approval evidence is required?"}),
        )
        payload = decode_response(response)

        self.assertIn("local wiki page", payload["answer"])
        self.assertEqual(payload["trace"]["retrieved_docs"][0]["doc_id"], "policy-a")
        self.assertEqual(payload["trace"]["citations"][0]["doc_id"], "policy-a")

    def test_graph_map_data_uses_relationships(self) -> None:
        payload = decode_response(self.app.dispatch("GET", "/graph_map_data"))

        self.assertEqual(payload["edges"], [{"from": "policy-a", "to": "procedure-b", "type": "requires"}])
        self.assertTrue(any(node["id"] == "procedure-b" for node in payload["nodes"]))

    def test_feedback_is_persisted_as_jsonl(self) -> None:
        self.app.dispatch("POST", "/feedback", FakeRequest({"rating": "down", "question": "Why?"}))

        events = [json.loads(line) for line in self.feedback_log.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(events[0]["rating"], "down")
        self.assertEqual(events[0]["question"], "Why?")

    def test_wiki_writeback_creates_page_and_updates_index(self) -> None:
        payload = decode_response(
            self.app.dispatch(
                "POST",
                "/wiki",
                FakeRequest({"title": "Analysis: Approval", "content": "Reusable approval answer."}),
            )
        )

        page_path = self.wiki_dir / f"{payload['page']['id']}.md"
        self.assertTrue(page_path.exists())
        self.assertIn("Reusable approval answer.", page_path.read_text(encoding="utf-8"))
        self.assertIn("Analysis: Approval", (self.wiki_dir / "index.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
