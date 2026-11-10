# ExecutionUsageSummary

**Location:** `frontend/src/types/executionUsage.ts:1`
**Kind:** Interface
**Bases:** —
**Module:** [executionUsage](../modules/executionUsage.md)

## Description

_Auto-generated from `ExecutionUsageSummary` in `frontend/src/types/executionUsage.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `window_start` | `string` | Yes | — | — |
| `window_end` | `string` | Yes | — | — |
| `window_basis` | `string` | Yes | — | — |
| `expected_runs` | `number` | Yes | — | — |
| `reported_runs` | `number` | Yes | — | — |
| `unreported_runs` | `number` | Yes | — | — |
| `partial_reports` | `number` | Yes | — | — |
| `unavailable_reports` | `number` | Yes | — | — |
| `simulated_reports` | `number` | Yes | — | — |
| `measured_report_count` | `number` | Yes | — | — |
| `provider_reported_cost` | `Record<string, string \| null>` | Yes | — | — |
| `estimated_cost` | `Record<string, string \| null>` | Yes | — | — |
| `known_cost_reports` | `Record<string, number>` | Yes | — | — |
| `unknown_cost_reports` | `number` | Yes | — | — |
| `accepted_task_identities` | `number` | Yes | — | — |
| `reports_linked_to_accepted_tasks` | `number` | Yes | — | — |
| `reported_human_effort_minutes` | `string \| null` | Yes | — | — |
| `human_effort_reports` | `number` | Yes | — | — |
| `reported_units` | `Record<string, string \| null>` | Yes | — | — |
| `unit_report_counts` | `Record<string, number>` | Yes | — | — |
| `simulated_reported_cost` | `Record<string, string>` | Yes | — | — |
| `simulated_estimated_cost` | `Record<string, string>` | Yes | — | — |
| `simulated_units` | `Record<string, string \| null>` | Yes | — | — |
| `independently_reconciled` | `false` | Yes | — | — |
| `advisory_budget` | <pre><code>&#123; amount&#58; string&#59; currency&#58; string&#59; known&#95;reported&#95;cost&#58; string &#124; null&#59;&#10;        known&#95;estimated&#95;cost&#58; string &#124; null&#59; coverage&#58; string&#59; advisory&#95;only&#58; true &#125; &#124; null</code></pre> | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["ExecutionUsageSummary (frontend/src/types/executionUsage.ts)"]
    n1["frontend/src/components/analytics/ExecutionUsagePanel.test.tsx"]
    n2["frontend/src/services/executionUsageService.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/executionUsage.md"
    click n1 "../modules/ExecutionUsagePanel.test.md"
    click n2 "../modules/executionUsageService.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [executionUsage](../modules/executionUsage.md) | 0 | `accepted_task_identities`, `advisory_budget`, `estimated_cost`, `expected_runs`, `human_effort_reports`, `independently_reconciled`, `known_cost_reports`, `measured_report_count`, `partial_reports`, `provider_reported_cost`, `reported_human_effort_minutes`, `reported_runs` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `ExecutionUsagePanel.test` | import | [ExecutionUsagePanel.test](../modules/ExecutionUsagePanel.test.md) | — |
| `executionUsageService` | import | [executionUsageService](../modules/executionUsageService.md) | — |
