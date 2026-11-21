# source_binding Module

**Path:** `scripts/load/source_binding.py`

## Description

Independently bind local measurements to the source that actually executes.

Measurement bindings hash executing backend service/migration and load-runner files plus lockfiles before and after execution, and record actual native Python/package identities. The digest scope is explicit and source drift fails the measurement. Full browser harness receipts additionally bind frontend and fixture orchestration source.

## Imports

| Source | Symbols |
|--------|---------|
| `hashlib` | `hashlib` |
| `importlib.metadata` | `version` |
| `json` | `json` |
| `pathlib` | `Path` |
| `platform` | `platform` |
| `sys` | `sys` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["scripts/load/local_baseline.py"]
    n1["scripts/load/service_worksets.py"]
    n2["scripts/load/source_binding.py"]
    n0 --> n2
    n1 --> n0
    n1 --> n2
    click n0 "../modules/local_baseline.md"
    click n1 "../modules/service_worksets.md"
    click n2 "../modules/source_binding.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [local_baseline](../modules/local_baseline.md) |
| Inbound | [service_worksets](../modules/service_worksets.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `source_binding` | `()` | — | — |
| `verify_binding` | `(before)` | — | — |
