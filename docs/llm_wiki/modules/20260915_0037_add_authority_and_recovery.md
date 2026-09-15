# 20260915_0037_add_authority_and_recovery Module

**Path:** `backend/app/migrations/versions/20260915_0037_add_authority_and_recovery.py`

## Description

Add durable authority, application snapshots and explicit schedule commitments.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `op` |
| `app.utils.time` | `UTCDateTime`, `utc_now` |
| `sqlalchemy` | `sa` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/migrations/versions/20260915_0037_add_authority_and_recovery.py"]
    n1["backend/app/utils/time.py"]
    n0 --> n1
    click n0 "../modules/20260915_0037_add_authority_and_recovery.md"
    click n1 "../modules/time.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [time](../modules/time.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `upgrade` | `()` | — | — |
| `downgrade` | `()` | — | — |
