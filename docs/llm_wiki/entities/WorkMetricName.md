# WorkMetricName

**Location:** `frontend/src/services/taskService.ts:274`
**Kind:** Type alias
**Bases:** —
**Module:** [taskService](../modules/taskService.md)
**Target:**

```typescript
'total' | 'planned' | 'active' | 'resolved' | 'closed' | 'implemented' | 'accepted' | 'blocked'
    | 'overdue' | 'late_start' | 'iteration_overflow' | 'acceptance_unknown' | 'unknown_estimate'
```

## Description

_Auto-generated from `WorkMetricName` in `frontend/src/services/taskService.ts`._

## Attributes

*See the alias definition for its member types.*

## Methods

*See the alias definition for callable and member types.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["WorkMetricName (frontend/src/services/taskService.ts)"]
    n1["MetricCount (frontend/src/components/tasks/MetricCount.tsx)"]
    n2["frontend/src/components/tasks/WorkMetricsLine.tsx"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/taskService.md"
    click n1 "../modules/MetricCount.md"
    click n2 "../modules/WorkMetricsLine.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [taskService](../modules/taskService.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `MetricCount` | type_reference | [MetricCount](../modules/MetricCount.md) | — |
| `WorkMetricsLine` | import | [WorkMetricsLine](../modules/WorkMetricsLine.md) | — |
