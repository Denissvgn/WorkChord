# build_identity

**Entry point:** `main` (`process`)
**Source:** [build_identity](../modules/build_identity.md)
**Modules touched:** [build_identity](../modules/build_identity.md)

**Related modules:** [autonomy_canonical](../modules/autonomy_canonical.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as _parse_args
    participant p2 as argparse.ArgumentParser
    participant p3 as parser.add_argument
    participant p4 as parser.parse_args
    participant p5 as Path(…).resolve
    participant p6 as Path
    participant p7 as BuildIdentity.model_validate_json
    participant p8 as args.frontend_identity.read_text
    participant p9 as ValueError (backend/app/build_identity.py:main)
    participant p10 as BackendBuildIdentity
    participant p11 as package_artifact_digest
    participant p12 as sha256
    participant p13 as sorted
    participant p14 as package_root.rglob
    participant p15 as path.is_file
    participant p16 as ValueError (backend/app/build_identit…py:package_artifact_digest)
    participant p17 as member.relative_to(…).as_posix().encode
    participant p18 as member.relative_to(…).as_posix
    participant p19 as member.relative_to
    participant p20 as digest.update
    participant p21 as sha256(…).digest
    participant p22 as member.read_bytes
    participant p23 as digest.hexdigest
    p0->>p1: _parse_args
    p1-->>p2: argparse.ArgumentParser
    p1-->>p3: parser.add_argument
    p1-->>p3: parser.add_argument
    p1-->>p3: parser.add_argument
    p1-->>p4: parser.parse_args
    p0-->>p5: Path(…).resolve
    p0-->>p6: Path
    p0-->>p7: BuildIdentity.model_validate_json
    p0-->>p8: args.frontend_identity.read_text
    p0-->>p9: ValueError (backend/app/build_identity.py:main)
    p0-->>p9: ValueError (backend/app/build_identity.py:main)
    p0->>p10: BackendBuildIdentity
    p0->>p11: package_artifact_digest
    p11-->>p12: sha256
    p11-->>p13: sorted
    p11-->>p14: package_root.rglob
    p11-->>p15: path.is_file
    p11-->>p16: ValueError (backend/app/build_identit…py:package_artifact_digest)
    p11-->>p17: member.relative_to(…).as_posix().encode
    p11-->>p18: member.relative_to(…).as_posix
    p11-->>p19: member.relative_to
    p11-->>p20: digest.update
    p11-->>p20: digest.update
    p11-->>p20: digest.update
    p11-->>p21: sha256(…).digest
    p11-->>p12: sha256
    p11-->>p22: member.read_bytes
    p11-->>p20: digest.update
    p11-->>p23: digest.hexdigest
```

> Call sequence diagram shows 30 of 35 interactions; 5 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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
