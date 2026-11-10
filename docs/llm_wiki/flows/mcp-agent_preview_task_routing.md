# agent_preview_task_routing

**Entry point:** `agent_preview_task_routing` (`mcp`)
**Source:** [mcp_server](../modules/mcp_server.md)
**Modules touched:** [agent_routing](../modules/agent_routing.md), [agent_routing_observability](../modules/agent_routing_observability.md), [agent_routing_policy](../modules/agent_routing_policy.md), and 23 more

**Complete modules touched:**

- [agent_routing](../modules/agent_routing.md)
- [agent_routing_observability](../modules/agent_routing_observability.md)
- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_routing_rollout](../modules/agent_routing_rollout.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [authority](../modules/authority.md)
- [calendar_service](../modules/calendar_service.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [discussion_service](../modules/discussion_service.md)
- [identity_service](../modules/identity_service.md)
- [maintenance](../modules/maintenance.md)
- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [mcp_server](../modules/mcp_server.md)
- [models_agent](../modules/models_agent.md)
- [models_identity](../modules/models_identity.md)
- [models_outbound_webhook](../modules/models_outbound_webhook.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [query_limits](../modules/query_limits.md)
- [schemas_calendar](../modules/schemas_calendar.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as agent_preview_task_routing
    participant p1 as _tool_call
    participant p2 as preview_task_routing
    participant p3 as enforce_mcp_access
    participant p4 as AgentRoutingService.preview_task_routing
    participant p5 as _agent_context
    participant p6 as get_settings
    participant p7 as AgentRoutingService._require_preview_rollout
    participant p8 as AgentRoutingService._require_read
    participant p9 as command_transaction
    participant p10 as _authenticate_agent_key
    participant p11 as _require_scope_requirement
    participant p12 as AgentRoutingService._build_preview
    participant p13 as IdentityService.actor_context
    participant p14 as record_routing_operational_event
    participant p15 as require_scope
    participant p16 as AgentTeamSetupService.routing_readiness
    participant p17 as build_routing_operational_payload
    participant p18 as AgentService.authenticate
    participant p19 as TaskService.record_task_event
    participant p20 as require_identity_writes
    participant p21 as emit_outbound_webhook_event
    participant p22 as DeliveryDependencyService.reconcile
    participant p23 as DiscussionService.enqueue
    participant p24 as AgentRoutingService._preview_context
    participant p25 as AgentRoutingService._capacity_inputs
    participant p26 as AgentRoutingService._routing_input_evidence
    participant p27 as AgentRoutingService._task_global_blockers
    participant p28 as AgentRoutingService._profile_evidence
    participant p29 as ToolError
    participant p30 as func
    p0->>p1: _tool_call
    p0->>p2: preview_task_routing
    p1->>p3: enforce_mcp_access
    p2->>p4: AgentRoutingService.preview_task_routing
    p1->>p5: _agent_context
    p3->>p6: get_settings
    p4->>p7: AgentRoutingService._require_preview_rollout
    p4->>p8: AgentRoutingService._require_read
    p5->>p9: command_transaction
    p5->>p10: _authenticate_agent_key
    p5->>p11: _require_scope_requirement
    p4->>p12: AgentRoutingService._build_preview
    p5->>p13: IdentityService.actor_context
    p4->>p14: record_routing_operational_event
    p11->>p15: require_scope
    p7->>p16: AgentTeamSetupService.routing_readiness
    p14->>p17: build_routing_operational_payload
    p10->>p18: AgentService.authenticate
    p14->>p19: TaskService.record_task_event
    p13->>p20: require_identity_writes
    p14->>p21: emit_outbound_webhook_event
    p9->>p22: DeliveryDependencyService.reconcile
    p9->>p23: DiscussionService.enqueue
    p12->>p24: AgentRoutingService._preview_context
    p12->>p25: AgentRoutingService._capacity_inputs
    p12->>p26: AgentRoutingService._routing_input_evidence
    p12->>p27: AgentRoutingService._task_global_blockers
    p12->>p28: AgentRoutingService._profile_evidence
    p1-->>p29: ToolError(_structured_tool_error(...))
    p1-->>p30: func(db, actor)
```

> Call sequence diagram shows 30 of 921 interactions; 891 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 373 (372 omitted); unresolved 1 of 336 (335 omitted). These counts cover the captured static trace.

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
> Omission summary shows 8 of 198 groups; 190 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 213; effect analysis evaluated: 133, partial: 12, unavailable: 68. Counts include steps omitted from the displayed trace.

Collector observations for 145 source steps with known totals: observed: 948, emitted: 838, omitted: 110. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `agent_preview_task_routing` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `_tool_call` | `available` | `partial` | `available` | `18` | `12` | `6` |
| `enforce_mcp_access` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `scope_requirement_is_mutating` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `isinstance (backend/app/maintenance.p…e_requirement_is_mutating)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `tuple (backend/app/maintenance.p…e_requirement_is_mutating)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `any (backend/app/maintenance.p…e_requirement_is_mutating)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `scope.endswith` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `any (backend/app/maintenance.p…e_requirement_is_mutating)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `scope.endswith` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. agent_preview_task_routing"]
    s2["2. _tool_call"]
    s3["3. enforce_mcp_access"]
    s4["4. get_settings"]
    s5["5. Settings"]
    s6["6. scope_requirement_is_mutating"]
    s7["7. isinstance (backend/app/maintenance.p…e_requirement_is_mutating)"]
    s8["8. tuple (backend/app/maintenance.p…e_requirement_is_mutating)"]
    s9["9. any (backend/app/maintenance.p…e_requirement_is_mutating)"]
    s10["10. scope.endswith"]
    s11["11. any (backend/app/maintenance.p…e_requirement_is_mutating)"]
    s12["12. scope.endswith"]
    s1 -->|"_tool_call(ROUTING_READ_SCOPE_REQUIREMENT, ...)"| s2
    s2 -->|"enforce_mcp_access(required_scope)"| s3
    s3 -->|"get_settings(data not statically known)"| s4
    s4 -->|"Settings(data not statically known)"| s5
    s3 -->|"scope_requirement_is_mutating(required_scope)"| s6
    s6 -. "isinstance (backend/app/maintenance.p…e_requirement_is_mutating)(required_scope, str)" .-> s7
    s6 -. "tuple (backend/app/maintenance.p…e_requirement_is_mutating)(required_scope)" .-> s8
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
| `agent_preview_task_routing` | `task_id: int`, `payload: dict[str, Any]` | `ROUTING_READ_SCOPE_REQUIREMENT` | - | `...` |
| `_tool_call` | `required_scope: ScopeRequirement`, `func: Callable[[Any, AgentActor], Any]`, `preview` | `ToolError`, `MissingMutationRevision`, `AggregateVersionConflict`, `HierarchyScopeError`, `AuthorityError`, `MCPAuthError`, `MaintenanceModeError`, `AgentRoutingConflictError` | - | `...` |
| `enforce_mcp_access` | `required_scope: Any` | - | - | `none` |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `scope_requirement_is_mutating` | `required_scope: Any` | - | - | `False`, `...` |
| `isinstance (backend/app/maintenance.p…e_requirement_is_mutating)` | - | - | - | - |
| `tuple (backend/app/maintenance.p…e_requirement_is_mutating)` | - | - | - | - |
| `any (backend/app/maintenance.p…e_requirement_is_mutating)` | - | - | - | - |
| `scope.endswith` | - | - | - | - |
| `any (backend/app/maintenance.p…e_requirement_is_mutating)` | - | - | - | - |
| `scope.endswith` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| agent_preview_task_routing | _tool_call | 508 | `_tool_call(ROUTING_READ_SCOPE_REQUIREMENT, ...)` |
| _tool_call | enforce_mcp_access | 303 | `enforce_mcp_access(required_scope)` |
| enforce_mcp_access | get_settings | 112 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| enforce_mcp_access | scope_requirement_is_mutating | 113 | `scope_requirement_is_mutating(required_scope)` |
| scope_requirement_is_mutating | isinstance (backend/app/maintenance.p…e_requirement_is_mutating) | 100 | `isinstance(required_scope, str)` |
| scope_requirement_is_mutating | tuple (backend/app/maintenance.p…e_requirement_is_mutating) | 100 | `tuple(required_scope)` |
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
| step_limit | `agent_preview_task_routing` | `first 12 steps` | 0 |
| truncated_flow | `agent_preview_task_routing` | `depth limit` | 0 |

## Behavior

This flow starts at `agent_preview_task_routing` and is classified as `mcp`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
