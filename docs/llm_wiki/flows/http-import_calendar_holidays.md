# import_calendar_holidays

**Entry point:** `import_calendar_holidays` (`http`)
**Source:** [calendars](../modules/calendars.md)
**Modules touched:** [calendars](../modules/calendars.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as import_calendar_holidays
    participant p1 as service.import_holidays
    participant p2 as HTTPException
    participant p3 as str
    p0-->>p1: service.import_holidays
    p0-->>p2: HTTPException
    p0-->>p3: str
    p0-->>p2: HTTPException
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. import_calendar_holidays"]
    s2["2. service.import_holidays"]
    s3["3. HTTPException"]
    s4["4. str"]
    s5["5. HTTPException"]
    s1 -. "service.import_holidays(calendar_id, data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s5
    click s1 "../modules/calendars.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `import_calendar_holidays` | `calendar_id: int`, `data: CalendarImportRequest`, `service: Annotated[CalendarService, Depends(get_calendar_service)]` | `status`, `status` | - | `result` |
| `service.import_holidays` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| import_calendar_holidays | service.import_holidays | 106 | `service.import_holidays(calendar_id, data)` |
| import_calendar_holidays | HTTPException | 108 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| import_calendar_holidays | str | 110 | `str(e)` |
| import_calendar_holidays | HTTPException | 113 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `import_calendar_holidays` | `service.import_holidays` | 106 |
| external_call | `import_calendar_holidays` | `HTTPException` | 108 |
| external_call | `import_calendar_holidays` | `HTTPException` | 113 |

## Behavior

This flow starts at `import_calendar_holidays` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
