# _Resolver

**Location:** `backend/app/services/task_routing_service.py:464`
**Kind:** Class
**Bases:** —
**Module:** [task_routing_service](../modules/task_routing_service.md)

## Description

Match a model named in prose to exactly one enabled catalog entry by exact key or alias.

## Attributes

*No annotated attributes found.*

## Methods

| Method | Signature | Decorators | Description |
|--------|-----------|------------|-------------|
| `__init__` | `(entries)` | — | — |
| `__call__` | `(name: str \| None, effort: str \| None, key: str \| None = None)` | — | — |
| `_with_effort` | `(matches, effort)` | `@staticmethod` | — |

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["_Resolver (backend/app/services/task_routing_service.py)"]
    n1["parse_text_routing (backend/app/services/task_routing_service.py)"]
    n1 --> n0
    click n0 "../modules/task_routing_service.md"
    click n1 "../modules/task_routing_service.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [task_routing_service](../modules/task_routing_service.md) | 3 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `parse_text_routing` | call | [task_routing_service](../modules/task_routing_service.md) | 1 |
