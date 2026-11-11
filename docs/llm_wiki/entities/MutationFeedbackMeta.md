# MutationFeedbackMeta

**Location:** `frontend/src/features/mutationFeedback.ts:15`
**Kind:** Interface
**Bases:** `Record<string, unknown>`
**Module:** [mutationFeedback](../modules/mutationFeedback.md)

## Description

Put on a mutation's `meta` to announce its result. One listener shows the
success toast, so every write ends with the same visible, announced message;
errors stay where they happened (inline) and in the error toast.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `success` | `string \| ((data: unknown, variables: unknown) => string \| null \| undefined)` | No | — | — |
| `undo` | `(data: unknown, variables: unknown) => MutationUndo \| null \| undefined` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MutationFeedbackMeta (frontend/src/features/mutationFeedback.ts)"]
    n1["Record#60;string, unknown#62;"]
    n2["frontend/src/components/projects/InitiativeForm.tsx"]
    n3["frontend/src/components/projects/ProjectForm.tsx"]
    n4["frontend/src/components/releases/ReleaseForm.tsx"]
    n5["frontend/src/components/tasks/DeliveryDependencies.tsx"]
    n6["frontend/src/components/tasks/ImportTasksModal.tsx"]
    n7["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
    n8["frontend/src/components/tasks/QuickCapture.tsx"]
    n9["frontend/src/components/tasks/StatusChangeControl.tsx"]
    n10["frontend/src/components/tasks/TaskBulkOperationsPanel.tsx"]
    n11["frontend/src/components/tasks/TaskForm.tsx"]
    n12["frontend/src/components/tasks/TaskWorkPanel.tsx"]
    n13["frontend/src/components/team/ImportTeamModal.tsx"]
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
    n11 --> n0
    n12 --> n0
    n13 --> n0
    click n0 "../modules/mutationFeedback.md"
    click n2 "../modules/InitiativeForm.md"
    click n3 "../modules/ProjectForm.md"
    click n4 "../modules/ReleaseForm.md"
    click n5 "../modules/DeliveryDependencies.md"
    click n6 "../modules/ImportTasksModal.md"
    click n7 "../modules/KanbanBoard.md"
    click n8 "../modules/QuickCapture.md"
    click n9 "../modules/StatusChangeControl.md"
    click n10 "../modules/TaskBulkOperationsPanel.md"
    click n11 "../modules/TaskForm.md"
    click n12 "../modules/TaskWorkPanel.md"
    click n13 "../modules/ImportTeamModal.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [mutationFeedback](../modules/mutationFeedback.md) | 0 | `success`, `undo` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Record<string, unknown>` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `InitiativeForm` | import | [InitiativeForm](../modules/InitiativeForm.md) | — |
| `ProjectForm` | import | [ProjectForm](../modules/ProjectForm.md) | — |
| `ReleaseForm` | import | [ReleaseForm](../modules/ReleaseForm.md) | — |
| `DeliveryDependencies` | import | [DeliveryDependencies](../modules/DeliveryDependencies.md) | — |
| `ImportTasksModal` | import | [ImportTasksModal](../modules/ImportTasksModal.md) | — |
| `KanbanBoard` | import | [KanbanBoard](../modules/KanbanBoard.md) | — |
| `QuickCapture` | import | [QuickCapture](../modules/QuickCapture.md) | — |
| `StatusChangeControl` | import | [StatusChangeControl](../modules/StatusChangeControl.md) | — |
| `TaskBulkOperationsPanel` | import | [TaskBulkOperationsPanel](../modules/TaskBulkOperationsPanel.md) | — |
| `TaskForm` | import | [TaskForm](../modules/TaskForm.md) | — |
| `TaskWorkPanel` | import | [TaskWorkPanel](../modules/TaskWorkPanel.md) | — |
| `ImportTeamModal` | import | [ImportTeamModal](../modules/ImportTeamModal.md) | — |

> References: showing 12 of 22 logical references; 10 omitted by the 12-row generated summary limit.
