# SortCriterionSchema

**Location:** `backend/app/schemas/scheduling_rules.py:7`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_scheduling_rules](../modules/schemas_scheduling_rules.md)

## Description

A single sort criterion.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `field` | `str` | `field` | Yes | No | — | — | — | Field to sort by (e.g., 'priority', 'adjusted_effort') |
| `order` | `str` | `order` | No | No | `'asc'` | pattern='^(asc\|desc)$' | — | Sort order: 'asc' or 'desc' |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SortCriterionSchema (backend/app/schemas/scheduling_rules.py)"]
    n1["BaseModel"]
    n0 --> n1
    click n0 "../modules/schemas_scheduling_rules.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_scheduling_rules](../modules/schemas_scheduling_rules.md) | 0 | `field`, `order` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
