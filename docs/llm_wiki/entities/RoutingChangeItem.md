# RoutingChangeItem

**Location:** `frontend/src/utils/routingCheck.ts:60`
**Kind:** Interface
**Bases:** —
**Module:** [routingCheck](../modules/routingCheck.md)

## Description

One task of a bulk reassignment whose routing the suggestion would rewrite, or that has no suggestion.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `taskId` | `number` | Yes | — | — |
| `issues` | `RoutingIssue[]` | Yes | — | — |
| `before` | `TaskRouting \| null` | Yes | — | — |
| `after` | `TaskRouting \| null` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RoutingChangeItem (frontend/src/utils/routingCheck.ts)"]
    n1["frontend/src/components/planning/PlanBlockersSection.tsx"]
    n2["RoutingResultsList (frontend/src/components/tasks/RoutingCheckNotice.tsx)"]
    n3["frontend/src/components/tasks/TaskBulkOperationsPanel.tsx"]
    n4["routingChangeItems (frontend/src/utils/routingCheck.ts)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/routingCheck.md"
    click n1 "../modules/PlanBlockersSection.md"
    click n2 "../modules/RoutingCheckNotice.md"
    click n3 "../modules/TaskBulkOperationsPanel.md"
    click n4 "../modules/routingCheck.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [routingCheck](../modules/routingCheck.md) | 0 | `after`, `before`, `issues`, `taskId` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `PlanBlockersSection` | import | [PlanBlockersSection](../modules/PlanBlockersSection.md) | — |
| `RoutingResultsList` | type_reference | [RoutingCheckNotice](../modules/RoutingCheckNotice.md) | — |
| `TaskBulkOperationsPanel` | import | [TaskBulkOperationsPanel](../modules/TaskBulkOperationsPanel.md) | — |
| `routingChangeItems` | type_reference | [routingCheck](../modules/routingCheck.md) | — |
