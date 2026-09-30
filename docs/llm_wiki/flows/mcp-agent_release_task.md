# agent_release_task

**Entry point:** `agent_release_task` (`mcp`)
**Source:** [mcp_server](../modules/mcp_server.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [commands](../modules/commands.md), [config](../modules/config.md), [identity_service](../modules/identity_service.md), and 3 more

**Complete modules touched:**

- [agent_service](../modules/agent_service.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [identity_service](../modules/identity_service.md)
- [maintenance](../modules/maintenance.md)
- [mcp_agent_tools](../modules/mcp_agent_tools.md)
- [mcp_server](../modules/mcp_server.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as agent_release_task
    participant p1 as _tool_call
    participant p2 as enforce_mcp_access
    participant p3 as get_settings
    participant p4 as Settings
    participant p5 as scope_requirement_is_mutating
    participant p6 as isinstance (backend/app/maintenance.p…pe_requirement_is_mutating)
    participant p7 as tuple
    participant p8 as any (backend/app/maintenance.p…pe_requirement_is_mutating)
    participant p9 as scope.endswith
    participant p10 as MaintenanceModeError
    participant p11 as _agent_context
    participant p12 as _current_agent_key
    participant p13 as _http_agent_key.get
    participant p14 as os.getenv
    participant p15 as MCPAuthError
    participant p16 as _open_db_session
    participant p17 as _session_factory
    participant p18 as hasattr
    participant p19 as command_transaction
    participant p20 as current_command
    participant p21 as getattr
    participant p22 as isinstance (backend/app/commands.py:current_command)
    participant p23 as info.get
    participant p24 as RuntimeError
    participant p25 as CommandState
    participant p26 as db.rollback
    p0->>p1: _tool_call
    p1->>p2: enforce_mcp_access
    p2->>p3: get_settings
    p3->>p4: Settings
    p2->>p5: scope_requirement_is_mutating
    p5-->>p6: isinstance (backend/app/maintenance.p…pe_requirement_is_mutating)
    p5-->>p7: tuple
    p5-->>p8: any (backend/app/maintenance.p…pe_requirement_is_mutating)
    p5-->>p9: scope.endswith
    p5-->>p8: any (backend/app/maintenance.p…pe_requirement_is_mutating)
    p5-->>p9: scope.endswith
    p5-->>p9: scope.endswith
    p2->>p10: MaintenanceModeError
    p1->>p11: _agent_context
    p11->>p12: _current_agent_key
    p12-->>p13: _http_agent_key.get
    p12-->>p14: os.getenv
    p11->>p15: MCPAuthError
    p11->>p16: _open_db_session
    p16-->>p17: _session_factory
    p16-->>p18: hasattr
    p11->>p19: command_transaction
    p19->>p20: current_command
    p20-->>p21: getattr
    p20-->>p22: isinstance (backend/app/commands.py:current_command)
    p20-->>p23: info.get
    p19-->>p24: RuntimeError
    p19->>p25: CommandState
    p19-->>p24: RuntimeError
    p19-->>p26: db.rollback
```

> Call sequence diagram shows 30 of 93 interactions; 63 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. agent_release_task"]
    s2["2. _tool_call"]
    s3["3. enforce_mcp_access"]
    s4["4. get_settings"]
    s5["5. Settings"]
    s6["6. scope_requirement_is_mutating"]
    s7["7. isinstance (backend/app/maintenance.p…pe_requirement_is_mutating)"]
    s8["8. tuple"]
    s9["9. any (backend/app/maintenance.p…pe_requirement_is_mutating)"]
    s10["10. scope.endswith"]
    s11["11. any (backend/app/maintenance.p…pe_requirement_is_mutating)"]
    s12["12. scope.endswith"]
    s1 -->|"_tool_call('tasks:write', ...)"| s2
    s2 -->|"enforce_mcp_access(required_scope)"| s3
    s3 -->|"get_settings(data not statically known)"| s4
    s4 -->|"Settings(data not statically known)"| s5
    s3 -->|"scope_requirement_is_mutating(required_scope)"| s6
    s6 -. "isinstance (backend/app/maintenance.p…pe_requirement_is_mutating)(required_scope, str)" .-> s7
    s6 -. "tuple(required_scope)" .-> s8
    s6 -. "any (backend/app/maintenance.p…pe_requirement_is_mutating)(...)" .-> s9
    s6 -. "scope.endswith(':read')" .-> s10
    s6 -. "any (backend/app/maintenance.p…pe_requirement_is_mutating)(...)" .-> s11
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
| `agent_release_task` | `task_id: int`, `idempotency_key: Optional[str]` | - | - | `...` |
| `_tool_call` | `required_scope: ScopeRequirement`, `func: Callable[[Any, AgentActor], Any]`, `preview` | `ToolError`, `AggregateVersionConflict`, `HierarchyScopeError`, `AuthorityError`, `MCPAuthError`, `MaintenanceModeError`, `AgentRoutingConflictError`, `AgentTeamSetupConflictError` | - | `...` |
| `enforce_mcp_access` | `required_scope: Any` | - | - | `none` |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `scope_requirement_is_mutating` | `required_scope: Any` | - | - | `False`, `...` |
| `isinstance (backend/app/maintenance.p…pe_requirement_is_mutating)` | - | - | - | - |
| `tuple` | - | - | - | - |
| `any (backend/app/maintenance.p…pe_requirement_is_mutating)` | - | - | - | - |
| `scope.endswith` | - | - | - | - |
| `any (backend/app/maintenance.p…pe_requirement_is_mutating)` | - | - | - | - |
| `scope.endswith` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| agent_release_task | _tool_call | 1040 | `_tool_call('tasks:write', ...)` |
| _tool_call | enforce_mcp_access | 302 | `enforce_mcp_access(required_scope)` |
| enforce_mcp_access | get_settings | 112 | `get_settings(data not statically known)` |
| get_settings | Settings | 479 | `Settings(data not statically known)` |
| enforce_mcp_access | scope_requirement_is_mutating | 113 | `scope_requirement_is_mutating(required_scope)` |
| scope_requirement_is_mutating | isinstance (backend/app/maintenance.p…pe_requirement_is_mutating) | 100 | `isinstance(required_scope, str)` |
| scope_requirement_is_mutating | tuple | 100 | `tuple(required_scope)` |
| scope_requirement_is_mutating | any (backend/app/maintenance.p…pe_requirement_is_mutating) | 101 | `any(...)` |
| scope_requirement_is_mutating | scope.endswith | 101 | `scope.endswith(':read')` |
| scope_requirement_is_mutating | any (backend/app/maintenance.p…pe_requirement_is_mutating) | 102 | `any(...)` |
| scope_requirement_is_mutating | scope.endswith | 103 | `scope.endswith(':write')` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `scope_requirement_is_mutating` | `isinstance` | 100 |
| external_call | `scope_requirement_is_mutating` | `any` | 101 |
| unresolved_call | `scope_requirement_is_mutating` | `scope.endswith` | 101 |
| external_call | `scope_requirement_is_mutating` | `any` | 102 |
| unresolved_call | `scope_requirement_is_mutating` | `scope.endswith` | 103 |
| step_limit | `agent_release_task` | `first 12 steps` | 0 |
| truncated_flow | `agent_release_task` | `depth limit` | 0 |

## Behavior

This flow starts at `agent_release_task` and is classified as `mcp`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
