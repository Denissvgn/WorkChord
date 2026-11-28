"""Backend test selection falls back to the full suite on any doubt."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import select_backend_tests as selector


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-c", "user.name=test", "-c", "user.email=test@example.invalid",
         "-c", "init.defaultBranch=main", "-C", str(cwd), *args],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def _write(root: Path, files: dict[str, str]) -> None:
    for path, text in files.items():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")


BASE_FILES = {
    "backend/app/__init__.py": "",
    "backend/app/services/__init__.py": "",
    "backend/app/services/alpha.py": "def alpha():\n    return 1\n",
    "backend/app/services/beta.py": "from app.services.alpha import alpha\n\ndef beta():\n    return alpha()\n",
    "backend/app/services/gamma.py": "def gamma():\n    return 3\n",
    "backend/app/routers/__init__.py": "",
    "backend/app/routers/api.py": "from ..services import beta\n",
    "backend/tests/__init__.py": "",
    "backend/tests/conftest.py": "",
    "backend/tests/test_alpha.py": "from app.services.alpha import alpha\n",
    "backend/tests/test_api.py": "import app.routers.api\n",
    "backend/tests/test_gamma.py": "from app.services import gamma\n",
    "backend/tests/test_docs.py": "DOC = 'docs/guide.md'\n",
    "backend/tests/test_server_features.py": "",
    "docs/guide.md": "guide\n",
    "docs/other.md": "other\n",
    # a nested conftest that imports a module its tests never import
    "backend/app/services/dbhelper.py": "def helper():\n    return 1\n",
    "backend/tests/database/__init__.py": "",
    "backend/tests/database/conftest.py": "from app.services.dbhelper import helper\n",
    "backend/tests/database/test_db.py": "def test_db():\n    pass\n",
    # a script run by path, by bare name on sys.path and by python -m
    "backend/app/services/delta.py": "def delta():\n    return 4\n",
    "scripts/tools/run_thing.py": "from app.services.delta import delta\n",
    "scripts/tools/peer.py": "def main():\n    pass\n",
    "scripts/tools/bare_tool.py": "def run():\n    pass\n",
    "backend/tests/test_tool.py": (
        "import runpy\nfrom pathlib import Path\n"
        "ROOT = Path(__file__).resolve().parents[2]\n"
        "runpy.run_path(str(ROOT / 'scripts' / 'tools' / 'run_thing.py'))\n"
    ),
    "backend/tests/test_peer.py": "CMD = ['python', '-m', 'scripts.tools.peer']\n",
    "backend/tests/test_bare.py": "import sys\nsys.path.insert(0, 'scripts/tools')\nimport bare_tool\n",
    # a relative import two packages up
    "backend/app/routers/v2/__init__.py": "",
    "backend/app/routers/v2/items.py": "from ...services.alpha import alpha\n",
    "backend/tests/test_items.py": "from app.routers.v2 import items\n",
    # a test that imports another test module
    "backend/tests/test_reuses_gamma.py": "from tests.test_gamma import gamma\n",
}


class RepositoryCase(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        _git(self.root, "init", "-q")
        _write(self.root, BASE_FILES)
        _git(self.root, "add", ".")
        _git(self.root, "commit", "-q", "-m", "base")
        self.base = _git(self.root, "rev-parse", "HEAD")

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def change(self, files: dict[str, str]) -> str:
        _write(self.root, files)
        _git(self.root, "add", ".")
        _git(self.root, "commit", "-q", "-m", "change")
        return _git(self.root, "rev-parse", "HEAD")

    def select(self, head: str, **kwargs):
        return selector.select(self.root, self.base, head, **kwargs)


class FallbackRuleTests(RepositoryCase):
    def assert_full(self, files: dict[str, str], reason: str) -> None:
        result = self.select(self.change(files), engine="ast")
        self.assertEqual(result["mode"], "full", result)
        self.assertEqual(result["tests"], [])
        self.assertTrue(any(reason in item for item in result["reasons"]), result["reasons"])

    def test_conftest_anywhere_is_shared_ground(self) -> None:
        self.assert_full({"backend/tests/conftest.py": "X = 1\n"}, "shared ground")

    def test_nested_conftest_is_shared_ground(self) -> None:
        self.assert_full({"backend/tests/database/conftest.py": ""}, "shared ground")

    def test_migrations_models_and_configuration_are_shared_ground(self) -> None:
        for path in (
            "backend/app/migrations/versions/x.py",
            "backend/app/models/task.py",
            "backend/app/config.py",
            "backend/app/database_runtime.py",
            "backend/app/authority.py",
            "backend/app/http_authority.py",
            "backend/app/commands.py",
            "backend/uv.lock",
            "backend/requirements.lock",
            "backend/pyproject.toml",
            ".github/workflows/ci.yml",
            "scripts/ci/select_backend_tests.py",
        ):
            with self.subTest(path=path):
                self.assertTrue(selector.is_shared_ground(path))
        self.assert_full({"backend/app/models/task.py": "X = 1\n"}, "shared ground")

    def test_ordinary_paths_are_not_shared_ground(self) -> None:
        for path in ("backend/app/services/alpha.py", "frontend/src/a.ts", "docs/x.md"):
            with self.subTest(path=path):
                self.assertFalse(selector.is_shared_ground(path))

    def test_missing_base_selects_full(self) -> None:
        head = self.change({"docs/other.md": "changed\n"})
        result = selector.select(self.root, "", head, engine="ast")
        self.assertEqual(result["mode"], "full")

    def test_unknown_commit_selects_full(self) -> None:
        result = selector.select(self.root, "f" * 40, self.base, engine="ast")
        self.assertEqual(result["mode"], "full")
        self.assertIn("git diff failed", result["reasons"][-1])

    def test_test_data_change_selects_full(self) -> None:
        self.assert_full({"backend/tests/fixtures/data.json": "{}"}, "test data")

    def test_unparseable_module_selects_full(self) -> None:
        self.assert_full({"backend/app/services/alpha.py": "def (:\n"}, "cannot parse")

    def test_deleted_module_selects_full(self) -> None:
        (self.root / "backend/app/services/gamma.py").unlink()
        self.assert_full({}, "deleted or renamed")

    def test_renamed_module_selects_full(self) -> None:
        _git(self.root, "mv", "backend/app/services/gamma.py", "backend/app/services/gamma2.py")
        self.assert_full({}, "deleted or renamed")

    def test_test_support_helper_is_shared_ground(self) -> None:
        self.assert_full({"backend/tests/support/database.py": "X = 1\n"}, "shared ground")

    def test_agent_skill_sources_and_build_script_are_shared_ground(self) -> None:
        for path in ("agent-skills/pm/SKILL.md", "scripts/build_agent_skills.py"):
            with self.subTest(path=path):
                self.assertTrue(selector.is_shared_ground(path))

    def test_non_python_file_in_application_selects_full(self) -> None:
        self.assert_full({"backend/app/autonomy/contracts/v1/schema.json": "{}"}, "application data")

    def test_checkout_not_at_head_selects_full(self) -> None:
        head = self.change({"docs/other.md": "changed\n"})
        _git(self.root, "checkout", "-q", self.base)
        result = selector.select(self.root, self.base, head, engine="ast")
        self.assertEqual(result["mode"], "full", result)
        self.assertIn("not the head commit", result["reasons"][-1])

    def test_selection_covering_every_test_is_full(self) -> None:
        # pytest imports every test module through the package backend/tests
        self.assert_full({"backend/tests/__init__.py": "X = 1\n"}, "covers every backend test")

    def test_full_mode_lists_only_existing_smoke_tests(self) -> None:
        result = self.select(self.change({"backend/app/config.py": "X = 1\n"}), engine="ast")
        self.assertEqual(result["mode"], "full")
        self.assertEqual(result["smoke"], ["backend/tests/test_server_features.py"])


class StaticSelectionTests(RepositoryCase):
    def test_reverse_imports_are_followed_transitively(self) -> None:
        result = self.select(self.change({"backend/app/services/alpha.py": "def alpha():\n    return 2\n"}), engine="ast")
        self.assertEqual(result["mode"], "selected", result)
        self.assertIn("backend/tests/test_alpha.py", result["tests"])
        # alpha <- beta <- routers.api (relative import) <- test_api
        self.assertIn("backend/tests/test_api.py", result["tests"])
        self.assertNotIn("backend/tests/test_gamma.py", result["tests"])

    def test_from_package_import_module_resolves_to_the_module(self) -> None:
        result = self.select(self.change({"backend/app/services/gamma.py": "def gamma():\n    return 4\n"}), engine="ast")
        self.assertEqual(result["sources"]["ast"], ["backend/tests/test_gamma.py", "backend/tests/test_reuses_gamma.py"])

    def test_changed_test_is_selected_with_smoke(self) -> None:
        result = self.select(self.change({"backend/tests/test_docs.py": "X = 2\n"}), engine="ast")
        self.assertEqual(result["mode"], "selected")
        self.assertEqual(result["tests"], ["backend/tests/test_docs.py", "backend/tests/test_server_features.py"])
        self.assertEqual(result["smoke"], ["backend/tests/test_server_features.py"])

    def test_non_python_change_selects_tests_that_name_it(self) -> None:
        result = self.select(self.change({"docs/guide.md": "new\n"}), engine="ast")
        self.assertEqual(result["sources"]["references"], ["backend/tests/test_docs.py"])

    def test_unrelated_change_selects_only_smoke(self) -> None:
        result = self.select(self.change({"docs/other.md": "new\n"}), engine="ast")
        self.assertEqual(result["mode"], "selected")
        self.assertEqual(result["tests"], ["backend/tests/test_server_features.py"])

    def test_conftest_import_selects_the_tests_below_it(self) -> None:
        result = self.select(self.change({"backend/app/services/dbhelper.py": "def helper():\n    return 2\n"}), engine="ast")
        self.assertEqual(result["mode"], "selected", result)
        self.assertEqual(result["sources"]["ast"], ["backend/tests/database/test_db.py"])

    def test_script_run_by_path_traces_its_imports(self) -> None:
        result = self.select(self.change({"backend/app/services/delta.py": "def delta():\n    return 5\n"}), engine="ast")
        self.assertEqual(result["sources"]["ast"], ["backend/tests/test_tool.py"])

    def test_changed_script_selects_tests_that_name_it(self) -> None:
        cases = {
            "scripts/tools/run_thing.py": "backend/tests/test_tool.py",
            "scripts/tools/peer.py": "backend/tests/test_peer.py",
            "scripts/tools/bare_tool.py": "backend/tests/test_bare.py",
        }
        for path, test in cases.items():
            with self.subTest(path=path):
                _git(self.root, "checkout", "-q", "--detach", self.base)
                result = self.select(self.change({path: "X = 1\n"}), engine="ast")
                self.assertEqual(result["sources"]["ast"], [test])

    def test_relative_import_more_than_one_level_up(self) -> None:
        result = self.select(self.change({"backend/app/services/alpha.py": "def alpha():\n    return 9\n"}), engine="ast")
        self.assertIn("backend/tests/test_items.py", result["tests"])

    def test_imported_names_resolve_relative_levels(self) -> None:
        import ast
        tree = ast.parse("from ...services.alpha import alpha\nfrom .. import sibling\n")
        names = selector._imported_names(tree, "app.routers.v2.items", is_package=False)
        self.assertIn("app.services.alpha", names)
        self.assertIn("app.routers.sibling", names)
        names = selector._imported_names(ast.parse("from .. import x\n"), "app.routers.v2", is_package=True)
        self.assertIn("app.routers.x", names)

    def test_test_importing_a_changed_test_is_selected(self) -> None:
        result = self.select(self.change({"backend/tests/test_gamma.py": "from app.services import gamma\nX = 2\n"}), engine="ast")
        self.assertIn("backend/tests/test_reuses_gamma.py", result["tests"])

    def test_non_ascii_path_is_read(self) -> None:
        result = self.select(self.change({"docs/gu\u00efde \u00fc.md": "x\n"}), engine="ast")
        self.assertEqual(result["mode"], "selected", result)

    def test_always_run_set_covers_contracts_and_source_scanners(self) -> None:
        for path in (
            "backend/tests/test_client_contract.py",
            "backend/tests/test_mobile_contract.py",
            "backend/tests/database/test_deployment_topology.py",
            "backend/tests/test_refusal_next_steps.py",
        ):
            with self.subTest(path=path):
                self.assertIn(path, selector.SMOKE_TESTS)

    def test_cli_prints_json(self) -> None:
        head = self.change({"docs/other.md": "new\n"})
        script = Path(selector.__file__)
        output = subprocess.run(
            [sys.executable, str(script), "--root", str(self.root), "--base", self.base,
             "--head", head, "--engine", "ast"],
            check=True, capture_output=True, text=True,
        ).stdout
        self.assertEqual(json.loads(output)["mode"], "selected")


class FakeWiki:
    """Stands in for llm-wiki: impact and incoming imports from fixed data."""

    def __init__(self, impact: dict, imports: dict[str, dict]) -> None:
        self._impact = impact
        self._imports = imports

    def impact_each(self, paths):
        return [(path, self._impact) for path in paths]

    def incoming_imports(self, locator):
        return self._imports[locator]


def _impact(paths: list[str], **overrides) -> dict:
    payload = {
        "found": True,
        "ambiguous": False,
        "truncated": False,
        "bounds": {"concepts": {"total": len(paths), "returned": len(paths), "truncated": False}},
        "knowledge": {"availability": "ready"},
        "concepts": [
            {"concept_kind": "source-module", "source_path": path, "locator": f"llm-wiki://modules/{Path(path).stem}"}
            for path in paths
        ],
    }
    payload.update(overrides)
    return payload


def _imports(*sources: str, resolution: str = "resolved", **overrides) -> dict:
    payload = {
        "found": True,
        "ambiguous": False,
        "truncated": False,
        "bounds": {"edges": {"total": len(sources), "returned": len(sources), "truncated": False}},
        "edges": [
            {"resolution": resolution, "related_concept": {"source_path": source, "locator": f"llm-wiki://modules/{Path(source).stem}"}}
            for source in sources
        ],
    }
    payload.update(overrides)
    return payload


class WikiSelectionTests(RepositoryCase):
    CHANGED = "backend/app/services/gamma.py"

    def setUp(self) -> None:
        super().setUp()
        record = {"store": {"bundle": {"repository": {"evaluated_revision": f"git:{self.base}"}}}}
        _write(self.root, {"docs/llm_wiki/.llm-wiki-knowledge.json": json.dumps(record)})
        _git(self.root, "add", ".")
        _git(self.root, "commit", "-q", "-m", "wiki")
        self.base = _git(self.root, "rev-parse", "HEAD")
        self.head = self.change({self.CHANGED: "def gamma():\n    return 5\n"})

    def run_wiki(self, impact: dict, imports: dict[str, dict]):
        return self.select(self.head, engine="wiki", wiki_graph=FakeWiki(impact, imports))

    def test_clean_wiki_result_is_unioned_with_static_selection(self) -> None:
        result = self.run_wiki(
            _impact([self.CHANGED]),
            {
                "llm-wiki://modules/gamma": _imports("backend/app/routers/api.py"),
                "llm-wiki://modules/api": _imports("backend/tests/test_api.py"),
                "llm-wiki://modules/test_api": _imports(),
            },
        )
        self.assertEqual(result["mode"], "selected", result)
        self.assertEqual(result["sources"]["wiki"], ["backend/tests/test_api.py"])
        self.assertIn("backend/tests/test_api.py", result["tests"])
        self.assertIn("backend/tests/test_gamma.py", result["tests"])

    def assert_full(self, impact: dict, imports: dict[str, dict], reason: str) -> None:
        result = self.run_wiki(impact, imports)
        self.assertEqual(result["mode"], "full", result)
        self.assertTrue(any(reason in item for item in result["reasons"]), result["reasons"])

    def test_truncated_impact_selects_full(self) -> None:
        self.assert_full(_impact([self.CHANGED], truncated=True), {}, "truncated")

    def test_bounded_impact_selects_full(self) -> None:
        bounds = {"concepts": {"total": 9, "returned": 1, "truncated": True}}
        self.assert_full(_impact([self.CHANGED], bounds=bounds), {}, "bounded")

    def test_ambiguous_impact_selects_full(self) -> None:
        self.assert_full(_impact([self.CHANGED], ambiguous=True), {}, "ambiguous")

    def test_not_found_selects_full(self) -> None:
        self.assert_full(_impact([self.CHANGED], found=False), {}, "found: false")

    def test_missing_module_concept_selects_full(self) -> None:
        self.assert_full(_impact([]), {}, "no module concept")

    def test_unready_knowledge_selects_full(self) -> None:
        self.assert_full(_impact([self.CHANGED], knowledge={"availability": "unavailable"}), {}, "knowledge")

    def test_unresolved_import_edge_selects_full(self) -> None:
        imports = {"llm-wiki://modules/gamma": _imports("backend/app/x.py", resolution="unresolved")}
        self.assert_full(_impact([self.CHANGED]), imports, "unresolved")

    def test_truncated_traversal_selects_full(self) -> None:
        imports = {"llm-wiki://modules/gamma": _imports(truncated=True)}
        self.assert_full(_impact([self.CHANGED]), imports, "truncated")

    def test_query_error_selects_full(self) -> None:
        self.assert_full(_impact([self.CHANGED]), {}, "selector error")

    def test_stale_snapshot_selects_full(self) -> None:
        _write(self.root, {"docs/llm_wiki/.llm-wiki-knowledge.json": json.dumps({"evaluated_revision": "git:" + "a" * 40})})
        self.assert_full(_impact([self.CHANGED]), {}, "not an ancestor")

    def test_unavailable_llm_wiki_selects_full(self) -> None:
        original = sys.modules.get("llm_wiki_cli")
        sys.modules["llm_wiki_cli"] = None  # makes the import fail
        try:
            result = self.select(self.head, engine="wiki")
        finally:
            if original is None:
                sys.modules.pop("llm_wiki_cli", None)
            else:
                sys.modules["llm_wiki_cli"] = original
        self.assertEqual(result["mode"], "full")
        self.assertIn("llm-wiki unavailable", result["reasons"][-1])


if __name__ == "__main__":
    unittest.main()
