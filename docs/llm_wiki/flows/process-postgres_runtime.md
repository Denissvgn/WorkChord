# postgres_runtime

**Entry point:** `main` (`process`)
**Source:** [postgres_runtime](../modules/postgres_runtime.md)
**Modules touched:** [postgres_runtime](../modules/postgres_runtime.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as argparse.ArgumentParser
    participant p2 as parser.add_argument
    participant p3 as parser.parse_args
    participant p4 as args.data_dir.resolve
    participant p5 as args.bin_dir.resolve
    participant p6 as parser.error
    participant p7 as (…).is_file
    participant p8 as data.exists
    participant p9 as (…).exists
    participant p10 as subprocess.run
    participant p11 as str
    participant p12 as subprocess.check_output
    participant p13 as re.search
    participant p14 as os.environ.get
    participant p15 as data.parent.mkdir
    participant p16 as tempfile.NamedTemporaryFile
    participant p17 as secret.write
    participant p18 as secret.flush
    p0-->>p1: argparse.ArgumentParser
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p3: parser.parse_args
    p0-->>p4: args.data_dir.resolve
    p0-->>p5: args.bin_dir.resolve
    p0-->>p6: parser.error
    p0-->>p7: (…).is_file
    p0-->>p8: data.exists
    p0-->>p6: parser.error
    p0-->>p9: (…).exists
    p0-->>p10: subprocess.run
    p0-->>p11: str
    p0-->>p11: str
    p0-->>p8: data.exists
    p0-->>p6: parser.error
    p0-->>p12: subprocess.check_output
    p0-->>p11: str
    p0-->>p13: re.search
    p0-->>p6: parser.error
    p0-->>p14: os.environ.get
    p0-->>p6: parser.error
    p0-->>p15: data.parent.mkdir
    p0-->>p16: tempfile.NamedTemporaryFile
    p0-->>p17: secret.write
    p0-->>p18: secret.flush
    p0-->>p10: subprocess.run
    p0-->>p11: str
```

> Call sequence diagram shows 30 of 38 interactions; 8 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

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
    s8["8. args.data_dir.resolve"]
    s9["9. args.bin_dir.resolve"]
    s10["10. parser.error"]
    s11["11. (…).is_file"]
    s12["12. data.exists"]
    s1 -. "argparse.ArgumentParser(description=__doc__)" .-> s2
    s1 -. "parser.add_argument('action', choices=[...])" .-> s3
    s1 -. "parser.add_argument('--data-dir', type=Path, required=True)" .-> s4
    s1 -. "parser.add_argument('--bin-dir', type=Path, required=True)" .-> s5
    s1 -. "parser.add_argument('--port', type=int, default=55432)" .-> s6
    s1 -. "parser.parse_args(data not statically known)" .-> s7
    s1 -. "args.data_dir.resolve(data not statically known)" .-> s8
    s1 -. "args.bin_dir.resolve(data not statically known)" .-> s9
    s1 -. "parser.error('Use an unprivileged local port')" .-> s10
    s1 -. "(…).is_file(data not statically known)" .-> s11
    s1 -. "data.exists(data not statically known)" .-> s12
    b0["process subprocess.run"]
    s1 -. "process subprocess.run" .-> b0
    b1["process subprocess.check_output"]
    s1 -. "process subprocess.check_output" .-> b1
    b2["environment_read os.environ.get"]
    s1 -. "environment_read os.environ.get" .-> b2
    b3["process subprocess.run"]
    s1 -. "process subprocess.run" .-> b3
    b4["process subprocess.run"]
    s1 -. "process subprocess.run" .-> b4
    click s1 "../modules/postgres_runtime.md"
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
| `main` | - | `Path`, `Path` | - | `0`, `0`, `0` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `args.data_dir.resolve` | - | - | - | - |
| `args.bin_dir.resolve` | - | - | - | - |
| `parser.error` | - | - | - | - |
| `(…).is_file` | - | - | - | - |
| `data.exists` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 17 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.add_argument | 18 | `parser.add_argument('action', choices=[...])` |
| main | parser.add_argument | 19 | `parser.add_argument('--data-dir', type=Path, required=True)` |
| main | parser.add_argument | 20 | `parser.add_argument('--bin-dir', type=Path, required=True)` |
| main | parser.add_argument | 21 | `parser.add_argument('--port', type=int, default=55432)` |
| main | parser.parse_args | 22 | `parser.parse_args(data not statically known)` |
| main | args.data_dir.resolve | 23 | `args.data_dir.resolve(data not statically known)` |
| main | args.bin_dir.resolve | 24 | `args.bin_dir.resolve(data not statically known)` |
| main | parser.error | 26 | `parser.error('Use an unprivileged local port')` |
| main | (…).is_file | 28 | `(data / MARKER).is_file(data not statically known)` |
| main | data.exists | 29 | `data.exists(data not statically known)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| process | `subprocess.run` | `main` | 33 |
| process | `subprocess.check_output` | `main` | 37 |
| environment_read | `os.environ.get` | `main` | 40 |
| process | `subprocess.run` | `main` | 47 |
| process | `subprocess.run` | `main` | 51 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 17 |
| unresolved_call | `main` | `parser.add_argument` | 18 |
| unresolved_call | `main` | `parser.add_argument` | 19 |
| unresolved_call | `main` | `parser.add_argument` | 20 |
| unresolved_call | `main` | `parser.add_argument` | 21 |
| unresolved_call | `main` | `parser.parse_args` | 22 |
| unresolved_call | `main` | `args.data_dir.resolve` | 23 |
| unresolved_call | `main` | `args.bin_dir.resolve` | 24 |
| unresolved_call | `main` | `parser.error` | 26 |
| unresolved_call | `main` | `(data / MARKER).is_file` | 28 |
| unresolved_call | `main` | `data.exists` | 29 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

The caller installs PostgreSQL 18 and provides a new data directory, local port and password. Initialization uses the builtin locale and a private temporary password file. Start records ownership before waiting for readiness. Stop operates only on a marked directory and leaves unrelated clusters alone.
