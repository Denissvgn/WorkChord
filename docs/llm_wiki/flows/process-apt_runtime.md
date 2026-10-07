# apt_runtime

**Entry point:** `main` (`process`)
**Source:** [apt_runtime](../modules/apt_runtime.md)
**Modules touched:** [apt_runtime](../modules/apt_runtime.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as argparse.ArgumentParser
    participant p2 as parser.parse_args
    participant p3 as subprocess.check_output(…).strip
    participant p4 as subprocess.check_output
    participant p5 as prepare
    participant p6 as ValueError
    participant p7 as sorted
    participant p8 as (…).glob
    participant p9 as path.is_file
    participant p10 as path.read_text
    participant p11 as re.sub
    participant p12 as path.write_text
    participant p13 as print
    participant p14 as config.parent.mkdir
    participant p15 as config.write_text
    participant p16 as Path
    p0-->>p1: argparse.ArgumentParser
    p0-->>p2: parser.parse_args
    p0-->>p3: subprocess.check_output(…).strip
    p0-->>p4: subprocess.check_output
    p0->>p5: prepare
    p5-->>p6: ValueError
    p5-->>p7: sorted
    p5-->>p8: (…).glob
    p5-->>p7: sorted
    p5-->>p8: (…).glob
    p5-->>p9: path.is_file
    p5-->>p10: path.read_text
    p5-->>p11: re.sub
    p5-->>p12: path.write_text
    p5-->>p13: print
    p5-->>p14: config.parent.mkdir
    p5-->>p15: config.write_text
    p0-->>p16: Path
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. main"]
    s2["2. argparse.ArgumentParser"]
    s3["3. parser.parse_args"]
    s4["4. subprocess.check_output(…).strip"]
    s5["5. subprocess.check_output"]
    s6["6. prepare"]
    s7["7. ValueError"]
    s8["8. sorted"]
    s9["9. (…).glob"]
    s10["10. sorted"]
    s11["11. (…).glob"]
    s12["12. path.is_file"]
    s1 -. "argparse.ArgumentParser(description=__doc__)" .-> s2
    s1 -. "parser.parse_args(data not statically known)" .-> s3
    s1 -. "subprocess.check_output(…).strip(data not statically known)" .-> s4
    s1 -. "subprocess.check_output([...], text=True)" .-> s5
    s1 -->|"prepare(Path(...), architecture)"| s6
    s6 -. "ValueError(...)" .-> s7
    s6 -. "sorted(...)" .-> s8
    s6 -. "(…).glob('*.list')" .-> s9
    s6 -. "sorted(...)" .-> s10
    s6 -. "(…).glob('*.sources')" .-> s11
    s6 -. "path.is_file(data not statically known)" .-> s12
    b0["filesystem_read path.read_text"]
    s6 -. "filesystem_read path.read_text" .-> b0
    b1["filesystem_write path.write_text"]
    s6 -. "filesystem_write path.write_text" .-> b1
    b2["output print"]
    s6 -. "output print" .-> b2
    b3["filesystem_write config.write_text"]
    s6 -. "filesystem_write config.write_text" .-> b3
    click s1 "../modules/apt_runtime.md"
    click s6 "../modules/apt_runtime.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | - | - | - |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `subprocess.check_output(…).strip` | - | - | - | - |
| `subprocess.check_output` | - | - | - | - |
| `prepare` | `root: Path`, `architecture: str` | `APT_CONFIG` | - | - |
| `ValueError` | - | - | - | - |
| `sorted` | - | - | - | - |
| `(…).glob` | - | - | - | - |
| `sorted` | - | - | - | - |
| `(…).glob` | - | - | - | - |
| `path.is_file` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 39 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.parse_args | 40 | `parser.parse_args(data not statically known)` |
| main | subprocess.check_output(…).strip | 41 | `subprocess.check_output(['dpkg', '--print-architecture'], text=True).strip(data not statically known)` |
| main | subprocess.check_output | 41 | `subprocess.check_output([...], text=True)` |
| main | prepare | 42 | `prepare(Path(...), architecture)` |
| prepare | ValueError | 19 | `ValueError(...)` |
| prepare | sorted | 23 | `sorted(...)` |
| prepare | (…).glob | 23 | `(root / 'sources.list.d').glob('*.list')` |
| prepare | sorted | 24 | `sorted(...)` |
| prepare | (…).glob | 24 | `(root / 'sources.list.d').glob('*.sources')` |
| prepare | path.is_file | 26 | `path.is_file(data not statically known)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| filesystem_read | `path.read_text` | `prepare` | 28 |
| filesystem_write | `path.write_text` | `prepare` | 31 |
| output | `print` | `prepare` | 32 |
| filesystem_write | `config.write_text` | `prepare` | 35 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 39 |
| unresolved_call | `main` | `parser.parse_args` | 40 |
| unresolved_call | `main` | `subprocess.check_output(['dpkg', '--print-architecture'], text=True).strip` | 41 |
| external_call | `main` | `subprocess.check_output` | 41 |
| external_call | `prepare` | `ValueError` | 19 |
| external_call | `prepare` | `sorted` | 23 |
| unresolved_call | `prepare` | `(root / 'sources.list.d').glob` | 23 |
| external_call | `prepare` | `sorted` | 24 |
| unresolved_call | `prepare` | `(root / 'sources.list.d').glob` | 24 |
| unresolved_call | `prepare` | `path.is_file` | 26 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
