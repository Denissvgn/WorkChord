# workchord_pm_role

**Entry point:** `workchord_pm_role` (`mcp`)
**Source:** [mcp_server](../modules/mcp_server.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [commands](../modules/commands.md), [config](../modules/config.md), [delivery_dependency_service](../modules/delivery_dependency_service.md), and 3 more

**Complete modules touched:**

- [agent_service](../modules/agent_service.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [delivery_dependency_service](../modules/delivery_dependency_service.md)
- [discussion_service](../modules/discussion_service.md)
- [identity_service](../modules/identity_service.md)
- [mcp_server](../modules/mcp_server.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as workchord_pm_role
    participant p1 as _skill_bundle_prompt
    participant p2 as _agent_context
    participant p3 as _current_agent_key
    participant p4 as _http_agent_key.get
    participant p5 as os.getenv
    participant p6 as MCPAuthError
    participant p7 as _open_db_session
    participant p8 as _session_factory
    participant p9 as hasattr
    participant p10 as command_transaction
    participant p11 as current_command
    participant p12 as getattr
    participant p13 as isinstance (backend/app/commands.py:current_command)
    participant p14 as info.get
    participant p15 as RuntimeError
    participant p16 as CommandState
    participant p17 as db.flush
    participant p18 as db.info.get
    participant p19 as DeliveryDependencyService(…).reconcile
    participant p20 as DeliveryDependencyService
    participant p21 as sorted
    participant p22 as db.info.pop
    participant p23 as set
    participant p24 as DiscussionService(…).enqueue
    participant p25 as DiscussionService
    participant p26 as db.rollback
    participant p27 as db.commit
    p0->>p1: _skill_bundle_prompt
    p1->>p2: _agent_context
    p2->>p3: _current_agent_key
    p3-->>p4: _http_agent_key.get
    p3-->>p5: os.getenv
    p2->>p6: MCPAuthError
    p2->>p7: _open_db_session
    p7-->>p8: _session_factory
    p7-->>p9: hasattr
    p2->>p10: command_transaction
    p10->>p11: current_command
    p11-->>p12: getattr
    p11-->>p13: isinstance (backend/app/commands.py:current_command)
    p11-->>p14: info.get
    p10-->>p15: RuntimeError
    p10->>p16: CommandState
    p10-->>p15: RuntimeError
    p10-->>p17: db.flush
    p10-->>p18: db.info.get
    p10-->>p18: db.info.get
    p10-->>p18: db.info.get
    p10-->>p19: DeliveryDependencyService(…).reconcile
    p10->>p20: DeliveryDependencyService
    p10-->>p21: sorted
    p10-->>p22: db.info.pop
    p10-->>p23: set
    p10-->>p24: DiscussionService(…).enqueue
    p10->>p25: DiscussionService
    p10-->>p26: db.rollback
    p10-->>p27: db.commit
```

> Call sequence diagram shows 30 of 57 interactions; 27 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. workchord_pm_role"]
    s2["2. _skill_bundle_prompt"]
    s3["3. _agent_context"]
    s4["4. _current_agent_key"]
    s5["5. _http_agent_key.get"]
    s6["6. os.getenv"]
    s7["7. MCPAuthError"]
    s8["8. _open_db_session"]
    s9["9. _session_factory"]
    s10["10. hasattr"]
    s11["11. command_transaction"]
    s12["12. current_command"]
    s1 -->|"_skill_bundle_prompt(…)"| s2
    s2 -->|"_agent_context(_skill_bundle_scope_requirement(...))"| s3
    s3 -->|"_current_agent_key(data not statically known)"| s4
    s4 -. "_http_agent_key.get(data not statically known)" .-> s5
    s4 -. "os.getenv(MCP_AGENT_API_KEY_ENV)" .-> s6
    s3 -->|"MCPAuthError(...)"| s7
    s3 -->|"_open_db_session(data not statically known)"| s8
    s8 -. "_session_factory(data not statically known)" .-> s9
    s8 -. "hasattr(session_context, '__aenter__')" .-> s10
    s3 -->|"command_transaction(db, mode=...)"| s11
    s11 -->|"current_command(db)"| s12
    b0["environment_read os.getenv"]
    s4 -. "environment_read os.getenv" .-> b0
    b1["mutation db.info.pop"]
    s11 -. "mutation db.info.pop" .-> b1
    b2["mutation db.info.pop"]
    s11 -. "mutation db.info.pop" .-> b2
    b3["mutation db.info.pop"]
    s11 -. "mutation db.info.pop" .-> b3
    b4["mutation db.info.pop"]
    s11 -. "mutation db.info.pop" .-> b4
    click s1 "../modules/mcp_server.md"
    click s2 "../modules/mcp_server.md"
    click s3 "../modules/mcp_server.md"
    click s4 "../modules/mcp_server.md"
    click s7 "../modules/mcp_server.md"
    click s8 "../modules/mcp_server.md"
    click s11 "../modules/commands.md"
    click s12 "../modules/commands.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
    class b4 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `workchord_pm_role` | - | - | - | `...` |
| `_skill_bundle_prompt` | `value: str` | - | - | `value` |
| `_agent_context` | `required_scope: ScopeRequirement`, `preview` | `MCP_AGENT_API_KEY_ENV` | `db.info[...]` | - |
| `_current_agent_key` | - | `MCP_AGENT_API_KEY_ENV` | - | `...` |
| `_http_agent_key.get` | - | - | - | - |
| `os.getenv` | - | - | - | - |
| `MCPAuthError` | - | - | - | - |
| `_open_db_session` | - | - | - | `none` |
| `_session_factory` | - | - | - | - |
| `hasattr` | - | - | - | - |
| `command_transaction` | `db: AsyncSession`, `mode`, `commit` | - | `previous.failed`, `db.info[...]` | `none` |
| `current_command` | `db` | - | - | `...` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| workchord_pm_role | _skill_bundle_prompt | 2327 | `_skill_bundle_prompt('Read workchord://agent/capabilities, resolve its recommended PM skill version, then read workchord://skill-bundles/workchord-pm/{version}/SKILL.md. Follow that controller skill and its referenced files; do not infer authority from profile capability matches.')` |
| _skill_bundle_prompt | _agent_context | 338 | `_agent_context(_skill_bundle_scope_requirement(...))` |
| _agent_context | _current_agent_key | 247 | `_current_agent_key(data not statically known)` |
| _current_agent_key | _http_agent_key.get | 200 | `_http_agent_key.get(data not statically known)` |
| _current_agent_key | os.getenv | 200 | `os.getenv(MCP_AGENT_API_KEY_ENV)` |
| _agent_context | MCPAuthError | 249 | `MCPAuthError(...)` |
| _agent_context | _open_db_session | 250 | `_open_db_session(data not statically known)` |
| _open_db_session | _session_factory | 181 | `_session_factory(data not statically known)` |
| _open_db_session | hasattr | 182 | `hasattr(session_context, '__aenter__')` |
| _agent_context | command_transaction | 251 | `command_transaction(db, mode=...)` |
| command_transaction | current_command | 87 | `current_command(db)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| environment_read | `os.getenv` | `_current_agent_key` | 200 |
| mutation | `db.info.pop` | `command_transaction` | 107 |
| mutation | `db.info.pop` | `command_transaction` | 120 |
| mutation | `db.info.pop` | `command_transaction` | 121 |
| mutation | `db.info.pop` | `command_transaction` | 123 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `_open_db_session` | `_session_factory` | 181 |
| external_call | `_open_db_session` | `hasattr` | 182 |
| step_limit | `workchord_pm_role` | `first 12 steps` | 0 |
| truncated_flow | `workchord_pm_role` | `depth limit` | 0 |

## Behavior

This flow starts at `workchord_pm_role` and is classified as `mcp`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
