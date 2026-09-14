# workchord_worker_role

**Entry point:** `workchord_worker_role` (`mcp`)
**Source:** [mcp_server](../modules/mcp_server.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [config](../modules/config.md), [mcp_server](../modules/mcp_server.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as workchord_worker_role
    participant p1 as _skill_bundle_prompt
    participant p2 as _agent_context
    participant p3 as _current_agent_key
    participant p4 as _http_agent_key.get
    participant p5 as os.getenv
    participant p6 as MCPAuthError
    participant p7 as _open_db_session
    participant p8 as _session_factory
    participant p9 as hasattr
    participant p10 as _authenticate_agent_key
    participant p11 as get_settings
    participant p12 as Settings
    participant p13 as AgentService(…).authenticate
    participant p14 as AgentService
    participant p15 as _require_scope_requirement
    participant p16 as isinstance
    participant p17 as require_scope
    participant p18 as actor_has_scope
    participant p19 as actor_scopes
    participant p20 as AgentPermissionError
    participant p21 as any
    participant p22 as ', '.join
    participant p23 as _skill_bundle_scope_requirement
    p0->>p1: _skill_bundle_prompt
    p1->>p2: _agent_context
    p2->>p3: _current_agent_key
    p3-->>p4: _http_agent_key.get
    p3-->>p5: os.getenv
    p2->>p6: MCPAuthError
    p2->>p7: _open_db_session
    p7-->>p8: _session_factory
    p7-->>p9: hasattr
    p2->>p10: _authenticate_agent_key
    p10->>p11: get_settings
    p11->>p12: Settings
    p10->>p6: MCPAuthError
    p10-->>p13: AgentService(…).authenticate
    p10->>p14: AgentService
    p10->>p6: MCPAuthError
    p10->>p6: MCPAuthError
    p2->>p15: _require_scope_requirement
    p15-->>p16: isinstance
    p15->>p17: require_scope
    p17->>p18: actor_has_scope
    p18->>p19: actor_scopes
    p17->>p20: AgentPermissionError
    p15-->>p21: any
    p15->>p18: actor_has_scope
    p15->>p20: AgentPermissionError
    p15-->>p22: ', '.join
    p1->>p23: _skill_bundle_scope_requirement
    p23->>p11: get_settings
```

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. workchord_worker_role"]
    s2["2. _skill_bundle_prompt"]
    s3["3. _agent_context"]
    s4["4. _current_agent_key"]
    s5["5. _http_agent_key.get"]
    s6["6. os.getenv"]
    s7["7. MCPAuthError"]
    s8["8. _open_db_session"]
    s9["9. _session_factory"]
    s10["10. hasattr"]
    s11["11. _authenticate_agent_key"]
    s12["12. get_settings"]
    s1 -->|"_skill_bundle_prompt(…)"| s2
    s2 -->|"_agent_context(_skill_bundle_scope_requirement(...))"| s3
    s3 -->|"_current_agent_key(data not statically known)"| s4
    s4 -. "_http_agent_key.get(data not statically known)" .-> s5
    s4 -. "os.getenv(MCP_AGENT_API_KEY_ENV)" .-> s6
    s3 -->|"MCPAuthError(...)"| s7
    s3 -->|"_open_db_session(data not statically known)"| s8
    s8 -. "_session_factory(data not statically known)" .-> s9
    s8 -. "hasattr(session_context, '__aenter__')" .-> s10
    s3 -->|"_authenticate_agent_key(db, api_key)"| s11
    s11 -->|"get_settings(data not statically known)"| s12
    b0["environment_read os.getenv"]
    s4 -. "environment_read os.getenv" .-> b0
    click s1 "../modules/mcp_server.md"
    click s2 "../modules/mcp_server.md"
    click s3 "../modules/mcp_server.md"
    click s4 "../modules/mcp_server.md"
    click s7 "../modules/mcp_server.md"
    click s8 "../modules/mcp_server.md"
    click s11 "../modules/mcp_server.md"
    click s12 "../modules/config.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `workchord_worker_role` | - | - | - | `...` |
| `_skill_bundle_prompt` | `value: str` | - | - | `value` |
| `_agent_context` | `required_scope: ScopeRequirement` | `MCP_AGENT_API_KEY_ENV` | - | - |
| `_current_agent_key` | - | `MCP_AGENT_API_KEY_ENV` | - | `...` |
| `_http_agent_key.get` | - | - | - | - |
| `os.getenv` | - | - | - | - |
| `MCPAuthError` | - | - | - | - |
| `_open_db_session` | - | - | - | `none` |
| `_session_factory` | - | - | - | - |
| `hasattr` | - | - | - | - |
| `_authenticate_agent_key` | `db: Any`, `api_key: str` | - | - | `actor` |
| `get_settings` | - | - | - | `Settings(...)` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| workchord_worker_role | _skill_bundle_prompt | 2257 | `_skill_bundle_prompt('Read workchord://agent/capabilities, resolve its recommended worker skill version, then read workchord://skill-bundles/workchord-worker/{version}/SKILL.md. Follow that skill, call workchord://agent/me/work, and execute only the exact server-selected assignment.')` |
| _skill_bundle_prompt | _agent_context | 309 | `_agent_context(_skill_bundle_scope_requirement(...))` |
| _agent_context | _current_agent_key | 227 | `_current_agent_key(data not statically known)` |
| _current_agent_key | _http_agent_key.get | 180 | `_http_agent_key.get(data not statically known)` |
| _current_agent_key | os.getenv | 180 | `os.getenv(MCP_AGENT_API_KEY_ENV)` |
| _agent_context | MCPAuthError | 229 | `MCPAuthError(...)` |
| _agent_context | _open_db_session | 230 | `_open_db_session(data not statically known)` |
| _open_db_session | _session_factory | 161 | `_session_factory(data not statically known)` |
| _open_db_session | hasattr | 162 | `hasattr(session_context, '__aenter__')` |
| _agent_context | _authenticate_agent_key | 231 | `_authenticate_agent_key(db, api_key)` |
| _authenticate_agent_key | get_settings | 185 | `get_settings(data not statically known)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| environment_read | `os.getenv` | `_current_agent_key` | 180 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `_open_db_session` | `_session_factory` | 161 |
| external_call | `_open_db_session` | `hasattr` | 162 |
| step_limit | `workchord_worker_role` | `first 12 steps` | 0 |
| truncated_flow | `workchord_worker_role` | `depth limit` | 0 |

## Behavior

This flow starts at `workchord_worker_role` and is classified as `mcp`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
