# agent_actor_roster_resource

**Entry point:** `agent_actor_roster_resource` (`mcp`)
**Source:** [mcp_server](../modules/mcp_server.md)
**Modules touched:** [agent_model_catalog_service](../modules/agent_model_catalog_service.md), [agent_routing](../modules/agent_routing.md), [agent_service](../modules/agent_service.md), and 19 more

**Complete modules touched:**

- [agent_model_catalog_service](../modules/agent_model_catalog_service.md)
- [agent_routing](../modules/agent_routing.md)
- [agent_service](../modules/agent_service.md)
- [agent_team_setup](../modules/agent_team_setup.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [agent_work_service](../modules/agent_work_service.md)
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
- [query_limits](../modules/query_limits.md)
- [schemas_agent](../modules/schemas_agent.md)
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as agent_actor_roster_resource
    participant p1 as _json_resource
    participant p2 as list_agent_actor_roster
    participant p3 as _tool_call
    participant p4 as _dump
    participant p5 as AgentWorkService.list_actor_roster
    participant p6 as enforce_mcp_access
    participant p7 as AgentWorkService._require_any_scope
    participant p8 as _agent_context
    participant p9 as AgentTeamSetupService.membership_boundary
    participant p10 as AgentWorkService._profile_roster_response
    participant p11 as AgentModelCatalogService.binding_response
    participant p12 as AgentWorkService.actor_response
    participant p13 as get_settings
    participant p14 as command_transaction
    participant p15 as _authenticate_agent_key
    participant p16 as _require_scope_requirement
    participant p17 as IdentityService.actor_context
    participant p18 as AgentTeamSetupService._status_for_topology
    participant p19 as require_scope
    participant p20 as AgentService.authenticate
    participant p21 as require_identity_writes
    participant p22 as DeliveryDependencyService.reconcile
    participant p23 as IdentityService.context
    participant p24 as DiscussionService.enqueue
    participant p25 as AgentTeamSetupService._handoff
    participant p26 as _canonical_json
    participant p27 as AgentWorkService
    participant p28 as _structured_tool_error
    participant p29 as json.dumps (backend/app/mcp_server.py:_json_resource)
    participant p30 as value.model_dump
    p0->>p1: _json_resource
    p0->>p2: list_agent_actor_roster
    p1->>p3: _tool_call
    p2->>p4: _dump
    p2->>p5: AgentWorkService.list_actor_roster
    p3->>p6: enforce_mcp_access
    p5->>p7: AgentWorkService._require_any_scope
    p3->>p8: _agent_context
    p5->>p9: AgentTeamSetupService.membership_boundary
    p5->>p10: AgentWorkService._profile_roster_response
    p5->>p11: AgentModelCatalogService.binding_response
    p5->>p12: AgentWorkService.actor_response
    p6->>p13: get_settings
    p8->>p14: command_transaction
    p8->>p15: _authenticate_agent_key
    p8->>p16: _require_scope_requirement
    p8->>p17: IdentityService.actor_context
    p9->>p18: AgentTeamSetupService._status_for_topology
    p16->>p19: require_scope
    p15->>p20: AgentService.authenticate
    p17->>p21: require_identity_writes
    p14->>p22: DeliveryDependencyService.reconcile
    p17->>p23: IdentityService.context
    p14->>p24: DiscussionService.enqueue
    p18->>p25: AgentTeamSetupService._handoff
    p18->>p26: _canonical_json
    p2->>p27: AgentWorkService
    p3->>p28: _structured_tool_error
    p1-->>p29: json.dumps (backend/app/mcp_server.py:_json_resource)(value, ensure_ascii=False, default=str)
    p4-->>p30: value.model_dump(mode='json')
```

> Call sequence diagram shows 30 of 449 interactions; 419 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 143 (142 omitted); unresolved 1 of 194 (193 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/config.py:get_settings` | 5 | [backend/app/config.py](../modules/config.md) | internal | 1 |
| `backend/app/maintenance.py:enforce_mcp_access` | 4 | [backend/app/maintenance.py](../modules/maintenance.md) | internal | 2 |
| `backend/app/maintenance.py:scope_requirement_is_mutating` | 7 | - | external | 4 |
| `backend/app/maintenance.py:scope_requirement_is_mutating` | 7 | - | unresolved | 3 |
| `backend/app/mcp_server.py:_agent_context` | 16 | [backend/app/mcp_server.py](../modules/mcp_server.md) | internal | 3 |
| `backend/app/mcp_server.py:_current_agent_key` | 17 | - | unresolved | 1 |
| `backend/app/mcp_server.py:_current_agent_key` | 17 | - | external | 1 |
| `backend/app/mcp_server.py:_open_db_session` | 21 | - | unresolved | 1 |
> Omission summary shows 8 of 97 groups; 89 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 113; effect analysis evaluated: 66, partial: 3, unavailable: 44. Counts include steps omitted from the displayed trace.

Collector observations for 69 source steps with known totals: observed: 313, emitted: 292, omitted: 21. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `agent_actor_roster_resource` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `_json_resource` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
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

```mermaid
flowchart LR
    s1["1. agent_actor_roster_resource"]
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
    click s4 "../modules/maintenance.md"
    click s5 "../modules/config.md"
    click s6 "../modules/config.md"
    click s7 "../modules/maintenance.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `agent_actor_roster_resource` | - | - | - | `...` |
| `_json_resource` | `required_scope: ScopeRequirement`, `func: Callable[[Any, AgentActor], Any]` | - | - | `json.dumps(...)` |
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

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| agent_actor_roster_resource | _json_resource | 2178 | `_json_resource((...), ...)` |
| _json_resource | _tool_call | 332 | `_tool_call(required_scope, func)` |
| _tool_call | enforce_mcp_access | 303 | `enforce_mcp_access(required_scope)` |
| enforce_mcp_access | get_settings | 112 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
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
| step_limit | `agent_actor_roster_resource` | `first 12 steps` | 0 |
| truncated_flow | `agent_actor_roster_resource` | `depth limit` | 0 |

## Behavior

This flow starts at `agent_actor_roster_resource` and is classified as `mcp`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
