# agent_preflight

**Entry point:** `main` (`process`)
**Source:** [agent_preflight](../modules/agent_preflight.md)
**Modules touched:** [agent_preflight](../modules/agent_preflight.md), [autonomy_canonical](../modules/autonomy_canonical.md), [loader](../modules/loader.md), [preflight](../modules/preflight.md)

**Related modules:** [autonomy_canonical](../modules/autonomy_canonical.md), [postgresql___init__](../modules/postgresql___init__.md), [preflight](../modules/preflight.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as load_postgresql_contract_bundle
    participant p2 as evaluate_agent_preflight
    participant p3 as _release_fingerprint
    participant p4 as parse_args
    participant p5 as canonical_json_bytes
    participant p6 as sha256_hex
    participant p7 as _validate_machine_semantics
    participant p8 as _json_value
    participant p9 as ContractBundleError
    participant p10 as PreflightPredicateResult
    participant p11 as AgentPreflightReport
    participant p12 as PostgreSQLContractBundle
    participant p13 as json.dumps (backend/app/cli/agent_preflight.py:main)
    participant p14 as report.model_dump
    participant p15 as args.output.write_text
    participant p16 as print
    participant p17 as argparse.ArgumentParser
    participant p18 as resources.files
    participant p19 as datetime.now
    participant p20 as subprocess.run(…).stdout.strip
    participant p21 as parser.add_argument
    participant p22 as package_root.joinpath(…).read_bytes (backend/app/autonomy/cont…ostgresql_contract_bundle)
    participant p23 as now.utcoffset
    participant p24 as subprocess.run
    participant p25 as parser.parse_args
    participant p26 as package_root.joinpath
    participant p27 as ValueError
    participant p28 as len (backend/app/cli/agent_pre…t.py:_release_fingerprint)
    participant p29 as all (backend/app/cli/agent_pre…t.py:_release_fingerprint)
    p0->>p1: load_postgresql_contract_bundle
    p0->>p2: evaluate_agent_preflight
    p0->>p3: _release_fingerprint
    p0->>p4: parse_args
    p1->>p5: canonical_json_bytes
    p1->>p6: sha256_hex
    p1->>p7: _validate_machine_semantics
    p5->>p8: _json_value
    p1->>p9: ContractBundleError
    p2->>p10: PreflightPredicateResult
    p2->>p11: AgentPreflightReport
    p1->>p12: PostgreSQLContractBundle
    p0-->>p13: json.dumps (backend/app/cli/agent_preflight.py:main)(payload, indent=2, sort_keys=True)
    p0-->>p14: report.model_dump(mode='json')
    p0-->>p15: args.output.write_text(rendered, encoding='utf-8')
    p0-->>p16: print(rendered, end='')
    p4-->>p17: argparse.ArgumentParser(…)
    p1-->>p18: resources.files(__package__)
    p2-->>p19: datetime.now(UTC)
    p3-->>p20: subprocess.run(…).stdout.strip
    p4-->>p21: parser.add_argument('--output', type=Path, help='Optional path for the unsigned diagnostic JSON.')
    p1-->>p22: package_root.joinpath(…).read_bytes (backend/app/autonomy/cont…ostgresql_contract_bundle)
    p2-->>p23: now.utcoffset
    p3-->>p24: subprocess.run([...], check=True, capture_output=True, text=True, timeout=5)
    p4-->>p25: parser.parse_args(argv)
    p1-->>p26: package_root.joinpath('contract-manifest-v1.json')
    p2-->>p27: ValueError('Preflight clock must be timezone-aware')
    p3-->>p28: len (backend/app/cli/agent_pre…t.py:_release_fingerprint)(value)
    p2-->>p27: ValueError('Preflight predicate has duplicate evidence')
    p3-->>p29: all (backend/app/cli/agent_pre…t.py:_release_fingerprint)(...)
```

> Call sequence diagram shows 30 of 153 interactions; 123 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 10 of 70 (60 omitted); unresolved 8 of 42 (34 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/autonomy/contracts/postgresql/loader.py:load_postgresql_contract_bundle` | 6 | - | unresolved | 6 |
| `backend/app/autonomy/contracts/postgresql/loader.py:load_postgresql_contract_bundle` | 6 | [backend/app/autonomy/contracts/postgresql/loader.py](../modules/loader.md) | internal | 8 |
| `backend/app/autonomy/canonical.py:canonical_json_bytes` | 13 | - | unresolved | 1 |
| `backend/app/autonomy/canonical.py:canonical_json_bytes` | 13 | - | external | 1 |
| `backend/app/autonomy/canonical.py:_json_value` | 16 | - | external | 7 |
| `backend/app/autonomy/canonical.py:_json_value` | 16 | - | unresolved | 3 |
| `backend/app/autonomy/canonical.py:_json_value` | 16 | [backend/app/autonomy/canonical.py](../modules/autonomy_canonical.md) | internal | 2 |
| `backend/app/autonomy/contracts/postgresql/loader.py:load_postgresql_contract_bundle` | 6 | - | external | 3 |
> Omission summary shows 8 of 19 groups; 11 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 42; effect analysis evaluated: 15, partial: 1, unavailable: 26. Counts include steps omitted from the displayed trace.

Collector observations for 16 source steps with known totals: observed: 92, emitted: 91, omitted: 1. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `parse_args` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.parse_args` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `load_postgresql_contract_bundle` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `resources.files` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `package_root.joinpath(…).read_bytes (backend/app/autonomy/cont…ostgresql_contract_bundle)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `package_root.joinpath` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `ContractBundleError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `PostgreSQLContractManifest.model_validate_json` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `ContractBundleError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. parse_args"]
    s3["3. argparse.ArgumentParser"]
    s4["4. parser.add_argument"]
    s5["5. parser.parse_args"]
    s6["6. load_postgresql_contract_bundle"]
    s7["7. resources.files"]
    s8["8. package_root.joinpath(…).read_bytes (backend/app/autonomy/cont…ostgresql_contract_bundle)"]
    s9["9. package_root.joinpath"]
    s10["10. ContractBundleError"]
    s11["11. PostgreSQLContractManifest.model_validate_json"]
    s12["12. ContractBundleError"]
    s1 -->|"parse_args(argv)"| s2
    s2 -. "argparse.ArgumentParser(…)" .-> s3
    s2 -. "parser.add_argument('--output', type=Path, help='Optional path for the unsigned diagnostic JSON.')" .-> s4
    s2 -. "parser.parse_args(argv)" .-> s5
    s1 -->|"load_postgresql_contract_bundle(data not statically known)"| s6
    s6 -. "resources.files(__package__)" .-> s7
    s6 -. "package_root.joinpath(…).read_bytes (backend/app/autonomy/cont…ostgresql_contract_bundle)(data not statically known)" .-> s8
    s6 -. "package_root.joinpath('contract-manifest-v1.json')" .-> s9
    s6 -->|"ContractBundleError('Packaged PostgreSQL contract manifest is absent')"| s10
    s6 -. "PostgreSQLContractManifest.model_validate_json(raw_manifest)" .-> s11
    s6 -->|"ContractBundleError('Packaged PostgreSQL contract manifest is invalid')"| s12
    b0["filesystem_write args.output.write_text"]
    s1 -. "filesystem_write args.output.write_text" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["mutation blocker_codes.append"]
    s6 -. "mutation blocker_codes.append" .-> b2
    click s1 "../modules/agent_preflight.md"
    click s2 "../modules/agent_preflight.md"
    click s6 "../modules/loader.md"
    click s10 "../modules/loader.md"
    click s12 "../modules/loader.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | `argv: list[str] \| None` | - | - | `2` |
| `parse_args` | `argv: list[str] \| None` | `Path` | - | `parser.parse_args(...)` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `load_postgresql_contract_bundle` | `archive: ImmutableContractArchive \| None`, `require_archive: bool` | - | `members[...]` | `PostgreSQLContractBundle(...)` |
| `resources.files` | - | - | - | - |
| `package_root.joinpath(…).read_bytes (backend/app/autonomy/cont…ostgresql_contract_bundle)` | - | - | - | - |
| `package_root.joinpath` | - | - | - | - |
| `ContractBundleError` | - | - | - | - |
| `PostgreSQLContractManifest.model_validate_json` | - | - | - | - |
| `ContractBundleError` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | parse_args | 50 | `parse_args(argv)` |
| parse_args | argparse.ArgumentParser | 35 | `argparse.ArgumentParser(description='Evaluate the locally discoverable PostgreSQL autonomous-start inputs. This diagnostic never substitutes for the required remote-signed preflight.')` |
| parse_args | parser.add_argument | 41 | `parser.add_argument('--output', type=Path, help='Optional path for the unsigned diagnostic JSON.')` |
| parse_args | parser.parse_args | 46 | `parser.parse_args(argv)` |
| main | load_postgresql_contract_bundle | 51 | `load_postgresql_contract_bundle(data not statically known)` |
| load_postgresql_contract_bundle | resources.files | 179 | `resources.files(__package__)` |
| load_postgresql_contract_bundle | package_root.joinpath(…).read_bytes (backend/app/autonomy/cont…ostgresql_contract_bundle) | 181 | `package_root.joinpath('contract-manifest-v1.json').read_bytes(data not statically known)` |
| load_postgresql_contract_bundle | package_root.joinpath | 181 | `package_root.joinpath('contract-manifest-v1.json')` |
| load_postgresql_contract_bundle | ContractBundleError | 183 | `ContractBundleError('Packaged PostgreSQL contract manifest is absent')` |
| load_postgresql_contract_bundle | PostgreSQLContractManifest.model_validate_json | 185 | `PostgreSQLContractManifest.model_validate_json(raw_manifest)` |
| load_postgresql_contract_bundle | ContractBundleError | 187 | `ContractBundleError('Packaged PostgreSQL contract manifest is invalid')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| filesystem_write | `args.output.write_text` | `main` | 64 |
| output | `print` | `main` | 66 |
| mutation | `blocker_codes.append` | `load_postgresql_contract_bundle` | 211 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `parse_args` | `argparse.ArgumentParser` | 35 |
| unresolved_call | `parse_args` | `parser.add_argument` | 41 |
| unresolved_call | `parse_args` | `parser.parse_args` | 46 |
| external_call | `load_postgresql_contract_bundle` | `resources.files` | 179 |
| unresolved_call | `load_postgresql_contract_bundle` | `package_root.joinpath('contract-manifest-v1.json').read_bytes` | 181 |
| unresolved_call | `load_postgresql_contract_bundle` | `package_root.joinpath` | 181 |
| unresolved_call | `load_postgresql_contract_bundle` | `PostgreSQLContractManifest.model_validate_json` | 185 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
