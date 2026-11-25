# PersonCapacityDay

**Location:** `backend/app/schemas/team.py:579`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_team](../modules/schemas_team.md)

## Description

The person's totals over every row of the same profile on one date.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `date` | `date` | `date` | Yes | No | — | — | — | — |
| `available_hours` | `Optional[float]` | `available_hours` | No | Yes | `None` | — | — | — |
| `allocated_hours_before` | `Optional[float]` | `allocated_hours_before` | No | Yes | `None` | — | — | — |
| `allocated_hours_after` | `Optional[float]` | `allocated_hours_after` | No | Yes | `None` | — | — | — |
| `overallocated_hours_before` | `Optional[float]` | `overallocated_hours_before` | No | Yes | `None` | — | — | — |
| `overallocated_hours_after` | `Optional[float]` | `overallocated_hours_after` | No | Yes | `None` | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["PersonCapacityDay (backend/app/schemas/team.py)"]
    n1["BaseModel"]
    n0 --> n1
    click n0 "../modules/schemas_team.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_team](../modules/schemas_team.md) | 0 | `allocated_hours_after`, `allocated_hours_before`, `available_hours`, `date`, `overallocated_hours_after`, `overallocated_hours_before` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
