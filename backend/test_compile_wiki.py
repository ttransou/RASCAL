import unittest

from backend.compile_wiki import compile_wiki


class CompileWikiTests(unittest.TestCase):
    def test_compile_wiki_uses_metadata_overrides_for_markdown(self) -> None:
        documents = [
            {
                "path": "raw/sample.txt",
                "text": "This is the extracted document body.",
            }
        ]
        metadata_overrides = {
            "documents": {
                "sample": {
                    "summary": "A concise summary for the wiki page.",
                    "human_reviewed": True,
                    "key_points": ["First point", "Second point"],
                    "relationships": {
                        "requires": ["Procedure B"],
                        "depends_on": [
                            {
                                "target": "Policy Parent",
                                "weight": 0.9,
                                "confidence": 0.97,
                                "human_reviewed": True,
                                "provenance": "curator",
                            }
                        ],
                        "related_to": [],
                    },
                }
            }
        }

        result = compile_wiki(documents, metadata_overrides)

        self.assertEqual(len(result["pages"]), 1)
        page = result["pages"][0]
        self.assertEqual(page["title"], "sample")
        self.assertIn("# sample", page["markdown"])
        self.assertIn("A concise summary for the wiki page.", page["markdown"])
        self.assertIn("- First point", page["markdown"])
        self.assertIn("- Second point", page["markdown"])
        self.assertIn('"target": "Procedure B"', page["markdown"])
        self.assertIn('"confidence": 0.95', page["markdown"])
        self.assertIn('"target": "Policy Parent"', page["markdown"])
        self.assertIn('"provenance": "curator"', page["markdown"])


if __name__ == "__main__":
    unittest.main()
