# NativeChecks

**Location:** `scripts/ci/tests/test_native_runtimes.py:113`
**Kind:** Class
**Bases:** `unittest.TestCase`
**Module:** [test_native_runtimes](../modules/test_native_runtimes.md)

## Description

_Auto-generated from `NativeChecks` in `scripts/ci/tests/test_native_runtimes.py`._

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `test_connection_parameters_cannot_override_the_loopback_host` | `()` | — | — |
| `test_port_preflight_rejects_listeners_but_accepts_closed_connections` | `()` | — | — |
| `test_incomplete_browser_evidence_cannot_pass` | `()` | — | — |
| `test_application_secrets_are_not_inherited` | `()` | — | — |
| `test_browser_worker_uses_harness_interpreter_outside_path` | `()` | — | — |
| `run_backend` | `(*, write_results, remote = False, scope = None)` | — | — |
| `test_empty_results_cannot_be_reported_as_success` | `()` | — | — |
| `test_both_database_results_are_required_and_recorded` | `()` | — | — |
| `test_remote_database_is_rejected_before_any_command` | `()` | — | — |
| `test_sqlite_scope_needs_no_postgresql_server` | `()` | — | — |
| `test_frontend_scope_does_not_run_backend_checks` | `()` | — | — |
| `test_browser_scope_does_not_repeat_unit_suites` | `()` | — | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["NativeChecks (scripts/ci/tests/test_native_runtimes.py)"]
    n1["unittest.TestCase"]
    n0 --> n1
    click n0 "../modules/test_native_runtimes.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [test_native_runtimes](../modules/test_native_runtimes.md) | 12 | — |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `unittest.TestCase` | — |
