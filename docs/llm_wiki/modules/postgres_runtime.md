# postgres_runtime Module

**Path:** `scripts/ci/postgres_runtime.py`

## Description

Starts only a new, job-owned PostgreSQL 18 data directory with builtin PG_UNICODE_FAST locale and password authentication. The server listens on loopback and an explicit unprivileged port. The password input file is private and removed after initialization. A marker prevents stopping an unrelated cluster; the caller retains ownership of installation and teardown.

## Imports

| Source | Symbols |
|--------|---------|
| `argparse` | `argparse` |
| `os` | `os` |
| `pathlib` | `Path` |
| `re` | `re` |
| `shlex` | `shlex` |
| `subprocess` | `subprocess` |
| `tempfile` | `tempfile` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `main` | `()` | — | — |
