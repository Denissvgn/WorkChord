# decline_planning_triage_item

**Entry point:** `decline_planning_triage_item` (`http`)
**Source:** [routers_agent_planning](../modules/routers_agent_planning.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [routers_agent_planning](../modules/routers_agent_planning.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as decline_planning_triage_item
    participant p1 as _run_triage_action
    participant p2 as require_scope
    participant p3 as actor_has_scope
    participant p4 as actor_scopes
    participant p5 as json.loads
    participant p6 as isinstance (backend/app/services/agent_service.py:actor_scopes)
    participant p7 as AgentPermissionError
    participant p8 as adapter
    participant p9 as data.model_dump
    participant p10 as _require_triage_result
    participant p11 as LookupError
    participant p12 as _handle_agent_error
    participant p13 as isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)
    participant p14 as HTTPException
    participant p15 as str
    participant p16 as exc.detail
    p0->>p1: _run_triage_action
    p1->>p2: require_scope
    p2->>p3: actor_has_scope
    p3->>p4: actor_scopes
    p4-->>p5: json.loads
    p4-->>p6: isinstance (backend/app/services/agent_service.py:actor_scopes)
    p2->>p7: AgentPermissionError
    p1-->>p8: adapter
    p1-->>p9: data.model_dump
    p1->>p10: _require_triage_result
    p10-->>p11: LookupError
    p0->>p12: _handle_agent_error
    p12-->>p13: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)
    p12-->>p14: HTTPException
    p12-->>p15: str
    p12-->>p13: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)
    p12-->>p14: HTTPException
    p12-->>p16: exc.detail
    p12-->>p13: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)
    p12-->>p14: HTTPException
    p12-->>p16: exc.detail
    p12-->>p13: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)
    p12-->>p14: HTTPException
    p12-->>p15: str
    p12-->>p13: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)
    p12-->>p14: HTTPException
    p12-->>p15: str
    p12-->>p13: isinstance (backend/app/routers/agent…ing.py:_handle_agent_error)
    p12-->>p14: HTTPException
    p12-->>p15: str
```

> Call sequence diagram shows 30 of 33 interactions; 3 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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
| `decline_planning_triage_item` | `triage_item_id: int`, `data: TriageActionRequest`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `db: Annotated[AsyncSession, Depends(get_db)]`, `command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)]` | `mcp_agent_tools` | - | `...` |
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
| require_scope | actor_has_scope | 84 | `actor_has_scope(actor, scope)` |
| actor_has_scope | actor_scopes | 78 | `actor_scopes(actor)` |
| actor_scopes | json.loads | 70 | `json.loads(actor.scopes)` |
| actor_scopes | isinstance (backend/app/services/agent_service.py:actor_scopes) | 73 | `isinstance(scopes, list)` |
| require_scope | AgentPermissionError | 85 | `AgentPermissionError(...)` |
| _run_triage_action | adapter | 674 | `adapter(db, actor, triage_item_id, data.model_dump(...), idempotency_key=command.idempotency_key, rationale=command.rationale, correlation_id=command.correlation_id)` |
| _run_triage_action | data.model_dump | 678 | `data.model_dump(mode='json', exclude_unset=True)` |
| _run_triage_action | _require_triage_result | 683 | `_require_triage_result(result, triage_item_id)` |
| _require_triage_result | LookupError | 578 | `LookupError(...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `actor_scopes` | `json.loads` | 70 |
| external_call | `actor_scopes` | `isinstance` | 73 |
| unresolved_call | `_run_triage_action` | `adapter` | 674 |
| unresolved_call | `_run_triage_action` | `data.model_dump` | 678 |
| external_call | `_require_triage_result` | `LookupError` | 578 |
| step_limit | `decline_planning_triage_item` | `first 12 steps` | 0 |

## Behavior

This flow starts at `decline_planning_triage_item` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
