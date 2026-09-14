# profile_skill_catalog_resource

**Entry point:** `profile_skill_catalog_resource` (`mcp`)
**Source:** [mcp_server](../modules/mcp_server.md)
**Modules touched:** [agent_profile_catalog_service](../modules/agent_profile_catalog_service.md), [agent_service](../modules/agent_service.md), [config](../modules/config.md), [maintenance](../modules/maintenance.md), and 2 more

**Complete modules touched:**

- [agent_profile_catalog_service](../modules/agent_profile_catalog_service.md)
- [agent_service](../modules/agent_service.md)
- [config](../modules/config.md)
- [maintenance](../modules/maintenance.md)
- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [mcp_server](../modules/mcp_server.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as profile_skill_catalog_resource
    participant p1 as _json_resource
    participant p2 as _tool_call
    participant p3 as enforce_mcp_access
    participant p4 as get_settings
    participant p5 as Settings
    participant p6 as scope_requirement_is_mutating
    participant p7 as isinstance (backend/app/maintenance.p…pe_requirement_is_mutating)
    participant p8 as tuple
    participant p9 as any (backend/app/maintenance.p…pe_requirement_is_mutating)
    participant p10 as scope.endswith
    participant p11 as MaintenanceModeError
    participant p12 as _agent_context
    participant p13 as _current_agent_key
    participant p14 as _http_agent_key.get
    participant p15 as os.getenv
    participant p16 as MCPAuthError
    participant p17 as _open_db_session
    participant p18 as _session_factory
    participant p19 as hasattr
    participant p20 as _authenticate_agent_key
    participant p21 as AgentService(…).authenticate
    participant p22 as AgentService
    participant p23 as _require_scope_requirement
    p0->>p1: _json_resource
    p1->>p2: _tool_call
    p2->>p3: enforce_mcp_access
    p3->>p4: get_settings
    p4->>p5: Settings
    p3->>p6: scope_requirement_is_mutating
    p6-->>p7: isinstance (backend/app/maintenance.p…pe_requirement_is_mutating)
    p6-->>p8: tuple
    p6-->>p9: any (backend/app/maintenance.p…pe_requirement_is_mutating)
    p6-->>p10: scope.endswith
    p6-->>p9: any (backend/app/maintenance.p…pe_requirement_is_mutating)
    p6-->>p10: scope.endswith
    p6-->>p10: scope.endswith
    p3->>p11: MaintenanceModeError
    p2->>p12: _agent_context
    p12->>p13: _current_agent_key
    p13-->>p14: _http_agent_key.get
    p13-->>p15: os.getenv
    p12->>p16: MCPAuthError
    p12->>p17: _open_db_session
    p17-->>p18: _session_factory
    p17-->>p19: hasattr
    p12->>p20: _authenticate_agent_key
    p20->>p4: get_settings
    p20->>p16: MCPAuthError
    p20-->>p21: AgentService(…).authenticate
    p20->>p22: AgentService
    p20->>p16: MCPAuthError
    p20->>p16: MCPAuthError
    p12->>p23: _require_scope_requirement
```

> Call sequence diagram shows 30 of 73 interactions; 43 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. profile_skill_catalog_resource"]
    s2["2. _json_resource"]
    s3["3. _tool_call"]
    s4["4. enforce_mcp_access"]
    s5["5. get_settings"]
    s6["6. Settings"]
    s7["7. scope_requirement_is_mutating"]
    s8["8. isinstance (backend/app/maintenance.p…pe_requirement_is_mutating)"]
    s9["9. tuple"]
    s10["10. any (backend/app/maintenance.p…pe_requirement_is_mutating)"]
    s11["11. scope.endswith"]
    s12["12. any (backend/app/maintenance.p…pe_requirement_is_mutating)"]
    s1 -->|"_json_resource((...), ...)"| s2
    s2 -->|"_tool_call(required_scope, func)"| s3
    s3 -->|"enforce_mcp_access(required_scope)"| s4
    s4 -->|"get_settings(data not statically known)"| s5
    s5 -->|"Settings(data not statically known)"| s6
    s4 -->|"scope_requirement_is_mutating(required_scope)"| s7
    s7 -. "isinstance (backend/app/maintenance.p…pe_requirement_is_mutating)(required_scope, str)" .-> s8
    s7 -. "tuple(required_scope)" .-> s9
    s7 -. "any (backend/app/maintenance.p…pe_requirement_is_mutating)(...)" .-> s10
    s7 -. "scope.endswith(':read')" .-> s11
    s7 -. "any (backend/app/maintenance.p…pe_requirement_is_mutating)(...)" .-> s12
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
| `profile_skill_catalog_resource` | - | - | - | `...` |
| `_json_resource` | `required_scope: ScopeRequirement`, `func: Callable[[Any, AgentActor], Any]` | - | - | `json.dumps(...)` |
| `_tool_call` | `required_scope: ScopeRequirement`, `func: Callable[[Any, AgentActor], Any]` | `ToolError`, `MCPAuthError`, `MaintenanceModeError`, `AgentRoutingConflictError`, `AgentTeamSetupConflictError`, `AgentModelConflictError`, `AgentConflictError`, `AgentPermissionError` | - | `...` |
| `enforce_mcp_access` | `required_scope: Any` | - | - | `none` |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `scope_requirement_is_mutating` | `required_scope: Any` | - | - | `False`, `...` |
| `isinstance (backend/app/maintenance.p…pe_requirement_is_mutating)` | - | - | - | - |
| `tuple` | - | - | - | - |
| `any (backend/app/maintenance.p…pe_requirement_is_mutating)` | - | - | - | - |
| `scope.endswith` | - | - | - | - |
| `any (backend/app/maintenance.p…pe_requirement_is_mutating)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| profile_skill_catalog_resource | _json_resource | 2165 | `_json_resource((...), ...)` |
| _json_resource | _tool_call | 303 | `_tool_call(required_scope, func)` |
| _tool_call | enforce_mcp_access | 278 | `enforce_mcp_access(required_scope)` |
| enforce_mcp_access | get_settings | 112 | `get_settings(data not statically known)` |
| get_settings | Settings | 469 | `Settings(data not statically known)` |
| enforce_mcp_access | scope_requirement_is_mutating | 113 | `scope_requirement_is_mutating(required_scope)` |
| scope_requirement_is_mutating | isinstance (backend/app/maintenance.p…pe_requirement_is_mutating) | 100 | `isinstance(required_scope, str)` |
| scope_requirement_is_mutating | tuple | 100 | `tuple(required_scope)` |
| scope_requirement_is_mutating | any (backend/app/maintenance.p…pe_requirement_is_mutating) | 101 | `any(...)` |
| scope_requirement_is_mutating | scope.endswith | 101 | `scope.endswith(':read')` |
| scope_requirement_is_mutating | any (backend/app/maintenance.p…pe_requirement_is_mutating) | 102 | `any(...)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `scope_requirement_is_mutating` | `isinstance` | 100 |
| external_call | `scope_requirement_is_mutating` | `any` | 101 |
| unresolved_call | `scope_requirement_is_mutating` | `scope.endswith` | 101 |
| external_call | `scope_requirement_is_mutating` | `any` | 102 |
| step_limit | `profile_skill_catalog_resource` | `first 12 steps` | 0 |
| truncated_flow | `profile_skill_catalog_resource` | `depth limit` | 0 |

## Behavior

This flow starts at `profile_skill_catalog_resource` and is classified as `mcp`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
