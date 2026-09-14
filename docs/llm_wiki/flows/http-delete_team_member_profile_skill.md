# delete_team_member_profile_skill

**Entry point:** `delete_team_member_profile_skill` (`http`)
**Source:** [routers_team](../modules/routers_team.md)
**Modules touched:** [routers_team](../modules/routers_team.md), [schemas_common](../modules/schemas_common.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as delete_team_member_profile_skill
    participant p1 as service.delete_profile_skill
    participant p2 as HTTPException
    participant p3 as MessageResponse
    p0-->>p1: service.delete_profile_skill
    p0-->>p2: HTTPException
    p0->>p3: MessageResponse
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. delete_team_member_profile_skill"]
    s2["2. service.delete_profile_skill"]
    s3["3. HTTPException"]
    s4["4. MessageResponse"]
    s1 -. "service.delete_profile_skill(profile_id, skill_id)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    s1 -->|"MessageResponse(message=..., success=True)"| s4
    click s1 "../modules/routers_team.md"
    click s4 "../modules/schemas_common.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `delete_team_member_profile_skill` | `profile_id: int`, `skill_id: int`, `service: Annotated[TeamService, Depends(get_team_service)]` | `status` | - | `MessageResponse(...)` |
| `service.delete_profile_skill` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `MessageResponse` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| delete_team_member_profile_skill | service.delete_profile_skill | 174 | `service.delete_profile_skill(profile_id, skill_id)` |
| delete_team_member_profile_skill | HTTPException | 176 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |
| delete_team_member_profile_skill | MessageResponse | 180 | `MessageResponse(message=..., success=True)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `delete_team_member_profile_skill` | `service.delete_profile_skill` | 174 |
| external_call | `delete_team_member_profile_skill` | `HTTPException` | 176 |

## Behavior

This flow starts at `delete_team_member_profile_skill` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
