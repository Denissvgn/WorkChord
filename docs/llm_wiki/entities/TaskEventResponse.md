# TaskEventResponse

**Location:** `backend/app/schemas/agent.py:296`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [schemas_agent](../modules/schemas_agent.md)

## Description

Task event response.

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `id` | `int` | `id` | Yes | No | — | — | — | — |
| `task_id` | `Optional[int]` | `task_id` | Yes | Yes | — | — | — | — |
| `actor_type` | `str` | `actor_type` | Yes | No | — | — | — | — |
| `actor_id` | `Optional[int]` | `actor_id` | Yes | Yes | — | — | — | — |
| `event_type` | `str` | `event_type` | Yes | No | — | — | — | — |
| `payload` | `dict[str, Any]` | `payload` | Yes | No | — | — | — | — |
| `trace_id` | `Optional[str]` | `trace_id` | No | Yes | `None` | — | — | — |
| `span_id` | `Optional[str]` | `span_id` | No | Yes | `None` | — | — | — |
| `correlation_id` | `Optional[str]` | `correlation_id` | No | Yes | `None` | — | — | — |
| `idempotency_key` | `Optional[str]` | `idempotency_key` | No | Yes | `None` | — | — | — |
| `created_at` | `datetime` | `created_at` | Yes | No | — | — | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskEventResponse (backend/app/schemas/agent.py)"]
    n1["BaseModel"]
    n2["append_task_event (backend/app/routers/agent.py)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/schemas_agent.md"
    click n2 "../modules/routers_agent.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [schemas_agent](../modules/schemas_agent.md) | 0 | `actor_id`, `actor_type`, `correlation_id`, `created_at`, `event_type`, `id`, `idempotency_key`, `payload`, `span_id`, `task_id`, `trace_id` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `append_task_event` | call | [routers_agent](../modules/routers_agent.md) | 1 |
| `append_task_event` | type_reference | [routers_agent](../modules/routers_agent.md) | — |
