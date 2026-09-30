# update_project_milestone

**Entry point:** `update_project_milestone` (`http`)
**Source:** [routers_agent_planning](../modules/routers_agent_planning.md)
**Modules touched:** [routers_agent_planning](../modules/routers_agent_planning.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_project_milestone
    participant p1 as service.update_milestone
    participant p2 as _handle_agent_error
    participant p3 as isinstance
    participant p4 as HTTPException
    participant p5 as str
    participant p6 as exc.detail
    p0-->>p1: service.update_milestone
    p0->>p2: _handle_agent_error
    p2-->>p3: isinstance
    p2-->>p4: HTTPException
    p2-->>p5: str
    p2-->>p3: isinstance
    p2-->>p4: HTTPException
    p2-->>p6: exc.detail
    p2-->>p3: isinstance
    p2-->>p4: HTTPException
    p2-->>p6: exc.detail
    p2-->>p3: isinstance
    p2-->>p4: HTTPException
    p2-->>p5: str
    p2-->>p3: isinstance
    p2-->>p4: HTTPException
    p2-->>p5: str
    p2-->>p3: isinstance
    p2-->>p4: HTTPException
    p2-->>p5: str
    p2-->>p3: isinstance
    p2-->>p4: HTTPException
    p2-->>p5: str
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. update_project_milestone"]
    s2["2. service.update_milestone"]
    s3["3. _handle_agent_error"]
    s4["4. isinstance"]
    s5["5. HTTPException"]
    s6["6. str"]
    s7["7. isinstance"]
    s8["8. HTTPException"]
    s9["9. exc.detail"]
    s10["10. isinstance"]
    s11["11. HTTPException"]
    s12["12. exc.detail"]
    s1 -. "service.update_milestone(project_id, milestone_id, actor, data, command=command)" .-> s2
    s1 -->|"_handle_agent_error(exc)"| s3
    s3 -. "isinstance(exc, AgentPermissionError)" .-> s4
    s3 -. "HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(...))" .-> s5
    s3 -. "str(exc)" .-> s6
    s3 -. "isinstance(exc, AgentRoutingConflictError)" .-> s7
    s3 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s8
    s3 -. "exc.detail(data not statically known)" .-> s9
    s3 -. "isinstance(exc, TaskVersionConflictError)" .-> s10
    s3 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s11
    s3 -. "exc.detail(data not statically known)" .-> s12
    click s1 "../modules/routers_agent_planning.md"
    click s3 "../modules/routers_agent_planning.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `update_project_milestone` | `project_id: int`, `milestone_id: int`, `data: ProjectMilestoneUpdate`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `service: Annotated[AgentPlanningService, Depends(get_agent_planning_service)]`, `command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)]` | - | - | `...` |
| `service.update_milestone` | - | - | - | - |
| `_handle_agent_error` | `exc: Exception` | `AgentPermissionError`, `status`, `AgentRoutingConflictError`, `status`, `TaskVersionConflictError`, `status`, `AgentConflictError`, `status` | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| update_project_milestone | service.update_milestone | 266 | `service.update_milestone(project_id, milestone_id, actor, data, command=command)` |
| update_project_milestone | _handle_agent_error | 274 | `_handle_agent_error(exc)` |
| _handle_agent_error | isinstance | 102 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | HTTPException | 103 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(...))` |
| _handle_agent_error | str | 103 | `str(exc)` |
| _handle_agent_error | isinstance | 104 | `isinstance(exc, AgentRoutingConflictError)` |
| _handle_agent_error | HTTPException | 105 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 105 | `exc.detail(data not statically known)` |
| _handle_agent_error | isinstance | 106 | `isinstance(exc, TaskVersionConflictError)` |
| _handle_agent_error | HTTPException | 107 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 107 | `exc.detail(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `update_project_milestone` | `service.update_milestone` | 266 |
| external_call | `_handle_agent_error` | `isinstance` | 102 |
| external_call | `_handle_agent_error` | `HTTPException` | 103 |
| external_call | `_handle_agent_error` | `isinstance` | 104 |
| external_call | `_handle_agent_error` | `HTTPException` | 105 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 105 |
| external_call | `_handle_agent_error` | `isinstance` | 106 |
| external_call | `_handle_agent_error` | `HTTPException` | 107 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 107 |
| step_limit | `update_project_milestone` | `first 12 steps` | 0 |

## Behavior

This flow starts at `update_project_milestone` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
