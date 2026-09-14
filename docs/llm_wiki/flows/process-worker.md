# worker

**Entry point:** `main` (`process`)
**Source:** [worker](../modules/worker.md)
**Modules touched:** [app_database](../modules/app_database.md), [config](../modules/config.md), [maintenance](../modules/maintenance.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), and 2 more

**Complete modules touched:**

- [app_database](../modules/app_database.md)
- [config](../modules/config.md)
- [maintenance](../modules/maintenance.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [upgrade_service](../modules/upgrade_service.md)
- [worker](../modules/worker.md)

**Related modules:** [app_database](../modules/app_database.md), [config](../modules/config.md), [outbound_webhook_service](../modules/outbound_webhook_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as build_parser().parse_args
    participant p2 as build_parser
    participant p3 as argparse.ArgumentParser
    participant p4 as parser.add_argument
    participant p5 as asyncio.run
    participant p6 as _run
    participant p7 as get_settings
    participant p8 as Settings
    participant p9 as print
    participant p10 as init_db
    participant p11 as assert_database_current
    participant p12 as inspect_database
    participant p13 as _inspect_database_connection
    participant p14 as inspect
    participant p15 as sorted
    participant p16 as inspector.get_table_names
    participant p17 as _current_revision
    participant p18 as set
    participant p19 as head_revision
    participant p20 as LEGACY_CORE_TABLES.issubset
    participant p21 as CURRENT_SENTINEL_TABLES.issubset
    participant p22 as DatabaseStatus
    participant p23 as len
    participant p24 as _sync_engine
    participant p25 as database_configuration
    participant p26 as create_engine
    participant p27 as dict
    p0-->>p1: build_parser().parse_args
    p0->>p2: build_parser
    p2-->>p3: argparse.ArgumentParser
    p2-->>p4: parser.add_argument
    p0-->>p5: asyncio.run
    p0->>p6: _run
    p6->>p7: get_settings
    p7->>p8: Settings
    p6-->>p9: print
    p6-->>p9: print
    p6-->>p9: print
    p6->>p10: init_db
    p10->>p11: assert_database_current
    p11->>p12: inspect_database
    p12->>p13: _inspect_database_connection
    p13-->>p14: inspect
    p13-->>p15: sorted
    p13-->>p16: inspector.get_table_names
    p13->>p17: _current_revision
    p13-->>p18: set
    p13->>p19: head_revision
    p13-->>p20: LEGACY_CORE_TABLES.issubset
    p13-->>p20: LEGACY_CORE_TABLES.issubset
    p13-->>p21: CURRENT_SENTINEL_TABLES.issubset
    p13->>p22: DatabaseStatus
    p13-->>p23: len
    p12->>p24: _sync_engine
    p24->>p25: database_configuration
    p24-->>p26: create_engine
    p24-->>p27: dict
```

> Call sequence diagram shows 30 of 56 interactions; 26 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. main"]
    s2["2. build_parser().parse_args"]
    s3["3. build_parser"]
    s4["4. argparse.ArgumentParser"]
    s5["5. parser.add_argument"]
    s6["6. asyncio.run"]
    s7["7. _run"]
    s8["8. get_settings"]
    s9["9. Settings"]
    s10["10. print"]
    s11["11. print"]
    s12["12. print"]
    s1 -. "build_parser().parse_args(argv)" .-> s2
    s1 -->|"build_parser(data not statically known)"| s3
    s3 -. "argparse.ArgumentParser(description='Run the WorkChord durable delivery worker.')" .-> s4
    s3 -. "parser.add_argument('--once', action='store_true', help='Process one bounded batch and exit.')" .-> s5
    s1 -. "asyncio.run(_run(...))" .-> s6
    s1 -->|"_run(once=args.once)"| s7
    s7 -->|"get_settings(data not statically known)"| s8
    s8 -->|"Settings(data not statically known)"| s9
    s7 -. "print('DATABASE_PROCESS_ROLE=delivery_worker is required', file=sys.stderr)" .-> s10
    s7 -. "print('Outbound delivery worker is disabled', file=sys.stderr)" .-> s11
    s7 -. "print(..., file=sys.stderr)" .-> s12
    b0["output print"]
    s7 -. "output print" .-> b0
    b1["output print"]
    s7 -. "output print" .-> b1
    b2["output print"]
    s7 -. "output print" .-> b2
    b3["output print"]
    s7 -. "output print" .-> b3
    click s1 "../modules/worker.md"
    click s3 "../modules/worker.md"
    click s7 "../modules/worker.md"
    click s8 "../modules/config.md"
    click s9 "../modules/config.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | `argv: Optional[list[str]]` | - | - | `asyncio.run(...)` |
| `build_parser().parse_args` | - | - | - | - |
| `build_parser` | - | - | - | `parser` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `asyncio.run` | - | - | - | - |
| `_run` | `once: bool` | `sys`, `sys`, `sys`, `signal` | - | `2`, `2`, `0`, `0`, `0` |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `print` | - | - | - | - |
| `print` | - | - | - | - |
| `print` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | build_parser().parse_args | 76 | `build_parser().parse_args(argv)` |
| main | build_parser | 76 | `build_parser(data not statically known)` |
| build_parser | argparse.ArgumentParser | 20 | `argparse.ArgumentParser(description='Run the WorkChord durable delivery worker.')` |
| build_parser | parser.add_argument | 23 | `parser.add_argument('--once', action='store_true', help='Process one bounded batch and exit.')` |
| main | asyncio.run | 77 | `asyncio.run(_run(...))` |
| main | _run | 77 | `_run(once=args.once)` |
| _run | get_settings | 32 | `get_settings(data not statically known)` |
| get_settings | Settings | 469 | `Settings(data not statically known)` |
| _run | print | 34 | `print('DATABASE_PROCESS_ROLE=delivery_worker is required', file=sys.stderr)` |
| _run | print | 40 | `print('Outbound delivery worker is disabled', file=sys.stderr)` |
| _run | print | 43 | `print(..., file=sys.stderr)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `_run` | 34 |
| output | `print` | `_run` | 40 |
| output | `print` | `_run` | 43 |
| output | `print` | `_run` | 55 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `main` | `build_parser().parse_args` | 76 |
| external_call | `build_parser` | `argparse.ArgumentParser` | 20 |
| unresolved_call | `build_parser` | `parser.add_argument` | 23 |
| external_call | `main` | `asyncio.run` | 77 |
| step_limit | `main` | `first 12 steps` | 0 |
| truncated_flow | `main` | `depth limit` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
