# GitHubSubmissionReview

**Location:** `backend/app/schemas/github.py:86`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_github](../modules/schemas_github.md)

## Description

One review assignment bound to a submitted commit.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `assignment_id` | `int` | `assignment_id` | Yes | No | — | — | — | — |
| `actor_id` | `Optional[int]` | `actor_id` | No | Yes | `None` | — | — | — |
| `state` | `str` | `state` | Yes | No | — | — | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GitHubSubmissionReview (backend/app/schemas/github.py)"]
    n1["BaseModel"]
    n0 --> n1
    click n0 "../modules/schemas_github.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_github](../modules/schemas_github.md) | 0 | `actor_id`, `assignment_id`, `state` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |
