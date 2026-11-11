# task_routing_assessment_resource

**Entry point:** `task_routing_assessment_resource` (`mcp`)
**Source:** [mcp_server](../modules/mcp_server.md)
**Modules touched:** [agent_routing](../modules/agent_routing.md), [agent_routing_service](../modules/agent_routing_service.md), [agent_service](../modules/agent_service.md), [authority](../modules/authority.md), and 13 more

**Complete modules touched:**

- [agent_routing](../modules/agent_routing.md)
- [agent_routing_service](../modules/agent_routing_service.md)
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
- [task_brief_service](../modules/task_brief_service.md)
- [task_service](../modules/task_service.md)
- [time](../modules/time.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as task_routing_assessment_resource
    participant p1 as _json_resource
    participant p2 as get_task_routing_assessment
    participant p3 as _tool_call
    participant p4 as AgentRoutingService.get_assessment_state
    participant p5 as enforce_mcp_access
    participant p6 as AgentRoutingService._require_read
    participant p7 as _agent_context
    participant p8 as get_settings
    participant p9 as command_transaction
    participant p10 as _authenticate_agent_key
    participant p11 as _require_scope_requirement
    participant p12 as IdentityService.actor_context
    participant p13 as require_scope
    participant p14 as AgentService.authenticate
    participant p15 as require_identity_writes
    participant p16 as DeliveryDependencyService.reconcile
    participant p17 as IdentityService.context
    participant p18 as DiscussionService.enqueue
    participant p19 as AgentRoutingService
    participant p20 as AgentRoutingService._task_version
    participant p21 as AgentRoutingService._assessment_rows
    participant p22 as TaskRoutingAssessmentResponse.from_record
    participant p23 as _structured_tool_error
    participant p24 as TaskRoutingAssessmentState
    participant p25 as _current_agent_key
    participant p26 as scope_requirement_is_mutating
    participant p27 as MCPAuthError
    participant p28 as actor_has_scope
    participant p29 as int (backend/app/mcp_server.py…uting_assessment_resource)
    participant p30 as state.model_dump
    p0->>p1: _json_resource
    p0->>p2: get_task_routing_assessment
    p1->>p3: _tool_call
    p2->>p4: AgentRoutingService.get_assessment_state
    p3->>p5: enforce_mcp_access
    p4->>p6: AgentRoutingService._require_read
    p3->>p7: _agent_context
    p5->>p8: get_settings
    p7->>p9: command_transaction
    p7->>p10: _authenticate_agent_key
    p7->>p11: _require_scope_requirement
    p7->>p12: IdentityService.actor_context
    p11->>p13: require_scope
    p10->>p14: AgentService.authenticate
    p12->>p15: require_identity_writes
    p9->>p16: DeliveryDependencyService.reconcile
    p12->>p17: IdentityService.context
    p9->>p18: DiscussionService.enqueue
    p2->>p19: AgentRoutingService
    p4->>p20: AgentRoutingService._task_version
    p4->>p21: AgentRoutingService._assessment_rows
    p4->>p22: TaskRoutingAssessmentResponse.from_record
    p3->>p23: _structured_tool_error
    p4->>p24: TaskRoutingAssessmentState
    p7->>p25: _current_agent_key
    p5->>p26: scope_requirement_is_mutating
    p7->>p27: MCPAuthError
    p6->>p28: actor_has_scope
    p0-->>p29: int (backend/app/mcp_server.py…uting_assessment_resource)(task_id)
    p2-->>p30: state.model_dump(mode='json')
```

> Call sequence diagram shows 30 of 241 interactions; 211 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 72 (71 omitted); unresolved 1 of 96 (95 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/config.py:get_settings` | 5 | [backend/app/config.py](../modules/config.md) | internal | 1 |
| `backend/app/maintenance.py:scope_requirement_is_mutating` | 7 | - | external | 4 |
| `backend/app/maintenance.py:scope_requirement_is_mutating` | 7 | - | unresolved | 3 |
| `backend/app/maintenance.py:enforce_mcp_access` | 4 | [backend/app/maintenance.py](../modules/maintenance.md) | internal | 1 |
| `backend/app/mcp_server.py:_current_agent_key` | 17 | - | unresolved | 1 |
| `backend/app/mcp_server.py:_current_agent_key` | 17 | - | external | 1 |
| `backend/app/mcp_server.py:_agent_context` | 16 | [backend/app/mcp_server.py](../modules/mcp_server.md) | internal | 1 |
| `backend/app/mcp_server.py:_open_db_session` | 21 | - | unresolved | 1 |
> Omission summary shows 8 of 68 groups; 60 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 74; effect analysis evaluated: 48, partial: 2, unavailable: 24. Counts include steps omitted from the displayed trace.

Collector observations for 50 source steps with known totals: observed: 210, emitted: 200, omitted: 10. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `task_routing_assessment_resource` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `_json_resource` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
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

```mermaid
flowchart LR
    s1["1. task_routing_assessment_resource"]
    s2["2. _json_resource"]
    s3["3. _tool_call"]
    s4["4. enforce_mcp_access"]
    s5["5. get_settings"]
    s6["6. Settings"]
    s7["7. scope_requirement_is_mutating"]
    s8["8. isinstance (backend/app/maintenance.p…e_requirement_is_mutating)"]
    s9["9. tuple"]
    s10["10. any (backend/app/maintenance.p…e_requirement_is_mutating)"]
    s11["11. scope.endswith"]
    s12["12. any (backend/app/maintenance.p…e_requirement_is_mutating)"]
    s1 -->|"_json_resource(ROUTING_READ_SCOPE_REQUIREMENT, ...)"| s2
    s2 -->|"_tool_call(required_scope, func)"| s3
    s3 -->|"enforce_mcp_access(required_scope)"| s4
    s4 -->|"get_settings(data not statically known)"| s5
    s5 -->|"Settings(data not statically known)"| s6
    s4 -->|"scope_requirement_is_mutating(required_scope)"| s7
    s7 -. "isinstance (backend/app/maintenance.p…e_requirement_is_mutating)(required_scope, str)" .-> s8
    s7 -. "tuple(required_scope)" .-> s9
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
| `task_routing_assessment_resource` | `task_id: str` | `ROUTING_READ_SCOPE_REQUIREMENT` | - | `...` |
| `_json_resource` | `required_scope: ScopeRequirement`, `func: Callable[[Any, AgentActor], Any]` | - | - | `json.dumps(...)` |
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

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| task_routing_assessment_resource | _json_resource | 2205 | `_json_resource(ROUTING_READ_SCOPE_REQUIREMENT, ...)` |
| _json_resource | _tool_call | 332 | `_tool_call(required_scope, func)` |
| _tool_call | enforce_mcp_access | 303 | `enforce_mcp_access(required_scope)` |
| enforce_mcp_access | get_settings | 112 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| enforce_mcp_access | scope_requirement_is_mutating | 113 | `scope_requirement_is_mutating(required_scope)` |
| scope_requirement_is_mutating | isinstance (backend/app/maintenance.p…e_requirement_is_mutating) | 100 | `isinstance(required_scope, str)` |
| scope_requirement_is_mutating | tuple | 100 | `tuple(required_scope)` |
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
| step_limit | `task_routing_assessment_resource` | `first 12 steps` | 0 |
| truncated_flow | `task_routing_assessment_resource` | `depth limit` | 0 |

## Behavior

This flow starts at `task_routing_assessment_resource` and is classified as `mcp`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
