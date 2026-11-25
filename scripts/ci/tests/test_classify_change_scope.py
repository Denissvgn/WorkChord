"""Documentation-only classification skips CI only for unchecked documentation."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import classify_change_scope as scope


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid",
         "-c", "init.defaultBranch=main", "-C", str(cwd), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


class PathRules(unittest.TestCase):
    def test_wiki_and_general_docs_are_documentation(self):
        self.assertTrue(scope.is_documentation("docs/llm_wiki/entities/Task.md"))
        self.assertTrue(scope.is_documentation("docs/llm_wiki/.llm-wiki-manifest.json"))
        self.assertTrue(scope.is_documentation("docs/local-development.md"))
        self.assertTrue(scope.is_documentation("SECURITY.md"))
        self.assertTrue(scope.is_documentation("README.md"))

    def test_operator_documents_read_by_tests_run_everything(self):
        self.assertFalse(scope.is_documentation("docs/database-runtime-policy.md"))
        self.assertFalse(scope.is_documentation("docs/runbooks/postgresql-operations.md"))

    def test_code_and_nested_markdown_are_not_documentation(self):
        self.assertFalse(scope.is_documentation("backend/app/main.py"))
        self.assertFalse(scope.is_documentation(".github/workflows/ci.yml"))
        self.assertFalse(scope.is_documentation("agent-skills/workchord-pm/SKILL.md"))
        self.assertFalse(scope.is_documentation("frontend/README.md"))
        self.assertFalse(scope.is_documentation("docs"))

    def test_mixed_or_empty_changes_run_everything(self):
        self.assertTrue(scope.docs_only(["docs/a.md", "SECURITY.md"]))
        self.assertFalse(scope.docs_only(["docs/a.md", "backend/app/main.py"]))
        self.assertFalse(scope.docs_only([]))


class GitClassification(unittest.TestCase):
    def setUp(self):
        self._dir = tempfile.TemporaryDirectory()
        self.repo = Path(self._dir.name)
        _git(self.repo, "init")
        (self.repo / "docs").mkdir()
        (self.repo / "docs" / "guide.md").write_text("one\n")
        (self.repo / "app.py").write_text("x = 1\n")
        _git(self.repo, "add", "-A")
        _git(self.repo, "commit", "-m", "base")
        self.base = _git(self.repo, "rev-parse", "HEAD")
        self._cwd = Path.cwd()

    def tearDown(self):
        self._dir.cleanup()

    def _commit(self, relative: str, text: str) -> str:
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
        _git(self.repo, "add", "-A")
        _git(self.repo, "commit", "-m", "change")
        return _git(self.repo, "rev-parse", "HEAD")

    def _classify(self, event: str, base: str, head: str) -> bool:
        import os
        os.chdir(self.repo)
        try:
            return scope.classify(event, base, head)
        finally:
            os.chdir(self._cwd)

    def test_docs_change_is_docs_only_for_pull_requests_and_pushes(self):
        head = self._commit("docs/guide.md", "two\n")
        self.assertTrue(self._classify("pull_request", self.base, head))
        self.assertTrue(self._classify("push", self.base, head))

    def test_code_change_runs_everything(self):
        head = self._commit("app.py", "x = 2\n")
        self.assertFalse(self._classify("pull_request", self.base, head))

    def test_unknown_event_or_base_runs_everything(self):
        head = self._commit("docs/guide.md", "two\n")
        self.assertFalse(self._classify("workflow_dispatch", self.base, head))
        self.assertFalse(self._classify("push", scope.ZERO_SHA, head))
        self.assertFalse(self._classify("push", "", head))
        self.assertFalse(self._classify("push", "f" * 40, head))


if __name__ == "__main__":
    unittest.main()
