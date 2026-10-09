# export_acceptance_artifacts

**Entry point:** `main` (`process`)
**Source:** [export_acceptance_artifacts](../modules/export_acceptance_artifacts.md)
**Modules touched:** [export_acceptance_artifacts](../modules/export_acceptance_artifacts.md)

**Related modules:** [acceptance_artifacts](../modules/acceptance_artifacts.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as argparse.ArgumentParser
    participant p2 as parser.add_argument
    participant p3 as parser.parse_args
    participant p4 as args.output.mkdir
    participant p5 as (…).encode
    participant p6 as json.dumps
    participant p7 as (…).write_bytes
    participant p8 as len
    participant p9 as sha256(…).hexdigest
    participant p10 as sha256
    participant p11 as (…).write_text
    participant p12 as export_artifacts
    participant p13 as print
    p0-->>p1: argparse.ArgumentParser
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p3: parser.parse_args
    p0-->>p4: args.output.mkdir
    p0-->>p5: (…).encode
    p0-->>p6: json.dumps
    p0-->>p7: (…).write_bytes
    p0-->>p8: len
    p0-->>p9: sha256(…).hexdigest
    p0-->>p10: sha256
    p0-->>p11: (…).write_text
    p0-->>p6: json.dumps
    p0-->>p12: export_artifacts
    p0-->>p13: print
    p0-->>p6: json.dumps
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. main"]
    s2["2. argparse.ArgumentParser"]
    s3["3. parser.add_argument"]
    s4["4. parser.add_argument"]
    s5["5. parser.add_argument"]
    s6["6. parser.parse_args"]
    s7["7. args.output.mkdir"]
    s8["8. (…).encode"]
    s9["9. json.dumps"]
    s10["10. (…).write_bytes"]
    s11["11. len"]
    s12["12. sha256(…).hexdigest"]
    s1 -. "argparse.ArgumentParser(description=__doc__)" .-> s2
    s1 -. "parser.add_argument('--reports', type=Path, required=True)" .-> s3
    s1 -. "parser.add_argument('--output', type=Path, required=True)" .-> s4
    s1 -. "parser.add_argument('--outcome', choices=[...], default='failure')" .-> s5
    s1 -. "parser.parse_args(data not statically known)" .-> s6
    s1 -. "args.output.mkdir(parents=True, exist_ok=False)" .-> s7
    s1 -. "(…).encode(data not statically known)" .-> s8
    s1 -. "json.dumps({...}, sort_keys=True, indent=2)" .-> s9
    s1 -. "(…).write_bytes(payload)" .-> s10
    s1 -. "len(payload)" .-> s11
    s1 -. "sha256(…).hexdigest(data not statically known)" .-> s12
    b0["output print"]
    s1 -. "output print" .-> b0
    click s1 "../modules/export_acceptance_artifacts.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `Path`, `Path` | - | `2`, `...` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `args.output.mkdir` | - | - | - | - |
| `(…).encode` | - | - | - | - |
| `json.dumps` | - | - | - | - |
| `(…).write_bytes` | - | - | - | - |
| `len` | - | - | - | - |
| `sha256(…).hexdigest` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 15 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.add_argument | 16 | `parser.add_argument('--reports', type=Path, required=True)` |
| main | parser.add_argument | 17 | `parser.add_argument('--output', type=Path, required=True)` |
| main | parser.add_argument | 18 | `parser.add_argument('--outcome', choices=[...], default='failure')` |
| main | parser.parse_args | 19 | `parser.parse_args(data not statically known)` |
| main | args.output.mkdir | 24 | `args.output.mkdir(parents=True, exist_ok=False)` |
| main | (…).encode | 25 | `(json.dumps({'schema_version': 1, 'run_outcome': 'failure', 'complete': False, 'status': 'export-validator-unavailable', 'accepted_as_production_evidence': False}, sort_keys=True, indent=2) + '\n').encode(data not statically known)` |
| main | json.dumps | 25 | `json.dumps({...}, sort_keys=True, indent=2)` |
| main | (…).write_bytes | 28 | `(args.output / 'failure-summary.json').write_bytes(payload)` |
| main | len | 30 | `len(payload)` |
| main | sha256(…).hexdigest | 30 | `sha256(payload).hexdigest(data not statically known)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 34 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 15 |
| unresolved_call | `main` | `parser.add_argument` | 16 |
| unresolved_call | `main` | `parser.add_argument` | 17 |
| unresolved_call | `main` | `parser.add_argument` | 18 |
| unresolved_call | `main` | `parser.parse_args` | 19 |
| unresolved_call | `main` | `args.output.mkdir` | 24 |
| unresolved_call | `main` | `(json.dumps({'schema_version': 1, 'run_outcome': 'failure', 'complete': False, 'status': 'export-validator-unavailable', 'accepted_as_production_evidence': False}, sort_keys=True, indent=2) + '\n').encode` | 25 |
| external_call | `main` | `json.dumps` | 25 |
| unresolved_call | `main` | `(args.output / 'failure-summary.json').write_bytes` | 28 |
| unresolved_call | `main` | `sha256(payload).hexdigest` | 30 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
