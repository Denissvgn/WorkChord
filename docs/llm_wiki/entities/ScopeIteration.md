# ScopeIteration

**Location:** `frontend/src/features/scope/workScope.ts:8`
**Kind:** Type alias
**Bases:** —
**Module:** [workScope](../modules/workScope.md)
**Target:**

```typescript
number | 'backlog'
```

## Description

One iteration, or work that has no iteration.

## Attributes

*See the alias definition for its member types.*

## Methods

*See the alias definition for callable and member types.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ScopeIteration (frontend/src/features/scope/workScope.ts)"]
    n1["frontend/src/components/layout/CommandMenu.tsx"]
    n2["frontend/src/components/layout/ScopeBar.tsx"]
    n3["PipelineView (frontend/src/components/tasks/PipelineView.tsx)"]
    n4["iterationsInView (frontend/src/features/overview/overviewSignals.ts)"]
    n5["pipelineTasksInScope (frontend/src/features/overview/overviewSignals.ts)"]
    n6["frontend/src/features/scope/scopeStore.ts"]
    n7["frontend/src/features/scope/useWorkScope.ts"]
    n8["defaultIterationForProject (frontend/src/features/scope/workScope.ts)"]
    n9["resolveWorkScope (frontend/src/features/scope/workScope.ts)"]
    n10["frontend/src/pages/OverviewPage.tsx"]
    n11["frontend/src/pages/TasksPage.tsx"]
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
    click n0 "../modules/workScope.md"
    click n1 "../modules/CommandMenu.md"
    click n2 "../modules/ScopeBar.md"
    click n3 "../modules/PipelineView.md"
    click n4 "../modules/overviewSignals.md"
    click n5 "../modules/overviewSignals.md"
    click n6 "../modules/scopeStore.md"
    click n7 "../modules/useWorkScope.md"
    click n8 "../modules/workScope.md"
    click n9 "../modules/workScope.md"
    click n10 "../modules/OverviewPage.md"
    click n11 "../modules/TasksPage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [workScope](../modules/workScope.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `CommandMenu` | import | [CommandMenu](../modules/CommandMenu.md) | — |
| `ScopeBar` | import | [ScopeBar](../modules/ScopeBar.md) | — |
| `PipelineView` | type_reference | [PipelineView](../modules/PipelineView.md) | — |
| `iterationsInView` | type_reference | [overviewSignals](../modules/overviewSignals.md) | — |
| `pipelineTasksInScope` | type_reference | [overviewSignals](../modules/overviewSignals.md) | — |
| `scopeStore` | import | [scopeStore](../modules/scopeStore.md) | — |
| `useWorkScope` | import | [useWorkScope](../modules/useWorkScope.md) | — |
| `defaultIterationForProject` | type_reference | [workScope](../modules/workScope.md) | — |
| `resolveWorkScope` | type_reference | [workScope](../modules/workScope.md) | — |
| `OverviewPage` | import | [OverviewPage](../modules/OverviewPage.md) | — |
| `TasksPage` | import | [TasksPage](../modules/TasksPage.md) | — |
