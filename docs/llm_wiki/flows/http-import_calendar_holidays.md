# import_calendar_holidays

**Entry point:** `import_calendar_holidays` (`http`)
**Source:** [calendars](../modules/calendars.md)
**Modules touched:** [calendars](../modules/calendars.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as import_calendar_holidays
    participant p1 as service.import_holidays
    participant p2 as HTTPException
    participant p3 as str
    p0-->>p1: service.import_holidays(calendar_id, data)
    p0-->>p2: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))
    p0-->>p3: str(e)
    p0-->>p2: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)
```

> Call sequence diagram shows 4 of 4 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 3 of 3 (0 omitted); unresolved 1 of 1 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 1; effect analysis evaluated: 1, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 6, emitted: 6, omitted: 0. Unavailable totals are excluded.

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

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `import_calendar_holidays` | `service.import_holidays` | 106 |
| external_call | `import_calendar_holidays` | `HTTPException` | 108 |
| external_call | `import_calendar_holidays` | `HTTPException` | 113 |

## Behavior

This flow starts at `import_calendar_holidays` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
