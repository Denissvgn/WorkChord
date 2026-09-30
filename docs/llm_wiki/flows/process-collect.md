# collect

**Entry point:** `main` (`process`)
**Source:** [collect](../modules/collect.md)
**Modules touched:** [collect](../modules/collect.md)

**Related modules:** [load_common](../modules/load_common.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as _parser().parse_args
    participant p2 as _parser
    participant p3 as argparse.ArgumentParser
    participant p4 as parser.add_subparsers
    participant p5 as subparsers.add_parser
    participant p6 as _add_target_arguments
    participant p7 as parser.add_argument
    participant p8 as snapshot.add_argument
    participant p9 as uuid4
    participant p10 as snapshot.set_defaults
    participant p11 as derive.add_argument
    participant p12 as derive.set_defaults
    participant p13 as int
    participant p14 as args.handler
    participant p15 as print
    p0-->>p1: _parser().parse_args
    p0->>p2: _parser
    p2-->>p3: argparse.ArgumentParser
    p2-->>p4: parser.add_subparsers
    p2-->>p5: subparsers.add_parser
    p2->>p6: _add_target_arguments
    p6-->>p7: parser.add_argument
    p6-->>p7: parser.add_argument
    p6-->>p7: parser.add_argument
    p6-->>p7: parser.add_argument
    p6-->>p7: parser.add_argument
    p2-->>p8: snapshot.add_argument
    p2-->>p8: snapshot.add_argument
    p2-->>p9: uuid4
    p2-->>p8: snapshot.add_argument
    p2-->>p8: snapshot.add_argument
    p2-->>p10: snapshot.set_defaults
    p2-->>p5: subparsers.add_parser
    p2-->>p11: derive.add_argument
    p2-->>p11: derive.add_argument
    p2-->>p11: derive.add_argument
    p2-->>p11: derive.add_argument
    p2-->>p11: derive.add_argument
    p2-->>p11: derive.add_argument
    p2-->>p11: derive.add_argument
    p2-->>p12: derive.set_defaults
    p0-->>p13: int
    p0-->>p14: args.handler
    p0-->>p15: print
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. main"]
    s2["2. _parser().parse_args"]
    s3["3. _parser"]
    s4["4. argparse.ArgumentParser"]
    s5["5. parser.add_subparsers"]
    s6["6. subparsers.add_parser"]
    s7["7. _add_target_arguments"]
    s8["8. parser.add_argument"]
    s9["9. parser.add_argument"]
    s10["10. parser.add_argument"]
    s11["11. parser.add_argument"]
    s12["12. parser.add_argument"]
    s1 -. "_parser().parse_args(data not statically known)" .-> s2
    s1 -->|"_parser(data not statically known)"| s3
    s3 -. "argparse.ArgumentParser(description='Collect fail-closed PostgreSQL qualification evidence.')" .-> s4
    s3 -. "parser.add_subparsers(dest='command', required=True)" .-> s5
    s3 -. "subparsers.add_parser('snapshot')" .-> s6
    s3 -->|"_add_target_arguments(snapshot)"| s7
    s7 -. "parser.add_argument('--database-url', required=True)" .-> s8
    s7 -. "parser.add_argument('--authorize-host', required=True)" .-> s9
    s7 -. "parser.add_argument('--environment', choices=(...), required=True)" .-> s10
    s7 -. "parser.add_argument('--production-authorization')" .-> s11
    s7 -. "parser.add_argument('--change-id')" .-> s12
    b0["output print"]
    s1 -. "output print" .-> b0
    click s1 "../modules/collect.md"
    click s3 "../modules/collect.md"
    click s7 "../modules/collect.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `QualificationInputError`, `psycopg`, `sys` | - | `int(...)`, `2` |
| `_parser().parse_args` | - | - | - | - |
| `_parser` | - | `Path`, `_snapshot`, `Path`, `Path`, `Path`, `DERIVATION_PHASES`, `Path`, `Path` | - | `parser` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_subparsers` | - | - | - | - |
| `subparsers.add_parser` | - | - | - | - |
| `_add_target_arguments` | `parser: argparse.ArgumentParser` | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | _parser().parse_args | 622 | `_parser().parse_args(data not statically known)` |
| main | _parser | 622 | `_parser(data not statically known)` |
| _parser | argparse.ArgumentParser | 596 | `argparse.ArgumentParser(description='Collect fail-closed PostgreSQL qualification evidence.')` |
| _parser | parser.add_subparsers | 599 | `parser.add_subparsers(dest='command', required=True)` |
| _parser | subparsers.add_parser | 601 | `subparsers.add_parser('snapshot')` |
| _parser | _add_target_arguments | 602 | `_add_target_arguments(snapshot)` |
| _add_target_arguments | parser.add_argument | 584 | `parser.add_argument('--database-url', required=True)` |
| _add_target_arguments | parser.add_argument | 585 | `parser.add_argument('--authorize-host', required=True)` |
| _add_target_arguments | parser.add_argument | 586 | `parser.add_argument('--environment', choices=(...), required=True)` |
| _add_target_arguments | parser.add_argument | 591 | `parser.add_argument('--production-authorization')` |
| _add_target_arguments | parser.add_argument | 592 | `parser.add_argument('--change-id')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 626 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `main` | `_parser().parse_args` | 622 |
| external_call | `_parser` | `argparse.ArgumentParser` | 596 |
| unresolved_call | `_parser` | `parser.add_subparsers` | 599 |
| unresolved_call | `_parser` | `subparsers.add_parser` | 601 |
| unresolved_call | `_add_target_arguments` | `parser.add_argument` | 584 |
| unresolved_call | `_add_target_arguments` | `parser.add_argument` | 585 |
| unresolved_call | `_add_target_arguments` | `parser.add_argument` | 586 |
| unresolved_call | `_add_target_arguments` | `parser.add_argument` | 591 |
| unresolved_call | `_add_target_arguments` | `parser.add_argument` | 592 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
