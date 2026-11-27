# ImportDependencyRows

**Location:** `backend/app/schemas/import_review.py:20`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [import_review](../modules/import_review.md)

## Description

_Auto-generated from `ImportDependencyRows` in `backend/app/schemas/import_review.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `created` | `list[dict[str, Any]]` | `created` | No | No | factory: `list` | — | — | — |
| `removed` | `list[dict[str, Any]]` | `removed` | No | No | factory: `list` | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ImportDependencyRows (backend/app/schemas/import_review.py)"]
    n1["BaseModel"]
    n0 --> n1
    click n0 "../modules/import_review.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [import_review](../modules/import_review.md) | 0 | `created`, `removed` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
