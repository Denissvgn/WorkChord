# Iteration

**Location:** `frontend/src/types/iteration.ts:9`
**Kind:** Interface
**Bases:** —
**Module:** [types_iteration](../modules/types_iteration.md)

## Description

_Auto-generated from `Iteration` in `frontend/src/types/iteration.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `nominal_day_hours` | `number` | No | — | — |
| `revision` | `number` | No | — | — |
| `id` | `number` | Yes | — | — |
| `name` | `string` | Yes | — | — |
| `calendar_id` | `number` | Yes | — | — |
| `project_id` | `number \| null` | No | — | — |
| `project` | `IterationProject \| null` | No | — | — |
| `start_date` | `string` | Yes | — | — |
| `end_date` | `string` | Yes | — | — |
| `manager_email` | `string` | No | — | — |
| `working_days` | `number` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Iteration (frontend/src/types/iteration.ts)"]
    n1["frontend/src/components/capacity/CapacitySection.test.tsx"]
    n2["CapacitySection (frontend/src/components/capacity/CapacitySection.tsx)"]
    n3["frontend/src/components/capacity/PlanQuickAddCapacity.test.tsx"]
    n4["PlanQuickAddCapacity (frontend/src/components/capacity/PlanQuickAddCapacity.tsx)"]
    n5["AllIterationsDrawer (frontend/src/components/iteration/AllIterationsDrawer.tsx)"]
    n6["IterationEditorDrawer (frontend/src/components/iteration/IterationEditorDrawer.tsx)"]
    n7["frontend/src/components/iteration/IterationForm.test.tsx"]
    n8["IterationForm (frontend/src/components/iteration/IterationForm.tsx)"]
    n9["IterationList (frontend/src/components/iteration/IterationList.tsx)"]
    n10["frontend/src/components/layout/planProgressPlacement.test.tsx"]
    n11["frontend/src/components/layout/ScopeBar.tsx"]
    n12["PlanIterationCheckpoint (frontend/src/components/planning/PlanIterationCheckpoint.tsx)"]
    n1 --> n0
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
    click n0 "../modules/types_iteration.md"
    click n1 "../modules/CapacitySection.test.md"
    click n2 "../modules/CapacitySection.md"
    click n3 "../modules/PlanQuickAddCapacity.test.md"
    click n4 "../modules/PlanQuickAddCapacity.md"
    click n5 "../modules/AllIterationsDrawer.md"
    click n6 "../modules/IterationEditorDrawer.md"
    click n7 "../modules/IterationForm.test.md"
    click n8 "../modules/IterationForm.md"
    click n9 "../modules/IterationList.md"
    click n10 "../modules/planProgressPlacement.test.md"
    click n11 "../modules/ScopeBar.md"
    click n12 "../modules/PlanIterationCheckpoint.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_iteration](../modules/types_iteration.md) | 0 | `calendar_id`, `end_date`, `id`, `manager_email`, `name`, `nominal_day_hours`, `project`, `project_id`, `revision`, `start_date`, `working_days` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `CapacitySection.test` | import | [CapacitySection.test](../modules/CapacitySection.test.md) | — |
| `CapacitySection` | type_reference | [CapacitySection](../modules/CapacitySection.md) | — |
| `PlanQuickAddCapacity.test` | import | [PlanQuickAddCapacity.test](../modules/PlanQuickAddCapacity.test.md) | — |
| `PlanQuickAddCapacity` | type_reference | [PlanQuickAddCapacity](../modules/PlanQuickAddCapacity.md) | — |
| `AllIterationsDrawer` | type_reference | [AllIterationsDrawer](../modules/AllIterationsDrawer.md) | — |
| `IterationEditorDrawer` | type_reference | [IterationEditorDrawer](../modules/IterationEditorDrawer.md) | — |
| `IterationForm.test` | import | [IterationForm.test](../modules/IterationForm.test.md) | — |
| `IterationForm` | type_reference | [IterationForm](../modules/IterationForm.md) | — |
| `IterationList` | type_reference | [IterationList](../modules/IterationList.md) | — |
| `planProgressPlacement.test` | import | [planProgressPlacement.test](../modules/planProgressPlacement.test.md) | — |
| `ScopeBar` | import | [ScopeBar](../modules/ScopeBar.md) | — |
| `PlanIterationCheckpoint` | type_reference | [PlanIterationCheckpoint](../modules/PlanIterationCheckpoint.md) | — |

> References: showing 12 of 44 logical references; 32 omitted by the 12-row generated summary limit.
