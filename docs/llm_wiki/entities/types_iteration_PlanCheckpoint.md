# PlanCheckpoint

**Location:** `frontend/src/types/iteration.ts:112`
**Kind:** Interface
**Bases:** —
**Module:** [types_iteration](../modules/types_iteration.md)

## Description

_Auto-generated from `PlanCheckpoint` in `frontend/src/types/iteration.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `'iteration' \| 'team' \| 'work' \| 'blockers' \| 'schedule' \| 'review'` | Yes | — | — |
| `state` | `'done' \| 'warn' \| 'todo' \| 'blocked'` | Yes | — | — |
| `reason_codes` | `string[]` | Yes | — | — |
| `counts` | `Record<string, number>` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["PlanCheckpoint (frontend/src/types/iteration.ts)"]
    n1["frontend/src/features/firstRun/GetStartedFlow.test.tsx"]
    n2["frontend/src/features/firstRun/GetStartedPanel.test.tsx"]
    n3["firstIncompleteCheckpoint (frontend/src/features/planningMasters/planCheckpoints.ts)"]
    n4["planCheckpointSections (frontend/src/features/planningMasters/planCheckpoints.ts)"]
    n5["frontend/src/pages/OverviewPage.test.tsx"]
    n6["frontend/src/pages/PlanIterations.test.tsx"]
    n7["frontend/src/pages/PlanPage.test.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    n7 --> n0
    click n0 "../modules/types_iteration.md"
    click n1 "../modules/GetStartedFlow.test.md"
    click n2 "../modules/GetStartedPanel.test.md"
    click n3 "../modules/planCheckpoints.md"
    click n4 "../modules/planCheckpoints.md"
    click n5 "../modules/OverviewPage.test.md"
    click n6 "../modules/PlanIterations.test.md"
    click n7 "../modules/PlanPage.test.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_iteration](../modules/types_iteration.md) | 0 | `counts`, `id`, `reason_codes`, `state` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `GetStartedFlow.test` | import | [GetStartedFlow.test](../modules/GetStartedFlow.test.md) | — |
| `GetStartedPanel.test` | import | [GetStartedPanel.test](../modules/GetStartedPanel.test.md) | — |
| `firstIncompleteCheckpoint` | type_reference | [planCheckpoints](../modules/planCheckpoints.md) | — |
| `planCheckpointSections` | type_reference | [planCheckpoints](../modules/planCheckpoints.md) | — |
| `OverviewPage.test` | import | [OverviewPage.test](../modules/OverviewPage.test.md) | — |
| `PlanIterations.test` | import | [PlanIterations.test](../modules/PlanIterations.test.md) | — |
| `PlanPage.test` | import | [PlanPage.test](../modules/PlanPage.test.md) | — |
