# compare Module

**Path:** `scripts/load/compare.py`

## Description

Create a sealed, machine-readable baseline versus tuned load comparison.

## Imports

| Source | Symbols |
|--------|---------|
| `__future__` | `annotations` |
| `argparse` | `argparse` |
| `pathlib` | `Path` |
| `scripts.load.common` | `QualificationInputError`, `atomic_write_json`, `read_json_object`, `utc_now_text` |
| `scripts.load.result` | `validate_result` |
| `sys` | `sys` |
| `typing` | `Any`, `Mapping` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["scripts/load/common.py"]
    n1["scripts/load/compare.py"]
    n2["scripts/load/result.py"]
    n1 --> n0
    n1 --> n2
    n2 --> n0
    click n0 "../modules/load_common.md"
    click n1 "../modules/compare.md"
    click n2 "../modules/result.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [load_common](../modules/load_common.md) |
| Outbound | [result](../modules/result.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_delta` | `(before: float, after: float) -> dict[str, float \| None]` | — | — |
| `_measurement_deltas` | `(before: Mapping[str, Any], after: Mapping[str, Any]) -> dict[str, Any]` | — | — |
| `_main` | `(args: argparse.Namespace) -> int` | — | — |
| `_parser` | `() -> argparse.ArgumentParser` | — | — |
| `main` | `() -> int` | — | — |
