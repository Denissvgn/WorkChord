# export_acceptance_artifacts Module

**Path:** `scripts/server/export_acceptance_artifacts.py`

## Description

Runs the bounded public receipt exporter for hosted retention. When receipt-validator dependencies are unavailable, it publishes only a sanitized failure summary and empty candidate/checksum index and exits unsuccessfully. Environment files, credentials, session state and runtime logs are never export inputs.

## Imports

| Source | Symbols |
|--------|---------|
| `app.autonomy.acceptance_artifacts` | `export_artifacts` |
| `argparse` | `argparse` |
| `hashlib` | `sha256` |
| `json` | `json` |
| `pathlib` | `Path` |
| `sys` | `sys` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/autonomy/acceptance_artifacts.py"]
    n1["scripts/server/export_acceptance_artifacts.py"]
    n1 --> n0
    click n0 "../modules/acceptance_artifacts.md"
    click n1 "../modules/export_acceptance_artifacts.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [acceptance_artifacts](../modules/acceptance_artifacts.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 1 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `main` | `()` | — | — |
