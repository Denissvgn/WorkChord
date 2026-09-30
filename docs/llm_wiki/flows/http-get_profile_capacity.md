# get_profile_capacity

**Entry point:** `get_profile_capacity` (`http`)
**Source:** [routers_capacity](../modules/routers_capacity.md)
**Modules touched:** [capacity_service](../modules/capacity_service.md), [routers_capacity](../modules/routers_capacity.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_profile_capacity
    participant p1 as CapacityService(…).projection
    participant p2 as CapacityService
    p0-->>p1: CapacityService(…).projection
    p0->>p2: CapacityService
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_profile_capacity"]
    s2["2. CapacityService(…).projection"]
    s3["3. CapacityService"]
    s1 -. "CapacityService(…).projection(profile_id, start, end)" .-> s2
    s1 -->|"CapacityService(db)"| s3
    click s1 "../modules/routers_capacity.md"
    click s3 "../modules/capacity_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_profile_capacity` | `profile_id: int`, `start: date`, `end: date`, `db: Database` | - | - | `...` |
| `CapacityService(…).projection` | - | - | - | - |
| `CapacityService` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_profile_capacity | CapacityService(…).projection | 59 | `CapacityService(db).projection(profile_id, start, end)` |
| get_profile_capacity | CapacityService | 59 | `CapacityService(db)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_profile_capacity` | `CapacityService(db).projection` | 59 |

## Behavior

Accepts an inclusive range of at most 366 days for a visible person. Authorized allocations expose their factors, private allocations only busy hours. Unknown effort and calendar coverage limitations remain explicit. Saved baseline effort is distributed over working dates for explanation, independently of forecast dates.
