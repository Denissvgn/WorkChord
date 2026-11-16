# 20261116_0017_run_harness_session Module

**Path:** `backend/app/migrations/versions/20261116_0017_run_harness_session.py`

## Description

Keep a run's declared harness session in columns a reader can search.

## Imports

| Source | Symbols |
|--------|---------|
| `alembic` | `op` |
| `app.schemas.agent` | `check_harness_identity` |
| `json` | `json` |
| `sqlalchemy` | `sa` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/migrations/versions/20261116_0017_run_harness_session.py"]
    n1["backend/app/schemas/agent.py"]
    n0 --> n1
    click n0 "../modules/20261116_0017_run_harness_session.md"
    click n1 "../modules/schemas_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [schemas_agent](../modules/schemas_agent.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `_declared` | `(metadata)` | — | — |
| `upgrade` | `()` | — | — |
| `downgrade` | `()` | — | — |
