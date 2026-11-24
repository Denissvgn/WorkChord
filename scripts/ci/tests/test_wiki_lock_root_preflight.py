"""Wiki writer preflight refuses checkouts whose lock root leaves the repository."""
import contextlib
import io
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import wiki_lock_root_preflight as preflight


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid",
         "-c", "init.defaultBranch=main", "-C", str(cwd), *args],
        check=True,
        capture_output=True,
        text=True,
    )


def _repository(path: Path) -> Path:
    path.mkdir(parents=True)
    _git(path, "init", "-q")
    _git(path, "commit", "-q", "--allow-empty", "-m", "initial")
    _wiki(path)
    return path


def _wiki(checkout: Path) -> None:
    (checkout / "docs" / "llm_wiki").mkdir(parents=True, exist_ok=True)


def _run_main(argv):
    output = io.StringIO()
    with contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
        status = preflight.main(argv)
    return status, output.getvalue()


class WikiLockRootPreflight(unittest.TestCase):
    def setUp(self):
        self._directory = tempfile.TemporaryDirectory()
        self.base = Path(self._directory.name).resolve()

    def tearDown(self):
        self._directory.cleanup()

    def test_linked_worktree_nested_in_other_checkout_is_refused(self):
        source = _repository(self.base / "source")
        outer = _repository(self.base / "outer")
        linked = outer / "linked"
        _git(source, "worktree", "add", "-q", "--detach", str(linked))
        _wiki(linked)

        ok, report = preflight.check(linked)

        self.assertFalse(ok)
        self.assertIn(f"effective lock root (.git): {(outer / '.git').resolve()}", report)
        self.assertIn(f"own repository git directory: {(source / '.git').resolve()}", report)
        self.assertIn("REFUSE", report)
        status, _ = _run_main(["--checkout", str(linked)])
        self.assertEqual(status, 1)

    def test_symlinked_git_nested_in_other_checkout_is_refused(self):
        source = _repository(self.base / "source")
        outer = _repository(self.base / "outer")
        linked = outer / "symlinked"
        linked.mkdir()
        (linked / ".git").symlink_to(source / ".git", target_is_directory=True)
        _wiki(linked)

        ok, report = preflight.check(linked)

        self.assertFalse(ok)
        self.assertIn(f"effective lock root (.git): {(outer / '.git').resolve()}", report)
        self.assertIn("REFUSE", report)

    def test_standalone_clone_passes(self):
        source = _repository(self.base / "source")
        clone = self.base / "standalone"
        subprocess.run(["git", "clone", "-q", str(source), str(clone)], check=True, capture_output=True)
        _wiki(clone)

        ok, report = preflight.check(clone)

        self.assertTrue(ok, report)
        status, output = _run_main(["--checkout", str(clone)])
        self.assertEqual(status, 0)
        self.assertIn("OK:", output)

    def test_isolated_clone_nested_in_other_checkout_passes(self):
        source = _repository(self.base / "source")
        outer = _repository(self.base / "outer")
        clone = outer / "isolated"
        subprocess.run(["git", "clone", "-q", str(source), str(clone)], check=True, capture_output=True)
        _wiki(clone)

        ok, report = preflight.check(clone)

        self.assertTrue(ok, report)

    def test_normal_checkout_passes(self):
        repo = _repository(self.base / "workchord")

        ok, report = preflight.check(repo)

        self.assertTrue(ok, report)
        self.assertIn(f"effective lock root (.git): {(repo / '.git').resolve()}", report)

    def test_missing_wiki_directory_is_refused(self):
        plain = self.base / "plain"
        plain.mkdir()
        _git(plain, "init", "-q")

        ok, report = preflight.check(plain)

        self.assertFalse(ok)
        self.assertIn("wiki directory not found", report)

    def test_non_git_directory_is_refused(self):
        plain = self.base / "plain"
        (plain / "docs" / "llm_wiki").mkdir(parents=True)

        status, _ = _run_main(["--checkout", str(plain)])
        self.assertEqual(status, 1)


if __name__ == "__main__":
    unittest.main()
