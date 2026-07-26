"""Machine-check the pre-cutover PostgreSQL operator documentation."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys
import tomllib


REPOSITORY_ROOT = Path(__file__).resolve().parents[3]


def test_postgresql_documentation_contract() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(REPOSITORY_ROOT / "scripts/ci/check_postgresql_documentation.py"),
        ],
        cwd=REPOSITORY_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "documentation contract passed" in result.stdout


def test_application_and_closeout_entrypoint_versions_are_consistent() -> None:
    project = tomllib.loads(
        (REPOSITORY_ROOT / "backend/pyproject.toml").read_text(encoding="utf-8")
    )
    source = (REPOSITORY_ROOT / "backend/app/main.py").read_text(encoding="utf-8")
    version = project["project"]["version"]
    assert f'version="{version}"' in source
    assert project["project"]["scripts"]["workchord-db-closeout"] == (
        "app.cli.closeout:main"
    )
