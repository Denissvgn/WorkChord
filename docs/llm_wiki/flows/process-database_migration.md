# database_migration

**Entry point:** `main` (`process`)
**Source:** [cli_database_migration](../modules/cli_database_migration.md)
**Modules touched:** [authority](../modules/authority.md), [calendar_service](../modules/calendar_service.md), [catalog](../modules/catalog.md), [cli_database_migration](../modules/cli_database_migration.md), and 17 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [calendar_service](../modules/calendar_service.md)
- [catalog](../modules/catalog.md)
- [cli_database_migration](../modules/cli_database_migration.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [database_config](../modules/database_config.md)
- [database_migration_canonical](../modules/database_migration_canonical.md)
- [database_migration_manifest](../modules/database_migration_manifest.md)
- [github_status_automation_service](../modules/github_status_automation_service.md)
- [identity_service](../modules/identity_service.md)
- [label_service](../modules/label_service.md)
- [maintenance](../modules/maintenance.md)
- [models_identity](../modules/models_identity.md)
- [saved_view_service](../modules/saved_view_service.md)
- [source](../modules/source.md)
- [system_settings_service](../modules/system_settings_service.md)
- [template_service](../modules/template_service.md)
- [time](../modules/time.md)
- [transfer](../modules/transfer.md)
- [upgrade_service](../modules/upgrade_service.md)

**Related modules:** [database_migration_manifest](../modules/database_migration_manifest.md), [source](../modules/source.md), [transfer](../modules/transfer.md), [upgrade_service](../modules/upgrade_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as build_parser().parse_args
    participant p2 as build_parser
    participant p3 as argparse.ArgumentParser
    participant p4 as parser.add_subparsers
    participant p5 as commands.add_parser
    participant p6 as preflight.add_argument
    participant p7 as load.add_argument
    participant p8 as repairs.add_argument
    participant p9 as reconcile.add_argument
    p0-->>p1: build_parser().parse_args
    p0->>p2: build_parser
    p2-->>p3: argparse.ArgumentParser
    p2-->>p4: parser.add_subparsers
    p2-->>p5: commands.add_parser
    p2-->>p6: preflight.add_argument
    p2-->>p6: preflight.add_argument
    p2-->>p6: preflight.add_argument
    p2-->>p6: preflight.add_argument
    p2-->>p5: commands.add_parser
    p2-->>p5: commands.add_parser
    p2-->>p7: load.add_argument
    p2-->>p7: load.add_argument
    p2-->>p7: load.add_argument
    p2-->>p7: load.add_argument
    p2-->>p7: load.add_argument
    p2-->>p7: load.add_argument
    p2-->>p7: load.add_argument
    p2-->>p5: commands.add_parser
    p2-->>p8: repairs.add_argument
    p2-->>p8: repairs.add_argument
    p2-->>p8: repairs.add_argument
    p2-->>p5: commands.add_parser
    p2-->>p9: reconcile.add_argument
    p2-->>p9: reconcile.add_argument
    p2-->>p9: reconcile.add_argument
    p2-->>p9: reconcile.add_argument
    p2-->>p9: reconcile.add_argument
    p2-->>p9: reconcile.add_argument
    p2-->>p9: reconcile.add_argument
```

> Call sequence diagram shows 30 of 1119 interactions; 1089 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. main"]
    s2["2. build_parser().parse_args"]
    s3["3. build_parser"]
    s4["4. argparse.ArgumentParser"]
    s5["5. parser.add_subparsers"]
    s6["6. commands.add_parser"]
    s7["7. preflight.add_argument"]
    s8["8. preflight.add_argument"]
    s9["9. preflight.add_argument"]
    s10["10. preflight.add_argument"]
    s11["11. commands.add_parser"]
    s12["12. commands.add_parser"]
    s1 -. "build_parser().parse_args(argv)" .-> s2
    s1 -->|"build_parser(data not statically known)"| s3
    s3 -. "argparse.ArgumentParser(description='Fail-closed WorkChord SQLite-to-PostgreSQL migration tooling.')" .-> s4
    s3 -. "parser.add_subparsers(dest='command', required=True)" .-> s5
    s3 -. "commands.add_parser('preflight', help='Create and validate a read-only SQLite snapshot.')" .-> s6
    s3 -. "preflight.add_argument('--source', type=Path, required=True)" .-> s7
    s3 -. "preflight.add_argument('--snapshot', type=Path, required=True)" .-> s8
    s3 -. "preflight.add_argument('--writer-drain-evidence', type=Path, required=True)" .-> s9
    s3 -. "preflight.add_argument('--manifest', type=Path, required=True)" .-> s10
    s3 -. "commands.add_parser('target-identity', help='Print the exact secret-free target authorization value.')" .-> s11
    s3 -. "commands.add_parser('load', help='Load a manifested snapshot into PostgreSQL.')" .-> s12
    b0["output print"]
    s1 -. "output print" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["output print"]
    s1 -. "output print" .-> b2
    b3["output print"]
    s1 -. "output print" .-> b3
    b4["output print"]
    s1 -. "output print" .-> b4
    b5["output print"]
    s1 -. "output print" .-> b5
    b6["output print"]
    s1 -. "output print" .-> b6
    click s1 "../modules/cli_database_migration.md"
    click s3 "../modules/cli_database_migration.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
    class b4 boundary
    class b5 boundary
    class b6 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | `argv: list[str] \| None` | `ManifestError`, `MigrationDataError`, `sys` | - | `0`, `0`, `0`, `0`, `0`, `0`, `2`, `2` |
| `build_parser().parse_args` | - | - | - | - |
| `build_parser` | - | `Path`, `Path`, `Path`, `Path`, `Path`, `Path`, `Path`, `Path` | - | `parser` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_subparsers` | - | - | - | - |
| `commands.add_parser` | - | - | - | - |
| `preflight.add_argument` | - | - | - | - |
| `preflight.add_argument` | - | - | - | - |
| `preflight.add_argument` | - | - | - | - |
| `preflight.add_argument` | - | - | - | - |
| `commands.add_parser` | - | - | - | - |
| `commands.add_parser` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | build_parser().parse_args | 94 | `build_parser().parse_args(argv)` |
| main | build_parser | 94 | `build_parser(data not statically known)` |
| build_parser | argparse.ArgumentParser | 22 | `argparse.ArgumentParser(description='Fail-closed WorkChord SQLite-to-PostgreSQL migration tooling.')` |
| build_parser | parser.add_subparsers | 25 | `parser.add_subparsers(dest='command', required=True)` |
| build_parser | commands.add_parser | 27 | `commands.add_parser('preflight', help='Create and validate a read-only SQLite snapshot.')` |
| build_parser | preflight.add_argument | 30 | `preflight.add_argument('--source', type=Path, required=True)` |
| build_parser | preflight.add_argument | 31 | `preflight.add_argument('--snapshot', type=Path, required=True)` |
| build_parser | preflight.add_argument | 32 | `preflight.add_argument('--writer-drain-evidence', type=Path, required=True)` |
| build_parser | preflight.add_argument | 33 | `preflight.add_argument('--manifest', type=Path, required=True)` |
| build_parser | commands.add_parser | 35 | `commands.add_parser('target-identity', help='Print the exact secret-free target authorization value.')` |
| build_parser | commands.add_parser | 39 | `commands.add_parser('load', help='Load a manifested snapshot into PostgreSQL.')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 103 |
| output | `print` | `main` | 114 |
| output | `print` | `main` | 126 |
| output | `print` | `main` | 137 |
| output | `print` | `main` | 152 |
| output | `print` | `main` | 159 |
| output | `print` | `main` | 163 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `main` | `build_parser().parse_args` | 94 |
| external_call | `build_parser` | `argparse.ArgumentParser` | 22 |
| unresolved_call | `build_parser` | `parser.add_subparsers` | 25 |
| unresolved_call | `build_parser` | `commands.add_parser` | 27 |
| unresolved_call | `build_parser` | `preflight.add_argument` | 30 |
| unresolved_call | `build_parser` | `preflight.add_argument` | 31 |
| unresolved_call | `build_parser` | `preflight.add_argument` | 32 |
| unresolved_call | `build_parser` | `preflight.add_argument` | 33 |
| unresolved_call | `build_parser` | `commands.add_parser` | 35 |
| unresolved_call | `build_parser` | `commands.add_parser` | 39 |
| step_limit | `main` | `first 12 steps` | 0 |
| truncated_flow | `main` | `depth limit` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
