# decline_planning_triage_item

**Entry point:** `decline_planning_triage_item` (`http`)
**Source:** [routers_agent_planning](../modules/routers_agent_planning.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [routers_agent_planning](../modules/routers_agent_planning.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as decline_planning_triage_item
    participant p1 as _run_triage_action
    participant p2 as _handle_agent_error
    participant p3 as require_scope
    participant p4 as actor_has_scope
    participant p5 as _require_triage_result
    participant p6 as AgentPermissionError
    participant p7 as actor_scopes
    participant p8 as isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)
    participant p9 as adapter
    participant p10 as HTTPException
    participant p11 as data.model_dump
    participant p12 as str
    participant p13 as exc.detail
    p0->>p1: _run_triage_action
    p0->>p2: _handle_agent_error
    p1->>p3: require_scope
    p3->>p4: actor_has_scope
    p1->>p5: _require_triage_result
    p3->>p6: AgentPermissionError
    p4->>p7: actor_scopes
    p2-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, AgentPermissionError)
    p1-->>p9: adapter(…)
    p2-->>p10: HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(...))
    p1-->>p11: data.model_dump(mode='json', exclude_unset=True)
    p2-->>p12: str(exc)
    p2-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, AgentRoutingConflictError)
    p2-->>p10: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p13: exc.detail
    p2-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, TaskVersionConflictError)
    p2-->>p10: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.detail(...))
    p2-->>p13: exc.detail
    p2-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, AgentConflictError)
    p2-->>p10: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))
    p2-->>p12: str(exc)
    p2-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, TriageConflictError)
    p2-->>p10: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))
    p2-->>p12: str(exc)
    p2-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, LookupError)
    p2-->>p10: HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(...))
    p2-->>p12: str(exc)
    p2-->>p8: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)(exc, ValueError)
    p2-->>p10: HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(...))
    p2-->>p12: str(exc)
```

> Call sequence diagram shows 30 of 33 interactions; 3 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 19 of 22 (3 omitted); unresolved 4 of 4 (0 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/agent_service.py:actor_scopes` | 5 | - | external | 2 |
| `backend/app/routers/agent_planning.py:_require_triage_result` | 11 | - | external | 1 |
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 8; effect analysis evaluated: 6, partial: 1, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 7 source steps with known totals: observed: 38, emitted: 34, omitted: 4. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `decline_planning_triage_item` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `_run_triage_action` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `require_scope` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `actor_has_scope` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `actor_scopes` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `json.loads` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AgentPermissionError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `adapter` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `data.model_dump` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_require_triage_result` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `LookupError` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. decline_planning_triage_item"]
    s2["2. _run_triage_action"]
    s3["3. require_scope"]
    s4["4. actor_has_scope"]
    s5["5. actor_scopes"]
    s6["6. json.loads"]
    s7["7. isinstance (backend/app/services/agent_service.py:actor_scopes)"]
    s8["8. AgentPermissionError"]
    s9["9. adapter"]
    s10["10. data.model_dump"]
    s11["11. _require_triage_result"]
    s12["12. LookupError"]
    s1 -->|"_run_triage_action(mcp_agent_tools.decline_triage_item, db=db, actor=actor, triage_item_id=triage_item_id, data=data, command=command)"| s2
    s2 -->|"require_scope(actor, 'planning:write')"| s3
    s3 -->|"actor_has_scope(actor, scope)"| s4
    s4 -->|"actor_scopes(actor)"| s5
    s5 -. "json.loads(actor.scopes)" .-> s6
    s5 -. "isinstance (backend/app/services/agent_service.py:actor_scopes)(scopes, list)" .-> s7
    s3 -->|"AgentPermissionError(...)"| s8
    s2 -. "adapter(…)" .-> s9
    s2 -. "data.model_dump(mode='json', exclude_unset=True)" .-> s10
    s2 -->|"_require_triage_result(result, triage_item_id)"| s11
    s11 -. "LookupError(...)" .-> s12
    click s1 "../modules/routers_agent_planning.md"
    click s2 "../modules/routers_agent_planning.md"
    click s3 "../modules/agent_service.md"
    click s4 "../modules/agent_service.md"
    click s5 "../modules/agent_service.md"
    click s8 "../modules/agent_service.md"
    click s11 "../modules/routers_agent_planning.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `decline_planning_triage_item` | `triage_item_id: int`, `data: TriageActionRequest`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)]` | `mcp_agent_tools` | - | `...` |
| `_run_triage_action` | `adapter`, `db: AsyncSession`, `actor: AgentActor`, `triage_item_id: int`, `data`, `command: AgentPlanningCommandContext` | - | - | `_require_triage_result(...)` |
| `require_scope` | `actor: AgentActor`, `scope: str` | - | - | - |
| `actor_has_scope` | `actor: AgentActor`, `scope: str` | - | - | `...` |
| `actor_scopes` | `actor: AgentActor` | `json` | - | `...` |
| `json.loads` | - | - | - | - |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | - | - | - | - |
| `AgentPermissionError` | - | - | - | - |
| `adapter` | - | - | - | - |
| `data.model_dump` | - | - | - | - |
| `_require_triage_result` | `result`, `triage_item_id: int` | - | - | `result` |
| `LookupError` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| decline_planning_triage_item | _run_triage_action | 724 | `_run_triage_action(mcp_agent_tools.decline_triage_item, db=db, actor=actor, triage_item_id=triage_item_id, data=data, command=command)` |
| _run_triage_action | require_scope | 673 | `require_scope(actor, 'planning:write')` |
| require_scope | actor_has_scope | 100 | `actor_has_scope(actor, scope)` |
| actor_has_scope | actor_scopes | 94 | `actor_scopes(actor)` |
| actor_scopes | json.loads | 86 | `json.loads(actor.scopes)` |
| actor_scopes | isinstance (backend/app/services/agent_service.py:actor_scopes) | 89 | `isinstance(scopes, list)` |
| require_scope | AgentPermissionError | 101 | `AgentPermissionError(...)` |
| _run_triage_action | adapter | 674 | `adapter(db, actor, triage_item_id, data.model_dump(...), idempotency_key=command.idempotency_key, rationale=command.rationale, correlation_id=command.correlation_id)` |
| _run_triage_action | data.model_dump | 678 | `data.model_dump(mode='json', exclude_unset=True)` |
| _run_triage_action | _require_triage_result | 683 | `_require_triage_result(result, triage_item_id)` |
| _require_triage_result | LookupError | 578 | `LookupError(...)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `actor_scopes` | `json.loads` | 86 |
| external_call | `actor_scopes` | `isinstance` | 89 |
| unresolved_call | `_run_triage_action` | `adapter` | 674 |
| unresolved_call | `_run_triage_action` | `data.model_dump` | 678 |
| external_call | `_require_triage_result` | `LookupError` | 578 |
| step_limit | `decline_planning_triage_item` | `first 12 steps` | 0 |

## Behavior

This flow starts at `decline_planning_triage_item` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
