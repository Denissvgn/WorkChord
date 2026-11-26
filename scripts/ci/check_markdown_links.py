#!/usr/bin/env python3
"""Fail when a changed Markdown document links to a repository file that does not exist.

Checks relative links only (external URLs, mail links and same-page anchors are
skipped) in the Markdown files changed between ``BASE_SHA`` and ``HEAD_SHA``.
Generated wiki pages under ``docs/llm_wiki/`` are left to the wiki tooling.
Paths can also be passed as arguments, which is how the tests call it.
"""

from __future__ import annotations

import os
from pathlib import Path
import re
import sys

from classify_change_scope import changed_paths

LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIPPED_PREFIXES = ("http://", "https://", "mailto:", "#", "tel:")
WIKI_PREFIX = "docs/llm_wiki/"


def broken_links(root: Path, relative_paths: list[str]) -> list[str]:
    problems: list[str] = []
    for relative in relative_paths:
        if not relative.endswith(".md") or relative.startswith(WIKI_PREFIX):
            continue
        source = root / relative
        if not source.is_file():
            continue  # deleted in this change
        for target in LINK_PATTERN.findall(source.read_text(encoding="utf-8")):
            if target.startswith(SKIPPED_PREFIXES) or "://" in target:
                continue
            path_part = target.split("#", 1)[0]
            if not path_part:
                continue
            resolved = (root / path_part.lstrip("/")) if path_part.startswith("/") else (source.parent / path_part)
            if not resolved.exists():
                problems.append(f"{relative}: link target does not exist: {target}")
    return problems


def main(argv: list[str]) -> int:
    root = Path.cwd()
    if argv:
        paths = argv
    else:
        paths = changed_paths(os.environ.get("BASE_SHA", ""), os.environ.get("HEAD_SHA", ""))
        if paths is None:
            print("Could not determine the changed files", file=sys.stderr)
            return 1
    problems = broken_links(root, paths)
    for problem in problems:
        print(problem, file=sys.stderr)
    checked = [p for p in paths if p.endswith(".md") and not p.startswith(WIKI_PREFIX)]
    print(f"Checked links in {len(checked)} changed Markdown file(s); {len(problems)} broken")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
