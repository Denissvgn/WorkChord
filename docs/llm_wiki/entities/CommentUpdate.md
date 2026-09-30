# CommentUpdate

**Location:** `backend/app/routers/discussion.py:22`
**Kind:** Pydantic model
**Bases:** `CommentCreate`
**Module:** [routers_discussion](../modules/routers_discussion.md)

## Description

_Auto-generated from `CommentUpdate` in `backend/app/routers/discussion.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `expected_version` | `int` | `expected_version` | Yes | No | — | gt=0 | — | — |
| `deleted` | `bool` | `deleted` | No | No | `False` | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["CommentUpdate (backend/app/routers/discussion.py)"]
    n1["CommentCreate (backend/app/routers/discussion.py)"]
    n2["update_task_comment (backend/app/routers/discussion.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/routers_discussion.md"
    click n1 "../modules/routers_discussion.md"
    click n2 "../modules/routers_discussion.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [routers_discussion](../modules/routers_discussion.md) | 0 | `deleted`, `expected_version` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `CommentCreate` | [routers_discussion](../modules/routers_discussion.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `update_task_comment` | type_reference | [routers_discussion](../modules/routers_discussion.md) | — |
