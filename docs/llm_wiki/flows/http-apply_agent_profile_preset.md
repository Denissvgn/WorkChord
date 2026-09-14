# apply_agent_profile_preset

**Entry point:** `apply_agent_profile_preset` (`http`)
**Source:** [agent_catalog](../modules/agent_catalog.md)
**Modules touched:** [agent_catalog](../modules/agent_catalog.md), [agent_planning_service](../modules/agent_planning_service.md), [routers_agent_planning](../modules/routers_agent_planning.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as apply_agent_profile_preset
    participant p1 as AgentPlanningService(…).apply_profile_preset
    participant p2 as AgentPlanningService
    participant p3 as TeamMemberProfileResponse.model_validate
    participant p4 as _handle_agent_error
    participant p5 as isinstance
    participant p6 as HTTPException
    participant p7 as str
    participant p8 as exc.detail
    p0-->>p1: AgentPlanningService(…).apply_profile_preset
    p0->>p2: AgentPlanningService
    p0-->>p3: TeamMemberProfileResponse.model_validate
    p0->>p4: _handle_agent_error
    p4-->>p5: isinstance
    p4-->>p6: HTTPException
    p4-->>p7: str
    p4-->>p5: isinstance
    p4-->>p6: HTTPException
    p4-->>p8: exc.detail
    p4-->>p5: isinstance
    p4-->>p6: HTTPException
    p4-->>p8: exc.detail
    p4-->>p5: isinstance
    p4-->>p6: HTTPException
    p4-->>p7: str
    p4-->>p5: isinstance
    p4-->>p6: HTTPException
    p4-->>p7: str
    p4-->>p5: isinstance
    p4-->>p6: HTTPException
    p4-->>p7: str
    p4-->>p5: isinstance
    p4-->>p6: HTTPException
    p4-->>p7: str
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. apply_agent_profile_preset"]
    s2["2. AgentPlanningService(…).apply_profile_preset"]
    s3["3. AgentPlanningService"]
    s4["4. TeamMemberProfileResponse.model_validate"]
    s5["5. _handle_agent_error"]
    s6["6. isinstance"]
    s7["7. HTTPException"]
    s8["8. str"]
    s9["9. isinstance"]
    s10["10. HTTPException"]
    s11["11. exc.detail"]
    s12["12. isinstance"]
    s1 -. "AgentPlanningService(…).apply_profile_preset(preset_key, actor, command=command)" .-> s2
    s1 -->|"AgentPlanningService(db)"| s3
    s1 -. "TeamMemberProfileResponse.model_validate(receipt.result)" .-> s4
    s1 -->|"_handle_agent_error(exc)"| s5
    s5 -. "isinstance(exc, AgentPermissionError)" .-> s6
    s5 -. "HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(...))" .-> s7
    s5 -. "str(exc)" .-> s8
    s5 -. "isinstance(exc, AgentRoutingConflictError)" .-> s9
    s5 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s10
    s5 -. "exc.detail(data not statically known)" .-> s11
    s5 -. "isinstance(exc, TaskVersionConflictError)" .-> s12
    click s1 "../modules/agent_catalog.md"
    click s3 "../modules/agent_planning_service.md"
    click s5 "../modules/routers_agent_planning.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `apply_agent_profile_preset` | `preset_key: str`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `db: Annotated[AsyncSession, Depends(get_db)]`, `command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)]` | - | - | `TeamMemberProfileResponse.model_validate(...)` |
| `AgentPlanningService(…).apply_profile_preset` | - | - | - | - |
| `AgentPlanningService` | - | - | - | - |
| `TeamMemberProfileResponse.model_validate` | - | - | - | - |
| `_handle_agent_error` | `exc: Exception` | `AgentPermissionError`, `status`, `AgentRoutingConflictError`, `status`, `TaskVersionConflictError`, `status`, `AgentConflictError`, `status` | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `isinstance` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| apply_agent_profile_preset | AgentPlanningService(…).apply_profile_preset | 124 | `AgentPlanningService(db).apply_profile_preset(preset_key, actor, command=command)` |
| apply_agent_profile_preset | AgentPlanningService | 124 | `AgentPlanningService(db)` |
| apply_agent_profile_preset | TeamMemberProfileResponse.model_validate | 129 | `TeamMemberProfileResponse.model_validate(receipt.result)` |
| apply_agent_profile_preset | _handle_agent_error | 131 | `_handle_agent_error(exc)` |
| _handle_agent_error | isinstance | 102 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | HTTPException | 103 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(...))` |
| _handle_agent_error | str | 103 | `str(exc)` |
| _handle_agent_error | isinstance | 104 | `isinstance(exc, AgentRoutingConflictError)` |
| _handle_agent_error | HTTPException | 105 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 105 | `exc.detail(data not statically known)` |
| _handle_agent_error | isinstance | 106 | `isinstance(exc, TaskVersionConflictError)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `apply_agent_profile_preset` | `AgentPlanningService(db).apply_profile_preset` | 124 |
| unresolved_call | `apply_agent_profile_preset` | `TeamMemberProfileResponse.model_validate` | 129 |
| external_call | `_handle_agent_error` | `isinstance` | 102 |
| external_call | `_handle_agent_error` | `HTTPException` | 103 |
| external_call | `_handle_agent_error` | `isinstance` | 104 |
| external_call | `_handle_agent_error` | `HTTPException` | 105 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 105 |
| external_call | `_handle_agent_error` | `isinstance` | 106 |
| step_limit | `apply_agent_profile_preset` | `first 12 steps` | 0 |

## Behavior

This flow starts at `apply_agent_profile_preset` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
