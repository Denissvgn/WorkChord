# TasksImportRequest

**Location:** `frontend/src/types/task.ts:278`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TasksImportRequest` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `text` | `string` | Yes | — | — |
| `destination` | `TaskImportDestination` | No | — | — |
| `expected_revision` | `number` | No | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TasksImportRequest (frontend/src/types/task.ts)"]
    n1["frontend/src/services/taskService.ts"]
    n1 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/taskService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `destination`, `expected_revision`, `text` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `taskService` | import | [taskService](../modules/taskService.md) | — |
