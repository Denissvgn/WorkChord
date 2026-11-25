# list_maintenance_windows

**Entry point:** `list_maintenance_windows` (`http`)
**Source:** [maintenance_windows](../modules/maintenance_windows.md)
**Modules touched:** [maintenance_windows](../modules/maintenance_windows.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_maintenance_windows
    participant p1 as service.list_windows
    p0-->>p1: service.list_windows(limit=limit)
```

> Call sequence diagram shows 1 of 1 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 0 of 0 (0 omitted); unresolved 1 of 1 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 1; effect analysis evaluated: 1, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 3, emitted: 3, omitted: 0. Unavailable totals are excluded.

```mermaid
flowchart LR
    s1["1. list_maintenance_windows"]
    s2["2. service.list_windows"]
    s1 -. "service.list_windows(limit=limit)" .-> s2
    click s1 "../modules/maintenance_windows.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_maintenance_windows` | `service: Service`, `limit: int` | - | - | `...` |
| `service.list_windows` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_maintenance_windows | service.list_windows | 52 | `service.list_windows(limit=limit)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_maintenance_windows` | `service.list_windows` | 52 |

## Behavior

Returns recent windows, newest first, with their recorded actual times. A coordinated control-plane maintenance window has one open window at a time. Announcing it closes admission for new work at once; work already holding a live claim keeps renewing and may finish. The operator can begin only when every live claim owner has acknowledged for the claim's current generation, each lease outlives the bounded outage plus its margin, no running run lacks a live claim and every PM has a notice receipt. A PM notice is recorded evidence of notification, never run-owner consent. Closing or cancelling reopens admission.
