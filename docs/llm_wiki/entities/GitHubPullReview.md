# GitHubPullReview

**Location:** `backend/app/schemas/github.py:114`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_github](../modules/schemas_github.md)

## Description

The WorkChord review state of the task, decided only by the independent reviewer.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `accepted` | `bool` | `accepted` | Yes | No | — | — | — | — |
| `state` | `str` | `state` | Yes | No | — | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GitHubPullReview (backend/app/schemas/github.py)"]
    n1["BaseModel"]
    n0 --> n1
    click n0 "../modules/schemas_github.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_github](../modules/schemas_github.md) | 0 | `accepted`, `state` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
