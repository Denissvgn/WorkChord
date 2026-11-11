# update_planning_triage_item

**Entry point:** `update_planning_triage_item` (`http`)
**Source:** [routers_agent_planning](../modules/routers_agent_planning.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [commands](../modules/commands.md), [mcp_agent_tools](../modules/mcp_agent_tools.md), [models_agent](../modules/models_agent.md), and 5 more

**Complete modules touched:**

- [agent_service](../modules/agent_service.md)
- [commands](../modules/commands.md)
- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [models_agent](../modules/models_agent.md)
- [routers_agent_planning](../modules/routers_agent_planning.md)
- [schemas_agent_planning](../modules/schemas_agent_planning.md)
- [schemas_triage](../modules/schemas_triage.md)
- [task_service](../modules/task_service.md)
- [triage_service](../modules/triage_service.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as update_planning_triage_item
    participant p1 as require_scope
    participant p2 as update_triage_item
    participant p3 as _require_triage_result
    participant p4 as _handle_agent_error
    participant p5 as actor_has_scope
    participant p6 as _mutate_triage_item
    participant p7 as _triage_command_context
    participant p8 as _triage_command_replay
    participant p9 as TriageService.get_by_id
    participant p10 as _stage_triage_command_audit_event
    participant p11 as _stage_triage_command_receipt
    participant p12 as _commit_triage_command
    participant p13 as TaskService.record_task_event
    participant p14 as commit_or_flush
    participant p15 as AgentPermissionError
    participant p16 as TriageItemUpdate
    participant p17 as actor_scopes
    participant p18 as _triage_audited_request
    participant p19 as TriageService
    participant p20 as _response
    participant p21 as validate_idempotency_key
    participant p22 as AgentPlanningCommandContext
    participant p23 as TaskService
    participant p24 as AgentIdempotencyRecord
    participant p25 as TriageService._query
    participant p26 as _triage_command_request_hash
    participant p27 as TriageService._response_options
    participant p28 as AgentConflictError
    participant p29 as LookupError
    participant p30 as data.model_dump (backend/app/routers/agent…date_planning_triage_item)
    p0->>p1: require_scope
    p0->>p2: update_triage_item
    p0->>p3: _require_triage_result
    p0->>p4: _handle_agent_error
    p1->>p5: actor_has_scope
    p2->>p6: _mutate_triage_item
    p6->>p7: _triage_command_context
    p6->>p8: _triage_command_replay
    p6->>p9: TriageService.get_by_id
    p6->>p10: _stage_triage_command_audit_event
    p6->>p11: _stage_triage_command_receipt
    p6->>p12: _commit_triage_command
    p10->>p13: TaskService.record_task_event
    p12->>p14: commit_or_flush
    p1->>p15: AgentPermissionError
    p2->>p16: TriageItemUpdate
    p5->>p17: actor_scopes
    p6->>p18: _triage_audited_request
    p6->>p19: TriageService
    p6->>p20: _response
    p7->>p21: validate_idempotency_key
    p7->>p22: AgentPlanningCommandContext
    p10->>p23: TaskService
    p11->>p24: AgentIdempotencyRecord
    p9->>p25: TriageService._query
    p11->>p26: _triage_command_request_hash
    p9->>p27: TriageService._response_options
    p8->>p28: AgentConflictError
    p3-->>p29: LookupError(...)
    p0-->>p30: data.model_dump (backend/app/routers/agent…date_planning_triage_item)(mode='json', exclude_unset=True)
```

> Call sequence diagram shows 30 of 106 interactions; 76 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 41 (40 omitted); unresolved 1 of 29 (28 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/agent_service.py:actor_scopes` | 4 | - | external | 2 |
| `backend/app/services/agent_service.py:validate_idempotency_key` | 11 | - | external | 6 |
| `backend/app/services/agent_service.py:validate_idempotency_key` | 11 | - | unresolved | 1 |
| `backend/app/mcp_agent_tools.py:_mutate_triage_item` | 9 | - | unresolved | 6 |
| `backend/app/mcp_agent_tools.py:_triage_command_replay` | 22 | - | unresolved | 3 |
| `backend/app/mcp_agent_tools.py:_triage_command_replay` | 22 | - | external | 4 |
| `backend/app/mcp_agent_tools.py:_triage_command_replay` | 22 | [backend/app/mcp_agent_tools.py](../modules/mcp_agent_tools.md) | internal | 1 |
| `backend/app/mcp_agent_tools.py:_triage_command_request_hash` | 27 | - | external | 2 |
> Omission summary shows 8 of 30 groups; 22 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 37; effect analysis evaluated: 23, partial: 4, unavailable: 10. Counts include steps omitted from the displayed trace.

Collector observations for 27 source steps with known totals: observed: 168, emitted: 161, omitted: 7. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `update_planning_triage_item` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `require_scope` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `actor_has_scope` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `actor_scopes` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `json.loads (backend/app/services/agent_service.py:actor_scopes)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AgentPermissionError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `update_triage_item` | `available` | `evaluated` | `available` | `8` | `8` | `0` |
| `_mutate_triage_item` | `available` | `partial` | `available` | `15` | `14` | `1` |
| `_triage_command_context` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `validate_idempotency_key` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `ValueError` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. update_planning_triage_item"]
    s2["2. require_scope"]
    s3["3. actor_has_scope"]
    s4["4. actor_scopes"]
    s5["5. json.loads (backend/app/services/agent_service.py:actor_scopes)"]
    s6["6. isinstance (backend/app/services/agent_service.py:actor_scopes)"]
    s7["7. AgentPermissionError"]
    s8["8. update_triage_item"]
    s9["9. _mutate_triage_item"]
    s10["10. _triage_command_context"]
    s11["11. validate_idempotency_key"]
    s12["12. ValueError"]
    s1 -->|"require_scope(actor, 'planning:write')"| s2
    s2 -->|"actor_has_scope(actor, scope)"| s3
    s3 -->|"actor_scopes(actor)"| s4
    s4 -. "json.loads (backend/app/services/agent_service.py:actor_scopes)(actor.scopes)" .-> s5
    s4 -. "isinstance (backend/app/services/agent_service.py:actor_scopes)(scopes, list)" .-> s6
    s2 -->|"AgentPermissionError(...)"| s7
    s1 -->|"update_triage_item(…)"| s8
    s8 -->|"_mutate_triage_item(…)"| s9
    s9 -->|"_triage_command_context(idempotency_key=idempotency_key, rationale=rationale, correlation_id=correlation_id)"| s10
    s10 -->|"validate_idempotency_key(idempotency_key, required=True)"| s11
    s11 -. "ValueError('Idempotency-Key is required')" .-> s12
    click s1 "../modules/routers_agent_planning.md"
    click s2 "../modules/agent_service.md"
    click s3 "../modules/agent_service.md"
    click s4 "../modules/agent_service.md"
    click s7 "../modules/agent_service.md"
    click s8 "../modules/mcp_agent_tools.md"
    click s9 "../modules/mcp_agent_tools.md"
    click s10 "../modules/mcp_agent_tools.md"
    click s11 "../modules/agent_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `update_planning_triage_item` | `triage_item_id: int`, `data: TriageItemUpdate`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)]` | - | - | `_require_triage_result(...)` |
| `require_scope` | `actor: AgentActor`, `scope: str` | - | - | - |
| `actor_has_scope` | `actor: AgentActor`, `scope: str` | - | - | `...` |
| `actor_scopes` | `actor: AgentActor` | `json` | - | `...` |
| `json.loads (backend/app/services/agent_service.py:actor_scopes)` | - | - | - | - |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | - | - | - | - |
| `AgentPermissionError` | - | - | - | - |
| `update_triage_item` | `db: AsyncSession`, `actor: AgentActor`, `triage_item_id: int`, `payload: dict[str, Any]`, `idempotency_key: str`, `rationale: str`, `correlation_id: str` | - | - | `...` |
| `_mutate_triage_item` | `db: AsyncSession`, `actor: AgentActor`, `triage_item_id: int`, `operation: str`, `idempotency_key: str`, `rationale: str`, `correlation_id: str`, `data: BaseModel` | `TriageItemResponse` | - | `replay`, `None`, `replay`, `None`, `...` |
| `_triage_command_context` | `idempotency_key: str`, `rationale: str`, `correlation_id: str` | - | - | `AgentPlanningCommandContext(...)` |
| `validate_idempotency_key` | `value: Optional[str]`, `required: bool` | - | - | `None`, `value` |
| `ValueError` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| update_planning_triage_item | require_scope | 672 | `require_scope(actor, 'planning:write')` |
| require_scope | actor_has_scope | 100 | `actor_has_scope(actor, scope)` |
| actor_has_scope | actor_scopes | 94 | `actor_scopes(actor)` |
| actor_scopes | json.loads (backend/app/services/agent_service.py:actor_scopes) | 86 | `json.loads(actor.scopes)` |
| actor_scopes | isinstance (backend/app/services/agent_service.py:actor_scopes) | 89 | `isinstance(scopes, list)` |
| require_scope | AgentPermissionError | 101 | `AgentPermissionError(...)` |
| update_planning_triage_item | update_triage_item | 673 | `mcp_agent_tools.update_triage_item(db, actor, triage_item_id, data.model_dump(...), idempotency_key=command.idempotency_key, rationale=command.rationale, correlation_id=command.correlation_id)` |
| update_triage_item | _mutate_triage_item | 2417 | `_mutate_triage_item(db, actor, triage_item_id, operation='triage.update', idempotency_key=idempotency_key, rationale=rationale, correlation_id=correlation_id, data=TriageItemUpdate(...), service_method='update')` |
| _mutate_triage_item | _triage_command_context | 417 | `_triage_command_context(idempotency_key=idempotency_key, rationale=rationale, correlation_id=correlation_id)` |
| _triage_command_context | validate_idempotency_key | 221 | `validate_idempotency_key(idempotency_key, required=True)` |
| validate_idempotency_key | ValueError | 110 | `ValueError('Idempotency-Key is required')` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `actor_scopes` | `json.loads` | 86 |
| external_call | `actor_scopes` | `isinstance` | 89 |
| external_call | `validate_idempotency_key` | `ValueError` | 110 |
| step_limit | `update_planning_triage_item` | `first 12 steps` | 0 |

## Behavior

This flow starts at `update_planning_triage_item` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
