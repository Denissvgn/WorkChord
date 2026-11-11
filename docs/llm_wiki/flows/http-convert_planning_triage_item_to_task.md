# convert_planning_triage_item_to_task

**Entry point:** `convert_planning_triage_item_to_task` (`http`)
**Source:** [routers_agent_planning](../modules/routers_agent_planning.md)
**Modules touched:** [agent_readiness](../modules/agent_readiness.md), [agent_service](../modules/agent_service.md), [commands](../modules/commands.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), and 20 more

**Complete modules touched:**

- [agent_readiness](../modules/agent_readiness.md)
- [agent_service](../modules/agent_service.md)
- [commands](../modules/commands.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [discussion_service](../modules/discussion_service.md)
- [external_link_service](../modules/external_link_service.md)
- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [models_agent](../modules/models_agent.md)
- [models_request_source](../modules/models_request_source.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [request_source_service](../modules/request_source_service.md)
- [routers_agent_planning](../modules/routers_agent_planning.md)
- [schemas_agent_planning](../modules/schemas_agent_planning.md)
- [schemas_external_link](../modules/schemas_external_link.md)
- [schemas_task](../modules/schemas_task.md)
- [schemas_task_brief](../modules/schemas_task_brief.md)
- [schemas_triage](../modules/schemas_triage.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [snapshot_service](../modules/snapshot_service.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_context_revision_service](../modules/task_context_revision_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)
- [triage_service](../modules/triage_service.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as convert_planning_triage_item_to_task
    participant p1 as require_scope
    participant p2 as convert_triage_to_task
    participant p3 as _require_triage_result
    participant p4 as _handle_agent_error
    participant p5 as actor_has_scope
    participant p6 as _triage_command_context
    participant p7 as _triage_command_replay
    participant p8 as TriageService.get_by_id
    participant p9 as TriageService.convert_to_task
    participant p10 as TaskService.task_to_response
    participant p11 as _stage_triage_command_audit_event
    participant p12 as _stage_triage_command_receipt
    participant p13 as _commit_triage_command
    participant p14 as TaskService.record_task_event
    participant p15 as TriageService._require_project_exists
    participant p16 as task_signals
    participant p17 as current_triage_brief
    participant p18 as brief_from_draft
    participant p19 as evaluate_agent_readiness
    participant p20 as ExternalLinkService.task_links_to_response
    participant p21 as RequestSourceService.copy_triage_links_to_task
    participant p22 as TriageService._record_triage_event
    participant p23 as emit_outbound_webhook_event
    participant p24 as commit_or_flush
    participant p25 as OutboundWebhookService.safe_emit_event
    participant p26 as working_today
    participant p27 as ExternalLinkService.link_to_response
    participant p28 as ExternalLinkService.legacy_task_link_response
    participant p29 as LookupError
    participant p30 as data.model_dump (backend/app/routers/agent…nning_triage_item_to_task)
    p0->>p1: require_scope
    p0->>p2: convert_triage_to_task
    p0->>p3: _require_triage_result
    p0->>p4: _handle_agent_error
    p1->>p5: actor_has_scope
    p2->>p6: _triage_command_context
    p2->>p7: _triage_command_replay
    p2->>p8: TriageService.get_by_id
    p2->>p9: TriageService.convert_to_task
    p2->>p10: TaskService.task_to_response
    p2->>p11: _stage_triage_command_audit_event
    p2->>p12: _stage_triage_command_receipt
    p2->>p13: _commit_triage_command
    p11->>p14: TaskService.record_task_event
    p9->>p15: TriageService._require_project_exists
    p10->>p16: task_signals
    p9->>p17: current_triage_brief
    p9->>p18: brief_from_draft
    p10->>p19: evaluate_agent_readiness
    p10->>p20: ExternalLinkService.task_links_to_response
    p9->>p21: RequestSourceService.copy_triage_links_to_task
    p9->>p22: TriageService._record_triage_event
    p9->>p23: emit_outbound_webhook_event
    p9->>p24: commit_or_flush
    p23->>p25: OutboundWebhookService.safe_emit_event
    p16->>p26: working_today
    p20->>p27: ExternalLinkService.link_to_response
    p20->>p28: ExternalLinkService.legacy_task_link_response
    p3-->>p29: LookupError(...)
    p0-->>p30: data.model_dump (backend/app/routers/agent…nning_triage_item_to_task)(mode='json')
```

> Call sequence diagram shows 30 of 393 interactions; 363 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 102 (101 omitted); unresolved 1 of 168 (167 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/services/agent_service.py:actor_has_scope` | 3 | [backend/app/services/agent_service.py](../modules/agent_service.md) | internal | 1 |
| `backend/app/services/agent_service.py:actor_scopes` | 4 | - | external | 2 |
| `backend/app/services/agent_service.py:require_scope` | 2 | [backend/app/services/agent_service.py](../modules/agent_service.md) | internal | 1 |
| `backend/app/mcp_agent_tools.py:_triage_command_context` | 9 | [backend/app/services/agent_service.py](../modules/agent_service.md) | internal | 1 |
| `backend/app/services/agent_service.py:validate_idempotency_key` | 10 | - | external | 6 |
| `backend/app/services/agent_service.py:validate_idempotency_key` | 10 | - | unresolved | 1 |
| `backend/app/mcp_agent_tools.py:_triage_command_context` | 9 | [backend/app/schemas/agent_planning.py](../modules/schemas_agent_planning.md) | internal | 1 |
| `backend/app/mcp_agent_tools.py:convert_triage_to_task` | 8 | [backend/app/schemas/triage.py](../modules/schemas_triage.md) | internal | 2 |
> Omission summary shows 8 of 120 groups; 112 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 124; effect analysis evaluated: 79, partial: 4, unavailable: 41. Counts include steps omitted from the displayed trace.

Collector observations for 83 source steps with known totals: observed: 526, emitted: 514, omitted: 12. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `convert_planning_triage_item_to_task` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `require_scope` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `actor_has_scope` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `actor_scopes` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `json.loads (backend/app/services/agent_service.py:actor_scopes)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AgentPermissionError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `convert_triage_to_task` | `available` | `evaluated` | `available` | `14` | `14` | `0` |
| `_triage_command_context` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `validate_idempotency_key` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `ValueError (backend/app/services/agen…:validate_idempotency_key)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `value.strip` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. convert_planning_triage_item_to_task"]
    s2["2. require_scope"]
    s3["3. actor_has_scope"]
    s4["4. actor_scopes"]
    s5["5. json.loads (backend/app/services/agent_service.py:actor_scopes)"]
    s6["6. isinstance (backend/app/services/agent_service.py:actor_scopes)"]
    s7["7. AgentPermissionError"]
    s8["8. convert_triage_to_task"]
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
    s1 -->|"convert_triage_to_task(…)"| s8
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
| `convert_planning_triage_item_to_task` | `triage_item_id: int`, `data: TriageConvertToTaskRequest`, `actor: Annotated[AgentActor, Depends(get_agent_actor)]`, `db: Annotated[AsyncSession, Depends(get_db, scope='function')]`, `command: Annotated[AgentPlanningCommandContext, Depends(get_agent_planning_command_context)]` | - | - | `_require_triage_result(...)` |
| `require_scope` | `actor: AgentActor`, `scope: str` | - | - | - |
| `actor_has_scope` | `actor: AgentActor`, `scope: str` | - | - | `...` |
| `actor_scopes` | `actor: AgentActor` | `json` | - | `...` |
| `json.loads (backend/app/services/agent_service.py:actor_scopes)` | - | - | - | - |
| `isinstance (backend/app/services/agent_service.py:actor_scopes)` | - | - | - | - |
| `AgentPermissionError` | - | - | - | - |
| `convert_triage_to_task` | `db: AsyncSession`, `actor: AgentActor`, `triage_item_id: int`, `payload: dict[str, Any]`, `idempotency_key: str`, `rationale: str`, `correlation_id: str` | `TriageConflictError` | - | `replay`, `None`, `replay`, `None`, `...`, `replay` |
| `_triage_command_context` | `idempotency_key: str`, `rationale: str`, `correlation_id: str` | - | - | `AgentPlanningCommandContext(...)` |
| `validate_idempotency_key` | `value: Optional[str]`, `required: bool` | - | - | `None`, `value` |
| `ValueError (backend/app/services/agen…:validate_idempotency_key)` | - | - | - | - |
| `value.strip` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| convert_planning_triage_item_to_task | require_scope | 823 | `require_scope(actor, 'planning:write')` |
| require_scope | actor_has_scope | 100 | `actor_has_scope(actor, scope)` |
| actor_has_scope | actor_scopes | 94 | `actor_scopes(actor)` |
| actor_scopes | json.loads (backend/app/services/agent_service.py:actor_scopes) | 86 | `json.loads(actor.scopes)` |
| actor_scopes | isinstance (backend/app/services/agent_service.py:actor_scopes) | 89 | `isinstance(scopes, list)` |
| require_scope | AgentPermissionError | 101 | `AgentPermissionError(...)` |
| convert_planning_triage_item_to_task | convert_triage_to_task | 824 | `mcp_agent_tools.convert_triage_to_task(db, actor, triage_item_id, data.model_dump(...), idempotency_key=command.idempotency_key, rationale=command.rationale, correlation_id=command.correlation_id)` |
| convert_triage_to_task | _triage_command_context | 2537 | `_triage_command_context(idempotency_key=idempotency_key, rationale=rationale, correlation_id=correlation_id)` |
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
| step_limit | `convert_planning_triage_item_to_task` | `first 12 steps` | 0 |
| truncated_flow | `convert_planning_triage_item_to_task` | `depth limit` | 0 |

## Behavior

This flow starts at `convert_planning_triage_item_to_task` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
