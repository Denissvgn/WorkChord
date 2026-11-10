# agent_finish_run

**Entry point:** `agent_finish_run` (`mcp`)
**Source:** [mcp_server](../modules/mcp_server.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [authority](../modules/authority.md), [commands](../modules/commands.md), [config](../modules/config.md), and 13 more

**Complete modules touched:**

- [agent_service](../modules/agent_service.md)
- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [discussion_service](../modules/discussion_service.md)
- [identity_service](../modules/identity_service.md)
- [maintenance](../modules/maintenance.md)
- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [mcp_server](../modules/mcp_server.md)
- [models_identity](../modules/models_identity.md)
- [models_outbound_webhook](../modules/models_outbound_webhook.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [schemas_agent](../modules/schemas_agent.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as agent_finish_run
    participant p1 as _tool_call
    participant p2 as finish_agent_run
    participant p3 as enforce_mcp_access
    participant p4 as _agent_context
    participant p5 as AgentService.finish_run
    participant p6 as AgentService._run_payload
    participant p7 as get_settings
    participant p8 as AgentService.event_to_payload
    participant p9 as AgentService.list_to_payload
    participant p10 as command_transaction
    participant p11 as _authenticate_agent_key
    participant p12 as _require_scope_requirement
    participant p13 as IdentityService.actor_context
    participant p14 as AgentService._validate_run_fence
    participant p15 as emit_outbound_webhook_event
    participant p16 as OutboundWebhookService.safe_emit_event
    participant p17 as require_scope
    participant p18 as AgentService.authenticate
    participant p19 as require_identity_writes
    participant p20 as AgentService._validate_task_fence
    participant p21 as DeliveryDependencyService.reconcile
    participant p22 as DiscussionService.enqueue
    participant p23 as actor_has_scope
    participant p24 as OutboundWebhookService.enqueue_event
    participant p25 as commit_or_flush
    participant p26 as DeliveryDependencyService.validate_cycles
    participant p27 as DiscussionService.recipient_authorized
    participant p28 as TaskService.reserve_task_version
    participant p29 as ToolError
    participant p30 as func
    p0->>p1: _tool_call
    p0->>p2: finish_agent_run
    p1->>p3: enforce_mcp_access
    p1->>p4: _agent_context
    p2->>p5: AgentService.finish_run
    p2->>p6: AgentService._run_payload
    p3->>p7: get_settings
    p6->>p8: AgentService.event_to_payload
    p6->>p9: AgentService.list_to_payload
    p4->>p10: command_transaction
    p4->>p11: _authenticate_agent_key
    p4->>p12: _require_scope_requirement
    p4->>p13: IdentityService.actor_context
    p5->>p14: AgentService._validate_run_fence
    p5->>p15: emit_outbound_webhook_event
    p15->>p16: OutboundWebhookService.safe_emit_event
    p12->>p17: require_scope
    p11->>p18: AgentService.authenticate
    p13->>p19: require_identity_writes
    p14->>p20: AgentService._validate_task_fence
    p10->>p21: DeliveryDependencyService.reconcile
    p10->>p22: DiscussionService.enqueue
    p17->>p23: actor_has_scope
    p16->>p24: OutboundWebhookService.enqueue_event
    p18->>p25: commit_or_flush
    p21->>p26: DeliveryDependencyService.validate_cycles
    p22->>p27: DiscussionService.recipient_authorized
    p21->>p28: TaskService.reserve_task_version
    p1-->>p29: ToolError(_structured_tool_error(...))
    p1-->>p30: func(db, actor)
```

> Call sequence diagram shows 30 of 293 interactions; 263 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 73 (72 omitted); unresolved 1 of 114 (113 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/config.py:get_settings` | 4 | [backend/app/config.py](../modules/config.md) | internal | 1 |
| `backend/app/maintenance.py:enforce_mcp_access` | 3 | [backend/app/maintenance.py](../modules/maintenance.md) | internal | 2 |
| `backend/app/maintenance.py:scope_requirement_is_mutating` | 6 | - | external | 4 |
| `backend/app/maintenance.py:scope_requirement_is_mutating` | 6 | - | unresolved | 3 |
| `backend/app/mcp_server.py:_agent_context` | 15 | [backend/app/mcp_server.py](../modules/mcp_server.md) | internal | 3 |
| `backend/app/mcp_server.py:_current_agent_key` | 16 | - | unresolved | 1 |
| `backend/app/mcp_server.py:_current_agent_key` | 16 | - | external | 1 |
| `backend/app/mcp_server.py:_open_db_session` | 20 | - | unresolved | 1 |
> Omission summary shows 8 of 91 groups; 83 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 107; effect analysis evaluated: 72, partial: 2, unavailable: 33. Counts include steps omitted from the displayed trace.

Collector observations for 74 source steps with known totals: observed: 321, emitted: 311, omitted: 10. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `agent_finish_run` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `_tool_call` | `available` | `partial` | `available` | `18` | `12` | `6` |
| `enforce_mcp_access` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `scope_requirement_is_mutating` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `isinstance (backend/app/maintenance.p…e_requirement_is_mutating)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `tuple` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `any (backend/app/maintenance.p…e_requirement_is_mutating)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `scope.endswith` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `any (backend/app/maintenance.p…e_requirement_is_mutating)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `scope.endswith` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. agent_finish_run"]
    s2["2. _tool_call"]
    s3["3. enforce_mcp_access"]
    s4["4. get_settings"]
    s5["5. Settings"]
    s6["6. scope_requirement_is_mutating"]
    s7["7. isinstance (backend/app/maintenance.p…e_requirement_is_mutating)"]
    s8["8. tuple"]
    s9["9. any (backend/app/maintenance.p…e_requirement_is_mutating)"]
    s10["10. scope.endswith"]
    s11["11. any (backend/app/maintenance.p…e_requirement_is_mutating)"]
    s12["12. scope.endswith"]
    s1 -->|"_tool_call('runs:write', ...)"| s2
    s2 -->|"enforce_mcp_access(required_scope)"| s3
    s3 -->|"get_settings(data not statically known)"| s4
    s4 -->|"Settings(data not statically known)"| s5
    s3 -->|"scope_requirement_is_mutating(required_scope)"| s6
    s6 -. "isinstance (backend/app/maintenance.p…e_requirement_is_mutating)(required_scope, str)" .-> s7
    s6 -. "tuple(required_scope)" .-> s8
    s6 -. "any (backend/app/maintenance.p…e_requirement_is_mutating)(...)" .-> s9
    s6 -. "scope.endswith(':read')" .-> s10
    s6 -. "any (backend/app/maintenance.p…e_requirement_is_mutating)(...)" .-> s11
    s6 -. "scope.endswith(':write')" .-> s12
    click s1 "../modules/mcp_server.md"
    click s2 "../modules/mcp_server.md"
    click s3 "../modules/maintenance.md"
    click s4 "../modules/config.md"
    click s5 "../modules/config.md"
    click s6 "../modules/maintenance.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `agent_finish_run` | `run_id: int`, `payload: dict[str, Any]` | - | - | `...` |
| `_tool_call` | `required_scope: ScopeRequirement`, `func: Callable[[Any, AgentActor], Any]`, `preview` | `ToolError`, `MissingMutationRevision`, `AggregateVersionConflict`, `HierarchyScopeError`, `AuthorityError`, `MCPAuthError`, `MaintenanceModeError`, `AgentRoutingConflictError` | - | `...` |
| `enforce_mcp_access` | `required_scope: Any` | - | - | `none` |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `scope_requirement_is_mutating` | `required_scope: Any` | - | - | `False`, `...` |
| `isinstance (backend/app/maintenance.p…e_requirement_is_mutating)` | - | - | - | - |
| `tuple` | - | - | - | - |
| `any (backend/app/maintenance.p…e_requirement_is_mutating)` | - | - | - | - |
| `scope.endswith` | - | - | - | - |
| `any (backend/app/maintenance.p…e_requirement_is_mutating)` | - | - | - | - |
| `scope.endswith` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| agent_finish_run | _tool_call | 1197 | `_tool_call('runs:write', ...)` |
| _tool_call | enforce_mcp_access | 303 | `enforce_mcp_access(required_scope)` |
| enforce_mcp_access | get_settings | 112 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| enforce_mcp_access | scope_requirement_is_mutating | 113 | `scope_requirement_is_mutating(required_scope)` |
| scope_requirement_is_mutating | isinstance (backend/app/maintenance.p…e_requirement_is_mutating) | 100 | `isinstance(required_scope, str)` |
| scope_requirement_is_mutating | tuple | 100 | `tuple(required_scope)` |
| scope_requirement_is_mutating | any (backend/app/maintenance.p…e_requirement_is_mutating) | 101 | `any(...)` |
| scope_requirement_is_mutating | scope.endswith | 101 | `scope.endswith(':read')` |
| scope_requirement_is_mutating | any (backend/app/maintenance.p…e_requirement_is_mutating) | 102 | `any(...)` |
| scope_requirement_is_mutating | scope.endswith | 103 | `scope.endswith(':write')` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `scope_requirement_is_mutating` | `isinstance` | 100 |
| external_call | `scope_requirement_is_mutating` | `any` | 101 |
| unresolved_call | `scope_requirement_is_mutating` | `scope.endswith` | 101 |
| external_call | `scope_requirement_is_mutating` | `any` | 102 |
| unresolved_call | `scope_requirement_is_mutating` | `scope.endswith` | 103 |
| step_limit | `agent_finish_run` | `first 12 steps` | 0 |
| truncated_flow | `agent_finish_run` | `depth limit` | 0 |

## Behavior

This flow starts at `agent_finish_run` and is classified as `mcp`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
