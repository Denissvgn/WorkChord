# RoutingRung

**Location:** `frontend/src/types/task.ts:470`
**Kind:** Interface
**Bases:** —
**Module:** [types_task](../modules/types_task.md)

## Description

One model catalog entry that may execute a task or review its result.

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `catalog_key` | `string` | Yes | — | — |
| `harness` | `string` | No | — | — |
| `effort` | `string \| null` | No | — | — |
| `publisher_key` | `string \| null` | No | — | — |
| `configured_model_alias` | `string \| null` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["RoutingRung (frontend/src/types/task.ts)"]
    n1["RoutingReviewer (frontend/src/types/task.ts)"]
    n2["rungLabel (frontend/src/utils/routingCheck.ts)"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/types_task.md"
    click n1 "../modules/types_task.md"
    click n2 "../modules/routingCheck.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_task](../modules/types_task.md) | 0 | `catalog_key`, `configured_model_alias`, `effort`, `harness`, `publisher_key` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Subclass | `RoutingReviewer` | [types_task](../modules/types_task.md) |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `rungLabel` | type_reference | [routingCheck](../modules/routingCheck.md) | — |
