# __init__ Module

**Path:** `backend/app/autonomy/__init__.py`

## Description

Fail-closed primitives for WorkChord autonomous execution.

The package deliberately contains no production credential loader and no local
private-key signer.  Production callers must inject charter-selected remote
services through the protocol boundaries exposed by the submodules.

## Imports

| Source | Symbols |
|--------|---------|
| `app.autonomy.canonical` | `canonical_json_bytes`, `sha256_hex` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/autonomy/__init__.py"]
    n1["backend/app/autonomy/canonical.py"]
    n0 --> n1
    click n0 "../modules/autonomy___init__.md"
    click n1 "../modules/autonomy_canonical.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [autonomy_canonical](../modules/autonomy_canonical.md) |
