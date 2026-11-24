"""Wiki writer preflight refuses a linked worktree nested in another checkout."""
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
    return path


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

        ok, report = preflight.check(linked)

        self.assertFalse(ok)
        self.assertIn(f"effective lock root (.git): {(outer / '.git').resolve()}", report)
        self.assertIn(f"own repository git directory: {(source / '.git').resolve()}", report)
        self.assertIn("REFUSE", report)
        self.assertEqual(preflight.main(["--checkout", str(linked)]), 1)

    def test_standalone_clone_passes(self):
        source = _repository(self.base / "source")
        clone = self.base / "standalone"
        subprocess.run(["git", "clone", "-q", str(source), str(clone)], check=True, capture_output=True)

        ok, report = preflight.check(clone)

        self.assertTrue(ok, report)
        self.assertEqual(preflight.main(["--checkout", str(clone)]), 0)

    def test_isolated_clone_nested_in_other_checkout_passes(self):
        source = _repository(self.base / "source")
        outer = _repository(self.base / "outer")
        clone = outer / "isolated"
        subprocess.run(["git", "clone", "-q", str(source), str(clone)], check=True, capture_output=True)

        ok, report = preflight.check(clone)

        self.assertTrue(ok, report)

    def test_normal_checkout_passes(self):
        repo = _repository(self.base / "workchord")

        ok, report = preflight.check(repo)

        self.assertTrue(ok, report)
        self.assertIn(f"effective lock root (.git): {(repo / '.git').resolve()}", report)

    def test_non_git_directory_is_refused(self):
        plain = self.base / "plain"
        plain.mkdir()

        self.assertEqual(preflight.main(["--checkout", str(plain)]), 1)


if __name__ == "__main__":
    unittest.main()
