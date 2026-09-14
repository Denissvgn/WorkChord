# import_team_vacations

**Entry point:** `import_team_vacations` (`http`)
**Source:** [routers_team](../modules/routers_team.md)
**Modules touched:** [routers_team](../modules/routers_team.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as import_team_vacations
    participant p1 as service.import_vacations
    participant p2 as HTTPException
    participant p3 as str
    p0-->>p1: service.import_vacations
    p0-->>p2: HTTPException
    p0-->>p3: str
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. import_team_vacations"]
    s2["2. service.import_vacations"]
    s3["3. HTTPException"]
    s4["4. str"]
    s1 -. "service.import_vacations(iteration_id, data.csv_text)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s3
    s1 -. "str(e)" .-> s4
    click s1 "../modules/routers_team.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `import_team_vacations` | `iteration_id: int`, `data: VacationImportRequest`, `service: Annotated[TeamService, Depends(get_team_service)]` | `status` | - | `...` |
| `service.import_vacations` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| import_team_vacations | service.import_vacations | 350 | `service.import_vacations(iteration_id, data.csv_text)` |
| import_team_vacations | HTTPException | 352 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| import_team_vacations | str | 354 | `str(e)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `import_team_vacations` | `service.import_vacations` | 350 |
| external_call | `import_team_vacations` | `HTTPException` | 352 |

## Behavior

This flow starts at `import_team_vacations` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
