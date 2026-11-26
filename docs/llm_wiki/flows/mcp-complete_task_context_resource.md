# complete_task_context_resource

**Entry point:** `complete_task_context_resource` (`mcp`)
**Source:** [mcp_server](../modules/mcp_server.md)
**Modules touched:** [agent_routing_policy](../modules/agent_routing_policy.md), [agent_routing_rollout](../modules/agent_routing_rollout.md), [agent_service](../modules/agent_service.md), and 26 more

**Complete modules touched:**

- [agent_routing_policy](../modules/agent_routing_policy.md)
- [agent_routing_rollout](../modules/agent_routing_rollout.md)
- [agent_service](../modules/agent_service.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [agent_work_service](../modules/agent_work_service.md)
- [app_maintenance](../modules/app_maintenance.md)
- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [discussion_service](../modules/discussion_service.md)
- [execution_planning_window](../modules/execution_planning_window.md)
- [execution_reconciliation](../modules/execution_reconciliation.md)
- [github_links](../modules/github_links.md)
- [identity_service](../modules/identity_service.md)
- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [mcp_server](../modules/mcp_server.md)
- [models_identity](../modules/models_identity.md)
- [models_outbound_webhook](../modules/models_outbound_webhook.md)
- [planning_window_reconciliation](../modules/planning_window_reconciliation.md)
- [query_limits](../modules/query_limits.md)
- [retained_planning_output](../modules/retained_planning_output.md)
- [review_provenance](../modules/review_provenance.md)
- [schemas_agent](../modules/schemas_agent.md)
- [services_work_metrics](../modules/services_work_metrics.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)
- [task_timeline_service](../modules/task_timeline_service.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as complete_task_context_resource
    participant p1 as _json_resource
    participant p2 as get_complete_task_context
    participant p3 as _tool_call
    participant p4 as AgentWorkService.get_task_context
    participant p5 as enforce_mcp_access
    participant p6 as AgentWorkService._require_any_scope
    participant p7 as _agent_context
    participant p8 as AgentWorkService._definition_blockers
    participant p9 as AgentWorkService.assignment_response
    participant p10 as AgentWorkService._validate_assignment_actor
    participant p11 as AgentWorkService._execution_assignment_view
    participant p12 as AgentWorkService._started_blockers
    participant p13 as AgentWorkService._start_blockers
    participant p14 as AgentService.get_task_timeline
    participant p15 as get_settings
    participant p16 as evaluate_actor_authorization
    participant p17 as window_authority_matches
    participant p18 as command_transaction
    participant p19 as TaskTimelineService.page
    participant p20 as _authenticate_agent_key
    participant p21 as recovery_attestation_hint
    participant p22 as _require_scope_requirement
    participant p23 as IdentityService.actor_context
    participant p24 as AgentWorkService._resolve_rollout
    participant p25 as AgentWorkService._shadow_handoff
    participant p26 as AgentWorkService._selection_pending
    participant p27 as AgentWorkService._is_model_aware_assignment
    participant p28 as AgentWorkService._working_today
    participant p29 as int (backend/app/mcp_server.py…ete_task_context_resource)
    participant p30 as context.model_dump
    p0->>p1: _json_resource
    p0->>p2: get_complete_task_context
    p1->>p3: _tool_call
    p2->>p4: AgentWorkService.get_task_context
    p3->>p5: enforce_mcp_access
    p4->>p6: AgentWorkService._require_any_scope
    p3->>p7: _agent_context
    p4->>p8: AgentWorkService._definition_blockers
    p4->>p9: AgentWorkService.assignment_response
    p4->>p10: AgentWorkService._validate_assignment_actor
    p4->>p11: AgentWorkService._execution_assignment_view
    p4->>p12: AgentWorkService._started_blockers
    p4->>p13: AgentWorkService._start_blockers
    p4->>p14: AgentService.get_task_timeline
    p5->>p15: get_settings
    p10->>p16: evaluate_actor_authorization
    p12->>p17: window_authority_matches
    p7->>p18: command_transaction
    p14->>p19: TaskTimelineService.page
    p7->>p20: _authenticate_agent_key
    p13->>p21: recovery_attestation_hint
    p7->>p22: _require_scope_requirement
    p7->>p23: IdentityService.actor_context
    p13->>p24: AgentWorkService._resolve_rollout
    p13->>p25: AgentWorkService._shadow_handoff
    p13->>p26: AgentWorkService._selection_pending
    p13->>p27: AgentWorkService._is_model_aware_assignment
    p13->>p28: AgentWorkService._working_today
    p0-->>p29: int (backend/app/mcp_server.py…ete_task_context_resource)(task_id)
    p2-->>p30: context.model_dump(mode='json')
```

> Call sequence diagram shows 30 of 853 interactions; 823 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 230 (229 omitted); unresolved 1 of 403 (402 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/config.py:get_settings` | 5 | [backend/app/config.py](../modules/config.md) | internal | 1 |
| `backend/app/maintenance.py:enforce_mcp_access` | 4 | [backend/app/maintenance.py](../modules/app_maintenance.md) | internal | 2 |
| `backend/app/maintenance.py:scope_requirement_is_mutating` | 7 | - | external | 4 |
| `backend/app/maintenance.py:scope_requirement_is_mutating` | 7 | - | unresolved | 3 |
| `backend/app/mcp_server.py:_agent_context` | 16 | [backend/app/mcp_server.py](../modules/mcp_server.md) | internal | 3 |
| `backend/app/mcp_server.py:_current_agent_key` | 17 | - | unresolved | 1 |
| `backend/app/mcp_server.py:_current_agent_key` | 17 | - | external | 1 |
| `backend/app/mcp_server.py:_open_db_session` | 21 | - | unresolved | 1 |
> Omission summary shows 8 of 181 groups; 173 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 221; effect analysis evaluated: 164, partial: 8, unavailable: 49. Counts include steps omitted from the displayed trace.

Collector observations for 172 source steps with known totals: observed: 1019, emitted: 950, omitted: 69. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `complete_task_context_resource` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `_json_resource` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `_tool_call` | `available` | `partial` | `available` | `19` | `12` | `7` |
| `enforce_mcp_access` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `scope_requirement_is_mutating` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `isinstance (backend/app/maintenance.p…e_requirement_is_mutating)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `tuple (backend/app/maintenance.p…e_requirement_is_mutating)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `any (backend/app/maintenance.p…e_requirement_is_mutating)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `scope.endswith` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `any (backend/app/maintenance.p…e_requirement_is_mutating)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. complete_task_context_resource"]
    s2["2. _json_resource"]
    s3["3. _tool_call"]
    s4["4. enforce_mcp_access"]
    s5["5. get_settings"]
    s6["6. Settings"]
    s7["7. scope_requirement_is_mutating"]
    s8["8. isinstance (backend/app/maintenance.p…e_requirement_is_mutating)"]
    s9["9. tuple (backend/app/maintenance.p…e_requirement_is_mutating)"]
    s10["10. any (backend/app/maintenance.p…e_requirement_is_mutating)"]
    s11["11. scope.endswith"]
    s12["12. any (backend/app/maintenance.p…e_requirement_is_mutating)"]
    s1 -->|"_json_resource((...), ...)"| s2
    s2 -->|"_tool_call(required_scope, func)"| s3
    s3 -->|"enforce_mcp_access(required_scope)"| s4
    s4 -->|"get_settings(data not statically known)"| s5
    s5 -->|"Settings(data not statically known)"| s6
    s4 -->|"scope_requirement_is_mutating(required_scope)"| s7
    s7 -. "isinstance (backend/app/maintenance.p…e_requirement_is_mutating)(required_scope, str)" .-> s8
    s7 -. "tuple (backend/app/maintenance.p…e_requirement_is_mutating)(required_scope)" .-> s9
    s7 -. "any (backend/app/maintenance.p…e_requirement_is_mutating)(...)" .-> s10
    s7 -. "scope.endswith(':read')" .-> s11
    s7 -. "any (backend/app/maintenance.p…e_requirement_is_mutating)(...)" .-> s12
    click s1 "../modules/mcp_server.md"
    click s2 "../modules/mcp_server.md"
    click s3 "../modules/mcp_server.md"
    click s4 "../modules/app_maintenance.md"
    click s5 "../modules/config.md"
    click s6 "../modules/config.md"
    click s7 "../modules/app_maintenance.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `complete_task_context_resource` | `task_id: str` | - | - | `...` |
| `_json_resource` | `required_scope: ScopeRequirement`, `func: Callable[[Any, AgentActor], Any]` | - | - | `json.dumps(...)` |
| `_tool_call` | `required_scope: ScopeRequirement`, `func: Callable[[Any, AgentActor], Any]`, `preview` | `ToolError`, `MissingMutationRevision`, `AggregateVersionConflict`, `HierarchyScopeError`, `PlanningConflict`, `AuthorityError`, `MCPAuthError`, `MaintenanceModeError` | - | `...` |
| `enforce_mcp_access` | `required_scope: Any` | - | - | `none` |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `scope_requirement_is_mutating` | `required_scope: Any` | - | - | `False`, `...` |
| `isinstance (backend/app/maintenance.p…e_requirement_is_mutating)` | - | - | - | - |
| `tuple (backend/app/maintenance.p…e_requirement_is_mutating)` | - | - | - | - |
| `any (backend/app/maintenance.p…e_requirement_is_mutating)` | - | - | - | - |
| `scope.endswith` | - | - | - | - |
| `any (backend/app/maintenance.p…e_requirement_is_mutating)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| complete_task_context_resource | _json_resource | 2587 | `_json_resource((...), ...)` |
| _json_resource | _tool_call | 367 | `_tool_call(required_scope, func)` |
| _tool_call | enforce_mcp_access | 337 | `enforce_mcp_access(required_scope)` |
| enforce_mcp_access | get_settings | 112 | `get_settings(data not statically known)` |
| get_settings | Settings | 528 | `Settings(data not statically known)` |
| enforce_mcp_access | scope_requirement_is_mutating | 113 | `scope_requirement_is_mutating(required_scope)` |
| scope_requirement_is_mutating | isinstance (backend/app/maintenance.p…e_requirement_is_mutating) | 100 | `isinstance(required_scope, str)` |
| scope_requirement_is_mutating | tuple (backend/app/maintenance.p…e_requirement_is_mutating) | 100 | `tuple(required_scope)` |
| scope_requirement_is_mutating | any (backend/app/maintenance.p…e_requirement_is_mutating) | 101 | `any(...)` |
| scope_requirement_is_mutating | scope.endswith | 101 | `scope.endswith(':read')` |
| scope_requirement_is_mutating | any (backend/app/maintenance.p…e_requirement_is_mutating) | 102 | `any(...)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `scope_requirement_is_mutating` | `isinstance` | 100 |
| external_call | `scope_requirement_is_mutating` | `any` | 101 |
| unresolved_call | `scope_requirement_is_mutating` | `scope.endswith` | 101 |
| external_call | `scope_requirement_is_mutating` | `any` | 102 |
| step_limit | `complete_task_context_resource` | `first 12 steps` | 0 |
| truncated_flow | `complete_task_context_resource` | `depth limit` | 0 |

## Behavior

This flow starts at `complete_task_context_resource` and is classified as `mcp`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
