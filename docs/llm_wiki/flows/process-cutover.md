# cutover

**Entry point:** `main` (`process`)
**Source:** [cli_cutover](../modules/cli_cutover.md)
**Modules touched:** [cli_cutover](../modules/cli_cutover.md), [database_migration_cutover](../modules/database_migration_cutover.md), [database_migration_manifest](../modules/database_migration_manifest.md), and 1 more

**Complete modules touched:**

- [cli_cutover](../modules/cli_cutover.md)
- [database_migration_cutover](../modules/database_migration_cutover.md)
- [database_migration_manifest](../modules/database_migration_manifest.md)
- [execution_mode](../modules/execution_mode.md)

**Related modules:** [database_migration_cutover](../modules/database_migration_cutover.md), [database_migration_manifest](../modules/database_migration_manifest.md)

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
    participant p6 as documentation.add_argument
    participant p7 as _signing_arguments
    participant p8 as parser.add_argument (backend/app/cli/cutover.py:_signing_arguments)
    participant p9 as seal.add_argument
    participant p10 as rehearsal.add_argument
    participant p11 as _trusted_dependency_arguments
    participant p12 as parser.add_argument (backend/app/cli/cutover.p…sted_dependency_arguments)
    participant p13 as series.add_argument
    participant p14 as authorization.add_argument
    p0-->>p1: build_parser().parse_args
    p0->>p2: build_parser
    p2-->>p3: argparse.ArgumentParser
    p2-->>p4: parser.add_subparsers
    p2-->>p5: commands.add_parser
    p2-->>p6: documentation.add_argument
    p2-->>p6: documentation.add_argument
    p2->>p7: _signing_arguments
    p7-->>p8: parser.add_argument (backend/app/cli/cutover.py:_signing_arguments)
    p7-->>p8: parser.add_argument (backend/app/cli/cutover.py:_signing_arguments)
    p7-->>p8: parser.add_argument (backend/app/cli/cutover.py:_signing_arguments)
    p2-->>p5: commands.add_parser
    p2-->>p9: seal.add_argument
    p2-->>p9: seal.add_argument
    p2-->>p5: commands.add_parser
    p2-->>p10: rehearsal.add_argument
    p2->>p11: _trusted_dependency_arguments
    p11-->>p12: parser.add_argument (backend/app/cli/cutover.p…sted_dependency_arguments)
    p11-->>p12: parser.add_argument (backend/app/cli/cutover.p…sted_dependency_arguments)
    p11-->>p12: parser.add_argument (backend/app/cli/cutover.p…sted_dependency_arguments)
    p11-->>p12: parser.add_argument (backend/app/cli/cutover.p…sted_dependency_arguments)
    p11-->>p12: parser.add_argument (backend/app/cli/cutover.p…sted_dependency_arguments)
    p2->>p7: _signing_arguments
    p2-->>p5: commands.add_parser
    p2-->>p13: series.add_argument
    p2-->>p13: series.add_argument
    p2-->>p13: series.add_argument
    p2->>p7: _signing_arguments
    p2-->>p5: commands.add_parser
    p2-->>p14: authorization.add_argument
```

> Call sequence diagram shows 30 of 879 interactions; 849 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

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
    s7["7. documentation.add_argument"]
    s8["8. documentation.add_argument"]
    s9["9. _signing_arguments"]
    s10["10. parser.add_argument (backend/app/cli/cutover.py:_signing_arguments)"]
    s11["11. parser.add_argument (backend/app/cli/cutover.py:_signing_arguments)"]
    s12["12. parser.add_argument (backend/app/cli/cutover.py:_signing_arguments)"]
    s1 -. "build_parser().parse_args(argv)" .-> s2
    s1 -->|"build_parser(data not statically known)"| s3
    s3 -. "argparse.ArgumentParser(…)" .-> s4
    s3 -. "parser.add_subparsers(dest='command', required=True)" .-> s5
    s3 -. "commands.add_parser('attest-documentation', help='Sign an independently reviewed pre-cutover documentation walkthrough.')" .-> s6
    s3 -. "documentation.add_argument('--input', type=Path, required=True)" .-> s7
    s3 -. "documentation.add_argument('--release-manifest', type=Path, required=True)" .-> s8
    s3 -->|"_signing_arguments(documentation)"| s9
    s9 -. "parser.add_argument (backend/app/cli/cutover.py:_signing_arguments)('--signing-key', type=Path, required=True)" .-> s10
    s9 -. "parser.add_argument (backend/app/cli/cutover.py:_signing_arguments)('--signer', required=True)" .-> s11
    s9 -. "parser.add_argument (backend/app/cli/cutover.py:_signing_arguments)('--output', type=Path, required=True)" .-> s12
    b0["output print"]
    s1 -. "output print" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["output print"]
    s1 -. "output print" .-> b2
    click s1 "../modules/cli_cutover.md"
    click s3 "../modules/cli_cutover.md"
    click s9 "../modules/cli_cutover.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | `argv: list[str] \| None` | `CutoverEvidenceError`, `ManifestError`, `sys` | - | `0`, `2`, `0`, `2` |
| `build_parser().parse_args` | - | - | - | - |
| `build_parser` | - | `Path`, `Path`, `Path`, `Path`, `Path`, `Path`, `Path`, `Path` | - | `parser` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_subparsers` | - | - | - | - |
| `commands.add_parser` | - | - | - | - |
| `documentation.add_argument` | - | - | - | - |
| `documentation.add_argument` | - | - | - | - |
| `_signing_arguments` | `parser: argparse.ArgumentParser` | `Path`, `Path` | - | - |
| `parser.add_argument (backend/app/cli/cutover.py:_signing_arguments)` | - | - | - | - |
| `parser.add_argument (backend/app/cli/cutover.py:_signing_arguments)` | - | - | - | - |
| `parser.add_argument (backend/app/cli/cutover.py:_signing_arguments)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | build_parser().parse_args | 109 | `build_parser().parse_args(argv)` |
| main | build_parser | 109 | `build_parser(data not statically known)` |
| build_parser | argparse.ArgumentParser | 37 | `argparse.ArgumentParser(description='Fail-closed PostgreSQL rehearsal and production-cutover evidence. This command records evidence; it never mutates a database or deployment.')` |
| build_parser | parser.add_subparsers | 43 | `parser.add_subparsers(dest='command', required=True)` |
| build_parser | commands.add_parser | 45 | `commands.add_parser('attest-documentation', help='Sign an independently reviewed pre-cutover documentation walkthrough.')` |
| build_parser | documentation.add_argument | 49 | `documentation.add_argument('--input', type=Path, required=True)` |
| build_parser | documentation.add_argument | 50 | `documentation.add_argument('--release-manifest', type=Path, required=True)` |
| build_parser | _signing_arguments | 51 | `_signing_arguments(documentation)` |
| _signing_arguments | parser.add_argument (backend/app/cli/cutover.py:_signing_arguments) | 31 | `parser.add_argument('--signing-key', type=Path, required=True)` |
| _signing_arguments | parser.add_argument (backend/app/cli/cutover.py:_signing_arguments) | 32 | `parser.add_argument('--signer', required=True)` |
| _signing_arguments | parser.add_argument (backend/app/cli/cutover.py:_signing_arguments) | 33 | `parser.add_argument('--output', type=Path, required=True)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 177 |
| output | `print` | `main` | 181 |
| output | `print` | `main` | 193 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `main` | `build_parser().parse_args` | 109 |
| external_call | `build_parser` | `argparse.ArgumentParser` | 37 |
| unresolved_call | `build_parser` | `parser.add_subparsers` | 43 |
| unresolved_call | `build_parser` | `commands.add_parser` | 45 |
| unresolved_call | `build_parser` | `documentation.add_argument` | 49 |
| unresolved_call | `build_parser` | `documentation.add_argument` | 50 |
| unresolved_call | `_signing_arguments` | `parser.add_argument` | 31 |
| unresolved_call | `_signing_arguments` | `parser.add_argument` | 32 |
| unresolved_call | `_signing_arguments` | `parser.add_argument` | 33 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
