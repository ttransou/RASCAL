import json
import tempfile
import unittest
from pathlib import Path

from backend.source_map import SourceUrlMap


class SourceUrlMapTests(unittest.TestCase):
    def test_resolves_by_doc_id_source_file_and_title(self) -> None:
        with tempfile.TemporaryDirectory() as tempdir:
            path = Path(tempdir) / "source_url_map.json"
            path.write_text(
                json.dumps(
                    {
                        "by_doc_id": {"policy-a": "https://example.org/doc-id"},
                        "by_source_file": {"backend/wiki/policy-b.md": "https://example.org/source-file"},
                        "by_title": {"Policy C": "https://example.org/title"},
                    }
                ),
                encoding="utf-8",
            )

            source_map = SourceUrlMap(path)

            self.assertEqual(source_map.resolve(doc_id="policy-a"), "https://example.org/doc-id")
            self.assertEqual(
                source_map.resolve(source_file="backend/wiki/policy-b.md"),
                "https://example.org/source-file",
            )
            self.assertEqual(source_map.resolve(title="Policy C"), "https://example.org/title")


if __name__ == "__main__":
    unittest.main()
