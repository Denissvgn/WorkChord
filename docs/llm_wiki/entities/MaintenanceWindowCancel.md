# MaintenanceWindowCancel

**Location:** `backend/app/schemas/maintenance.py:41`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_maintenance](../modules/schemas_maintenance.md)

## Description

Withdraw an announced window before it begins.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `note` | `Optional[str]` | `note` | No | Yes | `None` | max_length=4000 | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MaintenanceWindowCancel (backend/app/schemas/maintenance.py)"]
    n1["BaseModel"]
    n2["cancel_maintenance_window (backend/app/routers/maintenance_windows.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_maintenance.md"
    click n2 "../modules/maintenance_windows.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_maintenance](../modules/schemas_maintenance.md) | 0 | `note` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `cancel_maintenance_window` | type_reference | [maintenance_windows](../modules/maintenance_windows.md) | — |
