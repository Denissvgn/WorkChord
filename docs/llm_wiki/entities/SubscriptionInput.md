# SubscriptionInput

**Location:** `backend/app/routers/discussion.py:27`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [routers_discussion](../modules/routers_discussion.md)

## Description

_Auto-generated from `SubscriptionInput` in `backend/app/routers/discussion.py`._

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `expected_version` | `int` | `expected_version` | Yes | No | — | ge=0 | — | — |
| `enabled` | `bool` | `enabled` | Yes | No | — | — | — | — |
| `events` | `list[Literal['discussion', 'mention', 'review', 'block']]` | `events` | No | No | factory: `lambda: ['discussion', 'mention', 'review', 'block']` | max_length=4 | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SubscriptionInput (backend/app/routers/discussion.py)"]
    n1["BaseModel"]
    n2["set_task_subscription (backend/app/routers/discussion.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/routers_discussion.md"
    click n2 "../modules/routers_discussion.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [routers_discussion](../modules/routers_discussion.md) | 0 | `enabled`, `events`, `expected_version` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `set_task_subscription` | type_reference | [routers_discussion](../modules/routers_discussion.md) | — |
