# qualify

**Entry point:** `main` (`process`)
**Source:** [qualify](../modules/qualify.md)
**Modules touched:** [load_common](../modules/load_common.md), [qualify](../modules/qualify.md)

**Related modules:** [load_common](../modules/load_common.md), [result](../modules/result.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as _parser().parse_args
    participant p2 as _parser
    participant p3 as argparse.ArgumentParser
    participant p4 as parser.add_subparsers
    participant p5 as commands.add_parser
    participant p6 as freeze.add_argument
    participant p7 as freeze.set_defaults
    participant p8 as bundle.add_argument
    participant p9 as bundle.set_defaults
    participant p10 as finalize.add_argument
    participant p11 as uuid4
    p0-->>p1: _parser().parse_args
    p0->>p2: _parser
    p2-->>p3: argparse.ArgumentParser
    p2-->>p4: parser.add_subparsers
    p2-->>p5: commands.add_parser
    p2-->>p6: freeze.add_argument
    p2-->>p6: freeze.add_argument
    p2-->>p6: freeze.add_argument
    p2-->>p6: freeze.add_argument
    p2-->>p6: freeze.add_argument
    p2-->>p6: freeze.add_argument
    p2-->>p6: freeze.add_argument
    p2-->>p7: freeze.set_defaults
    p2-->>p5: commands.add_parser
    p2-->>p8: bundle.add_argument
    p2-->>p8: bundle.add_argument
    p2-->>p8: bundle.add_argument
    p2-->>p8: bundle.add_argument
    p2-->>p8: bundle.add_argument
    p2-->>p8: bundle.add_argument
    p2-->>p8: bundle.add_argument
    p2-->>p8: bundle.add_argument
    p2-->>p9: bundle.set_defaults
    p2-->>p5: commands.add_parser
    p2-->>p10: finalize.add_argument
    p2-->>p11: uuid4
    p2-->>p10: finalize.add_argument
    p2-->>p10: finalize.add_argument
    p2-->>p10: finalize.add_argument
    p2-->>p10: finalize.add_argument
```

> Call sequence diagram shows 30 of 40 interactions; 10 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. main"]
    s2["2. _parser().parse_args"]
    s3["3. _parser"]
    s4["4. argparse.ArgumentParser"]
    s5["5. parser.add_subparsers"]
    s6["6. commands.add_parser"]
    s7["7. freeze.add_argument"]
    s8["8. freeze.add_argument"]
    s9["9. freeze.add_argument"]
    s10["10. freeze.add_argument"]
    s11["11. freeze.add_argument"]
    s12["12. freeze.add_argument"]
    s1 -. "_parser().parse_args(data not statically known)" .-> s2
    s1 -->|"_parser(data not statically known)"| s3
    s3 -. "argparse.ArgumentParser(description='Build the fail-closed PostgreSQL pre-cutover qualification.')" .-> s4
    s3 -. "parser.add_subparsers(dest='command', required=True)" .-> s5
    s3 -. "commands.add_parser('freeze')" .-> s6
    s3 -. "freeze.add_argument('--commit', required=True)" .-> s7
    s3 -. "freeze.add_argument('--image', action='append', required=True)" .-> s8
    s3 -. "freeze.add_argument('--configuration', type=Path, required=True)" .-> s9
    s3 -. "freeze.add_argument('--hardware-evidence', type=Path, required=True)" .-> s10
    s3 -. "freeze.add_argument('--seed-manifest', type=Path, required=True)" .-> s11
    s3 -. "freeze.add_argument('--schema-head', required=True)" .-> s12
    b0["output print"]
    s1 -. "output print" .-> b0
    click s1 "../modules/qualify.md"
    click s3 "../modules/qualify.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `QualificationInputError`, `sys` | - | `int(...)`, `2` |
| `_parser().parse_args` | - | - | - | - |
| `_parser` | - | `Path`, `Path`, `Path`, `Path`, `_freeze`, `Path`, `Path`, `Path` | - | `parser` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_subparsers` | - | - | - | - |
| `commands.add_parser` | - | - | - | - |
| `freeze.add_argument` | - | - | - | - |
| `freeze.add_argument` | - | - | - | - |
| `freeze.add_argument` | - | - | - | - |
| `freeze.add_argument` | - | - | - | - |
| `freeze.add_argument` | - | - | - | - |
| `freeze.add_argument` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | _parser().parse_args | 791 | `_parser().parse_args(data not statically known)` |
| main | _parser | 791 | `_parser(data not statically known)` |
| _parser | argparse.ArgumentParser | 749 | `argparse.ArgumentParser(description='Build the fail-closed PostgreSQL pre-cutover qualification.')` |
| _parser | parser.add_subparsers | 752 | `parser.add_subparsers(dest='command', required=True)` |
| _parser | commands.add_parser | 754 | `commands.add_parser('freeze')` |
| _parser | freeze.add_argument | 755 | `freeze.add_argument('--commit', required=True)` |
| _parser | freeze.add_argument | 756 | `freeze.add_argument('--image', action='append', required=True)` |
| _parser | freeze.add_argument | 757 | `freeze.add_argument('--configuration', type=Path, required=True)` |
| _parser | freeze.add_argument | 758 | `freeze.add_argument('--hardware-evidence', type=Path, required=True)` |
| _parser | freeze.add_argument | 759 | `freeze.add_argument('--seed-manifest', type=Path, required=True)` |
| _parser | freeze.add_argument | 760 | `freeze.add_argument('--schema-head', required=True)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 797 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `main` | `_parser().parse_args` | 791 |
| external_call | `_parser` | `argparse.ArgumentParser` | 749 |
| unresolved_call | `_parser` | `parser.add_subparsers` | 752 |
| unresolved_call | `_parser` | `commands.add_parser` | 754 |
| unresolved_call | `_parser` | `freeze.add_argument` | 755 |
| unresolved_call | `_parser` | `freeze.add_argument` | 756 |
| unresolved_call | `_parser` | `freeze.add_argument` | 757 |
| unresolved_call | `_parser` | `freeze.add_argument` | 758 |
| unresolved_call | `_parser` | `freeze.add_argument` | 759 |
| unresolved_call | `_parser` | `freeze.add_argument` | 760 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
