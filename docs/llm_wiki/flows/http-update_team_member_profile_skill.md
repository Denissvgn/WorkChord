# update_team_member_profile_skill

**Entry point:** `update_team_member_profile_skill` (`http`)
**Source:** [routers_team](../modules/routers_team.md)
**Modules touched:** [routers_team](../modules/routers_team.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_team_member_profile_skill
    participant p1 as service.update_profile_skill
    participant p2 as HTTPException
    p0-->>p1: service.update_profile_skill
    p0-->>p2: HTTPException
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. update_team_member_profile_skill"]
    s2["2. service.update_profile_skill"]
    s3["3. HTTPException"]
    s1 -. "service.update_profile_skill(profile_id, skill_id, data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)" .-> s3
    click s1 "../modules/routers_team.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `update_team_member_profile_skill` | `profile_id: int`, `skill_id: int`, `data: TeamMemberProfileSkillUpdate`, `service: Annotated[TeamService, Depends(get_team_service)]` | `status` | - | `skill` |
| `service.update_profile_skill` | - | - | - | - |
| `HTTPException` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| update_team_member_profile_skill | service.update_profile_skill | 155 | `service.update_profile_skill(profile_id, skill_id, data)` |
| update_team_member_profile_skill | HTTPException | 157 | `HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `update_team_member_profile_skill` | `service.update_profile_skill` | 155 |
| external_call | `update_team_member_profile_skill` | `HTTPException` | 157 |

## Behavior

This flow starts at `update_team_member_profile_skill` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
