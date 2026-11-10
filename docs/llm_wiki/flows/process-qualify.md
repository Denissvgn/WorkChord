# qualify

**Entry point:** `main` (`process`)
**Source:** [qualify](../modules/qualify.md)
**Modules touched:** [load_common](../modules/load_common.md), [qualify](../modules/qualify.md)

**Related modules:** [load_common](../modules/load_common.md), [result](../modules/result.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as _parser
    participant p2 as QualificationInputError
    participant p3 as getattr
    participant p4 as _parser().parse_args
    participant p5 as int
    participant p6 as args.handler
    participant p7 as print
    participant p8 as argparse.ArgumentParser
    participant p9 as parser.add_subparsers
    participant p10 as commands.add_parser
    participant p11 as freeze.add_argument
    participant p12 as freeze.set_defaults
    participant p13 as bundle.add_argument
    participant p14 as bundle.set_defaults
    participant p15 as finalize.add_argument
    p0->>p1: _parser
    p0->>p2: QualificationInputError
    p0-->>p3: getattr(args, 'attempt_number', 1)
    p0-->>p4: _parser().parse_args
    p0-->>p5: int(args.handler(...))
    p0-->>p6: args.handler(args)
    p0-->>p7: print(..., file=sys.stderr)
    p1-->>p8: argparse.ArgumentParser(description='Build the fail-closed PostgreSQL pre-cutover qualification.')
    p1-->>p9: parser.add_subparsers(dest='command', required=True)
    p1-->>p10: commands.add_parser('freeze')
    p1-->>p11: freeze.add_argument('--commit', required=True)
    p1-->>p11: freeze.add_argument('--image', action='append', required=True)
    p1-->>p11: freeze.add_argument('--configuration', type=Path, required=True)
    p1-->>p11: freeze.add_argument('--hardware-evidence', type=Path, required=True)
    p1-->>p11: freeze.add_argument('--seed-manifest', type=Path, required=True)
    p1-->>p11: freeze.add_argument('--schema-head', required=True)
    p1-->>p11: freeze.add_argument('--output', type=Path, required=True)
    p1-->>p12: freeze.set_defaults(handler=_freeze)
    p1-->>p10: commands.add_parser('bundle-run')
    p1-->>p13: bundle.add_argument('--run-id', required=True)
    p1-->>p13: bundle.add_argument('--attempt-number', type=int, required=True)
    p1-->>p13: bundle.add_argument('--release-manifest', type=Path, required=True)
    p1-->>p13: bundle.add_argument('--seed-manifest', type=Path, required=True)
    p1-->>p13: bundle.add_argument('--result', type=Path, action='append', required=True)
    p1-->>p13: bundle.add_argument('--resilience', type=Path, required=True)
    p1-->>p13: bundle.add_argument('--ci-evidence', type=Path, required=True)
    p1-->>p13: bundle.add_argument('--output', type=Path, required=True)
    p1-->>p14: bundle.set_defaults(handler=_bundle)
    p1-->>p10: commands.add_parser('finalize')
    p1-->>p15: finalize.add_argument('--report-id', default=...)
```

> Call sequence diagram shows 30 of 40 interactions; 10 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 4 of 5 (1 omitted); unresolved 24 of 33 (9 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `scripts/load/qualify.py:_parser` | 3 | - | external | 1 |
| `scripts/load/qualify.py:_parser` | 3 | - | unresolved | 9 |
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 3; effect analysis evaluated: 1, partial: 1, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 2 source steps with known totals: observed: 25, emitted: 14, omitted: 11. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `_parser().parse_args` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_parser` | `available` | `partial` | `available` | `20` | `9` | `11` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_subparsers` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `commands.add_parser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `freeze.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `freeze.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `freeze.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `freeze.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `freeze.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `freeze.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

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
