# build_identity

**Entry point:** `main` (`process`)
**Source:** [build_identity](../modules/build_identity.md)
**Modules touched:** [build_identity](../modules/build_identity.md)

**Related modules:** [autonomy_canonical](../modules/autonomy_canonical.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as _parse_args
    participant p2 as BackendBuildIdentity
    participant p3 as package_artifact_digest
    participant p4 as Path
    participant p5 as Path(…).resolve
    participant p6 as BuildIdentity.model_validate_json
    participant p7 as args.frontend_identity.read_text
    participant p8 as ValueError (backend/app/build_identity.py:main)
    participant p9 as args.output.parent.mkdir
    participant p10 as args.output.write_text
    participant p11 as json.dumps
    participant p12 as identity.model_dump
    participant p13 as args.output.chmod
    participant p14 as argparse.ArgumentParser
    participant p15 as sha256
    participant p16 as parser.add_argument
    participant p17 as sorted
    participant p18 as package_root.rglob
    participant p19 as path.is_file
    participant p20 as parser.parse_args
    participant p21 as ValueError (backend/app/build_identit…py:package_artifact_digest)
    participant p22 as member.relative_to(…).as_posix().encode
    participant p23 as member.relative_to(…).as_posix
    participant p24 as member.relative_to
    participant p25 as digest.update
    p0->>p1: _parse_args
    p0->>p2: BackendBuildIdentity
    p0->>p3: package_artifact_digest
    p0-->>p4: Path(__file__)
    p0-->>p5: Path(…).resolve
    p0-->>p6: BuildIdentity.model_validate_json(args.frontend_identity.read_text(...))
    p0-->>p7: args.frontend_identity.read_text(encoding='utf-8')
    p0-->>p8: ValueError (backend/app/build_identity.py:main)('Expected a frontend build identity')
    p0-->>p8: ValueError (backend/app/build_identity.py:main)('Frontend and backend source revisions differ')
    p0-->>p9: args.output.parent.mkdir(parents=True, exist_ok=True)
    p0-->>p10: args.output.write_text(..., encoding='utf-8')
    p0-->>p11: json.dumps(identity.model_dump(...), sort_keys=True)
    p0-->>p12: identity.model_dump(mode='json')
    p0-->>p13: args.output.chmod(292)
    p1-->>p14: argparse.ArgumentParser(description='Write the immutable backend container build identity.')
    p3-->>p15: sha256
    p1-->>p16: parser.add_argument('--source-revision', required=True)
    p3-->>p17: sorted(...)
    p1-->>p16: parser.add_argument('--frontend-identity', type=Path, required=True)
    p3-->>p18: package_root.rglob('*')
    p1-->>p16: parser.add_argument('--output', type=Path, required=True)
    p3-->>p19: path.is_file
    p1-->>p20: parser.parse_args
    p3-->>p21: ValueError (backend/app/build_identit…py:package_artifact_digest)('Backend package contains no identity members')
    p3-->>p22: member.relative_to(…).as_posix().encode('utf-8')
    p3-->>p23: member.relative_to(…).as_posix
    p3-->>p24: member.relative_to(package_root)
    p3-->>p25: digest.update(relative)
    p3-->>p25: digest.update(b'\x00')
    p3-->>p25: digest.update(...)
```

> Call sequence diagram shows 30 of 35 interactions; 5 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 8 of 9 (1 omitted); unresolved 19 of 23 (4 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/build_identity.py:package_artifact_digest` | 15 | - | unresolved | 4 |
| `backend/app/build_identity.py:package_artifact_digest` | 15 | - | external | 1 |
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 4; effect analysis evaluated: 3, partial: 0, unavailable: 1. Counts include steps omitted from the displayed trace.

Collector observations for 3 source steps with known totals: observed: 12, emitted: 12, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `_parse_args` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.parse_args` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `Path(…).resolve` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `Path` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `BuildIdentity.model_validate_json` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `args.frontend_identity.read_text` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `ValueError (backend/app/build_identity.py:main)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. _parse_args"]
    s3["3. argparse.ArgumentParser"]
    s4["4. parser.add_argument"]
    s5["5. parser.add_argument"]
    s6["6. parser.add_argument"]
    s7["7. parser.parse_args"]
    s8["8. Path(…).resolve"]
    s9["9. Path"]
    s10["10. BuildIdentity.model_validate_json"]
    s11["11. args.frontend_identity.read_text"]
    s12["12. ValueError (backend/app/build_identity.py:main)"]
    s1 -->|"_parse_args(data not statically known)"| s2
    s2 -. "argparse.ArgumentParser(description='Write the immutable backend container build identity.')" .-> s3
    s2 -. "parser.add_argument('--source-revision', required=True)" .-> s4
    s2 -. "parser.add_argument('--frontend-identity', type=Path, required=True)" .-> s5
    s2 -. "parser.add_argument('--output', type=Path, required=True)" .-> s6
    s2 -. "parser.parse_args(data not statically known)" .-> s7
    s1 -. "Path(…).resolve(data not statically known)" .-> s8
    s1 -. "Path(__file__)" .-> s9
    s1 -. "BuildIdentity.model_validate_json(args.frontend_identity.read_text(...))" .-> s10
    s1 -. "args.frontend_identity.read_text(encoding='utf-8')" .-> s11
    s1 -. "ValueError (backend/app/build_identity.py:main)('Expected a frontend build identity')" .-> s12
    b0["filesystem_read args.frontend_identity.read_text"]
    s1 -. "filesystem_read args.frontend_identity.read_text" .-> b0
    b1["filesystem_write args.output.write_text"]
    s1 -. "filesystem_write args.output.write_text" .-> b1
    click s1 "../modules/build_identity.md"
    click s2 "../modules/build_identity.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | - | - | `0` |
| `_parse_args` | - | `Path`, `Path` | - | `parser.parse_args(...)` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `Path(…).resolve` | - | - | - | - |
| `Path` | - | - | - | - |
| `BuildIdentity.model_validate_json` | - | - | - | - |
| `args.frontend_identity.read_text` | - | - | - | - |
| `ValueError (backend/app/build_identity.py:main)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | _parse_args | 80 | `_parse_args(data not statically known)` |
| _parse_args | argparse.ArgumentParser | 70 | `argparse.ArgumentParser(description='Write the immutable backend container build identity.')` |
| _parse_args | parser.add_argument | 73 | `parser.add_argument('--source-revision', required=True)` |
| _parse_args | parser.add_argument | 74 | `parser.add_argument('--frontend-identity', type=Path, required=True)` |
| _parse_args | parser.add_argument | 75 | `parser.add_argument('--output', type=Path, required=True)` |
| _parse_args | parser.parse_args | 76 | `parser.parse_args(data not statically known)` |
| main | Path(…).resolve | 81 | `Path(__file__).resolve(data not statically known)` |
| main | Path | 81 | `Path(__file__)` |
| main | BuildIdentity.model_validate_json | 82 | `BuildIdentity.model_validate_json(args.frontend_identity.read_text(...))` |
| main | args.frontend_identity.read_text | 83 | `args.frontend_identity.read_text(encoding='utf-8')` |
| main | ValueError (backend/app/build_identity.py:main) | 86 | `ValueError('Expected a frontend build identity')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| filesystem_read | `args.frontend_identity.read_text` | `main` | 83 |
| filesystem_write | `args.output.write_text` | `main` | 95 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `_parse_args` | `argparse.ArgumentParser` | 70 |
| unresolved_call | `_parse_args` | `parser.add_argument` | 73 |
| unresolved_call | `_parse_args` | `parser.add_argument` | 74 |
| unresolved_call | `_parse_args` | `parser.add_argument` | 75 |
| unresolved_call | `_parse_args` | `parser.parse_args` | 76 |
| unresolved_call | `main` | `Path(__file__).resolve` | 81 |
| unresolved_call | `main` | `BuildIdentity.model_validate_json` | 82 |
| external_call | `main` | `ValueError` | 86 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
