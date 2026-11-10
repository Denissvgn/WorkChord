# get_unique_employees

**Entry point:** `get_unique_employees` (`http`)
**Source:** [routers_team](../modules/routers_team.md)
**Modules touched:** [routers_team](../modules/routers_team.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_unique_employees
    participant p1 as service.get_all_unique_members
    p0-->>p1: service.get_all_unique_members
```

> Call sequence diagram shows 1 of 1 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 0 of 0 (0 omitted); unresolved 1 of 1 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 1; effect analysis evaluated: 1, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 2, emitted: 2, omitted: 0. Unavailable totals are excluded.

```mermaid
flowchart LR
    s1["1. get_unique_employees"]
    s2["2. service.get_all_unique_members"]
    s1 -. "service.get_all_unique_members(data not statically known)" .-> s2
    click s1 "../modules/routers_team.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_unique_employees` | `service: Annotated[TeamService, Depends(get_team_service)]` | - | - | `...` |
| `service.get_all_unique_members` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_unique_employees | service.get_all_unique_members | 46 | `service.get_all_unique_members(data not statically known)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_unique_employees` | `service.get_all_unique_members` | 46 |

## Behavior

This flow starts at `get_unique_employees` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
