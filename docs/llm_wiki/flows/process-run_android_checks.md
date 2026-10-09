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
    participant p4 as bool
    participant p5 as parser.error
    participant p6 as Path
    participant p7 as tempfile.mkdtemp
    participant p8 as RunReceipt
    participant p9 as SystemExit
    participant p10 as str
    participant p11 as bind_source
    participant p12 as tempfile.TemporaryDirectory
    participant p13 as run.cleanups.append
    participant p14 as shutil.copytree
    participant p15 as shutil.ignore_patterns
    participant p16 as os.environ.copy
    participant p17 as env.get
    participant p18 as run.run
    participant p19 as (…).read_text (scripts/ci/run_android_checks.py:main)
    participant p20 as re.search
    participant p21 as RuntimeError
    p0-->>p1: argparse.ArgumentParser
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p3: parser.parse_args
    p0-->>p4: bool
    p0-->>p5: parser.error
    p0-->>p6: Path
    p0-->>p7: tempfile.mkdtemp
    p0-->>p8: RunReceipt
    p0-->>p9: SystemExit
    p0-->>p10: str
    p0-->>p11: bind_source
    p0-->>p12: tempfile.TemporaryDirectory
    p0-->>p13: run.cleanups.append
    p0-->>p6: Path
    p0-->>p14: shutil.copytree
    p0-->>p15: shutil.ignore_patterns
    p0-->>p16: os.environ.copy
    p0-->>p10: str
    p0-->>p6: Path
    p0-->>p17: env.get
    p0-->>p6: Path
    p0-->>p6: Path
    p0-->>p18: run.run
    p0-->>p10: str
    p0-->>p19: (…).read_text (scripts/ci/run_android_checks.py:main)
    p0-->>p20: re.search
    p0-->>p21: RuntimeError
```

> Call sequence diagram shows 30 of 65 interactions; 35 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

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
    s8["8. bool"]
    s9["9. parser.error"]
    s10["10. Path"]
    s11["11. tempfile.mkdtemp"]
    s12["12. RunReceipt"]
    s1 -. "argparse.ArgumentParser(description=__doc__)" .-> s2
    s1 -. "parser.add_argument('--output', type=Path)" .-> s3
    s1 -. "parser.add_argument('--timeout-seconds', type=positive_seconds, default=1200)" .-> s4
    s1 -. "parser.add_argument('--release-qualification', action='store_true')" .-> s5
    s1 -. "parser.add_argument('--qualification-inputs', type=Path)" .-> s6
    s1 -. "parser.parse_args(data not statically known)" .-> s7
    s1 -. "bool(args.qualification_inputs)" .-> s8
    s1 -. "parser.error('--release-qualification and --qualification-inputs must be selected together')" .-> s9
    s1 -. "Path(tempfile.mkdtemp(...))" .-> s10
    s1 -. "tempfile.mkdtemp(prefix='workchord-android-')" .-> s11
    s1 -. "RunReceipt(output, checks=[...], timeout_seconds=args.timeout_seconds)" .-> s12
    b0["mutation run.cleanups.append"]
    s1 -. "mutation run.cleanups.append" .-> b0
    b1["filesystem_write shutil.copytree"]
    s1 -. "filesystem_write shutil.copytree" .-> b1
    b2["filesystem_write shutil.copyfile"]
    s1 -. "filesystem_write shutil.copyfile" .-> b2
    b3["mutation run.finalizers.append"]
    s1 -. "mutation run.finalizers.append" .-> b3
    b4["mutation run.validators.append"]
    s1 -. "mutation run.validators.append" .-> b4
    click s1 "../modules/run_android_checks.md"
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
| `main` | - | `Path`, `positive_seconds`, `Path`, `source_digest`, `ROOT`, `ROOT` | `run.data[...]`, `env[...]`, `env[...]`, `env[...]`, `env[...]`, `run.data[...]` | `run.exit_code` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `bool` | - | - | - | - |
| `parser.error` | - | - | - | - |
| `Path` | - | - | - | - |
| `tempfile.mkdtemp` | - | - | - | - |
| `RunReceipt` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 19 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.add_argument | 20 | `parser.add_argument('--output', type=Path)` |
| main | parser.add_argument | 21 | `parser.add_argument('--timeout-seconds', type=positive_seconds, default=1200)` |
| main | parser.add_argument | 22 | `parser.add_argument('--release-qualification', action='store_true')` |
| main | parser.add_argument | 23 | `parser.add_argument('--qualification-inputs', type=Path)` |
| main | parser.parse_args | 24 | `parser.parse_args(data not statically known)` |
| main | bool | 25 | `bool(args.qualification_inputs)` |
| main | parser.error | 26 | `parser.error('--release-qualification and --qualification-inputs must be selected together')` |
| main | Path | 27 | `Path(tempfile.mkdtemp(...))` |
| main | tempfile.mkdtemp | 27 | `tempfile.mkdtemp(prefix='workchord-android-')` |
| main | RunReceipt | 29 | `RunReceipt(output, checks=[...], timeout_seconds=args.timeout_seconds)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `run.cleanups.append` | `main` | 36 |
| filesystem_write | `shutil.copytree` | `main` | 38 |
| filesystem_write | `shutil.copyfile` | `main` | 65 |
| mutation | `run.finalizers.append` | `main` | 82 |
| mutation | `run.validators.append` | `main` | 105 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 19 |
| unresolved_call | `main` | `parser.add_argument` | 20 |
| unresolved_call | `main` | `parser.add_argument` | 21 |
| unresolved_call | `main` | `parser.add_argument` | 22 |
| unresolved_call | `main` | `parser.add_argument` | 23 |
| unresolved_call | `main` | `parser.parse_args` | 24 |
| unresolved_call | `main` | `parser.error` | 26 |
| external_call | `main` | `tempfile.mkdtemp` | 27 |
| external_call | `main` | `RunReceipt` | 29 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

The command verifies its native JDK/SDK and Gradle wrapper, copies source without local SDK configuration or build caches, and runs both build variants before validating the debug APK. The shared runner records progress, streams logs and limits execution time. Available outputs are collected before temporary-project cleanup, including on interruption. Both variants need successful executed results and the APK must be nonempty; failed or interrupted commands cannot be upgraded to success by partial artifacts. Production signing and real-device behavior remain outside this command.
