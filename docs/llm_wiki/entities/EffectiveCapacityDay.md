# EffectiveCapacityDay

**Location:** `backend/app/schemas/team.py:465`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_team](../modules/schemas_team.md)

## Description

One date of this row and of every row sharing its person, before and after the change.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `date` | `date` | `date` | Yes | No | — | — | — | — |
| `availability_percent_before` | `float` | `availability_percent_before` | Yes | No | — | — | — | — |
| `availability_percent_after` | `float` | `availability_percent_after` | Yes | No | — | — | — | — |
| `row_hours_before` | `Optional[float]` | `row_hours_before` | No | Yes | `None` | — | — | — |
| `row_hours_after` | `Optional[float]` | `row_hours_after` | No | Yes | `None` | — | — | — |
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
    n0["EffectiveCapacityDay (backend/app/schemas/team.py)"]
    n1["BaseModel"]
    n0 --> n1
    click n0 "../modules/schemas_team.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_team](../modules/schemas_team.md) | 0 | `allocated_hours_after`, `allocated_hours_before`, `availability_percent_after`, `availability_percent_before`, `available_hours`, `date`, `overallocated_hours_after`, `overallocated_hours_before`, `row_hours_after`, `row_hours_before` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
