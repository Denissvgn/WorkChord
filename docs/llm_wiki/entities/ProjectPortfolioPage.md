# ProjectPortfolioPage

**Location:** `backend/app/schemas/project.py:368`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_project](../modules/schemas_project.md)

## Description

_Auto-generated from `ProjectPortfolioPage` in `backend/app/schemas/project.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `items` | `list[ProjectPortfolioSummary]` | `items` | Yes | No | — | — | — | — |
| `has_more` | `bool` | `has_more` | Yes | No | — | — | — | — |
| `next_after_id` | `int \| None` | `next_after_id` | Yes | Yes | — | — | — | — |
| `upper_id` | `int` | `upper_id` | Yes | No | — | — | — | — |
| `consistency` | `str` | `consistency` | No | No | `'live_bounded_id_order'` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProjectPortfolioPage (backend/app/schemas/project.py)"]
    n1["BaseModel"]
    n2["get_portfolio_summary_page (backend/app/routers/projects.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_project.md"
    click n2 "../modules/projects.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_project](../modules/schemas_project.md) | 0 | `consistency`, `has_more`, `items`, `next_after_id`, `upper_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `get_portfolio_summary_page` | type_reference | [projects](../modules/projects.md) | — |
