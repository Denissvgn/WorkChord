# TaskBrief

**Location:** `frontend/src/types/task.ts:441`
**Kind:** Interface
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `TaskBrief` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `schema_version` | `1` | Yes | — | — |
| `goal` | `string` | Yes | — | — |
| `context` | `string` | Yes | — | — |
| `scope` | `string` | Yes | — | — |
| `exclusions` | `string` | Yes | — | — |
| `acceptance_criteria` | `BriefCriterion[]` | Yes | — | — |
| `verification` | `string` | Yes | — | — |
| `artifact_expectations` | `string` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskBrief (frontend/src/types/task.ts)"]
    n1["TaskBriefEditor (frontend/src/components/tasks/TaskBriefEditor.tsx)"]
    n2["emptyTaskBrief (frontend/src/components/tasks/taskEditorContract.ts)"]
    n3["frontend/src/components/tasks/TaskReadView.tsx"]
    n4["TriageDraftPreview (frontend/src/components/triage/TriageDraftPreview.tsx)"]
    n5["frontend/src/features/firstRun/sampleProject.fixture.ts"]
    n6["frontend/src/services/taskService.ts"]
    n7["frontend/src/types/triage.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/TaskBriefEditor.md"
    click n2 "../modules/taskEditorContract.md"
    click n3 "../modules/TaskReadView.md"
    click n4 "../modules/TriageDraftPreview.md"
    click n5 "../modules/sampleProject.fixture.md"
    click n6 "../modules/taskService.md"
    click n7 "../modules/types_triage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `acceptance_criteria`, `artifact_expectations`, `context`, `exclusions`, `goal`, `schema_version`, `scope`, `verification` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `TaskBriefEditor` | type_reference | [TaskBriefEditor](../modules/TaskBriefEditor.md) | — |
| `emptyTaskBrief` | type_reference | [taskEditorContract](../modules/taskEditorContract.md) | — |
| `TaskReadView` | import | [TaskReadView](../modules/TaskReadView.md) | — |
| `TriageDraftPreview` | type_reference | [TriageDraftPreview](../modules/TriageDraftPreview.md) | — |
| `sampleProject.fixture` | import | [sampleProject.fixture](../modules/sampleProject.fixture.md) | — |
| `taskService` | import | [taskService](../modules/taskService.md) | — |
| `triage` | import | [types_triage](../modules/types_triage.md) | — |
