# test_android_cleanup Module

**Path:** `backend/tests/qualification/test_android_cleanup.py`

## Description

Emulator cleanup retains unrelated replacements and drains owned controllers.

## Imports

| Source | Symbols |
|--------|---------|
| `android_qualification` | `qualification` |
| `hashlib` | `hashlib` |
| `pathlib` | `Path` |
| `pytest` | `pytest` |
| `sys` | `sys` |
| `threading` | `threading` |
| `types` | `SimpleNamespace` |

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
| `owned_fixture` | `()` | — | — |
| `test_cleanup_aggregates_failures_and_preserves_replaced_resources` | `(monkeypatch)` | — | — |
| `test_cleanup_stops_controller_before_any_resource_observation` | `(monkeypatch)` | — | — |
| `test_unstopped_controller_holds_cleanup_before_resource_mutation` | `(monkeypatch)` | — | — |
| `test_cancelled_marker_wait_does_not_observe_or_restore_resources` | `()` | — | — |
| `test_instrumentation_failure_drains_started_controller` | `(tmp_path)` | — | — |
