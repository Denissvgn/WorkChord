# RoutingIssue

**Location:** `frontend/src/types/task.ts:496`
**Kind:** Interface
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

_Auto-generated from `RoutingIssue` in `frontend/src/types/task.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `code` | `string` | Yes | — | — |
| `severity` | `'conflict' \| 'warning'` | Yes | — | — |
| `field` | `'first_rung' \| 'escalation' \| 'reviewer' \| 'assignee' \| 'routing'` | Yes | — | — |
| `message` | `string` | Yes | — | — |
| `catalog_key` | `string \| null` | No | — | — |
| `publisher_key` | `string \| null` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RoutingIssue (frontend/src/types/task.ts)"]
    n1["frontend/src/utils/routingCheck.ts"]
    n1 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/routingCheck.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `catalog_key`, `code`, `field`, `message`, `publisher_key`, `severity` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `routingCheck` | import | [routingCheck](../modules/routingCheck.md) | — |
