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
                    "key_points": ["First point", "Second point"],
                    "relationships": {
                        "requires": [],
                        "depends_on": [],
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


if __name__ == "__main__":
    unittest.main()
