# ExternalLinkCreate

**Location:** `frontend/src/types/task.ts:62`
**Kind:** Class
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `ExternalLinkCreate` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `provider` | `ExternalLinkProvider` | *required* | — |
| `external_key` | `string \| null` | *required* | — |
| `url` | `string \| null` | *required* | — |
| `title` | `string \| null` | *required* | — |
| `status` | `string \| null` | *required* | — |
| `metadata_json` | `Record<string, unknown>` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ExternalLinkCreate (frontend/src/types/task.ts)"]
    n1["frontend/src/services/taskService.ts"]
    n1 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/taskService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `external_key`, `metadata_json`, `provider`, `status`, `title`, `url` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `taskService` | import | [taskService](../modules/taskService.md) | — |
