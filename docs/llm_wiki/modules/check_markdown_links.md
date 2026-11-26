# check_markdown_links Module

**Path:** `scripts/ci/check_markdown_links.py`

## Description

Fail when a changed Markdown document links to a repository file that does not exist.

Checks relative links only (external URLs, mail links and same-page anchors are
skipped) in the Markdown files changed between ``BASE_SHA`` and ``HEAD_SHA``.
Generated wiki pages under ``docs/llm_wiki/`` are left to the wiki tooling.
Paths can also be passed as arguments, which is how the tests call it.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `classify_change_scope` | `changed_paths` |
| `os` | `os` |
| `pathlib` | `Path` |
| `re` | `re` |
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
| `broken_links` | `(root: Path, relative_paths: list[str]) -> list[str]` | — | — |
| `main` | `(argv: list[str]) -> int` | — | — |
