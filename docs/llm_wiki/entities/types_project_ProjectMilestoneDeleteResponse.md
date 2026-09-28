# ProjectMilestoneDeleteResponse

**Location:** `frontend/src/types/project.ts:161`
**Kind:** Class
**Bases:** —
**Module:** [types_project](../modules/types_project.md)

## Description

_Auto-generated from `ProjectMilestoneDeleteResponse` in `frontend/src/types/project.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `success` | `boolean` | Yes | — | — |
| `message` | `string` | Yes | — | — |
| `detached_task_count` | `number` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ProjectMilestoneDeleteResponse (frontend/src/types/project.ts)"]
    n1["frontend/src/services/projectService.ts"]
    n1 --> n0
    click n0 "../modules/types_project.md"
    click n1 "../modules/projectService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_project](../modules/types_project.md) | 0 | `detached_task_count`, `message`, `success` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `projectService` | import | [projectService](../modules/projectService.md) | — |
