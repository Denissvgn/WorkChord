# resilience

**Entry point:** `main` (`process`)
**Source:** [resilience](../modules/resilience.md)
**Modules touched:** [autonomy_canonical](../modules/autonomy_canonical.md), [load_common](../modules/load_common.md), [loader](../modules/loader.md), [resilience](../modules/resilience.md), [result](../modules/result.md)

**Related modules:** [load_common](../modules/load_common.md), [result](../modules/result.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as atomic_write_json
    participant p2 as evaluate
    participant p3 as _parser
    participant p4 as seal_document
    participant p5 as contract_member_json
    participant p6 as _elapsed
    participant p7 as percentile
    participant p8 as capacity_contract
    participant p9 as contract_bundle
    participant p10 as _time
    participant p11 as load_postgresql_contract_bundle
    participant p12 as canonical_json_bytes (backend/app/autonomy/canonical.py)
    participant p13 as sha256_hex
    participant p14 as _validate_machine_semantics
    participant p15 as QualificationInputError
    participant p16 as _gate
    participant p17 as utc_now_text
    participant p18 as sha256_bytes
    participant p19 as canonical_json_bytes (scripts/load/common.py)
    participant p20 as ContractBundleError
    participant p21 as PostgreSQLContractBundle
    participant p22 as _json_value
    participant p23 as print
    participant p24 as _parser().parse_args
    participant p25 as read_json_object
    participant p26 as argparse.ArgumentParser
    participant p27 as parser.add_argument
    participant p28 as dict (scripts/load/common.py:atomic_write_json)
    participant p29 as sorted (scripts/load/resilience.py:evaluate)
    p0->>p1: atomic_write_json
    p0->>p2: evaluate
    p0->>p3: _parser
    p1->>p4: seal_document
    p2->>p5: contract_member_json
    p2->>p6: _elapsed
    p2->>p7: percentile
    p2->>p8: capacity_contract
    p5->>p9: contract_bundle
    p6->>p10: _time
    p9->>p11: load_postgresql_contract_bundle
    p11->>p12: canonical_json_bytes (backend/app/autonomy/canonical.py)
    p11->>p13: sha256_hex
    p11->>p14: _validate_machine_semantics
    p2->>p15: QualificationInputError
    p2->>p16: _gate
    p2->>p17: utc_now_text
    p4->>p18: sha256_bytes
    p4->>p19: canonical_json_bytes (scripts/load/common.py)
    p11->>p20: ContractBundleError
    p11->>p21: PostgreSQLContractBundle
    p12->>p22: _json_value
    p0-->>p23: print(...)
    p0-->>p24: _parser().parse_args
    p0-->>p25: read_json_object(args.observations, sealed=True)
    p0-->>p23: print(..., file=sys.stderr)
    p3-->>p26: argparse.ArgumentParser(description='Evaluate sealed PostgreSQL fault and recovery observations.')
    p3-->>p27: parser.add_argument('--observations', type=Path, required=True)
    p1-->>p28: dict (scripts/load/common.py:atomic_write_json)(payload)
    p2-->>p29: sorted (scripts/load/resilience.py:evaluate)(..., key=...)
```

> Call sequence diagram shows 30 of 217 interactions; 187 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 5 of 95 (90 omitted); unresolved 3 of 54 (51 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `scripts/load/resilience.py:_parser` | 3 | - | unresolved | 1 |
| `scripts/load/common.py:seal_document` | 9 | [scripts/load/common.py](../modules/load_common.md) | internal | 1 |
| `scripts/load/common.py:seal_document` | 9 | - | external | 1 |
| `scripts/load/common.py:sha256_bytes` | 12 | - | unresolved | 1 |
| `scripts/load/common.py:sha256_bytes` | 12 | - | external | 1 |
| `scripts/load/common.py:canonical_json_bytes` | 15 | - | unresolved | 1 |
| `scripts/load/common.py:canonical_json_bytes` | 15 | - | external | 1 |
| `scripts/load/common.py:atomic_write_json` | 8 | - | unresolved | 9 |
> Omission summary shows 8 of 41 groups; 33 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 69; effect analysis evaluated: 33, partial: 0, unavailable: 36. Counts include steps omitted from the displayed trace.

Collector observations for 33 source steps with known totals: observed: 123, emitted: 123, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `_parser().parse_args` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_parser` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `read_json_object` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `atomic_write_json` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `seal_document` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `QualificationInputError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `dict (scripts/load/common.py:seal_document)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `sha256_bytes` | `available` | `evaluated` | `available` | `2` | `2` | `0` |

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. _parser().parse_args"]
    s3["3. _parser"]
    s4["4. argparse.ArgumentParser"]
    s5["5. parser.add_argument"]
    s6["6. parser.add_argument"]
    s7["7. read_json_object"]
    s8["8. atomic_write_json"]
    s9["9. seal_document"]
    s10["10. QualificationInputError"]
    s11["11. dict (scripts/load/common.py:seal_document)"]
    s12["12. sha256_bytes"]
    s1 -. "_parser().parse_args(data not statically known)" .-> s2
    s1 -->|"_parser(data not statically known)"| s3
    s3 -. "argparse.ArgumentParser(description='Evaluate sealed PostgreSQL fault and recovery observations.')" .-> s4
    s3 -. "parser.add_argument('--observations', type=Path, required=True)" .-> s5
    s3 -. "parser.add_argument('--output', type=Path, required=True)" .-> s6
    s1 -. "read_json_object(args.observations, sealed=True)" .-> s7
    s1 -->|"atomic_write_json(args.output, evaluate(...))"| s8
    s8 -->|"seal_document(payload)"| s9
    s9 -->|"QualificationInputError(...)"| s10
    s9 -. "dict (scripts/load/common.py:seal_document)(payload)" .-> s11
    s9 -->|"sha256_bytes(canonical_json_bytes(...))"| s12
    b0["output print"]
    s1 -. "output print" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["filesystem_write temporary.unlink"]
    s8 -. "filesystem_write temporary.unlink" .-> b2
    click s1 "../modules/resilience.md"
    click s3 "../modules/resilience.md"
    click s8 "../modules/load_common.md"
    click s9 "../modules/load_common.md"
    click s10 "../modules/load_common.md"
    click s12 "../modules/load_common.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `QualificationInputError`, `sys` | - | `...`, `2` |
| `_parser().parse_args` | - | - | - | - |
| `_parser` | - | `Path`, `Path` | - | `parser` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `read_json_object` | - | - | - | - |
| `atomic_write_json` | `path: Path`, `payload: Mapping[str, Any]`, `sealed: bool`, `mode: int` | `os` | - | `document` |
| `seal_document` | `payload: Mapping[str, Any]` | `DOCUMENT_CHECKSUM_FIELD`, `DOCUMENT_CHECKSUM_FIELD` | `document[...]` | `document` |
| `QualificationInputError` | - | - | - | - |
| `dict (scripts/load/common.py:seal_document)` | - | - | - | - |
| `sha256_bytes` | `value: bytes` | - | - | `...` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | _parser().parse_args | 209 | `_parser().parse_args(data not statically known)` |
| main | _parser | 209 | `_parser(data not statically known)` |
| _parser | argparse.ArgumentParser | 200 | `argparse.ArgumentParser(description='Evaluate sealed PostgreSQL fault and recovery observations.')` |
| _parser | parser.add_argument | 203 | `parser.add_argument('--observations', type=Path, required=True)` |
| _parser | parser.add_argument | 204 | `parser.add_argument('--output', type=Path, required=True)` |
| main | read_json_object | 211 | `read_json_object(args.observations, sealed=True)` |
| main | atomic_write_json | 212 | `atomic_write_json(args.output, evaluate(...))` |
| atomic_write_json | seal_document | 141 | `seal_document(payload)` |
| seal_document | QualificationInputError | 62 | `QualificationInputError(...)` |
| seal_document | dict (scripts/load/common.py:seal_document) | 65 | `dict(payload)` |
| seal_document | sha256_bytes | 66 | `sha256_bytes(canonical_json_bytes(...))` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 213 |
| output | `print` | `main` | 219 |
| filesystem_write | `temporary.unlink` | `atomic_write_json` | 165 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `main` | `_parser().parse_args` | 209 |
| external_call | `_parser` | `argparse.ArgumentParser` | 200 |
| unresolved_call | `_parser` | `parser.add_argument` | 203 |
| unresolved_call | `_parser` | `parser.add_argument` | 204 |
| unresolved_call | `main` | `read_json_object` | 211 |
| step_limit | `main` | `first 12 steps` | 0 |
| truncated_flow | `main` | `depth limit` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
