# MaintenanceWindowNotice

**Location:** `backend/app/schemas/maintenance.py:22`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_maintenance](../modules/schemas_maintenance.md)

## Description

An operator's record that a PM was told through another channel.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `actor_id` | `int` | `actor_id` | Yes | No | — | ge=1 | — | — |
| `channel` | `str` | `channel` | Yes | No | — | max_length=60; min_length=1 | — | — |
| `reference` | `str` | `reference` | Yes | No | — | max_length=500; min_length=1 | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MaintenanceWindowNotice (backend/app/schemas/maintenance.py)"]
    n1["BaseModel"]
    n2["record_maintenance_notice (backend/app/routers/maintenance_windows.py)"]
    n3["MaintenanceWindowService.record_pm_notice (backend/app/services/maintenance_window_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    click n0 "../modules/schemas_maintenance.md"
    click n2 "../modules/maintenance_windows.md"
    click n3 "../modules/maintenance_window_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_maintenance](../modules/schemas_maintenance.md) | 0 | `actor_id`, `channel`, `reference` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `record_maintenance_notice` | type_reference | [maintenance_windows](../modules/maintenance_windows.md) | — |
| `MaintenanceWindowService.record_pm_notice` | type_reference | [maintenance_window_service](../modules/maintenance_window_service.md) | — |
