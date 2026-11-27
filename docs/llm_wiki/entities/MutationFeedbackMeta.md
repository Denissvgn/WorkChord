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
| `undo` | `(data: unknown, variables: unknown, context: unknown) => MutationUndo \| null \| undefined` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MutationFeedbackMeta (frontend/src/features/mutationFeedback.ts)"]
    n1["Record#60;string, unknown#62;"]
    n2["frontend/src/components/capacity/TeamForm.tsx"]
    n3["frontend/src/components/capacity/TeamList.tsx"]
    n4["frontend/src/components/capacity/VacationManager.tsx"]
    n5["frontend/src/components/projects/AddMilestoneModal.tsx"]
    n6["frontend/src/components/projects/InitiativeForm.tsx"]
    n7["frontend/src/components/projects/ProjectForm.tsx"]
    n8["frontend/src/components/projects/SetDatesPopover.tsx"]
    n9["frontend/src/components/releases/ReleaseForm.tsx"]
    n10["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n11["frontend/src/components/tasks/DeliveryDependencies.tsx"]
    n12["frontend/src/components/tasks/ImportTasksModal.tsx"]
    n13["frontend/src/components/tasks/KanbanBoard/KanbanBoard.tsx"]
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
    click n2 "../modules/TeamForm.md"
    click n3 "../modules/TeamList.md"
    click n4 "../modules/VacationManager.md"
    click n5 "../modules/AddMilestoneModal.md"
    click n6 "../modules/InitiativeForm.md"
    click n7 "../modules/ProjectForm.md"
    click n8 "../modules/SetDatesPopover.md"
    click n9 "../modules/ReleaseForm.md"
    click n10 "../modules/TemplateLabelSettings.md"
    click n11 "../modules/DeliveryDependencies.md"
    click n12 "../modules/ImportTasksModal.md"
    click n13 "../modules/KanbanBoard.md"
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
| `TeamForm` | import | [TeamForm](../modules/TeamForm.md) | — |
| `TeamList` | import | [TeamList](../modules/TeamList.md) | — |
| `VacationManager` | import | [VacationManager](../modules/VacationManager.md) | — |
| `AddMilestoneModal` | import | [AddMilestoneModal](../modules/AddMilestoneModal.md) | — |
| `InitiativeForm` | import | [InitiativeForm](../modules/InitiativeForm.md) | — |
| `ProjectForm` | import | [ProjectForm](../modules/ProjectForm.md) | — |
| `SetDatesPopover` | import | [SetDatesPopover](../modules/SetDatesPopover.md) | — |
| `ReleaseForm` | import | [ReleaseForm](../modules/ReleaseForm.md) | — |
| `TemplateLabelSettings` | import | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) | — |
| `DeliveryDependencies` | import | [DeliveryDependencies](../modules/DeliveryDependencies.md) | — |
| `ImportTasksModal` | import | [ImportTasksModal](../modules/ImportTasksModal.md) | — |
| `KanbanBoard` | import | [KanbanBoard](../modules/KanbanBoard.md) | — |

> References: showing 12 of 33 logical references; 21 omitted by the 12-row generated summary limit.
