# import_team_members

**Entry point:** `import_team_members` (`http`)
**Source:** [routers_team](../modules/routers_team.md)
**Modules touched:** [routers_team](../modules/routers_team.md), [schemas_team](../modules/schemas_team.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as import_team_members
    participant p1 as service.import_members
    participant p2 as service.get_by_id
    participant p3 as full_members.append
    participant p4 as TeamImportResponse
    participant p5 as len
    participant p6 as HTTPException
    participant p7 as str
    p0-->>p1: service.import_members
    p0-->>p2: service.get_by_id
    p0-->>p3: full_members.append
    p0->>p4: TeamImportResponse
    p0-->>p5: len
    p0-->>p6: HTTPException
    p0-->>p7: str
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. import_team_members"]
    s2["2. service.import_members"]
    s3["3. service.get_by_id"]
    s4["4. full_members.append"]
    s5["5. TeamImportResponse"]
    s6["6. len"]
    s7["7. HTTPException"]
    s8["8. str"]
    s1 -. "service.import_members(iteration_id, data.text)" .-> s2
    s1 -. "service.get_by_id(member.id)" .-> s3
    s1 -. "full_members.append(full_member)" .-> s4
    s1 -->|"TeamImportResponse(imported_count=len(...), members=full_members)"| s5
    s1 -. "len(full_members)" .-> s6
    s1 -. "HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))" .-> s7
    s1 -. "str(e)" .-> s8
    b0["mutation full_members.append"]
    s1 -. "mutation full_members.append" .-> b0
    click s1 "../modules/routers_team.md"
    click s5 "../modules/schemas_team.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `import_team_members` | `iteration_id: int`, `data: TeamImportRequest`, `service: Annotated[TeamService, Depends(get_team_service)]` | `status` | - | `TeamImportResponse(...)` |
| `service.import_members` | - | - | - | - |
| `service.get_by_id` | - | - | - | - |
| `full_members.append` | - | - | - | - |
| `TeamImportResponse` | - | - | - | - |
| `len` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| import_team_members | service.import_members | 370 | `service.import_members(iteration_id, data.text)` |
| import_team_members | service.get_by_id | 374 | `service.get_by_id(member.id)` |
| import_team_members | full_members.append | 375 | `full_members.append(full_member)` |
| import_team_members | TeamImportResponse | 377 | `TeamImportResponse(imported_count=len(...), members=full_members)` |
| import_team_members | len | 378 | `len(full_members)` |
| import_team_members | HTTPException | 382 | `HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))` |
| import_team_members | str | 384 | `str(e)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `full_members.append` | `import_team_members` | 375 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `import_team_members` | `service.import_members` | 370 |
| unresolved_call | `import_team_members` | `service.get_by_id` | 374 |
| external_call | `import_team_members` | `HTTPException` | 382 |

## Behavior

This flow starts at `import_team_members` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
