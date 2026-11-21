# mcp_server

**Entry point:** `main` (`process`)
**Source:** [mcp_server](../modules/mcp_server.md)
**Modules touched:** [agent_key_file](../modules/agent_key_file.md), [app_database](../modules/app_database.md), [config](../modules/config.md), [database_config](../modules/database_config.md), and 2 more

**Complete modules touched:**

- [agent_key_file](../modules/agent_key_file.md)
- [app_database](../modules/app_database.md)
- [config](../modules/config.md)
- [database_config](../modules/database_config.md)
- [mcp_server](../modules/mcp_server.md)
- [upgrade_service](../modules/upgrade_service.md)

**Related modules:** [agent_key_file](../modules/agent_key_file.md), [agent_model_catalog_service](../modules/agent_model_catalog_service.md), [agent_routing_service](../modules/agent_routing_service.md), and 17 more

**Complete related modules:**

- [agent_key_file](../modules/agent_key_file.md)
- [agent_model_catalog_service](../modules/agent_model_catalog_service.md)
- [agent_routing_service](../modules/agent_routing_service.md)
- [agent_service](../modules/agent_service.md)
- [agent_team_setup_service](../modules/agent_team_setup_service.md)
- [app_database](../modules/app_database.md)
- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [execution_reconciliation](../modules/execution_reconciliation.md)
- [http_authority](../modules/http_authority.md)
- [identity_service](../modules/identity_service.md)
- [maintenance](../modules/maintenance.md)
- [models_agent](../modules/models_agent.md)
- [mutation_versions](../modules/mutation_versions.md)
- [planning_window_reconciliation](../modules/planning_window_reconciliation.md)
- [retained_planning_output](../modules/retained_planning_output.md)
- [schemas_agent](../modules/schemas_agent.md)
- [task_service](../modules/task_service.md)
- [triage_service](../modules/triage_service.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as _load_stdio_agent_key
    participant p2 as init_db
    participant p3 as _run_standalone_transport
    participant p4 as assert_database_current
    participant p5 as read_agent_key_file
    participant p6 as inspect_database
    participant p7 as _inspect_database_connection
    participant p8 as _sync_engine
    participant p9 as database_configuration
    participant p10 as head_revision
    participant p11 as close_database
    participant p12 as UpgradeError
    participant p13 as AgentKeyFileError
    participant p14 as _current_revision
    participant p15 as DatabaseStatus
    participant p16 as parse_database_configuration
    participant p17 as alembic_config
    participant p18 as get_settings
    participant p19 as argparse.ArgumentParser
    participant p20 as parser.add_argument
    participant p21 as parser.parse_args
    participant p22 as print
    participant p23 as str
    participant p24 as SystemExit
    participant p25 as redirect_stdout
    participant p26 as asyncio.run
    p0->>p1: _load_stdio_agent_key
    p0->>p2: init_db
    p0->>p3: _run_standalone_transport
    p2->>p4: assert_database_current
    p1->>p5: read_agent_key_file
    p4->>p6: inspect_database
    p6->>p7: _inspect_database_connection
    p6->>p8: _sync_engine
    p8->>p9: database_configuration
    p7->>p10: head_revision
    p3->>p11: close_database
    p4->>p12: UpgradeError
    p5->>p13: AgentKeyFileError
    p7->>p14: _current_revision
    p7->>p15: DatabaseStatus
    p9->>p16: parse_database_configuration
    p10->>p17: alembic_config
    p9->>p18: get_settings
    p0-->>p19: argparse.ArgumentParser(description='Run WorkChord MCP server')
    p0-->>p20: parser.add_argument('--transport', choices=[...], default='stdio', help='MCP transport to run')
    p0-->>p21: parser.parse_args(argv)
    p0-->>p22: print(str(...), file=sys.stderr)
    p0-->>p23: str(exc)
    p0-->>p24: SystemExit(2)
    p0-->>p22: print(..., file=sys.stderr)
    p0-->>p24: SystemExit(2)
    p0-->>p25: redirect_stdout(sys.stderr)
    p0-->>p26: asyncio.run(init_db(...))
    p0-->>p26: asyncio.run(init_db(...))
    p0-->>p26: asyncio.run(_run_standalone_transport(...))
```

> Call sequence diagram shows 30 of 73 interactions; 43 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 10 of 27 (17 omitted); unresolved 2 of 20 (18 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/mcp_server.py:_load_stdio_agent_key` | 5 | - | external | 2 |
| `backend/app/agent_key_file.py:read_agent_key_file` | 8 | - | unresolved | 6 |
| `backend/app/agent_key_file.py:read_agent_key_file` | 8 | - | external | 3 |
| `backend/app/agent_key_file.py:read_agent_key_file` | 8 | [backend/app/agent_key_file.py](../modules/agent_key_file.md) | internal | 5 |
| `backend/app/services/upgrade_service.py:_inspect_database_connection` | 34 | - | external | 4 |
| `backend/app/services/upgrade_service.py:_inspect_database_connection` | 34 | - | unresolved | 1 |
| `backend/app/services/upgrade_service.py:_current_revision` | 38 | - | external | 4 |
| `backend/app/services/upgrade_service.py:_current_revision` | 38 | - | unresolved | 4 |
> Omission summary shows 8 of 17 groups; 9 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 27; effect analysis evaluated: 18, partial: 0, unavailable: 9. Counts include steps omitted from the displayed trace.

Collector observations for 18 source steps with known totals: observed: 55, emitted: 55, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `9` | `9` | `0` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.parse_args` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_load_stdio_agent_key` | `available` | `evaluated` | `available` | `8` | `8` | `0` |
| `os.getenv` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `os.getenv` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `read_agent_key_file` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `Path(…).expanduser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `Path` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `location.stat` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `AgentKeyFileError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. argparse.ArgumentParser"]
    s3["3. parser.add_argument"]
    s4["4. parser.parse_args"]
    s5["5. _load_stdio_agent_key"]
    s6["6. os.getenv"]
    s7["7. os.getenv"]
    s8["8. read_agent_key_file"]
    s9["9. Path(…).expanduser"]
    s10["10. Path"]
    s11["11. location.stat"]
    s12["12. AgentKeyFileError"]
    s1 -. "argparse.ArgumentParser(description='Run WorkChord MCP server')" .-> s2
    s1 -. "parser.add_argument('--transport', choices=[...], default='stdio', help='MCP transport to run')" .-> s3
    s1 -. "parser.parse_args(argv)" .-> s4
    s1 -->|"_load_stdio_agent_key(data not statically known)"| s5
    s5 -. "os.getenv(MCP_AGENT_API_KEY_ENV)" .-> s6
    s5 -. "os.getenv(MCP_AGENT_API_KEY_FILE_ENV)" .-> s7
    s5 -->|"read_agent_key_file(key_file)"| s8
    s8 -. "Path(…).expanduser(data not statically known)" .-> s9
    s8 -. "Path(path)" .-> s10
    s8 -. "location.stat(data not statically known)" .-> s11
    s8 -->|"AgentKeyFileError(...)"| s12
    b0["output print"]
    s1 -. "output print" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["environment_read os.getenv"]
    s5 -. "environment_read os.getenv" .-> b2
    b3["environment_read os.getenv"]
    s5 -. "environment_read os.getenv" .-> b3
    b4["filesystem_read location.read_text"]
    s8 -. "filesystem_read location.read_text" .-> b4
    click s1 "../modules/mcp_server.md"
    click s5 "../modules/mcp_server.md"
    click s8 "../modules/agent_key_file.md"
    click s12 "../modules/agent_key_file.md"
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
| `main` | `argv: Optional[list[str]]` | `AgentKeyFileError`, `sys`, `MCP_AGENT_API_KEY_ENV`, `MCP_AGENT_API_KEY_FILE_ENV`, `sys`, `sys` | - | - |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `_load_stdio_agent_key` | - | `MCP_AGENT_API_KEY_ENV`, `MCP_AGENT_API_KEY_FILE_ENV` | `_stdio_file_agent_key` | `True`, `False`, `True` |
| `os.getenv` | - | - | - | - |
| `os.getenv` | - | - | - | - |
| `read_agent_key_file` | `path: str \| os.PathLike[str]` | `os` | - | `lines[...]` |
| `Path(…).expanduser` | - | - | - | - |
| `Path` | - | - | - | - |
| `location.stat` | - | - | - | - |
| `AgentKeyFileError` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 2542 | `argparse.ArgumentParser(description='Run WorkChord MCP server')` |
| main | parser.add_argument | 2543 | `parser.add_argument('--transport', choices=[...], default='stdio', help='MCP transport to run')` |
| main | parser.parse_args | 2549 | `parser.parse_args(argv)` |
| main | _load_stdio_agent_key | 2553 | `_load_stdio_agent_key(data not statically known)` |
| _load_stdio_agent_key | os.getenv | 215 | `os.getenv(MCP_AGENT_API_KEY_ENV)` |
| _load_stdio_agent_key | os.getenv | 217 | `os.getenv(MCP_AGENT_API_KEY_FILE_ENV)` |
| _load_stdio_agent_key | read_agent_key_file | 220 | `read_agent_key_file(key_file)` |
| read_agent_key_file | Path(…).expanduser | 28 | `Path(path).expanduser(data not statically known)` |
| read_agent_key_file | Path | 28 | `Path(path)` |
| read_agent_key_file | location.stat | 30 | `location.stat(data not statically known)` |
| read_agent_key_file | AgentKeyFileError | 32 | `AgentKeyFileError(...)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 2555 |
| output | `print` | `main` | 2558 |
| environment_read | `os.getenv` | `_load_stdio_agent_key` | 215 |
| environment_read | `os.getenv` | `_load_stdio_agent_key` | 217 |
| filesystem_read | `location.read_text` | `read_agent_key_file` | 43 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 2542 |
| unresolved_call | `main` | `parser.add_argument` | 2543 |
| unresolved_call | `main` | `parser.parse_args` | 2549 |
| unresolved_call | `read_agent_key_file` | `Path(path).expanduser` | 28 |
| unresolved_call | `read_agent_key_file` | `location.stat` | 30 |
| step_limit | `main` | `first 12 steps` | 0 |
| truncated_flow | `main` | `depth limit` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
