#!/usr/bin/env python3
"""Decide whether a CI run covers documentation-only changes.

Documentation-only changes run the documentation checks instead of the build
and test jobs. A change qualifies only when every changed path is under
``docs/`` or is a Markdown file at the repository root, and none of those paths
is an operator document that the backend tests read (the PostgreSQL
documentation set, except ``README.md``, which the documentation checks cover).
Anything else, and any doubt (unknown event, missing base commit, git failure,
empty change), runs the full pipeline.

Usage in GitHub Actions: write the printed ``docs_only=...`` line to
``$GITHUB_OUTPUT``. Inputs come from the environment: ``EVENT_NAME``,
``BASE_SHA`` and ``HEAD_SHA``.
"""

from __future__ import annotations

import os
from pathlib import PurePosixPath
import subprocess
import sys

from check_postgresql_documentation import DOCUMENTS

CHECKED_DOCUMENTS = frozenset(path.as_posix() for path in DOCUMENTS) - {"README.md"}
CLASSIFIED_EVENTS = frozenset({"pull_request", "push"})
ZERO_SHA = "0" * 40


def is_documentation(path: str) -> bool:
    """Return True when a changed path is documentation that no check reads."""
    if path in CHECKED_DOCUMENTS:
        return False
    parts = PurePosixPath(path).parts
    if len(parts) > 1 and parts[0] == "docs":
        return True
    return len(parts) == 1 and parts[0].lower().endswith(".md")


def docs_only(paths: list[str]) -> bool:
    """Return True only for a non-empty change made entirely of documentation."""
    return bool(paths) and all(is_documentation(path) for path in paths)


def changed_paths(base_sha: str, head_sha: str) -> list[str] | None:
    """Return the paths changed between the merge base and the head, or None."""
    if not base_sha or not head_sha or base_sha == ZERO_SHA:
        return None
    result = subprocess.run(
        ["git", "diff", "--name-only", "--no-renames", f"{base_sha}...{head_sha}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        print(result.stderr.strip(), file=sys.stderr)
        return None
    return [line for line in result.stdout.splitlines() if line.strip()]


def classify(event_name: str, base_sha: str, head_sha: str) -> bool:
    if event_name not in CLASSIFIED_EVENTS:
        return False
    paths = changed_paths(base_sha, head_sha)
    if paths is None:
        return False
    return docs_only(paths)


def main() -> int:
    result = classify(
        os.environ.get("EVENT_NAME", ""),
        os.environ.get("BASE_SHA", ""),
        os.environ.get("HEAD_SHA", ""),
    )
    print(f"docs_only={'true' if result else 'false'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
