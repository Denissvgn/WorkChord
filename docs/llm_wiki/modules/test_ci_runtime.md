# test_ci_runtime Module

**Path:** `scripts/ci/tests/test_ci_runtime.py`

## Description

Exercise cancellation, deadlines and durable command results with real processes.

## Imports

| Source | Symbols |
|--------|---------|
| `ci_runtime` | `RunReceipt`, `stop_process_group` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `signal` | `signal` |
| `subprocess` | `subprocess` |
| `sys` | `sys` |
| `tempfile` | `tempfile` |
| `time` | `time` |
| `unittest` | `unittest` |
| `unittest.mock` | `patch`, `Mock` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [CommandLifecycle](../entities/CommandLifecycle.md) | 18 | `unittest.TestCase` | — |
