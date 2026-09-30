# set_availability

**Entry point:** `set_availability` (`http`)
**Source:** [routers_capacity](../modules/routers_capacity.md)
**Modules touched:** [capacity_service](../modules/capacity_service.md), [routers_capacity](../modules/routers_capacity.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as set_availability
    participant p1 as CapacityService(…).set_calendar
    participant p2 as CapacityService
    p0-->>p1: CapacityService(…).set_calendar
    p0->>p2: CapacityService
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `set_availability` | `CapacityService(db).set_calendar` | 39 |

## Behavior

Checks person ownership and the supplied availability version, then changes the canonical calendar in one transaction. The shared planning reservation precedes affected iteration and task revisions; conflicts and failure roll back all derived updates.
