# apply_agent_team_reconciliation

**Entry point:** `apply_agent_team_reconciliation` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [routers_agent](../modules/routers_agent.md), [schemas_agent_planning](../modules/schemas_agent_planning.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as apply_agent_team_reconciliation
    participant p1 as AgentPlanningCommandContext
    participant p2 as service.apply
    participant p3 as _handle_agent_error
    participant p4 as isinstance
    participant p5 as str
    participant p6 as HTTPException
    participant p7 as exc.detail
    p0->>p1: AgentPlanningCommandContext
    p0-->>p2: service.apply
    p0->>p3: _handle_agent_error
    p3-->>p4: isinstance
    p3-->>p5: str
    p3-->>p5: str
    p3-->>p6: HTTPException
    p3-->>p4: isinstance
    p3-->>p6: HTTPException
    p3-->>p7: exc.detail
    p3-->>p4: isinstance
    p3-->>p6: HTTPException
    p3-->>p7: exc.detail
    p3-->>p4: isinstance
    p3-->>p6: HTTPException
    p3-->>p7: exc.detail
    p3-->>p4: isinstance
    p3-->>p5: str
    p3-->>p5: str
    p3-->>p6: HTTPException
    p3-->>p4: isinstance
    p3-->>p5: str
    p3-->>p5: str
    p3-->>p6: HTTPException
    p3-->>p4: isinstance
    p3-->>p5: str
    p3-->>p5: str
    p3-->>p6: HTTPException
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. apply_agent_team_reconciliation"]
    s2["2. AgentPlanningCommandContext"]
    s3["3. service.apply"]
    s4["4. _handle_agent_error"]
    s5["5. isinstance"]
    s6["6. str"]
    s7["7. str"]
    s8["8. HTTPException"]
    s9["9. isinstance"]
    s10["10. HTTPException"]
    s11["11. exc.detail"]
    s12["12. isinstance"]
    s1 -->|"AgentPlanningCommandContext(idempotency_key=idempotency_key, rationale=rationale, correlation_id=correlation_id)"| s2
    s1 -. "service.apply(actor, data, command=command)" .-> s3
    s1 -->|"_handle_agent_error(exc, structured=True)"| s4
    s4 -. "isinstance(exc, AgentPermissionError)" .-> s5
    s4 -. "str(exc)" .-> s6
    s4 -. "str(exc)" .-> s7
    s4 -. "HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)" .-> s8
    s4 -. "isinstance(exc, AgentRoutingConflictError)" .-> s9
    s4 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))" .-> s10
    s4 -. "exc.detail(data not statically known)" .-> s11
    s4 -. "isinstance(exc, AgentTeamSetupConflictError)" .-> s12
    click s1 "../modules/routers_agent.md"
    click s2 "../modules/schemas_agent_planning.md"
    click s4 "../modules/routers_agent.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `apply_agent_team_reconciliation` | `data: AgentTeamApplyRequest`, `response: Response`, `actor: Annotated[AgentActor, Depends(get_agent_admin_actor)]`, `service: Annotated[AgentTeamSetupService, Depends(get_agent_team_setup_service)]`, `idempotency_key: Annotated[str, Header(alias='Idempotency-Key')]`, `rationale: Annotated[str, Header(alias='X-Agent-Rationale')]`, `correlation_id: Annotated[str, Header(alias='X-Correlation-ID')]` | - | `response.headers[...]`, `response.headers[...]` | `result` |
| `AgentPlanningCommandContext` | - | - | - | - |
| `service.apply` | - | - | - | - |
| `_handle_agent_error` | `exc: Exception`, `structured: bool` | `AgentPermissionError`, `status`, `AgentRoutingConflictError`, `status`, `AgentTeamSetupConflictError`, `status`, `TaskVersionConflictError`, `status` | - | - |
| `isinstance` | - | - | - | - |
| `str` | - | - | - | - |
| `str` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `exc.detail` | - | - | - | - |
| `isinstance` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| apply_agent_team_reconciliation | AgentPlanningCommandContext | 461 | `AgentPlanningCommandContext(idempotency_key=idempotency_key, rationale=rationale, correlation_id=correlation_id)` |
| apply_agent_team_reconciliation | service.apply | 466 | `service.apply(actor, data, command=command)` |
| apply_agent_team_reconciliation | _handle_agent_error | 468 | `_handle_agent_error(exc, structured=True)` |
| _handle_agent_error | isinstance | 254 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | str | 256 | `str(exc)` |
| _handle_agent_error | str | 258 | `str(exc)` |
| _handle_agent_error | HTTPException | 260 | `HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)` |
| _handle_agent_error | isinstance | 261 | `isinstance(exc, AgentRoutingConflictError)` |
| _handle_agent_error | HTTPException | 262 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))` |
| _handle_agent_error | exc.detail | 262 | `exc.detail(data not statically known)` |
| _handle_agent_error | isinstance | 263 | `isinstance(exc, AgentTeamSetupConflictError)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `apply_agent_team_reconciliation` | `service.apply` | 466 |
| external_call | `_handle_agent_error` | `isinstance` | 254 |
| external_call | `_handle_agent_error` | `HTTPException` | 260 |
| external_call | `_handle_agent_error` | `isinstance` | 261 |
| external_call | `_handle_agent_error` | `HTTPException` | 262 |
| unresolved_call | `_handle_agent_error` | `exc.detail` | 262 |
| external_call | `_handle_agent_error` | `isinstance` | 263 |
| step_limit | `apply_agent_team_reconciliation` | `first 12 steps` | 0 |

## Behavior

This flow starts at `apply_agent_team_reconciliation` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
