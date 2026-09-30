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
    participant p4 as Path
    participant p5 as tempfile.mkdtemp
    participant p6 as RunReceipt
    participant p7 as SystemExit
    participant p8 as str
    participant p9 as bind_source
    participant p10 as tempfile.TemporaryDirectory
    participant p11 as run.cleanups.append
    participant p12 as shutil.copytree
    participant p13 as shutil.ignore_patterns
    participant p14 as os.environ.copy
    participant p15 as env.get
    participant p16 as run.run
    participant p17 as (…).read_text
    participant p18 as re.search
    participant p19 as RuntimeError
    participant p20 as (…).is_file
    participant p21 as (…).is_dir
    p0-->>p1: argparse.ArgumentParser
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p3: parser.parse_args
    p0-->>p4: Path
    p0-->>p5: tempfile.mkdtemp
    p0-->>p6: RunReceipt
    p0-->>p7: SystemExit
    p0-->>p8: str
    p0-->>p9: bind_source
    p0-->>p10: tempfile.TemporaryDirectory
    p0-->>p11: run.cleanups.append
    p0-->>p4: Path
    p0-->>p12: shutil.copytree
    p0-->>p13: shutil.ignore_patterns
    p0-->>p14: os.environ.copy
    p0-->>p15: env.get
    p0-->>p4: Path
    p0-->>p4: Path
    p0-->>p16: run.run
    p0-->>p8: str
    p0-->>p17: (…).read_text
    p0-->>p18: re.search
    p0-->>p19: RuntimeError
    p0-->>p4: Path
    p0-->>p15: env.get
    p0-->>p15: env.get
    p0-->>p20: (…).is_file
    p0-->>p21: (…).is_dir
    p0-->>p19: RuntimeError
```

> Call sequence diagram shows 30 of 41 interactions; 11 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. main"]
    s2["2. argparse.ArgumentParser"]
    s3["3. parser.add_argument"]
    s4["4. parser.add_argument"]
    s5["5. parser.parse_args"]
    s6["6. Path"]
    s7["7. tempfile.mkdtemp"]
    s8["8. RunReceipt"]
    s9["9. SystemExit"]
    s10["10. str"]
    s11["11. bind_source"]
    s12["12. tempfile.TemporaryDirectory"]
    s1 -. "argparse.ArgumentParser(description=__doc__)" .-> s2
    s1 -. "parser.add_argument('--output', type=Path)" .-> s3
    s1 -. "parser.add_argument('--timeout-seconds', type=positive_seconds, default=1200)" .-> s4
    s1 -. "parser.parse_args(data not statically known)" .-> s5
    s1 -. "Path(tempfile.mkdtemp(...))" .-> s6
    s1 -. "tempfile.mkdtemp(prefix='workchord-android-')" .-> s7
    s1 -. "RunReceipt(output, checks=[...], timeout_seconds=args.timeout_seconds)" .-> s8
    s1 -. "SystemExit(str(...))" .-> s9
    s1 -. "str(exc)" .-> s10
    s1 -. "bind_source(run, source_digest)" .-> s11
    s1 -. "tempfile.TemporaryDirectory(prefix='workchord-android-runtime-')" .-> s12
    b0["mutation run.cleanups.append"]
    s1 -. "mutation run.cleanups.append" .-> b0
    b1["filesystem_write shutil.copytree"]
    s1 -. "filesystem_write shutil.copytree" .-> b1
    b2["mutation run.finalizers.append"]
    s1 -. "mutation run.finalizers.append" .-> b2
    b3["mutation run.validators.append"]
    s1 -. "mutation run.validators.append" .-> b3
    click s1 "../modules/run_android_checks.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `Path`, `positive_seconds`, `source_digest`, `ROOT` | `run.data[...]`, `run.data[...]` | `run.exit_code` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `Path` | - | - | - | - |
| `tempfile.mkdtemp` | - | - | - | - |
| `RunReceipt` | - | - | - | - |
| `SystemExit` | - | - | - | - |
| `str` | - | - | - | - |
| `bind_source` | - | - | - | - |
| `tempfile.TemporaryDirectory` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 18 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.add_argument | 19 | `parser.add_argument('--output', type=Path)` |
| main | parser.add_argument | 20 | `parser.add_argument('--timeout-seconds', type=positive_seconds, default=1200)` |
| main | parser.parse_args | 21 | `parser.parse_args(data not statically known)` |
| main | Path | 22 | `Path(tempfile.mkdtemp(...))` |
| main | tempfile.mkdtemp | 22 | `tempfile.mkdtemp(prefix='workchord-android-')` |
| main | RunReceipt | 24 | `RunReceipt(output, checks=[...], timeout_seconds=args.timeout_seconds)` |
| main | SystemExit | 26 | `SystemExit(str(...))` |
| main | str | 26 | `str(exc)` |
| main | bind_source | 28 | `bind_source(run, source_digest)` |
| main | tempfile.TemporaryDirectory | 30 | `tempfile.TemporaryDirectory(prefix='workchord-android-runtime-')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `run.cleanups.append` | `main` | 31 |
| filesystem_write | `shutil.copytree` | `main` | 33 |
| mutation | `run.finalizers.append` | `main` | 55 |
| mutation | `run.validators.append` | `main` | 78 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 18 |
| unresolved_call | `main` | `parser.add_argument` | 19 |
| unresolved_call | `main` | `parser.add_argument` | 20 |
| unresolved_call | `main` | `parser.parse_args` | 21 |
| external_call | `main` | `tempfile.mkdtemp` | 22 |
| external_call | `main` | `RunReceipt` | 24 |
| external_call | `main` | `SystemExit` | 26 |
| external_call | `main` | `bind_source` | 28 |
| external_call | `main` | `tempfile.TemporaryDirectory` | 30 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

The command verifies its native JDK/SDK and Gradle wrapper, copies source without local SDK configuration or build caches, and runs both build variants before validating the debug APK. The shared runner records progress, streams logs and limits execution time. Available outputs are collected before temporary-project cleanup, including on interruption. Both variants need successful executed results and the APK must be nonempty; failed or interrupted commands cannot be upgraded to success by partial artifacts. Production signing and real-device behavior remain outside this command.
