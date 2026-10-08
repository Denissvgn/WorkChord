# ObservedPlanningInput

**Location:** `frontend/src/services/planningInputService.ts:4`
**Kind:** Class
**Bases:** —
**Module:** [planningInputService](../modules/planningInputService.md)

## Description

_Auto-generated from `ObservedPlanningInput` in `frontend/src/services/planningInputService.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `kind` | `PlanningInputKind` | Yes | — | — |
| `resource_id` | `number` | Yes | — | — |
| `resource` | `T` | Yes | — | — |
| `expected_revisions` | `Record<number, number>` | Yes | — | — |
| `complete` | `true` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ObservedPlanningInput (frontend/src/services/planningInputService.ts)"]
    n1["PlanningInputBoundary (frontend/src/components/planning/PlanningInputBoundary.tsx)"]
    n2["frontend/src/features/usePlanningObservation.ts"]
    n3["frontend/src/pages/ProjectDetailPage.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/planningInputService.md"
    click n1 "../modules/PlanningInputBoundary.md"
    click n2 "../modules/usePlanningObservation.md"
    click n3 "../modules/ProjectDetailPage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [planningInputService](../modules/planningInputService.md) | 0 | `complete`, `expected_revisions`, `kind`, `resource`, `resource_id` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `PlanningInputBoundary` | type_reference | [PlanningInputBoundary](../modules/PlanningInputBoundary.md) | — |
| `usePlanningObservation` | import | [usePlanningObservation](../modules/usePlanningObservation.md) | — |
| `ProjectDetailPage` | import | [ProjectDetailPage](../modules/ProjectDetailPage.md) | — |
