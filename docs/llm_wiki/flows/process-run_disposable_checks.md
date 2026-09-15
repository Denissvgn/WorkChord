# run_disposable_checks

**Entry point:** `main` (`process`)
**Source:** [run_disposable_checks](../modules/run_disposable_checks.md)
**Modules touched:** [run_disposable_checks](../modules/run_disposable_checks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as argparse.ArgumentParser
    participant p2 as parser.add_argument
    participant p3 as parser.parse_args
    participant p4 as args.output.resolve
    participant p5 as Path
    participant p6 as tempfile.mkdtemp
    participant p7 as output.exists
    participant p8 as any
    participant p9 as output.iterdir
    participant p10 as parser.error
    participant p11 as output.mkdir
    participant p12 as uuid4
    participant p13 as subprocess.check_output(…).strip
    participant p14 as subprocess.check_output (scripts/ci/run_disposable_checks.py:main)
    participant p15 as source_digest
    participant p16 as subprocess.check_output(…).split
    participant p17 as subprocess.check_output (scripts/ci/run_disposable_checks.py:source_digest)
    participant p18 as hashlib.sha256 (scripts/ci/run_disposable_checks.py:source_digest)
    participant p19 as sorted (scripts/ci/run_disposable_checks.py:source_digest)
    participant p20 as set
    participant p21 as raw.decode
    participant p22 as path.is_file (scripts/ci/run_disposable_checks.py:source_digest)
    participant p23 as name.startswith
    participant p24 as digest.update
    participant p25 as path.read_bytes (scripts/ci/run_disposable_checks.py:source_digest)
    participant p26 as digest.hexdigest
    participant p27 as datetime.now(…).isoformat
    p0-->>p1: argparse.ArgumentParser
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p3: parser.parse_args
    p0-->>p4: args.output.resolve
    p0-->>p5: Path
    p0-->>p6: tempfile.mkdtemp
    p0-->>p7: output.exists
    p0-->>p8: any
    p0-->>p9: output.iterdir
    p0-->>p10: parser.error
    p0-->>p11: output.mkdir
    p0-->>p12: uuid4
    p0-->>p13: subprocess.check_output(…).strip
    p0-->>p14: subprocess.check_output (scripts/ci/run_disposable_checks.py:main)
    p0->>p15: source_digest
    p15-->>p16: subprocess.check_output(…).split
    p15-->>p17: subprocess.check_output (scripts/ci/run_disposable_checks.py:source_digest)
    p15-->>p18: hashlib.sha256 (scripts/ci/run_disposable_checks.py:source_digest)
    p15-->>p19: sorted (scripts/ci/run_disposable_checks.py:source_digest)
    p15-->>p20: set
    p15-->>p21: raw.decode
    p15-->>p22: path.is_file (scripts/ci/run_disposable_checks.py:source_digest)
    p15-->>p23: name.startswith
    p15-->>p24: digest.update
    p15-->>p25: path.read_bytes (scripts/ci/run_disposable_checks.py:source_digest)
    p15-->>p26: digest.hexdigest
    p0-->>p27: datetime.now(…).isoformat
```

> Call sequence diagram shows 30 of 87 interactions; 57 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. main"]
    s2["2. argparse.ArgumentParser"]
    s3["3. parser.add_argument"]
    s4["4. parser.add_argument"]
    s5["5. parser.add_argument"]
    s6["6. parser.add_argument"]
    s7["7. parser.parse_args"]
    s8["8. args.output.resolve"]
    s9["9. Path"]
    s10["10. tempfile.mkdtemp"]
    s11["11. output.exists"]
    s12["12. any"]
    s1 -. "argparse.ArgumentParser(description=__doc__)" .-> s2
    s1 -. "parser.add_argument('--output', type=Path)" .-> s3
    s1 -. "parser.add_argument('--backend-only', action='store_true')" .-> s4
    s1 -. "parser.add_argument('--full-backend', action='store_true')" .-> s5
    s1 -. "parser.add_argument('--managed-browser', action='store_true')" .-> s6
    s1 -. "parser.parse_args(data not statically known)" .-> s7
    s1 -. "args.output.resolve(data not statically known)" .-> s8
    s1 -. "Path(tempfile.mkdtemp(...))" .-> s9
    s1 -. "tempfile.mkdtemp(prefix='workchord-checks-')" .-> s10
    s1 -. "output.exists(data not statically known)" .-> s11
    s1 -. "any(output.iterdir(...))" .-> s12
    b0["process subprocess.run"]
    s1 -. "process subprocess.run" .-> b0
    b1["mutation failures.append"]
    s1 -. "mutation failures.append" .-> b1
    b2["mutation failures.append"]
    s1 -. "mutation failures.append" .-> b2
    b3["mutation failures.append"]
    s1 -. "mutation failures.append" .-> b3
    b4["output print"]
    s1 -. "output print" .-> b4
    click s1 "../modules/run_disposable_checks.md"
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
| `main` | - | `Path`, `NODE_IMAGE`, `POSTGRES_IMAGE`, `BROWSER_IMAGE`, `POSTGRES_IMAGE`, `subprocess`, `ROOT`, `ROOT` | `receipt[...]`, `receipt[...]`, `receipt[...]`, `receipt[...]`, `receipt[...]`, `receipt[...]`, `receipt[...]`, `receipt[...]` | `...` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `args.output.resolve` | - | - | - | - |
| `Path` | - | - | - | - |
| `tempfile.mkdtemp` | - | - | - | - |
| `output.exists` | - | - | - | - |
| `any` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 37 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.add_argument | 38 | `parser.add_argument('--output', type=Path)` |
| main | parser.add_argument | 39 | `parser.add_argument('--backend-only', action='store_true')` |
| main | parser.add_argument | 40 | `parser.add_argument('--full-backend', action='store_true')` |
| main | parser.add_argument | 41 | `parser.add_argument('--managed-browser', action='store_true')` |
| main | parser.parse_args | 42 | `parser.parse_args(data not statically known)` |
| main | args.output.resolve | 43 | `args.output.resolve(data not statically known)` |
| main | Path | 43 | `Path(tempfile.mkdtemp(...))` |
| main | tempfile.mkdtemp | 43 | `tempfile.mkdtemp(prefix='workchord-checks-')` |
| main | output.exists | 44 | `output.exists(data not statically known)` |
| main | any | 44 | `any(output.iterdir(...))` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| process | `subprocess.run` | `main` | 84 |
| mutation | `failures.append` | `main` | 107 |
| mutation | `failures.append` | `main` | 127 |
| mutation | `failures.append` | `main` | 135 |
| output | `print` | `main` | 175 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 37 |
| unresolved_call | `main` | `parser.add_argument` | 38 |
| unresolved_call | `main` | `parser.add_argument` | 39 |
| unresolved_call | `main` | `parser.add_argument` | 40 |
| unresolved_call | `main` | `parser.add_argument` | 41 |
| unresolved_call | `main` | `parser.parse_args` | 42 |
| unresolved_call | `main` | `args.output.resolve` | 43 |
| external_call | `main` | `tempfile.mkdtemp` | 43 |
| unresolved_call | `main` | `output.exists` | 44 |
| external_call | `main` | `any` | 44 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

The command builds locked dependencies, creates only its UUID-scoped Docker resources, and runs the application with isolated database and filesystem state. Rendered browser interactions and independent HTTP readback supply functional evidence. Its receipt distinguishes expected failures from executed passes. A source change during execution or a failed resource cleanup makes the result unsuccessful. Static call diagrams omit parts of the subprocess orchestration; they do not independently verify isolation.
