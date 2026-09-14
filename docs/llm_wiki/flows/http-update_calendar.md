# update_calendar

**Entry point:** `update_calendar` (`http`)
**Source:** [calendars](../modules/calendars.md)
**Modules touched:** [calendars](../modules/calendars.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_calendar
    participant p1 as service.update
    participant p2 as HTTPException
    p0-->>p1: service.update
    p0-->>p2: HTTPException
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. update_calendar"]
    s2["2. service.update"]
    s3["3. HTTPException"]
    s1 -. "service.update(calendar_id, data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    b0["mutation service.update"]
    s1 -. "mutation service.update" .-> b0
    click s1 "../modules/calendars.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `update_calendar` | `calendar_id: int`, `data: CalendarUpdate`, `service: Annotated[CalendarService, Depends(get_calendar_service)]` | `status` | - | `calendar` |
| `service.update` | - | - | - | - |
| `HTTPException` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| update_calendar | service.update | 68 | `service.update(calendar_id, data)` |
| update_calendar | HTTPException | 70 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `service.update` | `update_calendar` | 68 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `update_calendar` | `HTTPException` | 70 |

## Behavior

This flow starts at `update_calendar` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
