# ManualProvenanceWrite

**Location:** `frontend/src/types/task.ts:520`
**Kind:** Interface
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `ManualProvenanceWrite` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `expected_version` | `number` | Yes | — | — |
| `artifact_revision` | `number` | Yes | — | — |
| `executor` | `ManualProvenanceExecutor` | Yes | — | — |
| `head_commit_url` | `string` | Yes | — | — |
| `commit_urls` | `string[]` | Yes | — | — |
| `pr_url` | `string` | No | — | — |
| `base_commit_url` | `string` | No | — | — |
| `reason` | `string` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ManualProvenanceWrite (frontend/src/types/task.ts)"]
    n1["frontend/src/services/taskService.ts"]
    n1 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/taskService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `artifact_revision`, `base_commit_url`, `commit_urls`, `executor`, `expected_version`, `head_commit_url`, `pr_url`, `reason` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `taskService` | import | [taskService](../modules/taskService.md) | — |
