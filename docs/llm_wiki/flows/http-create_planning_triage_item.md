# create_planning_triage_item

**Entry point:** `create_planning_triage_item` (`http`)
**Source:** [routers_agent_planning](../modules/routers_agent_planning.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [commands](../modules/commands.md), [mcp_agent_tools](../modules/mcp_agent_tools.md), [models_agent](../modules/models_agent.md), and 8 more

**Complete modules touched:**

- [agent_service](../modules/agent_service.md)
- [commands](../modules/commands.md)
- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [models_agent](../modules/models_agent.md)
- [models_triage](../modules/models_triage.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [routers_agent_planning](../modules/routers_agent_planning.md)
- [schemas_agent_planning](../modules/schemas_agent_planning.md)
- [schemas_triage](../modules/schemas_triage.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)
- [triage_service](../modules/triage_service.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_planning_triage_item
    participant p1 as require_scope
    participant p2 as create_triage_item
    participant p3 as _handle_agent_error
    participant p4 as actor_has_scope
    participant p5 as _triage_command_context
    participant p6 as _triage_command_replay
    participant p7 as TriageService.create
    participant p8 as _stage_triage_command_audit_event
    participant p9 as _stage_triage_command_receipt
    participant p10 as _commit_triage_command
    participant p11 as TriageService._validate_common_references
    participant p12 as TaskService.record_task_event
    participant p13 as TriageService._record_triage_event
    participant p14 as emit_outbound_webhook_event
    participant p15 as commit_or_flush
    participant p16 as TriageService._require_project_exists
    participant p17 as TriageService.get_by_id
    participant p18 as OutboundWebhookService.safe_emit_event
    participant p19 as TriageService._require_iteration_exists
    participant p20 as TriageService._require_duplicate_item_exists
    participant p21 as TriageService._require_task_exists
    participant p22 as OutboundWebhookService.enqueue_event
    participant p23 as AgentPermissionError
    participant p24 as TriageItemCreate
    participant p25 as _triage_audited_request
    participant p26 as TriageService
    participant p27 as _response
    participant p28 as actor_scopes
    participant p29 as isinstance (backend/app/routers/agent…ng.py:_handle_agent_error)
    participant p30 as data.model_dump (backend/app/routers/agent…eate_planning_triage_item)
    p0->>p1: require_scope
    p0->>p2: create_triage_item
    p0->>p3: _handle_agent_error
    p1->>p4: actor_has_scope
    p2->>p5: _triage_command_context
    p2->>p6: _triage_command_replay
    p2->>p7: TriageService.create
    p2->>p8: _stage_triage_command_audit_event
    p2->>p9: _stage_triage_command_receipt
    p2->>p10: _commit_triage_command
    p7->>p11: TriageService._validate_common_references
    p8->>p12: TaskService.record_task_event
    p7->>p13: TriageService._record_triage_event
    p7->>p14: emit_outbound_webhook_event
    p7->>p15: commit_or_flush
    p11->>p16: TriageService._require_project_exists
    p13->>p17: TriageService.get_by_id
    p14->>p18: OutboundWebhookService.safe_emit_event
    p11->>p19: TriageService._require_iteration_exists
    p11->>p20: TriageService._require_duplicate_item_exists
    p11->>p21: TriageService._require_task_exists
    p18->>p22: OutboundWebhookService.enqueue_event
    p1->>p23: AgentPermissionError
    p2->>p24: TriageItemCreate
    p2->>p25: _triage_audited_request
    p2->>p26: TriageService
    p2->>p27: _response
    p4->>p28: actor_scopes
    p3-->>p29: isinstance (backend/app/routers/agent…ng.py:_handle_agent_error)(exc, AgentPermissionError)
    p0-->>p30: data.model_dump (backend/app/routers/agent…eate_planning_triage_item)(mode='json')
```

> Call sequence diagram shows 30 of 150 interactions; 120 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 50 (49 omitted); unresolved 1 of 45 (44 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/agent_service.py:actor_scopes` | 4 | - | external | 2 |
| `backend/app/mcp_agent_tools.py:_triage_command_context` | 9 | [backend/app/services/agent_service.py](../modules/agent_service.md) | internal | 1 |
| `backend/app/services/agent_service.py:validate_idempotency_key` | 10 | - | external | 6 |
| `backend/app/services/agent_service.py:validate_idempotency_key` | 10 | - | unresolved | 1 |
| `backend/app/mcp_agent_tools.py:_triage_command_context` | 9 | [backend/app/schemas/agent_planning.py](../modules/schemas_agent_planning.md) | internal | 1 |
| `backend/app/mcp_agent_tools.py:create_triage_item` | 8 | - | unresolved | 2 |
| `backend/app/mcp_agent_tools.py:_triage_command_replay` | 22 | - | unresolved | 3 |
| `backend/app/mcp_agent_tools.py:_triage_command_replay` | 22 | - | external | 4 |
> Omission summary shows 8 of 59 groups; 51 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 56; effect analysis evaluated: 41, partial: 3, unavailable: 12. Counts include steps omitted from the displayed trace.

Collector observations for 44 source steps with known totals: observed: 218, emitted: 212, omitted: 6. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `create_planning_triage_item` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `require_scope` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `actor_has_scope` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `actor_scopes` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `json.loads (backend/app/services/agent_service.py:actor_scopes)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AgentPermissionError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `create_triage_item` | `available` | `evaluated` | `available` | `9` | `9` | `0` |
| `_triage_command_context` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `validate_idempotency_key` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `ValueError (backend/app/services/agen…:validate_idempotency_key)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `value.strip` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. create_planning_triage_item"]
    s2["2. require_scope"]
    s3["3. actor_has_scope"]
    s4["4. actor_scopes"]
    s5["5. json.loads (backend/app/services/agent_service.py:actor_scopes)"]
    s6["6. isinstance (backend/app/services/agent_service.py:actor_scopes)"]
    s7["7. AgentPermissionError"]
    s8["8. create_triage_item"]
    s9["9. _triage_command_context"]
    s10["10. validate_idempotency_key"]
    s11["11. ValueError (backend/app/services/agen…:validate_idempotency_key)"]
    s12["12. value.strip"]
    s1 -->|"require_scope(actor, 'planning:write')"| s2
    s2 -->|"actor_has_scope(actor, scope)"| s3
    s3 -->|"actor_scopes(actor)"| s4
    s4 -. "json.loads (backend/app/services/agent_service.py:actor_scopes)(actor.scopes)" .-> s5
    s4 -. "isinstance (backend/app/services/agent_service.py:actor_scopes)(scopes, list)" .-> s6
    s2 -->|"AgentPermissionError(...)"| s7
    s1 -->|"create_triage_item(db, actor, data.model_dump(...), idempotency_key=command.idempotency_key, rationale=command.rationale, correlation_id=command.correlation_id)"| s8
    s8 -->|"_triage_command_context(idempotency_key=idempotency_key, rationale=rationale, correlation_id=correlation_id)"| s9
    s9 -->|"validate_idempotency_key(idempotency_key, required=True)"| s10
    s10 -. "ValueError (backend/app/services/agen…:validate_idempotency_key)('Idempotency-Key is required')" .-> s11
    s10 -. "value.strip(data not statically known)" .-> s12
    click s1 "../modules/routers_agent_planning.md"
    click s2 "../modules/agent_service.md"
    click s3 "../modules/agent_service.md"
    click s4 "../modules/agent_service.md"
    click s7 "../modules/agent_service.md"
    click s8 "../modules/mcp_agent_tools.md"
    click s9 "../modules/mcp_agent_tools.md"
    click s10 "../modules/agent_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_planning_triage_item` | `data: TriageItemCreate`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)]` | - | - | `...` |
| `require_scope` | `actor: AgentActor`, `scope: str` | - | - | - |
| `actor_has_scope` | `actor: AgentActor`, `scope: str` | - | - | `...` |
| `actor_scopes` | `actor: AgentActor` | `json` | - | `...` |
| `json.loads (backend/app/services/agent_service.py:actor_scopes)` | - | - | - | - |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | - | - | - | - |
| `AgentPermissionError` | - | - | - | - |
| `create_triage_item` | `db: AsyncSession`, `actor: AgentActor`, `payload: dict[str, Any]`, `idempotency_key: str`, `rationale: str`, `correlation_id: str` | `TriageItemResponse` | - | `replay`, `...` |
| `_triage_command_context` | `idempotency_key: str`, `rationale: str`, `correlation_id: str` | - | - | `AgentPlanningCommandContext(...)` |
| `validate_idempotency_key` | `value: Optional[str]`, `required: bool` | - | - | `None`, `value` |
| `ValueError (backend/app/services/agen…:validate_idempotency_key)` | - | - | - | - |
| `value.strip` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_planning_triage_item | require_scope | 619 | `require_scope(actor, 'planning:write')` |
| require_scope | actor_has_scope | 100 | `actor_has_scope(actor, scope)` |
| actor_has_scope | actor_scopes | 94 | `actor_scopes(actor)` |
| actor_scopes | json.loads (backend/app/services/agent_service.py:actor_scopes) | 86 | `json.loads(actor.scopes)` |
| actor_scopes | isinstance (backend/app/services/agent_service.py:actor_scopes) | 89 | `isinstance(scopes, list)` |
| require_scope | AgentPermissionError | 101 | `AgentPermissionError(...)` |
| create_planning_triage_item | create_triage_item | 620 | `mcp_agent_tools.create_triage_item(db, actor, data.model_dump(...), idempotency_key=command.idempotency_key, rationale=command.rationale, correlation_id=command.correlation_id)` |
| create_triage_item | _triage_command_context | 2253 | `_triage_command_context(idempotency_key=idempotency_key, rationale=rationale, correlation_id=correlation_id)` |
| _triage_command_context | validate_idempotency_key | 221 | `validate_idempotency_key(idempotency_key, required=True)` |
| validate_idempotency_key | ValueError (backend/app/services/agen…:validate_idempotency_key) | 110 | `ValueError('Idempotency-Key is required')` |
| validate_idempotency_key | value.strip | 114 | `value.strip(data not statically known)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `actor_scopes` | `json.loads` | 86 |
| external_call | `actor_scopes` | `isinstance` | 89 |
| external_call | `validate_idempotency_key` | `ValueError` | 110 |
| unresolved_call | `validate_idempotency_key` | `value.strip` | 114 |
| step_limit | `create_planning_triage_item` | `first 12 steps` | 0 |
| truncated_flow | `create_planning_triage_item` | `depth limit` | 0 |

## Behavior

This flow starts at `create_planning_triage_item` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
