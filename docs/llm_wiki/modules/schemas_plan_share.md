# plan_share Module

**Path:** `backend/app/schemas/plan_share.py`

## Description

Schemas for immutable read-only plan shares.

## Imports

| Source | Symbols |
|--------|---------|
| `datetime` | `datetime` |
| `pydantic` | `BaseModel`, `ConfigDict`, `Field` |
| `typing` | `Any` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/routers/plan_shares.py"]
    n1["backend/app/schemas/plan_share.py"]
    n2["backend/app/services/plan_share_service.py"]
    n0 --> n1
    n0 --> n2
    n2 --> n1
    click n0 "../modules/plan_shares.md"
    click n1 "../modules/schemas_plan_share.md"
    click n2 "../modules/plan_share_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [plan_shares](../modules/plan_shares.md) |
| Inbound | [plan_share_service](../modules/plan_share_service.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [PlanShareResponse](../entities/PlanShareResponse.md) | 9 | `BaseModel` | A revocable plan snapshot link and its immutable captured data. |
