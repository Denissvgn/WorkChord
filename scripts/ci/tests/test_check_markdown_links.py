"""The documentation job fails on relative links that point nowhere."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import check_markdown_links as links


class BrokenLinks(unittest.TestCase):
    def setUp(self):
        self._dir = tempfile.TemporaryDirectory()
        self.root = Path(self._dir.name)
        (self.root / "docs" / "runbooks").mkdir(parents=True)
        (self.root / "docs" / "runbooks" / "deploy.md").write_text("# Deploy\n")
        (self.root / "SECURITY.md").write_text("# Security\n")

    def tearDown(self):
        self._dir.cleanup()

    def _write(self, relative: str, text: str) -> str:
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        return relative

    def test_existing_relative_and_external_links_pass(self):
        doc = self._write("docs/guide.md", (
            "[deploy](runbooks/deploy.md) [anchor](runbooks/deploy.md#steps) "
            "[root](../SECURITY.md) [web](https://example.org/x) [top](#intro) "
            "[mail](mailto:a@example.invalid) ![img](/SECURITY.md)\n"))
        self.assertEqual(links.broken_links(self.root, [doc]), [])

    def test_missing_target_is_reported(self):
        doc = self._write("docs/guide.md", "[gone](runbooks/missing.md)\n")
        self.assertEqual(
            links.broken_links(self.root, [doc]),
            ["docs/guide.md: link target does not exist: runbooks/missing.md"],
        )

    def test_wiki_pages_deleted_files_and_non_markdown_are_skipped(self):
        wiki = self._write("docs/llm_wiki/entities/A.md", "[gone](missing.md)\n")
        self.assertEqual(
            links.broken_links(self.root, [wiki, "docs/deleted.md", "docs/data.json"]),
            [],
        )


if __name__ == "__main__":
    unittest.main()
