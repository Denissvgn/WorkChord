# collect

**Entry point:** `main` (`process`)
**Source:** [collect](../modules/collect.md)
**Modules touched:** [collect](../modules/collect.md)

**Related modules:** [load_common](../modules/load_common.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as _parser().parse_args
    participant p2 as _parser
    participant p3 as int
    participant p4 as args.handler
    participant p5 as print
    participant p6 as argparse.ArgumentParser
    participant p7 as parser.add_subparsers
    participant p8 as subparsers.add_parser
    participant p9 as _add_target_arguments
    participant p10 as snapshot.add_argument
    participant p11 as uuid4
    participant p12 as snapshot.set_defaults
    participant p13 as derive.add_argument
    participant p14 as derive.set_defaults
    participant p15 as parser.add_argument
    p0-->>p1: _parser().parse_args
    p0->>p2: _parser
    p0-->>p3: int(args.handler(...))
    p0-->>p4: args.handler(args)
    p0-->>p5: print(..., file=sys.stderr)
    p2-->>p6: argparse.ArgumentParser(description='Collect fail-closed PostgreSQL qualification evidence.')
    p2-->>p7: parser.add_subparsers(dest='command', required=True)
    p2-->>p8: subparsers.add_parser('snapshot')
    p2->>p9: _add_target_arguments
    p2-->>p10: snapshot.add_argument('--label', required=True)
    p2-->>p10: snapshot.add_argument('--snapshot-id', default=...)
    p2-->>p11: uuid4
    p2-->>p10: snapshot.add_argument('--include-explain', action='store_true')
    p2-->>p10: snapshot.add_argument('--output', type=Path, required=True)
    p2-->>p12: snapshot.set_defaults(handler=_snapshot)
    p2-->>p8: subparsers.add_parser('derive')
    p2-->>p13: derive.add_argument('--before', type=Path, required=True)
    p2-->>p13: derive.add_argument('--after', type=Path, required=True)
    p2-->>p13: derive.add_argument('--load-result', type=Path, required=True)
    p2-->>p13: derive.add_argument('--phase', choices=DERIVATION_PHASES, required=True)
    p2-->>p13: derive.add_argument('--evidence', type=Path, action='append', default=[...])
    p2-->>p13: derive.add_argument('--external-output', type=Path, required=True)
    p2-->>p13: derive.add_argument('--integrity-output', type=Path, required=True)
    p2-->>p14: derive.set_defaults(handler=_derive)
    p9-->>p15: parser.add_argument('--database-url', required=True)
    p9-->>p15: parser.add_argument('--authorize-host', required=True)
    p9-->>p15: parser.add_argument('--environment', choices=(...), required=True)
    p9-->>p15: parser.add_argument('--production-authorization')
    p9-->>p15: parser.add_argument('--change-id')
```

> Call sequence diagram shows 29 of 29 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 4 of 4 (0 omitted); unresolved 23 of 23 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 3; effect analysis evaluated: 2, partial: 1, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 3 source steps with known totals: observed: 18, emitted: 16, omitted: 2. Unavailable totals are excluded.

- Effect collector omitted observations before flow assembly; displayed effects are partial.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `_parser().parse_args` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_parser` | `available` | `partial` | `available` | `11` | `9` | `2` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_subparsers` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `subparsers.add_parser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_add_target_arguments` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

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
