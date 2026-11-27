# RefusalNextStep

**Location:** `frontend/src/types/task.ts:574`
**Kind:** Interface
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

What a person or agent may do about a refusal, from the server's one refusal catalogue.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `kind` | `string` | Yes | — | — |
| `authority` | `string` | Yes | — | — |
| `message` | `string` | Yes | — | — |
| `commands` | `Record<string, string>` | Yes | — | — |
| `ui_action` | `'record_provenance' \| 'accept_as_owner' \| null` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RefusalNextStep (frontend/src/types/task.ts)"]
    n1["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n2["RefusalNextStepNote (frontend/src/components/tasks/RefusalNextStepNote.tsx)"]
    n3["frontend/src/components/tasks/TaskRefusalNextSteps.test.tsx"]
    n4["frontend/src/components/tasks/TaskWorkPanel.tsx"]
    n5["getApiNextStep (frontend/src/utils/apiError.ts)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/TaskRoutingPanel.md"
    click n2 "../modules/RefusalNextStepNote.md"
    click n3 "../modules/TaskRefusalNextSteps.test.md"
    click n4 "../modules/TaskWorkPanel.md"
    click n5 "../modules/apiError.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `authority`, `commands`, `kind`, `message`, `ui_action` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskRoutingPanel` | import | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) | — |
| `RefusalNextStepNote` | type_reference | [RefusalNextStepNote](../modules/RefusalNextStepNote.md) | — |
| `TaskRefusalNextSteps.test` | import | [TaskRefusalNextSteps.test](../modules/TaskRefusalNextSteps.test.md) | — |
| `TaskWorkPanel` | import | [TaskWorkPanel](../modules/TaskWorkPanel.md) | — |
| `getApiNextStep` | type_reference | [apiError](../modules/apiError.md) | — |
