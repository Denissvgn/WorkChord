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

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as _parser().parse_args
    participant p2 as _parser
    participant p3 as argparse.ArgumentParser
    participant p4 as parser.add_argument
    participant p5 as os.getenv (scripts/load/seed.py:_parser)
    participant p6 as QualificationInputError
    participant p7 as _dry_manifest
    participant p8 as _profile_cardinalities
    participant p9 as dict (scripts/load/seed.py:_profile_cardinalities)
    participant p10 as capacity_contract
    participant p11 as contract_member_json
    participant p12 as contract_bundle().member_json
    participant p13 as contract_bundle
    participant p14 as load_postgresql_contract_bundle
    participant p15 as isinstance (scripts/load/common.py:contract_member_json)
    participant p16 as contract.get
    p0-->>p1: _parser().parse_args
    p0->>p2: _parser
    p2-->>p3: argparse.ArgumentParser
    p2-->>p4: parser.add_argument
    p2-->>p4: parser.add_argument
    p2-->>p4: parser.add_argument
    p2-->>p4: parser.add_argument
    p2-->>p4: parser.add_argument
    p2-->>p5: os.getenv (scripts/load/seed.py:_parser)
    p2-->>p4: parser.add_argument
    p2-->>p4: parser.add_argument
    p2-->>p4: parser.add_argument
    p2-->>p4: parser.add_argument
    p2-->>p4: parser.add_argument
    p0->>p6: QualificationInputError
    p0->>p7: _dry_manifest
    p7->>p8: _profile_cardinalities
    p8-->>p9: dict (scripts/load/seed.py:_profile_cardinalities)
    p8->>p10: capacity_contract
    p10->>p11: contract_member_json
    p11-->>p12: contract_bundle().member_json
    p11->>p13: contract_bundle
    p13->>p14: load_postgresql_contract_bundle
    p13->>p6: QualificationInputError
    p11->>p6: QualificationInputError
    p11-->>p15: isinstance (scripts/load/common.py:contract_member_json)
    p11->>p6: QualificationInputError
    p10-->>p16: contract.get
    p10-->>p16: contract.get
    p10->>p6: QualificationInputError
```

> Call sequence diagram shows 30 of 360 interactions; 330 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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
| main | _parser().parse_args | 1087 | `_parser().parse_args(data not statically known)` |
| main | _parser | 1087 | `_parser(data not statically known)` |
| _parser | argparse.ArgumentParser | 1067 | `argparse.ArgumentParser(description='Seed an isolated PostgreSQL qualification database.')` |
| _parser | parser.add_argument | 1070 | `parser.add_argument('--profile', choices=(...), required=True)` |
| _parser | parser.add_argument | 1071 | `parser.add_argument('--seed', type=int, default=20260718)` |
| _parser | parser.add_argument | 1072 | `parser.add_argument('--as-of', help='Timezone-aware deterministic reference time for session states')` |
| _parser | parser.add_argument | 1076 | `parser.add_argument('--dry-run', action='store_true')` |
| _parser | parser.add_argument | 1077 | `parser.add_argument('--database-url', default=os.getenv(...))` |
| _parser | os.getenv (scripts/load/seed.py:_parser) | 1077 | `os.getenv('DATABASE_URL')` |
| _parser | parser.add_argument | 1078 | `parser.add_argument('--authorize-target')` |
| _parser | parser.add_argument | 1079 | `parser.add_argument('--checkpoint', type=Path)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 1110 |
| output | `print` | `main` | 1116 |
| environment_read | `os.getenv` | `_parser` | 1077 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `main` | `_parser().parse_args` | 1087 |
| external_call | `_parser` | `argparse.ArgumentParser` | 1067 |
| unresolved_call | `_parser` | `parser.add_argument` | 1070 |
| unresolved_call | `_parser` | `parser.add_argument` | 1071 |
| unresolved_call | `_parser` | `parser.add_argument` | 1072 |
| unresolved_call | `_parser` | `parser.add_argument` | 1076 |
| unresolved_call | `_parser` | `parser.add_argument` | 1078 |
| unresolved_call | `_parser` | `parser.add_argument` | 1079 |
| step_limit | `main` | `first 12 steps` | 0 |
| truncated_flow | `main` | `depth limit` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
