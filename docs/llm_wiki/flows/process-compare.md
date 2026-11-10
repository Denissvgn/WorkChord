# compare

**Entry point:** `main` (`process`)
**Source:** [compare](../modules/compare.md)
**Modules touched:** [autonomy_canonical](../modules/autonomy_canonical.md), [compare](../modules/compare.md), [load_common](../modules/load_common.md), [loader](../modules/loader.md), [result](../modules/result.md)

**Related modules:** [load_common](../modules/load_common.md), [result](../modules/result.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as _main
    participant p2 as _parser
    participant p3 as read_json_object
    participant p4 as validate_result
    participant p5 as atomic_write_json
    participant p6 as _measurement_deltas
    participant p7 as seal_document
    participant p8 as contract_member_json
    participant p9 as verify_document
    participant p10 as contract_bundle
    participant p11 as load_postgresql_contract_bundle
    participant p12 as QualificationInputError
    participant p13 as utc_now_text
    participant p14 as _delta
    participant p15 as sha256_bytes
    participant p16 as canonical_json_bytes (scripts/load/common.py)
    participant p17 as ContractBundleError
    participant p18 as canonical_json_bytes (backend/app/autonomy/canonical.py)
    participant p19 as sha256_hex
    participant p20 as _validate_machine_semantics
    participant p21 as PostgreSQLContractBundle
    participant p22 as print (scripts/load/compare.py:main)
    participant p23 as _parser().parse_args
    participant p24 as argparse.ArgumentParser
    participant p25 as parser.add_argument
    participant p26 as sorted (scripts/load/compare.py:_main)
    participant p27 as set (scripts/load/compare.py:_main)
    p0->>p1: _main
    p0->>p2: _parser
    p1->>p3: read_json_object
    p1->>p4: validate_result
    p1->>p5: atomic_write_json
    p1->>p6: _measurement_deltas
    p5->>p7: seal_document
    p4->>p8: contract_member_json
    p3->>p9: verify_document
    p8->>p10: contract_bundle
    p10->>p11: load_postgresql_contract_bundle
    p1->>p12: QualificationInputError
    p1->>p13: utc_now_text
    p6->>p14: _delta
    p7->>p15: sha256_bytes
    p7->>p16: canonical_json_bytes (scripts/load/common.py)
    p11->>p17: ContractBundleError
    p11->>p18: canonical_json_bytes (backend/app/autonomy/canonical.py)
    p11->>p19: sha256_hex
    p11->>p20: _validate_machine_semantics
    p11->>p21: PostgreSQLContractBundle
    p0-->>p22: print (scripts/load/compare.py:main)(..., file=sys.stderr)
    p0-->>p23: _parser().parse_args
    p2-->>p24: argparse.ArgumentParser(description='Compare two sealed load results.')
    p2-->>p25: parser.add_argument('--baseline', type=Path, required=True)
    p2-->>p25: parser.add_argument('--tuned', type=Path, required=True)
    p2-->>p25: parser.add_argument('--change', action='append', required=True)
    p2-->>p25: parser.add_argument('--output', type=Path, required=True)
    p1-->>p26: sorted (scripts/load/compare.py:_main)(...)
    p1-->>p27: set (scripts/load/compare.py:_main)(baseline[...])
```

> Call sequence diagram shows 30 of 134 interactions; 104 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 4 of 39 (35 omitted); unresolved 5 of 48 (43 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `scripts/load/common.py:read_json_object` | 10 | - | external | 2 |
| `scripts/load/common.py:read_json_object` | 10 | - | unresolved | 1 |
| `scripts/load/common.py:read_json_object` | 10 | [scripts/load/common.py](../modules/load_common.md) | internal | 2 |
| `scripts/load/common.py:verify_document` | 16 | - | unresolved | 2 |
| `scripts/load/common.py:verify_document` | 16 | - | external | 3 |
| `scripts/load/common.py:verify_document` | 16 | [scripts/load/common.py](../modules/load_common.md) | internal | 4 |
| `scripts/load/common.py:sha256_bytes` | 23 | - | unresolved | 1 |
| `scripts/load/common.py:sha256_bytes` | 23 | - | external | 1 |
> Omission summary shows 8 of 34 groups; 26 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 48; effect analysis evaluated: 27, partial: 0, unavailable: 21. Counts include steps omitted from the displayed trace.

Collector observations for 27 source steps with known totals: observed: 99, emitted: 99, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `_parser().parse_args` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_parser` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_main` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `read_json_object` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `json.loads` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `path.read_text` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. _parser().parse_args"]
    s3["3. _parser"]
    s4["4. argparse.ArgumentParser"]
    s5["5. parser.add_argument"]
    s6["6. parser.add_argument"]
    s7["7. parser.add_argument"]
    s8["8. parser.add_argument"]
    s9["9. _main"]
    s10["10. read_json_object"]
    s11["11. json.loads"]
    s12["12. path.read_text"]
    s1 -. "_parser().parse_args(data not statically known)" .-> s2
    s1 -->|"_parser(data not statically known)"| s3
    s3 -. "argparse.ArgumentParser(description='Compare two sealed load results.')" .-> s4
    s3 -. "parser.add_argument('--baseline', type=Path, required=True)" .-> s5
    s3 -. "parser.add_argument('--tuned', type=Path, required=True)" .-> s6
    s3 -. "parser.add_argument('--change', action='append', required=True)" .-> s7
    s3 -. "parser.add_argument('--output', type=Path, required=True)" .-> s8
    s1 -->|"_main(args)"| s9
    s9 -->|"read_json_object(args.baseline, sealed=True)"| s10
    s10 -. "json.loads(path.read_text(...))" .-> s11
    s10 -. "path.read_text(encoding='utf-8')" .-> s12
    b0["output print"]
    s1 -. "output print" .-> b0
    b1["mutation regressions.append"]
    s9 -. "mutation regressions.append" .-> b1
    b2["mutation improvements.append"]
    s9 -. "mutation improvements.append" .-> b2
    b3["output print"]
    s9 -. "output print" .-> b3
    b4["filesystem_read path.read_text"]
    s10 -. "filesystem_read path.read_text" .-> b4
    click s1 "../modules/compare.md"
    click s3 "../modules/compare.md"
    click s9 "../modules/compare.md"
    click s10 "../modules/load_common.md"
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
| `main` | - | `QualificationInputError`, `sys` | - | `_main(...)`, `2` |
| `_parser().parse_args` | - | - | - | - |
| `_parser` | - | `Path`, `Path`, `Path` | - | `parser` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `_main` | `args: argparse.Namespace` | - | `gate_transitions[...]` | `...` |
| `read_json_object` | `path: Path`, `sealed: bool` | `json` | - | `value` |
| `json.loads` | - | - | - | - |
| `path.read_text` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | _parser().parse_args | 148 | `_parser().parse_args(data not statically known)` |
| main | _parser | 148 | `_parser(data not statically known)` |
| _parser | argparse.ArgumentParser | 139 | `argparse.ArgumentParser(description='Compare two sealed load results.')` |
| _parser | parser.add_argument | 140 | `parser.add_argument('--baseline', type=Path, required=True)` |
| _parser | parser.add_argument | 141 | `parser.add_argument('--tuned', type=Path, required=True)` |
| _parser | parser.add_argument | 142 | `parser.add_argument('--change', action='append', required=True)` |
| _parser | parser.add_argument | 143 | `parser.add_argument('--output', type=Path, required=True)` |
| main | _main | 150 | `_main(args)` |
| _main | read_json_object | 50 | `read_json_object(args.baseline, sealed=True)` |
| read_json_object | json.loads | 90 | `json.loads(path.read_text(...))` |
| read_json_object | path.read_text | 90 | `path.read_text(encoding='utf-8')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 152 |
| mutation | `regressions.append` | `_main` | 83 |
| mutation | `improvements.append` | `_main` | 85 |
| output | `print` | `_main` | 132 |
| filesystem_read | `path.read_text` | `read_json_object` | 90 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `main` | `_parser().parse_args` | 148 |
| external_call | `_parser` | `argparse.ArgumentParser` | 139 |
| unresolved_call | `_parser` | `parser.add_argument` | 140 |
| unresolved_call | `_parser` | `parser.add_argument` | 141 |
| unresolved_call | `_parser` | `parser.add_argument` | 142 |
| unresolved_call | `_parser` | `parser.add_argument` | 143 |
| step_limit | `main` | `first 12 steps` | 0 |
| truncated_flow | `main` | `depth limit` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
