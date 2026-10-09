# test_rehearsal_ownership Module

**Path:** `backend/tests/test_rehearsal_ownership.py`

## Description

Isolation cannot adopt operator paths, names, architectures or unrelated resources.

## Imports

| Source | Symbols |
|--------|---------|
| `json` | `json` |
| `pytest` | `pytest` |
| `scripts.server` | `isolated_rehearsal` |
| `subprocess` | `subprocess` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 2 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `test_prepare_refuses_existing_and_operator_paths` | `(tmp_path, monkeypatch)` | — | — |
| `test_platform_and_fixed_external_names_fail_before_launch` | `(tmp_path, monkeypatch)` | — | — |
| `test_cleanup_removes_only_matching_identities_and_keeps_failure_evidence` | `(tmp_path, monkeypatch)` | — | — |
