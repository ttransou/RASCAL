import unittest

from backend.relationships import normalize_relationship, normalize_relationships


class RelationshipSemanticsTests(unittest.TestCase):
    def test_string_relationship_defaults_to_provisional_strength(self) -> None:
        edge = normalize_relationship("requires", "Procedure B")

        self.assertEqual(edge["target"], "Procedure B")
        self.assertEqual(edge["weight"], 0.5)
        self.assertEqual(edge["confidence"], 0.5)
        self.assertFalse(edge["human_reviewed"])
        self.assertEqual(edge["review_state"], "provisional")

    def test_reviewed_relationship_uses_type_defaults(self) -> None:
        edge = normalize_relationship("requires", "Procedure B", document_human_reviewed=True)

        self.assertEqual(edge["weight"], 1.0)
        self.assertEqual(edge["confidence"], 0.95)
        self.assertTrue(edge["human_reviewed"])
        self.assertEqual(edge["review_state"], "reviewed")

    def test_explicit_strength_is_honored_only_after_review(self) -> None:
        provisional = normalize_relationship(
            "depends_on",
            {"target": "Policy B", "weight": 0.95, "confidence": 1.0},
        )
        reviewed = normalize_relationship(
            "depends_on",
            {"target": "Policy B", "weight": 0.95, "confidence": 1.0, "human_reviewed": True},
        )

        self.assertEqual(provisional["weight"], 0.5)
        self.assertEqual(provisional["confidence"], 0.5)
        self.assertEqual(reviewed["weight"], 0.95)
        self.assertEqual(reviewed["confidence"], 1.0)

    def test_normalize_relationships_accepts_scalar_values(self) -> None:
        relationships = normalize_relationships({"related_to": "Concept A"}, document_human_reviewed=True)

        self.assertEqual(relationships["related_to"][0]["target"], "Concept A")
        self.assertEqual(relationships["related_to"][0]["confidence"], 0.65)


if __name__ == "__main__":
    unittest.main()
