# update_agent_actor

**Entry point:** `update_agent_actor` (`http`)
**Source:** [routers_agent](../modules/routers_agent.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [routers_agent](../modules/routers_agent.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_agent_actor
    participant p1 as require_scope
    participant p2 as _handle_agent_error
    participant p3 as actor_has_scope
    participant p4 as AgentPermissionError
    participant p5 as actor_scopes
    participant p6 as ValueError
    participant p7 as service.db.get
    participant p8 as getattr
    participant p9 as json.dumps
    participant p10 as setattr
    participant p11 as service.db.commit
    participant p12 as service.db.refresh
    participant p13 as service.actor_response
    participant p14 as isinstance (backend/app/routers/agent.py:_handle_agent_error)
    participant p15 as str
    participant p16 as HTTPException
    participant p17 as exc.detail
    p0->>p1: require_scope
    p0->>p2: _handle_agent_error
    p1->>p3: actor_has_scope
    p1->>p4: AgentPermissionError
    p3->>p5: actor_scopes
    p0-->>p6: ValueError('Agent actor not found')
    p0-->>p7: service.db.get(AgentActor, actor_id)
    p0-->>p7: service.db.get(TeamMemberProfile, data.profile_id)
    p0-->>p6: ValueError('Team member profile not found')
    p0-->>p8: getattr(data, field_name)
    p0-->>p9: json.dumps(value)
    p0-->>p8: getattr(target, field_name)
    p0-->>p10: setattr(target, field_name, stored_value)
    p0-->>p11: service.db.commit
    p0-->>p12: service.db.refresh(target)
    p0-->>p13: service.actor_response(target)
    p2-->>p14: isinstance (backend/app/routers/agent.py:_handle_agent_error)(exc, AgentPermissionError)
    p2-->>p15: str(exc)
    p2-->>p15: str(exc)
    p2-->>p16: HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=detail)
    p2-->>p14: isinstance (backend/app/routers/agent.py:_handle_agent_error)(exc, AgentRoutingConflictError)
    p2-->>p16: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p17: exc.detail
    p2-->>p14: isinstance (backend/app/routers/agent.py:_handle_agent_error)(exc, AgentTeamSetupConflictError)
    p2-->>p16: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p17: exc.detail
    p2-->>p14: isinstance (backend/app/routers/agent.py:_handle_agent_error)(exc, TaskVersionConflictError)
    p2-->>p16: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p17: exc.detail
    p2-->>p14: isinstance (backend/app/routers/agent.py:_handle_agent_error)(exc, AgentConflictError)
```

> Call sequence diagram shows 30 of 43 interactions; 13 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 17 of 30 (13 omitted); unresolved 8 of 8 (0 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/agent_service.py:actor_scopes` | 4 | - | external | 2 |
| `backend/app/routers/agent.py:_handle_agent_error` | 19 | - | external | 11 |
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 6; effect analysis evaluated: 4, partial: 1, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 5 source steps with known totals: observed: 31, emitted: 27, omitted: 4. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `update_agent_actor` | `available` | `evaluated` | `available` | `9` | `9` | `0` |
| `require_scope` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `actor_has_scope` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `actor_scopes` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `json.loads` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AgentPermissionError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `service.db.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `ValueError` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `service.db.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `ValueError` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `getattr` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

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
| update_agent_actor | require_scope | 642 | `require_scope(actor, 'admin')` |
| require_scope | actor_has_scope | 100 | `actor_has_scope(actor, scope)` |
| actor_has_scope | actor_scopes | 94 | `actor_scopes(actor)` |
| actor_scopes | json.loads | 86 | `json.loads(actor.scopes)` |
| actor_scopes | isinstance (backend/app/services/agent_service.py:actor_scopes) | 89 | `isinstance(scopes, list)` |
| require_scope | AgentPermissionError | 101 | `AgentPermissionError(...)` |
| update_agent_actor | service.db.get | 643 | `service.db.get(AgentActor, actor_id)` |
| update_agent_actor | ValueError | 645 | `ValueError('Agent actor not found')` |
| update_agent_actor | service.db.get | 647 | `service.db.get(TeamMemberProfile, data.profile_id)` |
| update_agent_actor | ValueError | 649 | `ValueError('Team member profile not found')` |
| update_agent_actor | getattr | 661 | `getattr(data, field_name)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `actor_scopes` | `json.loads` | 86 |
| external_call | `actor_scopes` | `isinstance` | 89 |
| unresolved_call | `update_agent_actor` | `service.db.get` | 643 |
| external_call | `update_agent_actor` | `ValueError` | 645 |
| unresolved_call | `update_agent_actor` | `service.db.get` | 647 |
| external_call | `update_agent_actor` | `ValueError` | 649 |
| external_call | `update_agent_actor` | `getattr` | 661 |
| step_limit | `update_agent_actor` | `first 12 steps` | 0 |

## Behavior

This flow starts at `update_agent_actor` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
