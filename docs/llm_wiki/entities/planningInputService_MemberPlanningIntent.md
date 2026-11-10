# MemberPlanningIntent

**Location:** `frontend/src/services/planningInputService.ts:12`
**Kind:** Type alias
**Bases:** —
**Module:** [planningInputService](../modules/planningInputService.md)
**Target:**

```typescript
{ profile_id?: number | null; name?: string; email?: string | null; text?: string; csv_text?: string }
```

## Description

_Auto-generated from `MemberPlanningIntent` in `frontend/src/services/planningInputService.ts`._

## Attributes

*See the alias definition for its member types.*

## Methods

*See the alias definition for callable and member types.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MemberPlanningIntent (frontend/src/services/planningInputService.ts)"]
    n1["PlanningInputBoundary (frontend/src/components/planning/PlanningInputBoundary.tsx)"]
    n2["frontend/src/components/team/TeamForm.tsx"]
    n3["frontend/src/features/usePlanningObservation.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    click n0 "../modules/planningInputService.md"
    click n1 "../modules/PlanningInputBoundary.md"
    click n2 "../modules/TeamForm.md"
    click n3 "../modules/usePlanningObservation.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [planningInputService](../modules/planningInputService.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `PlanningInputBoundary` | type_reference | [PlanningInputBoundary](../modules/PlanningInputBoundary.md) | — |
| `TeamForm` | import | [TeamForm](../modules/TeamForm.md) | — |
| `usePlanningObservation` | import | [usePlanningObservation](../modules/usePlanningObservation.md) | — |
