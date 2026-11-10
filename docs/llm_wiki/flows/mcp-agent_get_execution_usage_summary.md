# agent_get_execution_usage_summary

**Entry point:** `agent_get_execution_usage_summary` (`mcp`)
**Source:** [mcp_server](../modules/mcp_server.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [authority](../modules/authority.md), [commands](../modules/commands.md), [config](../modules/config.md), and 16 more

**Complete modules touched:**

- [agent_service](../modules/agent_service.md)
- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [delivery_metrics](../modules/delivery_metrics.md)
- [delivery_metrics_service](../modules/delivery_metrics_service.md)
- [discussion_service](../modules/discussion_service.md)
- [execution_usage_service](../modules/execution_usage_service.md)
- [identity_service](../modules/identity_service.md)
- [maintenance](../modules/maintenance.md)
- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [mcp_server](../modules/mcp_server.md)
- [models_identity](../modules/models_identity.md)
- [models_outbound_webhook](../modules/models_outbound_webhook.md)
- [query_limits](../modules/query_limits.md)
- [schemas_execution_usage](../modules/schemas_execution_usage.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as agent_get_execution_usage_summary
    participant p1 as _tool_call
    participant p2 as get_execution_usage_summary
    participant p3 as enforce_mcp_access
    participant p4 as _agent_context
    participant p5 as ExecutionUsageService.summary
    participant p6 as get_settings
    participant p7 as require_project
    participant p8 as command_transaction
    participant p9 as _authenticate_agent_key
    participant p10 as _require_scope_requirement
    participant p11 as IdentityService.actor_context
    participant p12 as run_identity
    participant p13 as DeliveryMetricsService.report
    participant p14 as require_scope
    participant p15 as AgentService.authenticate
    participant p16 as require_identity_writes
    participant p17 as DeliveryDependencyService.reconcile
    participant p18 as DiscussionService.enqueue
    participant p19 as DeliveryMetricsService._window_observations
    participant p20 as summarize_observations
    participant p21 as actor_has_scope
    participant p22 as commit_or_flush
    participant p23 as DeliveryDependencyService.validate_cycles
    participant p24 as DiscussionService.recipient_authorized
    participant p25 as _samples
    participant p26 as TaskService.reserve_task_version
    participant p27 as clear_execution_evidence
    participant p28 as AgentPermissionError
    participant p29 as any (backend/app/mcp_agent_too…t_execution_usage_summary)
    participant p30 as func
    p0->>p1: _tool_call
    p0->>p2: get_execution_usage_summary
    p1->>p3: enforce_mcp_access
    p1->>p4: _agent_context
    p2->>p5: ExecutionUsageService.summary
    p3->>p6: get_settings
    p5->>p7: require_project
    p4->>p8: command_transaction
    p4->>p9: _authenticate_agent_key
    p4->>p10: _require_scope_requirement
    p4->>p11: IdentityService.actor_context
    p5->>p12: run_identity
    p5->>p13: DeliveryMetricsService.report
    p10->>p14: require_scope
    p9->>p15: AgentService.authenticate
    p11->>p16: require_identity_writes
    p8->>p17: DeliveryDependencyService.reconcile
    p8->>p18: DiscussionService.enqueue
    p13->>p19: DeliveryMetricsService._window_observations
    p13->>p20: summarize_observations
    p14->>p21: actor_has_scope
    p15->>p22: commit_or_flush
    p17->>p23: DeliveryDependencyService.validate_cycles
    p18->>p24: DiscussionService.recipient_authorized
    p20->>p25: _samples
    p17->>p26: TaskService.reserve_task_version
    p17->>p27: clear_execution_evidence
    p2->>p28: AgentPermissionError
    p2-->>p29: any (backend/app/mcp_agent_too…t_execution_usage_summary)(...)
    p1-->>p30: func(db, actor)
```

> Call sequence diagram shows 30 of 520 interactions; 490 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 172 (171 omitted); unresolved 1 of 224 (223 omitted). These counts cover the captured static trace.

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
> Omission summary shows 8 of 106 groups; 98 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 125; effect analysis evaluated: 82, partial: 4, unavailable: 39. Counts include steps omitted from the displayed trace.

Collector observations for 86 source steps with known totals: observed: 420, emitted: 392, omitted: 28. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `agent_get_execution_usage_summary` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
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
    s1["1. agent_get_execution_usage_summary"]
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
    s1 -->|"_tool_call((...), ...)"| s2
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
| `agent_get_execution_usage_summary` | `project_id: Optional[int]`, `iteration_id: Optional[int]`, `lookback_days: int`, `budget_amount: Optional[str]`, `budget_currency: Optional[str]` | - | - | `...` |
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
| agent_get_execution_usage_summary | _tool_call | 952 | `_tool_call((...), ...)` |
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
| step_limit | `agent_get_execution_usage_summary` | `first 12 steps` | 0 |
| truncated_flow | `agent_get_execution_usage_summary` | `depth limit` | 0 |

## Behavior

This flow starts at `agent_get_execution_usage_summary` and is classified as `mcp`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
