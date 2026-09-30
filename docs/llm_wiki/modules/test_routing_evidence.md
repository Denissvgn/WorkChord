# test_routing_evidence Module

**Path:** `backend/tests/qualification/test_routing_evidence.py`

## Description

Keep CI evidence inventories aligned with the checked-in implementation.

## Imports

| Source | Symbols |
|--------|---------|
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `scripts.ci` | `check_model_aware_routing_closeout` |
| `subprocess` | `subprocess` |
| `sys` | `sys` |

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
| `test_routing_inventory_passes_the_tracked_ci_contract` | `()` | `@pytest.mark.contract` | — |
| `test_missing_evidence_is_rejected` | `(tmp_path, monkeypatch)` | `@pytest.mark.contract` | — |
| `test_untracked_evidence_is_rejected` | `(tmp_path, monkeypatch)` | `@pytest.mark.contract` | — |
