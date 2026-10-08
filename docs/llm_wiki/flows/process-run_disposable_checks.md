# run_disposable_checks

**Entry point:** `main` (`process`)
**Source:** [run_disposable_checks](../modules/run_disposable_checks.md)
**Modules touched:** [run_disposable_checks](../modules/run_disposable_checks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as parse_args
    participant p2 as argparse.ArgumentParser
    participant p3 as parser.add_argument
    participant p4 as parser.add_mutually_exclusive_group
    participant p5 as mode.add_argument
    participant p6 as parser.parse_args
    participant p7 as parser.error
    participant p8 as set(…).intersection (scripts/ci/run_disposable_checks.py:parse_args)
    participant p9 as set (scripts/ci/run_disposable_checks.py:parse_args)
    participant p10 as Path
    participant p11 as tempfile.mkdtemp
    participant p12 as RunReceipt
    participant p13 as SystemExit
    participant p14 as str
    participant p15 as bind_source
    participant p16 as run.check_budget
    participant p17 as subprocess.check_output(…).strip
    participant p18 as subprocess.check_output
    participant p19 as digest
    participant p20 as run.checkpoint
    participant p21 as run.validators.append (scripts/ci/run_disposable_checks.py:bind_source)
    participant p22 as tempfile.TemporaryDirectory
    participant p23 as run.cleanups.append
    p0->>p1: parse_args
    p1-->>p2: argparse.ArgumentParser
    p1-->>p3: parser.add_argument
    p1-->>p4: parser.add_mutually_exclusive_group
    p1-->>p5: mode.add_argument
    p1-->>p5: mode.add_argument
    p1-->>p5: mode.add_argument
    p1-->>p3: parser.add_argument
    p1-->>p3: parser.add_argument
    p1-->>p3: parser.add_argument
    p1-->>p3: parser.add_argument
    p1-->>p6: parser.parse_args
    p1-->>p7: parser.error
    p1-->>p8: set(…).intersection (scripts/ci/run_disposable_checks.py:parse_args)
    p1-->>p9: set (scripts/ci/run_disposable_checks.py:parse_args)
    p1-->>p7: parser.error
    p0-->>p10: Path
    p0-->>p11: tempfile.mkdtemp
    p0-->>p12: RunReceipt
    p0-->>p13: SystemExit
    p0-->>p14: str
    p0->>p15: bind_source
    p15-->>p16: run.check_budget
    p15-->>p17: subprocess.check_output(…).strip
    p15-->>p18: subprocess.check_output
    p15-->>p19: digest
    p15-->>p20: run.checkpoint
    p15-->>p21: run.validators.append (scripts/ci/run_disposable_checks.py:bind_source)
    p0-->>p22: tempfile.TemporaryDirectory
    p0-->>p23: run.cleanups.append
```

> Call sequence diagram shows 30 of 95 interactions; 65 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. main"]
    s2["2. parse_args"]
    s3["3. argparse.ArgumentParser"]
    s4["4. parser.add_argument"]
    s5["5. parser.add_mutually_exclusive_group"]
    s6["6. mode.add_argument"]
    s7["7. mode.add_argument"]
    s8["8. mode.add_argument"]
    s9["9. parser.add_argument"]
    s10["10. parser.add_argument"]
    s11["11. parser.add_argument"]
    s12["12. parser.add_argument"]
    s1 -->|"parse_args(data not statically known)"| s2
    s2 -. "argparse.ArgumentParser(description=__doc__)" .-> s3
    s2 -. "parser.add_argument('--output', type=Path)" .-> s4
    s2 -. "parser.add_mutually_exclusive_group(data not statically known)" .-> s5
    s2 -. "mode.add_argument('--scope', choices=[...])" .-> s6
    s2 -. "mode.add_argument('--browser-only', action='store_true')" .-> s7
    s2 -. "mode.add_argument('--backend-only', action='store_true')" .-> s8
    s2 -. "parser.add_argument('--full-backend', action='store_true')" .-> s9
    s2 -. "parser.add_argument('--managed-browser', action='store_true')" .-> s10
    s2 -. "parser.add_argument('--time-entries', action='store_true')" .-> s11
    s2 -. "parser.add_argument('--timeout-seconds', type=positive_seconds, default=1800, help='Work budget; leave time outside this for cleanup and uploads')" .-> s12
    b0["mutation run.cleanups.append"]
    s1 -. "mutation run.cleanups.append" .-> b0
    b1["mutation run.validators.append"]
    s1 -. "mutation run.validators.append" .-> b1
    b2["mutation run.validators.append"]
    s1 -. "mutation run.validators.append" .-> b2
    b3["filesystem_write shutil.copytree"]
    s1 -. "filesystem_write shutil.copytree" .-> b3
    b4["filesystem_write shutil.copyfile"]
    s1 -. "filesystem_write shutil.copyfile" .-> b4
    b5["filesystem_write shutil.copyfile"]
    s1 -. "filesystem_write shutil.copyfile" .-> b5
    b6["mutation app_env.update"]
    s1 -. "mutation app_env.update" .-> b6
    click s1 "../modules/run_disposable_checks.md"
    click s2 "../modules/run_disposable_checks.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
    class b4 boundary
    class b5 boundary
    class b6 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `source_digest`, `PLAYWRIGHT_VERSION`, `ROOT`, `sys`, `sys`, `ROOT`, `ROOT`, `sys` | `run.data[...]`, `run.data[...]`, `env[...]`, `app_env[...]` | `run.exit_code` |
| `parse_args` | - | `Path`, `positive_seconds` | - | `(...)` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_mutually_exclusive_group` | - | - | - | - |
| `mode.add_argument` | - | - | - | - |
| `mode.add_argument` | - | - | - | - |
| `mode.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | parse_args | 140 | `parse_args(data not statically known)` |
| parse_args | argparse.ArgumentParser | 114 | `argparse.ArgumentParser(description=__doc__)` |
| parse_args | parser.add_argument | 115 | `parser.add_argument('--output', type=Path)` |
| parse_args | parser.add_mutually_exclusive_group | 116 | `parser.add_mutually_exclusive_group(data not statically known)` |
| parse_args | mode.add_argument | 117 | `mode.add_argument('--scope', choices=[...])` |
| parse_args | mode.add_argument | 118 | `mode.add_argument('--browser-only', action='store_true')` |
| parse_args | mode.add_argument | 119 | `mode.add_argument('--backend-only', action='store_true')` |
| parse_args | parser.add_argument | 120 | `parser.add_argument('--full-backend', action='store_true')` |
| parse_args | parser.add_argument | 121 | `parser.add_argument('--managed-browser', action='store_true')` |
| parse_args | parser.add_argument | 122 | `parser.add_argument('--time-entries', action='store_true')` |
| parse_args | parser.add_argument | 123 | `parser.add_argument('--timeout-seconds', type=positive_seconds, default=1800, help='Work budget; leave time outside this for cleanup and uploads')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `run.cleanups.append` | `main` | 151 |
| mutation | `run.validators.append` | `main` | 152 |
| mutation | `run.validators.append` | `main` | 179 |
| filesystem_write | `shutil.copytree` | `main` | 182 |
| filesystem_write | `shutil.copyfile` | `main` | 198 |
| filesystem_write | `shutil.copyfile` | `main` | 200 |
| mutation | `app_env.update` | `main` | 207 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `parse_args` | `argparse.ArgumentParser` | 114 |
| unresolved_call | `parse_args` | `parser.add_argument` | 115 |
| unresolved_call | `parse_args` | `parser.add_mutually_exclusive_group` | 116 |
| unresolved_call | `parse_args` | `mode.add_argument` | 117 |
| unresolved_call | `parse_args` | `mode.add_argument` | 118 |
| unresolved_call | `parse_args` | `mode.add_argument` | 119 |
| unresolved_call | `parse_args` | `parser.add_argument` | 120 |
| unresolved_call | `parse_args` | `parser.add_argument` | 121 |
| unresolved_call | `parse_args` | `parser.add_argument` | 122 |
| unresolved_call | `parse_args` | `parser.add_argument` | 123 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

The runner supplies its exact Python executable to the managed browser and copies the inbox dispatch helper beside the scenario. Node launches the worker through that absolute executable, retaining the backend dependency environment even when a different Python is on `PATH`. The helper requires the owned disposable database and invocation nonce before starting delivery.

The selected scope determines prerequisites, commands and required artifacts. SQLite runs without a PostgreSQL admin endpoint; PostgreSQL uses a validated loopback cluster; frontend owns its JUnit, lint and build outcomes; browser-only mode provisions the isolated application and Playwright scenario without repeating those suites. Existing combined command-line modes remain available.

The runner writes an initial receipt before commands, streams command logs with periodic heartbeats, records stage durations, and enforces command/run deadlines. Workflow setup time reduces the remaining budget so cleanup and uploads have reserved headroom. Missing evidence, nonzero commands, source changes and unsuccessful cleanup fail the run. Graceful cancellation is recorded; a hard-killed run remains incomplete. The browser invocation nonce and active-port ownership checks remain enforced.
