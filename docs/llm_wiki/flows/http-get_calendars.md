# get_calendars

**Entry point:** `get_calendars` (`http`)
**Source:** [calendars](../modules/calendars.md)
**Modules touched:** [calendars](../modules/calendars.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_calendars
    participant p1 as service.get_all
    p0-->>p1: service.get_all
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_calendars"]
    s2["2. service.get_all"]
    s1 -. "service.get_all(data not statically known)" .-> s2
    click s1 "../modules/calendars.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_calendars` | `service: Annotated[CalendarService, Depends(get_calendar_service)]` | - | - | `...` |
| `service.get_all` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_calendars | service.get_all | 30 | `service.get_all(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_calendars` | `service.get_all` | 30 |

## Behavior

This flow starts at `get_calendars` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
