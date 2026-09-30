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
    participant p12 as tempfile.TemporaryDirectory
    participant p13 as subprocess.check_output(…).strip
    participant p14 as subprocess.check_output
    participant p15 as source_digest
    participant p16 as datetime.now(…).isoformat
    participant p17 as datetime.now
    participant p18 as shutil.copytree
    participant p19 as shutil.ignore_patterns
    participant p20 as os.environ.get
    participant p21 as str
    participant p22 as (…).write_text (scripts/ci/run_android_checks.py:main)
    participant p23 as re.search
    participant p24 as RuntimeError
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
    p0-->>p12: tempfile.TemporaryDirectory
    p0-->>p5: Path
    p0-->>p13: subprocess.check_output(…).strip
    p0-->>p14: subprocess.check_output
    p0-->>p15: source_digest
    p0-->>p16: datetime.now(…).isoformat
    p0-->>p17: datetime.now
    p0-->>p18: shutil.copytree
    p0-->>p19: shutil.ignore_patterns
    p0-->>p20: os.environ.get
    p0-->>p5: Path
    p0-->>p5: Path
    p0-->>p14: subprocess.check_output
    p0-->>p21: str
    p0-->>p22: (…).write_text (scripts/ci/run_android_checks.py:main)
    p0-->>p23: re.search
    p0-->>p24: RuntimeError
    p0-->>p5: Path
    p0-->>p20: os.environ.get
```

> Call sequence diagram shows 30 of 79 interactions; 49 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

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
    b0["filesystem_write shutil.copytree"]
    s1 -. "filesystem_write shutil.copytree" .-> b0
    b1["environment_read os.environ.get"]
    s1 -. "environment_read os.environ.get" .-> b1
    b2["environment_read os.environ[...]"]
    s1 -. "environment_read os.environ[...]" .-> b2
    b3["process subprocess.check_output"]
    s1 -. "process subprocess.check_output" .-> b3
    b4["environment_read os.environ.get"]
    s1 -. "environment_read os.environ.get" .-> b4
    b5["filesystem_write shutil.copytree"]
    s1 -. "filesystem_write shutil.copytree" .-> b5
    b6["mutation suites.extend"]
    s1 -. "mutation suites.extend" .-> b6
    b7["output print"]
    s1 -. "output print" .-> b7
    click s1 "../modules/run_android_checks.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
    class b4 boundary
    class b5 boundary
    class b6 boundary
    class b7 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `Path`, `ROOT`, `os`, `subprocess` | `receipt[...]`, `receipt[...]`, `receipt[...]`, `receipt[...]`, `receipt[...]`, `receipt[...]`, `receipt[...]`, `receipt[...]` | `...` |
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
| main | argparse.ArgumentParser | 20 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.add_argument | 21 | `parser.add_argument('--output', type=Path)` |
| main | parser.parse_args | 22 | `parser.parse_args(data not statically known)` |
| main | args.output.resolve | 23 | `args.output.resolve(data not statically known)` |
| main | Path | 23 | `Path(tempfile.mkdtemp(...))` |
| main | tempfile.mkdtemp | 23 | `tempfile.mkdtemp(prefix='workchord-android-')` |
| main | output.exists | 24 | `output.exists(data not statically known)` |
| main | any | 24 | `any(output.iterdir(...))` |
| main | output.iterdir | 24 | `output.iterdir(data not statically known)` |
| main | parser.error | 25 | `parser.error('Output must be a new or empty directory')` |
| main | output.mkdir | 26 | `output.mkdir(parents=True, exist_ok=True)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| filesystem_write | `shutil.copytree` | `main` | 43 |
| environment_read | `os.environ.get` | `main` | 45 |
| environment_read | `os.environ[...]` | `main` | 45 |
| process | `subprocess.check_output` | `main` | 46 |
| environment_read | `os.environ.get` | `main` | 50 |
| filesystem_write | `shutil.copytree` | `main` | 64 |
| mutation | `suites.extend` | `main` | 77 |
| output | `print` | `main` | 99 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 20 |
| unresolved_call | `main` | `parser.add_argument` | 21 |
| unresolved_call | `main` | `parser.parse_args` | 22 |
| unresolved_call | `main` | `args.output.resolve` | 23 |
| external_call | `main` | `tempfile.mkdtemp` | 23 |
| unresolved_call | `main` | `output.exists` | 24 |
| external_call | `main` | `any` | 24 |
| unresolved_call | `main` | `output.iterdir` | 24 |
| unresolved_call | `main` | `parser.error` | 25 |
| unresolved_call | `main` | `output.mkdir` | 26 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

The command verifies the configured JDK/SDK and Gradle wrapper, copies source without local SDK configuration or build caches, and runs both build variants before collecting a debug APK. Each variant needs successful executed results. Logs, source hashes and artifact digests remain in the requested output directory after temporary project cleanup. Production signing and real-device behavior are outside this command.
