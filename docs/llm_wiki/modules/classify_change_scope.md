# classify_change_scope Module

**Path:** `scripts/ci/classify_change_scope.py`

## Description

Decide whether a CI run covers documentation-only changes.

Documentation-only changes run the documentation checks instead of the build
and test jobs. A change qualifies only when every changed path is under
``docs/`` or is a Markdown file at the repository root, and none of those paths
is a document that a full-pipeline check or test reads: the PostgreSQL
documentation set (including ``README.md``) and the evidence documents listed in
``config/model-aware-routing-closeout.json``.
Anything else, and any doubt (unknown event, missing base commit, git failure,
empty change), runs the full pipeline.

Usage in GitHub Actions: write the printed ``docs_only=...`` line to
``$GITHUB_OUTPUT``. Inputs come from the environment: ``EVENT_NAME``,
``BASE_SHA`` and ``HEAD_SHA``.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `check_postgresql_documentation` | `DOCUMENTS` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path`, `PurePosixPath` |
| `subprocess` | `subprocess` |
| `sys` | `sys` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_inventory_documents` | `(inventory: Path) -> frozenset[str]` | — | Return every documentation path the routing closeout check requires. |
| `_is_documentation_path` | `(path: str) -> bool` | — | — |
| `is_documentation` | `(path: str) -> bool` | — | Return True when a changed path is documentation that no check reads. |
| `docs_only` | `(paths: list[str]) -> bool` | — | Return True only for a non-empty change made entirely of documentation. |
| `changed_paths` | `(base_sha: str, head_sha: str) -> list[str] \| None` | — | Return the paths changed between the merge base and the head, or None. |
| `classify` | `(event_name: str, base_sha: str, head_sha: str) -> bool` | — | — |
| `main` | `() -> int` | — | — |
