# DestinationCounterValues

**Location:** `frontend/src/navigation/destinations.ts:218`
**Kind:** Interface
**Bases:** —
**Module:** [destinations](../modules/destinations.md)

## Description

_Auto-generated from `DestinationCounterValues` in `frontend/src/navigation/destinations.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `requestsWaiting` | `number` | No | — | — |
| `planProgress` | `{ done: number; total: number }` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["DestinationCounterValues (frontend/src/navigation/destinations.ts)"]
    n1["frontend/src/components/layout/AppSidebar.tsx"]
    n2["formatDestinationCounter (frontend/src/navigation/destinations.ts)"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/destinations.md"
    click n1 "../modules/AppSidebar.md"
    click n2 "../modules/destinations.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [destinations](../modules/destinations.md) | 0 | `planProgress`, `requestsWaiting` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AppSidebar` | import | [AppSidebar](../modules/AppSidebar.md) | — |
| `formatDestinationCounter` | type_reference | [destinations](../modules/destinations.md) | — |
