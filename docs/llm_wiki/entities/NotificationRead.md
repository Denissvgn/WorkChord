# NotificationRead

**Location:** `backend/app/routers/discussion.py:33`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [routers_discussion](../modules/routers_discussion.md)

## Description

_Auto-generated from `NotificationRead` in `backend/app/routers/discussion.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `read` | `bool` | `read` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["NotificationRead (backend/app/routers/discussion.py)"]
    n1["BaseModel"]
    n2["mark_notification_read (backend/app/routers/discussion.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/routers_discussion.md"
    click n2 "../modules/routers_discussion.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [routers_discussion](../modules/routers_discussion.md) | 0 | `read` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `mark_notification_read` | type_reference | [routers_discussion](../modules/routers_discussion.md) | — |
