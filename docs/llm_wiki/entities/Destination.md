# Destination

**Location:** `frontend/src/navigation/destinations.ts:44`
**Kind:** Interface
**Bases:** —
**Module:** [destinations](../modules/destinations.md)

## Description

_Auto-generated from `Destination` in `frontend/src/navigation/destinations.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `DestinationId` | Yes | — | — |
| `path` | `string` | Yes | — | — |
| `labelKey` | `string` | Yes | — | — |
| `defaultLabel` | `string` | Yes | — | — |
| `icon` | `LucideIcon` | Yes | — | — |
| `counter` | `DestinationCounterSource` | No | — | — |
| `owns` | `readonly string[]` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["Destination (frontend/src/navigation/destinations.ts)"]
    n1["frontend/src/components/layout/AppSidebar.tsx"]
    n2["destinationsOwningPath (frontend/src/navigation/destinations.ts)"]
    n3["formatDestinationCounter (frontend/src/navigation/destinations.ts)"]
    n4["getCounterSource (frontend/src/navigation/destinations.ts)"]
    n5["getDestination (frontend/src/navigation/destinations.ts)"]
    n6["getDestinationForPath (frontend/src/navigation/destinations.ts)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/destinations.md"
    click n1 "../modules/AppSidebar.md"
    click n2 "../modules/destinations.md"
    click n3 "../modules/destinations.md"
    click n4 "../modules/destinations.md"
    click n5 "../modules/destinations.md"
    click n6 "../modules/destinations.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [destinations](../modules/destinations.md) | 0 | `counter`, `defaultLabel`, `icon`, `id`, `labelKey`, `owns`, `path` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AppSidebar` | import | [AppSidebar](../modules/AppSidebar.md) | — |
| `destinationsOwningPath` | type_reference | [destinations](../modules/destinations.md) | — |
| `formatDestinationCounter` | type_reference | [destinations](../modules/destinations.md) | — |
| `getCounterSource` | type_reference | [destinations](../modules/destinations.md) | — |
| `getDestination` | type_reference | [destinations](../modules/destinations.md) | — |
| `getDestinationForPath` | type_reference | [destinations](../modules/destinations.md) | — |
