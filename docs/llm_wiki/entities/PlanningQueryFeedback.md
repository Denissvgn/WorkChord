# PlanningQueryFeedback

**Location:** `frontend/src/features/planningMasters/usePlanningReadiness.ts:35`
**Kind:** Type alias
**Bases:** —
**Module:** [usePlanningReadiness](../modules/usePlanningReadiness.md)
**Target:**

```typescript
{
    enabled: boolean;
    hasData: boolean;
    dataUpdatedAt: number;
    isLoading: boolean;
    isFetching: boolean;
    isError: boolean;
    isBlockingError: boolean;
    isRefetchError: boolean;
    error: unknown;
    refetch: () => Promise<unknown>;
}
```

## Description

_Auto-generated from `PlanningQueryFeedback` in `frontend/src/features/planningMasters/usePlanningReadiness.ts`._

## Attributes

*See the alias definition for its member types.*

## Methods

*See the alias definition for callable and member types.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["PlanningQueryFeedback (frontend/src/features/planningMasters/usePlanningReadiness.ts)"]
    n1["frontend/src/pages/PlanPage.tsx"]
    n1 --> n0
    click n0 "../modules/usePlanningReadiness.md"
    click n1 "../modules/PlanPage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [usePlanningReadiness](../modules/usePlanningReadiness.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `PlanPage` | import | [PlanPage](../modules/PlanPage.md) | — |
