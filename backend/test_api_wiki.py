import json
import tempfile
import unittest
from io import BytesIO
from pathlib import Path

from backend.api import RASCALApp


class FakeRequest:
    def __init__(self, payload: dict, path: str = "/") -> None:
        body = json.dumps(payload).encode("utf-8")
        self.headers = {"Content-Length": str(len(body))}
        self.rfile = BytesIO(body)
        self.path = path


def decode_response(response: tuple[int, str, dict[str, str], bytes]) -> dict:
    return json.loads(response[3].decode("utf-8"))


class WikiBackedApiTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        self.wiki_dir = self.root / "wiki"
        self.feedback_log = self.root / "feedback.jsonl"
        self.source_map_path = self.root / "source_url_map.json"
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
        self.source_map_path.write_text(
            json.dumps({"by_doc_id": {"policy-a": "https://example.org/policy-a"}}),
            encoding="utf-8",
        )
        self.app = RASCALApp(
            wiki_dir=self.wiki_dir,
            feedback_log=self.feedback_log,
            source_map_path=self.source_map_path,
        )

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_wiki_index_reads_markdown_pages(self) -> None:
        payload = decode_response(self.app.dispatch("GET", "/wiki_index"))

        self.assertEqual(len(payload["documents"]), 1)
        self.assertEqual(payload["documents"][0]["id"], "policy-a")
        self.assertEqual(payload["documents"][0]["title"], "Policy A")
        self.assertIn("approval thresholds", payload["documents"][0]["summary"])
        self.assertEqual(payload["documents"][0]["source_url"], "https://example.org/policy-a")

    def test_wiki_detail_reads_markdown_content(self) -> None:
        payload = decode_response(self.app.dispatch("GET", "/wiki/policy-a"))

        self.assertEqual(payload["title"], "Policy A")
        self.assertIn("## Source Extract", payload["content"])
        self.assertEqual(payload["source_url"], "https://example.org/policy-a")

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
        self.assertEqual(payload["trace"]["citations"][0]["source_url"], "https://example.org/policy-a")

    def test_graph_map_data_uses_relationships(self) -> None:
        payload = decode_response(self.app.dispatch("GET", "/graph_map_data"))

        self.assertEqual(len(payload["edges"]), 1)
        self.assertEqual(payload["edges"][0]["from"], "policy-a")
        self.assertEqual(payload["edges"][0]["to"], "procedure-b")
        self.assertEqual(payload["edges"][0]["type"], "requires")
        self.assertEqual(payload["edges"][0]["weight"], 0.5)
        self.assertEqual(payload["edges"][0]["confidence"], 0.5)
        self.assertEqual(payload["edges"][0]["review_state"], "provisional")
        self.assertTrue(any(node["id"] == "procedure-b" for node in payload["nodes"]))

    def test_feedback_is_persisted_as_jsonl(self) -> None:
        response = self.app.dispatch(
            "POST",
            "/feedback",
            FakeRequest(
                {
                    "rating": "down",
                    "question": "Why?",
                    "answer": "Because.",
                    "comment": "Needs more detail.",
                    "trace": {"summary": "trace"},
                }
            ),
        )
        payload = decode_response(response)

        events = [json.loads(line) for line in self.feedback_log.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(events[0]["rating"], "down")
        self.assertEqual(events[0]["question"], "Why?")
        self.assertEqual(events[0]["status"], "new")
        self.assertEqual(payload["event"]["answer"], "Because.")

    def test_feedback_data_returns_events(self) -> None:
        self.app.dispatch("POST", "/feedback", FakeRequest({"rating": "up", "question": "Good?"}))
        self.app.dispatch("POST", "/feedback", FakeRequest({"rating": "down", "question": "Bad?"}))

        payload = decode_response(
            self.app.dispatch("GET", "/feedback-data?rating=down", FakeRequest({}, path="/feedback-data?rating=down"))
        )

        self.assertEqual(payload["count"], 1)
        self.assertEqual(payload["events"][0]["question"], "Bad?")

    def test_feedback_triage_updates_event(self) -> None:
        created = decode_response(
            self.app.dispatch("POST", "/feedback", FakeRequest({"rating": "down", "question": "Needs review?"}))
        )

        payload = decode_response(
            self.app.dispatch(
                "POST",
                "/feedback-triage",
                FakeRequest(
                    {
                        "id": created["event"]["id"],
                        "status": "reviewed",
                        "curator_note": "Looks like a coverage gap.",
                    }
                ),
            )
        )

        self.assertTrue(payload["ok"])
        self.assertEqual(payload["event"]["status"], "reviewed")
        self.assertEqual(payload["event"]["curator_note"], "Looks like a coverage gap.")

    def test_curator_routes_return_local_summaries(self) -> None:
        created = decode_response(
            self.app.dispatch("POST", "/feedback", FakeRequest({"rating": "down", "question": "Approval gap?"}))
        )
        self.app.dispatch(
            "POST",
            "/feedback-triage",
            FakeRequest({"id": created["event"]["id"], "status": "reviewed", "curator_note": "Check policy."}),
        )

        proposal = decode_response(
            self.app.dispatch("POST", "/feedback-propose-wiki", FakeRequest({"ids": [created["event"]["id"]]}))
        )
        audit = decode_response(self.app.dispatch("GET", "/triage_audit"))
        freshness = decode_response(self.app.dispatch("GET", "/wiki_freshness"))
        lint = decode_response(self.app.dispatch("GET", "/lint/document"))
        cascade = decode_response(self.app.dispatch("GET", "/cascade_status"))
        telemetry = decode_response(self.app.dispatch("GET", "/query_telemetry_summary"))
        graph = decode_response(self.app.dispatch("GET", "/graph_analytics_summary"))
        reviewed = decode_response(
            self.app.dispatch("POST", "/wiki_mark_reviewed", FakeRequest({"id": "policy-a", "note": "Reviewed"}))
        )

        self.assertTrue(proposal["ok"])
        self.assertIn("markdown", proposal["proposal"])
        self.assertEqual(audit["count"], 1)
        self.assertEqual(freshness["pages"][0]["id"], "policy-a")
        self.assertEqual(lint["error_count"], 0)
        self.assertFalse(cascade["available"])
        self.assertEqual(telemetry["query_count"], 1)
        self.assertEqual(graph["edge_count"], 1)
        self.assertTrue(reviewed["ok"])

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
