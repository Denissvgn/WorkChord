# run_disposable_checks Module

**Path:** `scripts/ci/run_disposable_checks.py`

## Description

Runs validation in a UUID-scoped Docker network with unique build-image tags, disposable database state, and read-only source mounts. Receipts bind the revision, source digest, commands and artifacts. Source drift or failed cleanup prevents a successful receipt. The caller needs Docker and a standard-library Python interpreter; no running WorkChord stack is reused.

## Imports

| Source | Symbols |
|--------|---------|
| `argparse` | `argparse` |
| `datetime` | `datetime`, `timezone` |
| `hashlib` | `hashlib` |
| `json` | `json` |
| `pathlib` | `Path` |
| `subprocess` | `subprocess` |
| `tempfile` | `tempfile` |
| `time` | `time` |
| `uuid` | `uuid4` |
| `xml.etree.ElementTree` | `ET` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `source_digest` | `()` | — | — |
| `main` | `()` | — | — |