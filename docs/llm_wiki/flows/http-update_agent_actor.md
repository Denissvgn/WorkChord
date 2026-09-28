# update_agent_actor

**Entry point:** `update_agent_actor` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [routers_agent](../modules/routers_agent.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_agent_actor
    participant p1 as require_scope
    participant p2 as actor_has_scope
    participant p3 as actor_scopes
    participant p4 as json.loads
    participant p5 as isinstance (backend/app/services/agent_service.py:actor_scopes)
    participant p6 as AgentPermissionError
    participant p7 as service.db.get
    participant p8 as ValueError
    participant p9 as getattr
    participant p10 as json.dumps
    participant p11 as setattr
    participant p12 as service.db.commit
    participant p13 as service.db.refresh
    participant p14 as service.actor_response
    participant p15 as _handle_agent_error
    participant p16 as isinstance (backend/app/routers/agent.py:_handle_agent_error)
    participant p17 as str
    participant p18 as HTTPException
    participant p19 as exc.detail
    p0->>p1: require_scope
    p1->>p2: actor_has_scope
    p2->>p3: actor_scopes
    p3-->>p4: json.loads
    p3-->>p5: isinstance (backend/app/services/agent_service.py:actor_scopes)
    p1->>p6: AgentPermissionError
    p0-->>p7: service.db.get
    p0-->>p8: ValueError
    p0-->>p7: service.db.get
    p0-->>p8: ValueError
    p0-->>p9: getattr
    p0-->>p10: json.dumps
    p0-->>p9: getattr
    p0-->>p11: setattr
    p0-->>p12: service.db.commit
    p0-->>p13: service.db.refresh
    p0-->>p14: service.actor_response
    p0->>p15: _handle_agent_error
    p15-->>p16: isinstance (backend/app/routers/agent.py:_handle_agent_error)
    p15-->>p17: str
    p15-->>p17: str
    p15-->>p18: HTTPException
    p15-->>p16: isinstance (backend/app/routers/agent.py:_handle_agent_error)
    p15-->>p18: HTTPException
    p15-->>p19: exc.detail
    p15-->>p16: isinstance (backend/app/routers/agent.py:_handle_agent_error)
    p15-->>p18: HTTPException
    p15-->>p19: exc.detail
    p15-->>p16: isinstance (backend/app/routers/agent.py:_handle_agent_error)
    p15-->>p18: HTTPException
```

> Call sequence diagram shows 30 of 43 interactions; 13 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. update_agent_actor"]
    s2["2. require_scope"]
    s3["3. actor_has_scope"]
    s4["4. actor_scopes"]
    s5["5. json.loads"]
    s6["6. isinstance (backend/app/services/agent_service.py:actor_scopes)"]
    s7["7. AgentPermissionError"]
    s8["8. service.db.get"]
    s9["9. ValueError"]
    s10["10. service.db.get"]
    s11["11. ValueError"]
    s12["12. getattr"]
    s1 -->|"require_scope(actor, 'admin')"| s2
    s2 -->|"actor_has_scope(actor, scope)"| s3
    s3 -->|"actor_scopes(actor)"| s4
    s4 -. "json.loads(actor.scopes)" .-> s5
    s4 -. "isinstance (backend/app/services/agent_service.py:actor_scopes)(scopes, list)" .-> s6
    s2 -->|"AgentPermissionError(...)"| s7
    s1 -. "service.db.get(AgentActor, actor_id)" .-> s8
    s1 -. "ValueError('Agent actor not found')" .-> s9
    s1 -. "service.db.get(TeamMemberProfile, data.profile_id)" .-> s10
    s1 -. "ValueError('Team member profile not found')" .-> s11
    s1 -. "getattr(data, field_name)" .-> s12
    click s1 "../modules/routers_agent.md"
    click s2 "../modules/agent_service.md"
    click s3 "../modules/agent_service.md"
    click s4 "../modules/agent_service.md"
    click s7 "../modules/agent_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `update_agent_actor` | `actor_id: int`, `data: AgentActorUpdate`, `actor: Annotated[AgentActor, Depends(get_agent_admin_actor)]`, `service: Annotated[AgentWorkService, Depends(get_agent_work_service)]` | `AgentActor`, `TeamMemberProfile` | `target.lifecycle_state`, `target.queue_revision` | `service.actor_response(...)` |
| `require_scope` | `actor: AgentActor`, `scope: str` | - | - | - |
| `actor_has_scope` | `actor: AgentActor`, `scope: str` | - | - | `...` |
| `actor_scopes` | `actor: AgentActor` | `json` | - | `...` |
| `json.loads` | - | - | - | - |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | - | - | - | - |
| `AgentPermissionError` | - | - | - | - |
| `service.db.get` | - | - | - | - |
| `ValueError` | - | - | - | - |
| `service.db.get` | - | - | - | - |
| `ValueError` | - | - | - | - |
| `getattr` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| update_agent_actor | require_scope | 607 | `require_scope(actor, 'admin')` |
| require_scope | actor_has_scope | 86 | `actor_has_scope(actor, scope)` |
| actor_has_scope | actor_scopes | 80 | `actor_scopes(actor)` |
| actor_scopes | json.loads | 72 | `json.loads(actor.scopes)` |
| actor_scopes | isinstance (backend/app/services/agent_service.py:actor_scopes) | 75 | `isinstance(scopes, list)` |
| require_scope | AgentPermissionError | 87 | `AgentPermissionError(...)` |
| update_agent_actor | service.db.get | 608 | `service.db.get(AgentActor, actor_id)` |
| update_agent_actor | ValueError | 610 | `ValueError('Agent actor not found')` |
| update_agent_actor | service.db.get | 612 | `service.db.get(TeamMemberProfile, data.profile_id)` |
| update_agent_actor | ValueError | 614 | `ValueError('Team member profile not found')` |
| update_agent_actor | getattr | 626 | `getattr(data, field_name)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `actor_scopes` | `json.loads` | 72 |
| external_call | `actor_scopes` | `isinstance` | 75 |
| unresolved_call | `update_agent_actor` | `service.db.get` | 608 |
| external_call | `update_agent_actor` | `ValueError` | 610 |
| unresolved_call | `update_agent_actor` | `service.db.get` | 612 |
| external_call | `update_agent_actor` | `ValueError` | 614 |
| external_call | `update_agent_actor` | `getattr` | 626 |
| step_limit | `update_agent_actor` | `first 12 steps` | 0 |

## Behavior

This flow starts at `update_agent_actor` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
