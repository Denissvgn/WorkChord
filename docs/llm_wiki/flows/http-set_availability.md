# set_availability

**Entry point:** `set_availability` (`http`)
**Source:** [routers_capacity](../modules/routers_capacity.md)
**Modules touched:** [capacity_service](../modules/capacity_service.md), [routers_capacity](../modules/routers_capacity.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as set_availability
    participant p1 as CapacityService(…).set_calendar
    participant p2 as CapacityService
    p0-->>p1: CapacityService(…).set_calendar(profile_id, data.calendar_id, data.expected_version)
    p0->>p2: CapacityService
```

> Call sequence diagram shows 2 of 2 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 0 of 0 (0 omitted); unresolved 1 of 1 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 2; effect analysis evaluated: 1, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 4, emitted: 4, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `set_availability` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `CapacityService(…).set_calendar` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `CapacityService` | `unavailable` | `unavailable` | `unavailable` | — | — | — |

```mermaid
flowchart LR
    s1["1. set_availability"]
    s2["2. CapacityService(…).set_calendar"]
    s3["3. CapacityService"]
    s1 -. "CapacityService(…).set_calendar(profile_id, data.calendar_id, data.expected_version)" .-> s2
    s1 -->|"CapacityService(db)"| s3
    click s1 "../modules/routers_capacity.md"
    click s3 "../modules/capacity_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `set_availability` | `profile_id: int`, `data: CalendarSelection`, `db: Database` | - | - | `...` |
| `CapacityService(…).set_calendar` | - | - | - | - |
| `CapacityService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| set_availability | CapacityService(…).set_calendar | 39 | `CapacityService(db).set_calendar(profile_id, data.calendar_id, data.expected_version)` |
| set_availability | CapacityService | 39 | `CapacityService(db)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `set_availability` | `CapacityService(db).set_calendar` | 39 |

## Behavior

Checks person ownership and the supplied availability version, then changes the canonical calendar in one transaction. The shared planning reservation precedes affected iteration and task revisions; conflicts and failure roll back all derived updates.
