# import_review Module

**Path:** `backend/app/schemas/import_review.py`

## Description

Response of a plan-import dry run.

## Imports

| Source | Symbols |
|--------|---------|
| `pydantic` | `BaseModel`, `Field` |
| `typing` | `Any`, `Literal`, `Optional` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/routers/agent_planning.py"]
    n1["backend/app/schemas/import_review.py"]
    n0 --> n1
    click n0 "../modules/routers_agent_planning.md"
    click n1 "../modules/import_review.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [routers_agent_planning](../modules/routers_agent_planning.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [ImportChangeRows](../entities/ImportChangeRows.md) | 8 | `BaseModel` | Rows the import creates, changes and removes. |
| [ImportDependencyRows](../entities/ImportDependencyRows.md) | 20 | `BaseModel` | — |
| [ImportProfileRows](../entities/ImportProfileRows.md) | 25 | `BaseModel` | — |
| [ImportChanges](../entities/ImportChanges.md) | 29 | `BaseModel` | — |
| [ImportDryRunResponse](../entities/ImportDryRunResponse.md) | 39 | `BaseModel` | The exact change set of one import file; nothing was written. |
