# export

**Entry point:** `export` (`http`)
**Source:** [time_entries](../modules/time_entries.md)
**Modules touched:** [routers_task_domain](../modules/routers_task_domain.md), [time_entries](../modules/time_entries.md), [time_report_service](../modules/time_report_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as export
    participant p1 as domain_result
    participant p2 as HTTPException
    participant p3 as exc.detail
    participant p4 as str
    participant p5 as TimeReportService(…).export
    participant p6 as TimeReportService
    participant p7 as Response
    p0->>p1: domain_result
    p1-->>p2: HTTPException
    p1-->>p3: exc.detail
    p1-->>p2: HTTPException
    p1-->>p4: str
    p1-->>p2: HTTPException
    p1-->>p4: str
    p1-->>p2: HTTPException
    p0-->>p5: TimeReportService(…).export
    p0->>p6: TimeReportService
    p0-->>p7: Response
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. export"]
    s2["2. domain_result"]
    s3["3. HTTPException"]
    s4["4. exc.detail"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. HTTPException"]
    s8["8. str"]
    s9["9. HTTPException"]
    s10["10. TimeReportService(…).export"]
    s11["11. TimeReportService"]
    s12["12. Response"]
    s1 -->|"domain_result(...)"| s2
    s2 -. "HTTPException(409, detail=exc.detail(...))" .-> s3
    s2 -. "exc.detail(data not statically known)" .-> s4
    s2 -. "HTTPException(404, detail=str(...))" .-> s5
    s2 -. "str(exc)" .-> s6
    s2 -. "HTTPException(422, detail=[...])" .-> s7
    s2 -. "str(exc)" .-> s8
    s2 -. "HTTPException(404, detail='Task not found or inaccessible')" .-> s9
    s1 -. "TimeReportService(…).export(project_id, start, end, scope=scope, kind=kind)" .-> s10
    s1 -->|"TimeReportService(db)"| s11
    s1 -. "Response(content=content, media_type='text/csv', headers={...})" .-> s12
    click s1 "../modules/time_entries.md"
    click s2 "../modules/routers_task_domain.md"
    click s11 "../modules/time_report_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `export` | `db: DB`, `project_id: int`, `start: date`, `end: date`, `scope: Literal['mine', 'project']`, `kind: Literal['totals', 'entries']` | - | - | `Response(...)` |
| `domain_result` | `awaitable` | `TaskVersionConflictError` | - | `result` |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `TimeReportService(…).export` | - | - | - | - |
| `TimeReportService` | - | - | - | - |
| `Response` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| export | domain_result | 60 | `domain_result(...)` |
| domain_result | HTTPException | 51 | `HTTPException(409, detail=exc.detail(...))` |
| domain_result | exc.detail | 51 | `exc.detail(data not statically known)` |
| domain_result | HTTPException | 53 | `HTTPException(404, detail=str(...))` |
| domain_result | str | 53 | `str(exc)` |
| domain_result | HTTPException | 55 | `HTTPException(422, detail=[...])` |
| domain_result | str | 55 | `str(exc)` |
| domain_result | HTTPException | 57 | `HTTPException(404, detail='Task not found or inaccessible')` |
| export | TimeReportService(…).export | 60 | `TimeReportService(db).export(project_id, start, end, scope=scope, kind=kind)` |
| export | TimeReportService | 60 | `TimeReportService(db)` |
| export | Response | 61 | `Response(content=content, media_type='text/csv', headers={...})` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `domain_result` | `HTTPException` | 51 |
| unresolved_call | `domain_result` | `exc.detail` | 51 |
| external_call | `domain_result` | `HTTPException` | 53 |
| external_call | `domain_result` | `HTTPException` | 55 |
| external_call | `domain_result` | `HTTPException` | 57 |
| unresolved_call | `export` | `TimeReportService(db).export` | 60 |
| external_call | `export` | `Response` | 61 |

## Behavior

This flow starts at `export` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
