# resilience Module

**Path:** `scripts/load/resilience.py`

## Description

Derive fail-closed resilience metrics from sealed fault observations.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `argparse` | `argparse` |
| `datetime` | `datetime` |
| `jsonschema` | `Draft202012Validator`, `FormatChecker` |
| `pathlib` | `Path` |
| `scripts.load.common` | `QualificationInputError`, `RESILIENCE_SCHEMA_MEMBER`, `atomic_write_json`, `capacity_contract`, `contract_member_json`, `utc_now_text` |
| `scripts.load.result` | `percentile` |
| `sys` | `sys` |
| `typing` | `Any`, `Mapping` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["scripts/load/common.py"]
    n1["scripts/load/resilience.py"]
    n2["scripts/load/result.py"]
    n1 --> n0
    n1 --> n2
    n2 --> n0
    click n0 "../modules/load_common.md"
    click n1 "../modules/resilience.md"
    click n2 "../modules/result.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [load_common](../modules/load_common.md) |
| Outbound | [result](../modules/result.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_time` | `(value: str) -> datetime` | — | — |
| `_elapsed` | `(start: str, end: str, name: str) -> float` | — | — |
| `_gate` | `(actual: float, maximum: float) -> dict[str, Any]` | — | — |
| `evaluate` | `(document: Mapping[str, Any]) -> dict[str, Any]` | — | — |
| `_parser` | `() -> argparse.ArgumentParser` | — | — |
| `main` | `() -> int` | — | — |
