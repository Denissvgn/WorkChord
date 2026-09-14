# create_agent_actor

**Entry point:** `create_agent_actor` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [routers_agent](../modules/routers_agent.md), [schemas_agent](../modules/schemas_agent.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_agent_actor
    participant p1 as require_scope
    participant p2 as actor_has_scope
    participant p3 as actor_scopes
    participant p4 as json.loads
    participant p5 as isinstance (backend/app/services/agent_service.py:actor_scopes)
    participant p6 as AgentPermissionError
    participant p7 as service.create_actor
    participant p8 as _handle_agent_error
    participant p9 as isinstance (backend/app/routers/agent.py:_handle_agent_error)
    participant p10 as str
    participant p11 as HTTPException
    participant p12 as exc.detail
    p0->>p1: require_scope
    p1->>p2: actor_has_scope
    p2->>p3: actor_scopes
    p3-->>p4: json.loads
    p3-->>p5: isinstance (backend/app/services/agent_service.py:actor_scopes)
    p1->>p6: AgentPermissionError
    p0-->>p7: service.create_actor
    p0->>p8: _handle_agent_error
    p8-->>p9: isinstance (backend/app/routers/agent.py:_handle_agent_error)
    p8-->>p10: str
    p8-->>p10: str
    p8-->>p11: HTTPException
    p8-->>p9: isinstance (backend/app/routers/agent.py:_handle_agent_error)
    p8-->>p11: HTTPException
    p8-->>p12: exc.detail
    p8-->>p9: isinstance (backend/app/routers/agent.py:_handle_agent_error)
    p8-->>p11: HTTPException
    p8-->>p12: exc.detail
    p8-->>p9: isinstance (backend/app/routers/agent.py:_handle_agent_error)
    p8-->>p11: HTTPException
    p8-->>p12: exc.detail
    p8-->>p9: isinstance (backend/app/routers/agent.py:_handle_agent_error)
    p8-->>p10: str
    p8-->>p10: str
    p8-->>p11: HTTPException
    p8-->>p9: isinstance (backend/app/routers/agent.py:_handle_agent_error)
    p8-->>p10: str
    p8-->>p10: str
    p8-->>p11: HTTPException
    p8-->>p9: isinstance (backend/app/routers/agent.py:_handle_agent_error)
```

> Call sequence diagram shows 30 of 38 interactions; 8 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. create_agent_actor"]
    s2["2. require_scope"]
    s3["3. actor_has_scope"]
    s4["4. actor_scopes"]
    s5["5. json.loads"]
    s6["6. isinstance (backend/app/services/agent_service.py:actor_scopes)"]
    s7["7. AgentPermissionError"]
    s8["8. service.create_actor"]
    s9["9. _handle_agent_error"]
    s10["10. isinstance (backend/app/routers/agent.py:_handle_agent_error)"]
    s11["11. str"]
    s12["12. str"]
    s1 -->|"require_scope(actor, 'admin')"| s2
    s2 -->|"actor_has_scope(actor, scope)"| s3
    s3 -->|"actor_scopes(actor)"| s4
    s4 -. "json.loads(actor.scopes)" .-> s5
    s4 -. "isinstance (backend/app/services/agent_service.py:actor_scopes)(scopes, list)" .-> s6
    s2 -->|"AgentPermissionError(...)"| s7
    s1 -. "service.create_actor(data, principal=actor)" .-> s8
    s1 -->|"_handle_agent_error(exc)"| s9
    s9 -. "isinstance (backend/app/routers/agent.py:_handle_agent_error)(exc, AgentPermissionError)" .-> s10
    s9 -. "str(exc)" .-> s11
    s9 -. "str(exc)" .-> s12
    click s1 "../modules/routers_agent.md"
    click s2 "../modules/agent_service.md"
    click s3 "../modules/agent_service.md"
    click s4 "../modules/agent_service.md"
    click s7 "../modules/agent_service.md"
    click s9 "../modules/routers_agent.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_agent_actor` | `data: AgentActorCreate`, `response: Response`, `actor: Annotated[AgentActor, Depends(get_agent_admin_actor)]`, `service: Annotated[AgentService, Depends(get_agent_service)]` | - | `response.headers[...]`, `response.headers[...]`, `response.headers[...]` | `AgentActorCreatedResponse(...)` |
| `require_scope` | `actor: AgentActor`, `scope: str` | - | - | - |
| `actor_has_scope` | `actor: AgentActor`, `scope: str` | - | - | `...` |
| `actor_scopes` | `actor: AgentActor` | `json` | - | `...` |
| `json.loads` | - | - | - | - |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | - | - | - | - |
| `AgentPermissionError` | - | - | - | - |
| `service.create_actor` | - | - | - | - |
| `_handle_agent_error` | `exc: Exception`, `structured: bool` | `AgentPermissionError`, `status`, `AgentRoutingConflictError`, `status`, `AgentTeamSetupConflictError`, `status`, `TaskVersionConflictError`, `status` | - | - |
| `isinstance (backend/app/routers/agent.py:_handle_agent_error)` | - | - | - | - |
| `str` | - | - | - | - |
| `str` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_agent_actor | require_scope | 546 | `require_scope(actor, 'admin')` |
| require_scope | actor_has_scope | 84 | `actor_has_scope(actor, scope)` |
| actor_has_scope | actor_scopes | 78 | `actor_scopes(actor)` |
| actor_scopes | json.loads | 70 | `json.loads(actor.scopes)` |
| actor_scopes | isinstance (backend/app/services/agent_service.py:actor_scopes) | 73 | `isinstance(scopes, list)` |
| require_scope | AgentPermissionError | 85 | `AgentPermissionError(...)` |
| create_agent_actor | service.create_actor | 547 | `service.create_actor(data, principal=actor)` |
| create_agent_actor | _handle_agent_error | 552 | `_handle_agent_error(exc)` |
| _handle_agent_error | isinstance (backend/app/routers/agent.py:_handle_agent_error) | 244 | `isinstance(exc, AgentPermissionError)` |
| _handle_agent_error | str | 246 | `str(exc)` |
| _handle_agent_error | str | 248 | `str(exc)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `actor_scopes` | `json.loads` | 70 |
| external_call | `actor_scopes` | `isinstance` | 73 |
| unresolved_call | `create_agent_actor` | `service.create_actor` | 547 |
| external_call | `_handle_agent_error` | `isinstance` | 244 |
| step_limit | `create_agent_actor` | `first 12 steps` | 0 |

## Behavior

This flow starts at `create_agent_actor` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
