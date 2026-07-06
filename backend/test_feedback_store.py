import tempfile
import unittest
from pathlib import Path

from backend.feedback_store import FeedbackStore


class FeedbackStoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.path = Path(self.tempdir.name) / "feedback.jsonl"
        self.store = FeedbackStore(self.path)

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_create_normalizes_feedback_event(self) -> None:
        event = self.store.create(
            {
                "rating": "down",
                "question": "What changed?",
                "answer": "A local answer.",
                "comment": "Missing source.",
                "cited_docs": [{"doc_id": "policy-a"}],
                "trace": {"summary": "local trace"},
            }
        )

        self.assertEqual(event["status"], "new")
        self.assertEqual(event["rating"], "down")
        self.assertEqual(event["question"], "What changed?")
        self.assertEqual(len(self.store.list()), 1)

    def test_list_filters_by_status_and_rating(self) -> None:
        self.store.create({"rating": "up", "question": "Good?"})
        event = self.store.create({"rating": "down", "question": "Bad?"})
        self.store.triage(event["id"], status="reviewed", curator_note="Known gap")

        reviewed = self.store.list(status="reviewed")
        down = self.store.list(rating="down")

        self.assertEqual([event["id"] for event in reviewed], [event["id"]])
        self.assertEqual([event["id"] for event in down], [event["id"]])

    def test_triage_updates_event(self) -> None:
        event = self.store.create({"rating": "down", "question": "Needs curation?"})

        updated = self.store.triage(
            event["id"],
            status="proposed_wiki",
            curator_note="Draft useful answer.",
            linked_wiki_page="analysis-page",
        )

        self.assertIsNotNone(updated)
        self.assertEqual(updated["status"], "proposed_wiki")
        self.assertEqual(updated["curator_note"], "Draft useful answer.")
        self.assertEqual(updated["linked_wiki_page"], "analysis-page")

    def test_triage_rejects_unknown_status(self) -> None:
        event = self.store.create({"rating": "down"})

        with self.assertRaises(ValueError):
            self.store.triage(event["id"], status="not-real")


if __name__ == "__main__":
    unittest.main()
