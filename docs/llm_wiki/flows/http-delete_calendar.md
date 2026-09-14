# delete_calendar

**Entry point:** `delete_calendar` (`http`)
**Source:** [calendars](../modules/calendars.md)
**Modules touched:** [calendars](../modules/calendars.md), [schemas_common](../modules/schemas_common.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as delete_calendar
    participant p1 as service.delete
    participant p2 as HTTPException
    participant p3 as str
    participant p4 as MessageResponse
    p0-->>p1: service.delete
    p0-->>p2: HTTPException
    p0-->>p3: str
    p0-->>p2: HTTPException
    p0->>p4: MessageResponse
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. delete_calendar"]
    s2["2. service.delete"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. HTTPException"]
    s6["6. MessageResponse"]
    s1 -. "service.delete(calendar_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s5
    s1 -->|"MessageResponse(message=..., success=True)"| s6
    click s1 "../modules/calendars.md"
    click s6 "../modules/schemas_common.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `delete_calendar` | `calendar_id: int`, `service: Annotated[CalendarService, Depends(get_calendar_service)]` | `status`, `status` | - | `MessageResponse(...)` |
| `service.delete` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `MessageResponse` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| delete_calendar | service.delete | 84 | `service.delete(calendar_id)` |
| delete_calendar | HTTPException | 86 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))` |
| delete_calendar | str | 88 | `str(e)` |
| delete_calendar | HTTPException | 91 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| delete_calendar | MessageResponse | 95 | `MessageResponse(message=..., success=True)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `delete_calendar` | `service.delete` | 84 |
| external_call | `delete_calendar` | `HTTPException` | 86 |
| external_call | `delete_calendar` | `HTTPException` | 91 |

## Behavior

This flow starts at `delete_calendar` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
