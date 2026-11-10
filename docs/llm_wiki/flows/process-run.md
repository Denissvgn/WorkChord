# run

**Entry point:** `main` (`process`)
**Source:** [run](../modules/run.md)
**Modules touched:** [autonomy_canonical](../modules/autonomy_canonical.md), [load_common](../modules/load_common.md), [loader](../modules/loader.md), [result](../modules/result.md), [run](../modules/run.md)

**Related modules:** [load_common](../modules/load_common.md), [result](../modules/result.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as authorized_base_url
    participant p2 as capacity_contract
    participant p3 as traffic_profile
    participant p4 as _phase_shape
    participant p5 as read_json_object
    participant p6 as _load_optional
    participant p7 as _load_external_metrics
    participant p8 as _run_live
    participant p9 as _result_payload
    participant p10 as write_result
    participant p11 as _parser
    participant p12 as QualificationInputError
    participant p13 as sha256_file
    participant p14 as Recorder
    participant p15 as evaluate_external_gates
    participant p16 as contract_member_json
    participant p17 as atomic_write_json
    participant p18 as validate_result
    participant p19 as verify_document
    participant p20 as measurement
    participant p21 as _select_browser_credentials
    participant p22 as _validated_retry_policy
    participant p23 as contract_sha256
    participant p24 as _perform_attempt
    participant p25 as evaluate_client_gates
    participant p26 as evaluate_workload_gates
    participant p27 as contract_member_sha256
    participant p28 as seal_document
    participant p29 as int (scripts/load/run.py:main)
    participant p30 as _parser().parse_args
    p0->>p1: authorized_base_url
    p0->>p2: capacity_contract
    p0->>p3: traffic_profile
    p0->>p4: _phase_shape
    p0->>p5: read_json_object
    p0->>p6: _load_optional
    p0->>p7: _load_external_metrics
    p0->>p8: _run_live
    p0->>p9: _result_payload
    p0->>p10: write_result
    p0->>p11: _parser
    p0->>p12: QualificationInputError
    p0->>p13: sha256_file
    p0->>p14: Recorder
    p0->>p15: evaluate_external_gates
    p2->>p16: contract_member_json
    p10->>p17: atomic_write_json
    p10->>p18: validate_result
    p5->>p19: verify_document
    p9->>p20: measurement
    p8->>p21: _select_browser_credentials
    p8->>p22: _validated_retry_policy
    p9->>p23: contract_sha256
    p8->>p24: _perform_attempt
    p9->>p25: evaluate_client_gates
    p9->>p26: evaluate_workload_gates
    p23->>p27: contract_member_sha256
    p17->>p28: seal_document
    p0-->>p29: int (scripts/load/run.py:main)(...)
    p0-->>p30: _parser().parse_args
```

> Call sequence diagram shows 30 of 914 interactions; 884 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 442 (441 omitted); unresolved 1 of 293 (292 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `scripts/load/run.py:_parser` | 3 | - | external | 3 |
| `scripts/load/run.py:_parser` | 3 | - | unresolved | 21 |
| `scripts/load/common.py:authorized_base_url` | 28 | - | external | 3 |
| `scripts/load/common.py:authorized_base_url` | 28 | [scripts/load/common.py](../modules/load_common.md) | internal | 6 |
| `scripts/load/common.py:authorized_base_url` | 28 | - | unresolved | 2 |
| `scripts/load/common.py:contract_member_json` | 41 | - | unresolved | 1 |
| `scripts/load/common.py:contract_member_json` | 41 | [scripts/load/common.py](../modules/load_common.md) | internal | 3 |
| `scripts/load/common.py:contract_bundle` | 43 | [backend/app/autonomy/contracts/postgresql/loader.py](../modules/loader.md) | internal | 1 |
> Omission summary shows 8 of 119 groups; 111 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 180; effect analysis evaluated: 104, partial: 5, unavailable: 71. Counts include steps omitted from the displayed trace.

Collector observations for 109 source steps with known totals: observed: 541, emitted: 511, omitted: 30. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `11` | `11` | `0` |
| `_parser().parse_args` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_parser` | `available` | `evaluated` | `available` | `8` | `8` | `0` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `tuple (scripts/load/run.py:_parser)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
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
    s5["5. parser.add_argument"]
    s6["6. parser.add_argument"]
    s7["7. tuple (scripts/load/run.py:_parser)"]
    s8["8. parser.add_argument"]
    s9["9. parser.add_argument"]
    s10["10. parser.add_argument"]
    s11["11. parser.add_argument"]
    s12["12. parser.add_argument"]
    s1 -. "_parser().parse_args(data not statically known)" .-> s2
    s1 -->|"_parser(data not statically known)"| s3
    s3 -. "argparse.ArgumentParser(description='Run the WorkChord production-shaped public API load profile.')" .-> s4
    s3 -. "parser.add_argument('--profile', choices=(...), required=True)" .-> s5
    s3 -. "parser.add_argument('--phase', choices=tuple(...), required=True)" .-> s6
    s3 -. "tuple (scripts/load/run.py:_parser)(PHASE_DEFAULTS)" .-> s7
    s3 -. "parser.add_argument('--base-url', required=True)" .-> s8
    s3 -. "parser.add_argument('--authorize-host', required=True)" .-> s9
    s3 -. "parser.add_argument('--environment', choices=(...), required=True)" .-> s10
    s3 -. "parser.add_argument('--production-authorization')" .-> s11
    s3 -. "parser.add_argument('--change-id')" .-> s12
    b0["output print"]
    s1 -. "output print" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["output print"]
    s1 -. "output print" .-> b2
    click s1 "../modules/run.md"
    click s3 "../modules/run.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `QualificationInputError`, `httpx`, `sys` | `args.base_url`, `credentials[...]` | `0`, `...`, `2` |
| `_parser().parse_args` | - | - | - | - |
| `_parser` | - | `PHASE_DEFAULTS`, `Path`, `Path`, `Path`, `Path`, `Path`, `Path` | - | `parser` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `tuple (scripts/load/run.py:_parser)` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | _parser().parse_args | 1541 | `_parser().parse_args(data not statically known)` |
| main | _parser | 1541 | `_parser(data not statically known)` |
| _parser | argparse.ArgumentParser | 1495 | `argparse.ArgumentParser(description='Run the WorkChord production-shaped public API load profile.')` |
| _parser | parser.add_argument | 1498 | `parser.add_argument('--profile', choices=(...), required=True)` |
| _parser | parser.add_argument | 1508 | `parser.add_argument('--phase', choices=tuple(...), required=True)` |
| _parser | tuple (scripts/load/run.py:_parser) | 1508 | `tuple(PHASE_DEFAULTS)` |
| _parser | parser.add_argument | 1509 | `parser.add_argument('--base-url', required=True)` |
| _parser | parser.add_argument | 1510 | `parser.add_argument('--authorize-host', required=True)` |
| _parser | parser.add_argument | 1511 | `parser.add_argument('--environment', choices=(...), required=True)` |
| _parser | parser.add_argument | 1514 | `parser.add_argument('--production-authorization')` |
| _parser | parser.add_argument | 1515 | `parser.add_argument('--change-id')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 1670 |
| output | `print` | `main` | 1682 |
| output | `print` | `main` | 1689 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `main` | `_parser().parse_args` | 1541 |
| external_call | `_parser` | `argparse.ArgumentParser` | 1495 |
| unresolved_call | `_parser` | `parser.add_argument` | 1498 |
| unresolved_call | `_parser` | `parser.add_argument` | 1508 |
| unresolved_call | `_parser` | `parser.add_argument` | 1509 |
| unresolved_call | `_parser` | `parser.add_argument` | 1510 |
| unresolved_call | `_parser` | `parser.add_argument` | 1511 |
| unresolved_call | `_parser` | `parser.add_argument` | 1514 |
| unresolved_call | `_parser` | `parser.add_argument` | 1515 |
| step_limit | `main` | `first 12 steps` | 0 |
| truncated_flow | `main` | `depth limit` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
