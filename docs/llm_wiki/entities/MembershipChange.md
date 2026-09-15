# MembershipChange

**Location:** `backend/app/routers/identity.py:32`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [routers_identity](../modules/routers_identity.md)

## Description

_Auto-generated from `MembershipChange` in `backend/app/routers/identity.py`._

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `role` | `Literal['owner', 'operator', 'member', 'viewer', 'editor', 'executor', 'reviewer', 'manager'] \| None` | `role` | Yes | Yes | — | — | — | — |
| `reason` | `str` | `reason` | Yes | No | — | min_length=8; max_length=2000 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MembershipChange (backend/app/routers/identity.py)"]
    n1["BaseModel"]
    n2["project_member (backend/app/routers/identity.py)"]
    n3["workspace_member (backend/app/routers/identity.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/routers_identity.md"
    click n2 "../modules/routers_identity.md"
    click n3 "../modules/routers_identity.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [routers_identity](../modules/routers_identity.md) | 0 | `reason`, `role` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `project_member` | type_reference | [routers_identity](../modules/routers_identity.md) | — |
| `workspace_member` | type_reference | [routers_identity](../modules/routers_identity.md) | — |
