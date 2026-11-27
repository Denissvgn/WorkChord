# TaskRouting

**Location:** `backend/app/schemas/task_routing.py:42`
**Kind:** Pydantic model
**Bases:** `BaseModel`
**Module:** [task_routing](../modules/task_routing.md)

## Description

First rung, escalation ladder and reviewer of one task.

## Model Configuration

| Setting | Value | Source |
|---------|-------|--------|
| `extra` | `'forbid'` | model_config |

## Validators

| Method | Scope | Fields | Mode | Options |
|--------|-------|--------|------|---------|
| `bounded_source` | field | source_text | after | — |
| `distinct_rungs` | model | — | after | — |

## Attributes

| Name | Type | Wire name | Required | Nullable | Default | Constraints | Examples | Description |
|------|------|-----------|----------|----------|---------|-------------|-------------|----------|
| `schema_version` | `Literal[1]` | `schema_version` | No | No | `1` | — | — | — |
| `first_rung` | `RoutingRung \| None` | `first_rung` | No | Yes | `None` | — | — | — |
| `escalation` | `list[RoutingRung]` | `escalation` | No | No | factory: `list` | max_length=8 | — | — |
| `escalate_after_failed_runs` | `int` | `escalate_after_failed_runs` | No | No | `2` | ge=1; le=10 | — | — |
| `after_last_rung` | `str` | `after_last_rung` | No | No | `''` | max_length=2000 | — | What happens when the ladder is exhausted. |
| `reviewer` | `RoutingReviewer \| None` | `reviewer` | No | Yes | `None` | — | — | — |
| `notes` | `str` | `notes` | No | No | `''` | max_length=4000 | — | Further routing rules, rendered after the ladder. |
| `source_text` | `list[str]` | `source_text` | No | No | factory: `list` | max_length=20 | — | Original sentences a conversion replaced with this structure; kept for audit and never rendered. |

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `bounded_source` | `(value: list[str]) -> list[str]` | `@field_validator('source_text')`, `@classmethod` | — |
| `distinct_rungs` | `()` | `@model_validator(mode='after')` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskRouting (backend/app/schemas/task_routing.py)"]
    n1["BaseModel"]
    n2["backend/app/schemas/task_brief.py"]
    n3["backend/app/services/task_brief_service.py"]
    n4["_issues (backend/app/services/task_routing_service.py)"]
    n5["_refreshed (backend/app/services/task_routing_service.py)"]
    n6["_routing_keys (backend/app/services/task_routing_service.py)"]
    n7["check_routing (backend/app/services/task_routing_service.py)"]
    n8["convert_text_routing (backend/app/services/task_routing_service.py)"]
    n9["resolve_routing (backend/app/services/task_routing_service.py)"]
    n10["suggest_routing (backend/app/services/task_routing_service.py)"]
    n0 --> n1
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    n8 --> n0
    n9 --> n0
    n10 --> n0
    click n0 "../modules/task_routing.md"
    click n2 "../modules/schemas_task_brief.md"
    click n3 "../modules/task_brief_service.md"
    click n4 "../modules/task_routing_service.md"
    click n5 "../modules/task_routing_service.md"
    click n6 "../modules/task_routing_service.md"
    click n7 "../modules/task_routing_service.md"
    click n8 "../modules/task_routing_service.md"
    click n9 "../modules/task_routing_service.md"
    click n10 "../modules/task_routing_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [task_routing](../modules/task_routing.md) | 2 | `after_last_rung`, `escalate_after_failed_runs`, `escalation`, `first_rung`, `notes`, `reviewer`, `schema_version`, `source_text` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `BaseModel` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `task_brief` | import | [schemas_task_brief](../modules/schemas_task_brief.md) | — |
| `task_brief_service` | import | [task_brief_service](../modules/task_brief_service.md) | — |
| `_issues` | type_reference | [task_routing_service](../modules/task_routing_service.md) | — |
| `_refreshed` | type_reference | [task_routing_service](../modules/task_routing_service.md) | — |
| `_routing_keys` | type_reference | [task_routing_service](../modules/task_routing_service.md) | — |
| `check_routing` | type_reference | [task_routing_service](../modules/task_routing_service.md) | — |
| `convert_text_routing` | type_reference | [task_routing_service](../modules/task_routing_service.md) | — |
| `resolve_routing` | type_reference | [task_routing_service](../modules/task_routing_service.md) | — |
| `suggest_routing` | type_reference | [task_routing_service](../modules/task_routing_service.md) | — |
