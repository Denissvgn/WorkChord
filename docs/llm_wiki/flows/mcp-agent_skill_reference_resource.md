# agent_skill_reference_resource

**Entry point:** `agent_skill_reference_resource` (`mcp`)
**Source:** [mcp_server](../modules/mcp_server.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md), [authority](../modules/authority.md), [commands](../modules/commands.md), and 12 more

**Complete modules touched:**

- [agent_service](../modules/agent_service.md)
- [agent_skill_bundle_service](../modules/agent_skill_bundle_service.md)
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
    participant p0 as agent_skill_reference_resource
    participant p1 as _tool_call
    participant p2 as _skill_bundle_scope_requirement
    participant p3 as get_agent_skill_reference
    participant p4 as enforce_mcp_access
    participant p5 as _agent_context
    participant p6 as get_agent_skill_file
    participant p7 as get_settings
    participant p8 as _agent_skill_bundle_service
    participant p9 as command_transaction
    participant p10 as _authenticate_agent_key
    participant p11 as _require_scope_requirement
    participant p12 as IdentityService.actor_context
    participant p13 as require_scope
    participant p14 as AgentService.authenticate
    participant p15 as require_identity_writes
    participant p16 as DeliveryDependencyService.reconcile
    participant p17 as DiscussionService.enqueue
    participant p18 as actor_has_scope
    participant p19 as commit_or_flush
    participant p20 as DeliveryDependencyService.validate_cycles
    participant p21 as DiscussionService.recipient_authorized
    participant p22 as TaskService.reserve_task_version
    participant p23 as clear_execution_evidence
    participant p24 as _structured_tool_error
    participant p25 as _current_agent_key
    participant p26 as scope_requirement_is_mutating
    participant p27 as MCPAuthError
    participant p28 as MaintenanceModeError
    participant p29 as LookupError (backend/app/mcp_agent_too…get_agent_skill_reference)
    participant p30 as reference_name.endswith
    p0->>p1: _tool_call
    p0->>p2: _skill_bundle_scope_requirement
    p0->>p3: get_agent_skill_reference
    p1->>p4: enforce_mcp_access
    p1->>p5: _agent_context
    p3->>p6: get_agent_skill_file
    p4->>p7: get_settings
    p6->>p8: _agent_skill_bundle_service
    p5->>p9: command_transaction
    p5->>p10: _authenticate_agent_key
    p5->>p11: _require_scope_requirement
    p5->>p12: IdentityService.actor_context
    p11->>p13: require_scope
    p10->>p14: AgentService.authenticate
    p12->>p15: require_identity_writes
    p9->>p16: DeliveryDependencyService.reconcile
    p9->>p17: DiscussionService.enqueue
    p13->>p18: actor_has_scope
    p14->>p19: commit_or_flush
    p16->>p20: DeliveryDependencyService.validate_cycles
    p17->>p21: DiscussionService.recipient_authorized
    p16->>p22: TaskService.reserve_task_version
    p16->>p23: clear_execution_evidence
    p1->>p24: _structured_tool_error
    p5->>p25: _current_agent_key
    p4->>p26: scope_requirement_is_mutating
    p5->>p27: MCPAuthError
    p4->>p28: MaintenanceModeError
    p3-->>p29: LookupError (backend/app/mcp_agent_too…get_agent_skill_reference)('Agent skill reference was not found')
    p3-->>p30: reference_name.endswith('.md')
```

> Call sequence diagram shows 30 of 262 interactions; 232 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 75 (74 omitted); unresolved 1 of 107 (106 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/config.py:get_settings` | 4 | [backend/app/config.py](../modules/config.md) | internal | 1 |
| `backend/app/maintenance.py:scope_requirement_is_mutating` | 6 | - | external | 4 |
| `backend/app/maintenance.py:scope_requirement_is_mutating` | 6 | - | unresolved | 3 |
| `backend/app/mcp_server.py:_current_agent_key` | 16 | - | unresolved | 1 |
| `backend/app/mcp_server.py:_current_agent_key` | 16 | - | external | 1 |
| `backend/app/mcp_server.py:_agent_context` | 15 | [backend/app/mcp_server.py](../modules/mcp_server.md) | internal | 1 |
| `backend/app/mcp_server.py:_open_db_session` | 20 | - | unresolved | 1 |
| `backend/app/mcp_server.py:_open_db_session` | 20 | - | external | 1 |
> Omission summary shows 8 of 78 groups; 70 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 81; effect analysis evaluated: 54, partial: 2, unavailable: 25. Counts include steps omitted from the displayed trace.

Collector observations for 56 source steps with known totals: observed: 231, emitted: 221, omitted: 10. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `agent_skill_reference_resource` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
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
    s1["1. agent_skill_reference_resource"]
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
    s1 -->|"_tool_call(_skill_bundle_scope_requirement(...), ...)"| s2
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
| `agent_skill_reference_resource` | `skill_name: str`, `skill_version: str`, `reference_name: str` | - | - | `...` |
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
| agent_skill_reference_resource | _tool_call | 2323 | `_tool_call(_skill_bundle_scope_requirement(...), ...)` |
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
| step_limit | `agent_skill_reference_resource` | `first 12 steps` | 0 |
| truncated_flow | `agent_skill_reference_resource` | `depth limit` | 0 |

## Behavior

This flow starts at `agent_skill_reference_resource` and is classified as `mcp`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
