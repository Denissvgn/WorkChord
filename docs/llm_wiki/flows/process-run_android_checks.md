# run_android_checks

**Entry point:** `main` (`process`)
**Source:** [run_android_checks](../modules/run_android_checks.md)
**Modules touched:** [run_android_checks](../modules/run_android_checks.md)

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
    participant p14 as subprocess.check_output
    participant p15 as source_digest
    participant p16 as datetime.now(…).isoformat
    participant p17 as datetime.now
    participant p18 as run
    participant p19 as RuntimeError
    participant p20 as str
    participant p21 as ET.parse(…).getroot
    participant p22 as ET.parse
    participant p23 as (…).glob (scripts/ci/run_android_checks.py:main, 1)
    participant p24 as sum
    participant p25 as int
    p0-->>p1: argparse.ArgumentParser
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
    p0-->>p12: uuid4
    p0-->>p13: subprocess.check_output(…).strip
    p0-->>p14: subprocess.check_output
    p0-->>p15: source_digest
    p0-->>p16: datetime.now(…).isoformat
    p0-->>p17: datetime.now
    p0-->>p18: run
    p0-->>p19: RuntimeError
    p0-->>p18: run
    p0-->>p19: RuntimeError
    p0-->>p18: run
    p0-->>p18: run
    p0-->>p20: str
    p0-->>p21: ET.parse(…).getroot
    p0-->>p22: ET.parse
    p0-->>p23: (…).glob (scripts/ci/run_android_checks.py:main, 1)
    p0-->>p24: sum
    p0-->>p25: int
```

> Call sequence diagram shows 30 of 52 interactions; 22 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. main"]
    s2["2. argparse.ArgumentParser"]
    s3["3. parser.add_argument"]
    s4["4. parser.parse_args"]
    s5["5. args.output.resolve"]
    s6["6. Path"]
    s7["7. tempfile.mkdtemp"]
    s8["8. output.exists"]
    s9["9. any"]
    s10["10. output.iterdir"]
    s11["11. parser.error"]
    s12["12. output.mkdir"]
    s1 -. "argparse.ArgumentParser(description=__doc__)" .-> s2
    s1 -. "parser.add_argument('--output', type=Path)" .-> s3
    s1 -. "parser.parse_args(data not statically known)" .-> s4
    s1 -. "args.output.resolve(data not statically known)" .-> s5
    s1 -. "Path(tempfile.mkdtemp(...))" .-> s6
    s1 -. "tempfile.mkdtemp(prefix='workchord-android-')" .-> s7
    s1 -. "output.exists(data not statically known)" .-> s8
    s1 -. "any(output.iterdir(...))" .-> s9
    s1 -. "output.iterdir(data not statically known)" .-> s10
    s1 -. "parser.error('Output must be a new or empty directory')" .-> s11
    s1 -. "output.mkdir(parents=True, exist_ok=True)" .-> s12
    b0["output print"]
    s1 -. "output print" .-> b0
    click s1 "../modules/run_android_checks.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `Path` | `receipt[...]`, `receipt[...]`, `receipt[...]`, `receipt[...]`, `receipt[...]`, `receipt[...]`, `receipt[...]`, `receipt[...]` | `...` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `args.output.resolve` | - | - | - | - |
| `Path` | - | - | - | - |
| `tempfile.mkdtemp` | - | - | - | - |
| `output.exists` | - | - | - | - |
| `any` | - | - | - | - |
| `output.iterdir` | - | - | - | - |
| `parser.error` | - | - | - | - |
| `output.mkdir` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 18 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.add_argument | 19 | `parser.add_argument('--output', type=Path)` |
| main | parser.parse_args | 20 | `parser.parse_args(data not statically known)` |
| main | args.output.resolve | 21 | `args.output.resolve(data not statically known)` |
| main | Path | 21 | `Path(tempfile.mkdtemp(...))` |
| main | tempfile.mkdtemp | 21 | `tempfile.mkdtemp(prefix='workchord-android-')` |
| main | output.exists | 22 | `output.exists(data not statically known)` |
| main | any | 22 | `any(output.iterdir(...))` |
| main | output.iterdir | 22 | `output.iterdir(data not statically known)` |
| main | parser.error | 23 | `parser.error('Output must be a new or empty directory')` |
| main | output.mkdir | 24 | `output.mkdir(parents=True, exist_ok=True)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 78 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 18 |
| unresolved_call | `main` | `parser.add_argument` | 19 |
| unresolved_call | `main` | `parser.parse_args` | 20 |
| unresolved_call | `main` | `args.output.resolve` | 21 |
| external_call | `main` | `tempfile.mkdtemp` | 21 |
| unresolved_call | `main` | `output.exists` | 22 |
| external_call | `main` | `any` | 22 |
| unresolved_call | `main` | `output.iterdir` | 22 |
| unresolved_call | `main` | `parser.error` | 23 |
| unresolved_call | `main` | `output.mkdir` | 24 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

The command creates a unique image tag and container, runs the Gradle wrapper, and copies execution reports and the debug APK to a new output directory. Nonempty executed results and an APK are required before reporting success. Source stability and cleanup are checked. SDK configuration and debug signing material stay inside the disposable image/container; production signing is outside this workflow.
