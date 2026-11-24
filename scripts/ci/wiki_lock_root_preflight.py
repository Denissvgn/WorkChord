#!/usr/bin/env python3
"""Refuse wiki writer runs whose storage and governance locks would leave this repository.

The installed llm-wiki resolver places its lock root at the nearest real
directory named ``.git`` found by searching upward from the wiki directory
(``docs/llm_wiki``). A linked worktree has a ``.git`` file, and a symlinked
``.git`` is not a real directory, so the resolver skips both and can select an
enclosing repository. This preflight reads Git metadata only. It never opens a
lock and never runs the writer.

Exit status: 0 when the selected lock root is the checkout's own repository,
1 when it is not or cannot be determined.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

WIKI_DIRECTORY = Path("docs/llm_wiki")


def _git_path(checkout: Path, *args: str) -> Path:
    result = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "--path-format=absolute", *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"not a usable Git checkout: {checkout} ({result.stderr.strip()})")
    return Path(result.stdout.strip()).resolve()


def own_repository_git_dir(checkout: Path) -> Path:
    """Return the shared Git directory the checkout belongs to.

    For a standalone clone or a normal checkout this is ``<checkout>/.git``. For a
    linked worktree it is the admin repository's directory (``--git-common-dir``).
    """
    return _git_path(checkout, "--git-common-dir")


def _is_real_git_directory(candidate: Path) -> bool:
    # Mirror the upstream resolver: a .git file (linked worktree marker) or a
    # symlink is skipped, only a real directory counts.
    return candidate.is_dir() and not candidate.is_symlink()


def selected_lock_git_dir(wiki_directory: Path) -> Path | None:
    """Return the nearest real ``.git`` directory searching upward from the wiki directory."""
    start = wiki_directory.resolve()
    for directory in (start, *start.parents):
        candidate = directory / ".git"
        if _is_real_git_directory(candidate):
            return candidate.resolve()
    return None


def check(checkout: Path) -> tuple[bool, str]:
    own = own_repository_git_dir(checkout)
    wiki_directory = checkout / WIKI_DIRECTORY
    lines = [
        f"checkout: {checkout.resolve()}",
        f"own repository git directory: {own}",
    ]
    if not wiki_directory.is_dir():
        lines.append(f"REFUSE: wiki directory not found at {wiki_directory}; the writer cannot be checked.")
        return False, "\n".join(lines)
    selected = selected_lock_git_dir(wiki_directory)
    lines.append(f"effective lock root (.git): {selected if selected is not None else '<none found>'}")
    if selected is None:
        lines.append(
            "REFUSE: no .git directory found above the wiki directory; "
            "the writer would use the wiki directory as its lock root."
        )
        return False, "\n".join(lines)
    if selected != own:
        lines.append(
            "REFUSE: the effective lock root is outside this repository. "
            "Run the writer from a standalone clone with its own .git directory "
            "(see docs/local-development.md, 'Maintain the LLM wiki')."
        )
        return False, "\n".join(lines)
    lines.append("OK: the effective lock root belongs to this repository.")
    return True, "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--checkout",
        type=Path,
        default=Path.cwd(),
        help="checkout or linked worktree to check (default: current directory)",
    )
    args = parser.parse_args(argv)
    try:
        ok, report = check(args.checkout)
    except RuntimeError as error:
        print(f"REFUSE: {error}", file=sys.stderr)
        return 1
    print(report)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
