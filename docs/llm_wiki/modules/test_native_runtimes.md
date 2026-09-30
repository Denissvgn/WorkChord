# test_native_runtimes Module

**Path:** `scripts/ci/tests/test_native_runtimes.py`

## Description

Native orchestration preserves isolation, real result requirements and cleanup.

## Imports

| Source | Symbols |
|--------|---------|
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `postgres_runtime` | `postgres_runtime` |
| `run_android_checks` | `android` |
| `run_disposable_checks` | `checks` |
| `shutil` | `shutil` |
| `socket` | `socket` |
| `subprocess` | `subprocess` |
| `sys` | `sys` |
| `tempfile` | `tempfile` |
| `types` | `SimpleNamespace` |
| `unittest` | `unittest` |
| `unittest.mock` | `Mock`, `patch` |
| `xml.etree.ElementTree` | `ET` |
| `yaml` | `yaml` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 4 | 4 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [WorkflowContracts](../entities/WorkflowContracts.md) | 26 | `unittest.TestCase` | — |
| [NativeChecks](../entities/NativeChecks.md) | 112 | `unittest.TestCase` | — |
| [PostgresOwnership](../entities/PostgresOwnership.md) | 227 | `unittest.TestCase` | — |
| [AndroidArtifacts](../entities/AndroidArtifacts.md) | 257 | `unittest.TestCase` | — |
