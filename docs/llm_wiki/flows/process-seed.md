# seed

**Entry point:** `main` (`process`)
**Source:** [seed](../modules/seed.md)
**Modules touched:** [config](../modules/config.md), [database_config](../modules/database_config.md), [load_common](../modules/load_common.md), [loader](../modules/loader.md), and 2 more

**Complete modules touched:**

- [config](../modules/config.md)
- [database_config](../modules/database_config.md)
- [load_common](../modules/load_common.md)
- [loader](../modules/loader.md)
- [seed](../modules/seed.md)
- [upgrade_service](../modules/upgrade_service.md)

**Related modules:** [load_common](../modules/load_common.md), [upgrade_service](../modules/upgrade_service.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as _dry_manifest
    participant p2 as seed_database
    participant p3 as _parser
    participant p4 as QualificationInputError
    participant p5 as _profile_cardinalities
    participant p6 as contract_sha256
    participant p7 as _derived_cardinalities
    participant p8 as atomic_write_json
    participant p9 as _validate_target
    participant p10 as _load_checkpoint
    participant p11 as _session_rows
    participant p12 as _actor_rows
    participant p13 as _require_initial_target
    participant p14 as _single_stage
    participant p15 as _chunk_stage
    participant p16 as _insert_dependencies
    participant p17 as _write_credentials
    participant p18 as contract_member_sha256
    participant p19 as seal_document
    participant p20 as capacity_contract
    participant p21 as _empty_checkpoint
    participant p22 as read_json_object
    participant p23 as _dependency_edges
    participant p24 as _record_stage
    participant p25 as head_revision
    participant p26 as _count
    participant p27 as contract_member_json
    participant p28 as _save_checkpoint
    participant p29 as print
    participant p30 as _parser().parse_args
    p0->>p1: _dry_manifest
    p0->>p2: seed_database
    p0->>p3: _parser
    p0->>p4: QualificationInputError
    p1->>p5: _profile_cardinalities
    p1->>p6: contract_sha256
    p1->>p7: _derived_cardinalities
    p1->>p8: atomic_write_json
    p2->>p9: _validate_target
    p2->>p10: _load_checkpoint
    p2->>p11: _session_rows
    p2->>p12: _actor_rows
    p2->>p13: _require_initial_target
    p2->>p14: _single_stage
    p2->>p15: _chunk_stage
    p2->>p16: _insert_dependencies
    p2->>p17: _write_credentials
    p6->>p18: contract_member_sha256
    p8->>p19: seal_document
    p5->>p20: capacity_contract
    p10->>p21: _empty_checkpoint
    p10->>p22: read_json_object
    p16->>p23: _dependency_edges
    p14->>p24: _record_stage
    p13->>p25: head_revision
    p13->>p26: _count
    p20->>p27: contract_member_json
    p24->>p28: _save_checkpoint
    p0-->>p29: print(...)
    p0-->>p30: _parser().parse_args
```

> Call sequence diagram shows 30 of 362 interactions; 332 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 112 (111 omitted); unresolved 1 of 121 (120 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `scripts/load/seed.py:_parser` | 3 | - | external | 2 |
| `scripts/load/seed.py:_parser` | 3 | - | unresolved | 10 |
| `scripts/load/seed.py:_profile_cardinalities` | 18 | - | external | 2 |
| `scripts/load/common.py:contract_member_json` | 21 | - | unresolved | 1 |
| `scripts/load/common.py:contract_member_json` | 21 | [scripts/load/common.py](../modules/load_common.md) | internal | 3 |
| `scripts/load/common.py:contract_bundle` | 23 | [backend/app/autonomy/contracts/postgresql/loader.py](../modules/loader.md) | internal | 1 |
| `scripts/load/common.py:contract_bundle` | 23 | [scripts/load/common.py](../modules/load_common.md) | internal | 1 |
| `scripts/load/common.py:contract_member_json` | 21 | - | external | 1 |
> Omission summary shows 8 of 124 groups; 116 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 130; effect analysis evaluated: 99, partial: 0, unavailable: 31. Counts include steps omitted from the displayed trace.

Collector observations for 99 source steps with known totals: observed: 418, emitted: 418, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `_parser().parse_args` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_parser` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `os.getenv (scripts/load/seed.py:_parser)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
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
    s7["7. parser.add_argument"]
    s8["8. parser.add_argument"]
    s9["9. parser.add_argument"]
    s10["10. os.getenv (scripts/load/seed.py:_parser)"]
    s11["11. parser.add_argument"]
    s12["12. parser.add_argument"]
    s1 -. "_parser().parse_args(data not statically known)" .-> s2
    s1 -->|"_parser(data not statically known)"| s3
    s3 -. "argparse.ArgumentParser(description='Seed an isolated PostgreSQL qualification database.')" .-> s4
    s3 -. "parser.add_argument('--profile', choices=(...), required=True)" .-> s5
    s3 -. "parser.add_argument('--seed', type=int, default=20260718)" .-> s6
    s3 -. "parser.add_argument('--as-of', help='Timezone-aware deterministic reference time for session states')" .-> s7
    s3 -. "parser.add_argument('--dry-run', action='store_true')" .-> s8
    s3 -. "parser.add_argument('--database-url', default=os.getenv(...))" .-> s9
    s3 -. "os.getenv (scripts/load/seed.py:_parser)('DATABASE_URL')" .-> s10
    s3 -. "parser.add_argument('--authorize-target')" .-> s11
    s3 -. "parser.add_argument('--checkpoint', type=Path)" .-> s12
    b0["output print"]
    s1 -. "output print" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["environment_read os.getenv"]
    s3 -. "environment_read os.getenv" .-> b2
    click s1 "../modules/seed.md"
    click s3 "../modules/seed.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `QualificationInputError`, `sys` | - | `0`, `2` |
| `_parser().parse_args` | - | - | - | - |
| `_parser` | - | `Path`, `Path`, `Path` | - | `parser` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `os.getenv (scripts/load/seed.py:_parser)` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | _parser().parse_args | 1092 | `_parser().parse_args(data not statically known)` |
| main | _parser | 1092 | `_parser(data not statically known)` |
| _parser | argparse.ArgumentParser | 1072 | `argparse.ArgumentParser(description='Seed an isolated PostgreSQL qualification database.')` |
| _parser | parser.add_argument | 1075 | `parser.add_argument('--profile', choices=(...), required=True)` |
| _parser | parser.add_argument | 1076 | `parser.add_argument('--seed', type=int, default=20260718)` |
| _parser | parser.add_argument | 1077 | `parser.add_argument('--as-of', help='Timezone-aware deterministic reference time for session states')` |
| _parser | parser.add_argument | 1081 | `parser.add_argument('--dry-run', action='store_true')` |
| _parser | parser.add_argument | 1082 | `parser.add_argument('--database-url', default=os.getenv(...))` |
| _parser | os.getenv (scripts/load/seed.py:_parser) | 1082 | `os.getenv('DATABASE_URL')` |
| _parser | parser.add_argument | 1083 | `parser.add_argument('--authorize-target')` |
| _parser | parser.add_argument | 1084 | `parser.add_argument('--checkpoint', type=Path)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 1115 |
| output | `print` | `main` | 1121 |
| environment_read | `os.getenv` | `_parser` | 1082 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `main` | `_parser().parse_args` | 1092 |
| external_call | `_parser` | `argparse.ArgumentParser` | 1072 |
| unresolved_call | `_parser` | `parser.add_argument` | 1075 |
| unresolved_call | `_parser` | `parser.add_argument` | 1076 |
| unresolved_call | `_parser` | `parser.add_argument` | 1077 |
| unresolved_call | `_parser` | `parser.add_argument` | 1081 |
| unresolved_call | `_parser` | `parser.add_argument` | 1083 |
| unresolved_call | `_parser` | `parser.add_argument` | 1084 |
| step_limit | `main` | `first 12 steps` | 0 |
| truncated_flow | `main` | `depth limit` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
