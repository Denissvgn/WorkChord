# AnalyticsScope

**Location:** `frontend/src/types/analyticsScope.ts:1`
**Kind:** Interface
**Bases:** —
**Module:** [analyticsScope](../modules/analyticsScope.md)

## Description

_Auto-generated from `AnalyticsScope` in `frontend/src/types/analyticsScope.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `project_id` | `number` | No | — | — |
| `iteration_id` | `number` | No | — | — |
| `backlog` | `boolean` | No | — | — |
| `all_projects` | `boolean` | No | — | — |
| `all_projects_backlog` | `boolean` | No | — | — |
| `lookback_days` | `number` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AnalyticsScope (frontend/src/types/analyticsScope.ts)"]
    n1["ExecutionUsagePanel (frontend/src/components/analytics/ExecutionUsagePanel.tsx)"]
    n2["useAnalyticsScope (frontend/src/components/analytics/useAnalyticsScope.ts)"]
    n3["frontend/src/services/deliveryMetricsService.ts"]
    n4["frontend/src/services/executionUsageService.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/analyticsScope.md"
    click n1 "../modules/ExecutionUsagePanel.md"
    click n2 "../modules/useAnalyticsScope.md"
    click n3 "../modules/deliveryMetricsService.md"
    click n4 "../modules/executionUsageService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [analyticsScope](../modules/analyticsScope.md) | 0 | `all_projects`, `all_projects_backlog`, `backlog`, `iteration_id`, `lookback_days`, `project_id` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ExecutionUsagePanel` | type_reference | [ExecutionUsagePanel](../modules/ExecutionUsagePanel.md) | — |
| `useAnalyticsScope` | type_reference | [useAnalyticsScope](../modules/useAnalyticsScope.md) | — |
| `deliveryMetricsService` | import | [deliveryMetricsService](../modules/deliveryMetricsService.md) | — |
| `executionUsageService` | import | [executionUsageService](../modules/executionUsageService.md) | — |
