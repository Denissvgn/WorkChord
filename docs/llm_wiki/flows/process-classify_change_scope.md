# classify_change_scope

**Entry point:** `main` (`process`)
**Source:** [classify_change_scope](../modules/classify_change_scope.md)
**Modules touched:** [classify_change_scope](../modules/classify_change_scope.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as classify
    participant p2 as os.environ.get
    participant p3 as print (scripts/ci/classify_change_scope.py:main)
    participant p4 as changed_paths
    participant p5 as docs_only
    participant p6 as subprocess.run
    participant p7 as bool
    participant p8 as print (scripts/ci/classify_change_scope.py:changed_paths)
    participant p9 as all
    participant p10 as result.stderr.strip
    participant p11 as is_documentation
    participant p12 as result.stdout.splitlines
    participant p13 as line.strip
    participant p14 as _is_documentation_path
    participant p15 as PurePosixPath
    participant p16 as len
    participant p17 as parts[…].lower().endswith
    participant p18 as parts[…].lower
    p0->>p1: classify
    p0-->>p2: os.environ.get('EVENT_NAME', '')
    p0-->>p2: os.environ.get('BASE_SHA', '')
    p0-->>p2: os.environ.get('HEAD_SHA', '')
    p0-->>p3: print (scripts/ci/classify_change_scope.py:main)(...)
    p1->>p4: changed_paths
    p1->>p5: docs_only
    p4-->>p6: subprocess.run([...], capture_output=True, text=True, check=False)
    p5-->>p7: bool(paths)
    p4-->>p8: print (scripts/ci/classify_change_scope.py:changed_paths)(result.stderr.strip(...), file=sys.stderr)
    p5-->>p9: all(...)
    p4-->>p10: result.stderr.strip
    p5->>p11: is_documentation
    p4-->>p12: result.stdout.splitlines
    p4-->>p13: line.strip
    p11->>p14: _is_documentation_path
    p14-->>p15: PurePosixPath(path)
    p14-->>p16: len(parts)
    p14-->>p16: len(parts)
    p14-->>p17: parts[…].lower().endswith('.md')
    p14-->>p18: parts[…].lower
```

> Call sequence diagram shows 21 of 21 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 11 of 11 (0 omitted); unresolved 5 of 5 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 6; effect analysis evaluated: 6, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 6 source steps with known totals: observed: 29, emitted: 29, omitted: 0. Unavailable totals are excluded.

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. classify"]
    s3["3. changed_paths"]
    s4["4. subprocess.run"]
    s5["5. print (scripts/ci/classify_change_scope.py:changed_paths)"]
    s6["6. result.stderr.strip"]
    s7["7. result.stdout.splitlines"]
    s8["8. line.strip"]
    s9["9. docs_only"]
    s10["10. bool"]
    s11["11. all"]
    s12["12. is_documentation"]
    s1 -->|"classify(os.environ.get(...), os.environ.get(...), os.environ.get(...))"| s2
    s2 -->|"changed_paths(base_sha, head_sha)"| s3
    s3 -. "subprocess.run([...], capture_output=True, text=True, check=False)" .-> s4
    s3 -. "print (scripts/ci/classify_change_scope.py:changed_paths)(result.stderr.strip(...), file=sys.stderr)" .-> s5
    s3 -. "result.stderr.strip(data not statically known)" .-> s6
    s3 -. "result.stdout.splitlines(data not statically known)" .-> s7
    s3 -. "line.strip(data not statically known)" .-> s8
    s2 -->|"docs_only(paths)"| s9
    s9 -. "bool(paths)" .-> s10
    s9 -. "all(...)" .-> s11
    s9 -->|"is_documentation(path)"| s12
    b0["environment_read os.environ.get"]
    s1 -. "environment_read os.environ.get" .-> b0
    b1["environment_read os.environ.get"]
    s1 -. "environment_read os.environ.get" .-> b1
    b2["environment_read os.environ.get"]
    s1 -. "environment_read os.environ.get" .-> b2
    b3["output print"]
    s1 -. "output print" .-> b3
    b4["process subprocess.run"]
    s3 -. "process subprocess.run" .-> b4
    b5["output print"]
    s3 -. "output print" .-> b5
    click s1 "../modules/classify_change_scope.md"
    click s2 "../modules/classify_change_scope.md"
    click s3 "../modules/classify_change_scope.md"
    click s9 "../modules/classify_change_scope.md"
    click s12 "../modules/classify_change_scope.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
    class b4 boundary
    class b5 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | - | - | `0` |
| `classify` | `event_name: str`, `base_sha: str`, `head_sha: str` | `CLASSIFIED_EVENTS` | - | `False`, `False`, `docs_only(...)` |
| `changed_paths` | `base_sha: str`, `head_sha: str` | `ZERO_SHA`, `sys` | - | `None`, `None`, `...` |
| `subprocess.run` | - | - | - | - |
| `print (scripts/ci/classify_change_scope.py:changed_paths)` | - | - | - | - |
| `result.stderr.strip` | - | - | - | - |
| `result.stdout.splitlines` | - | - | - | - |
| `line.strip` | - | - | - | - |
| `docs_only` | `paths: list[str]` | - | - | `...` |
| `bool` | - | - | - | - |
| `all` | - | - | - | - |
| `is_documentation` | `path: str` | `CHECKED_DOCUMENTS` | - | `...` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | classify | 97 | `classify(os.environ.get(...), os.environ.get(...), os.environ.get(...))` |
| classify | changed_paths | 90 | `changed_paths(base_sha, head_sha)` |
| changed_paths | subprocess.run | 75 | `subprocess.run([...], capture_output=True, text=True, check=False)` |
| changed_paths | print (scripts/ci/classify_change_scope.py:changed_paths) | 82 | `print(result.stderr.strip(...), file=sys.stderr)` |
| changed_paths | result.stderr.strip | 82 | `result.stderr.strip(data not statically known)` |
| changed_paths | result.stdout.splitlines | 84 | `result.stdout.splitlines(data not statically known)` |
| changed_paths | line.strip | 84 | `line.strip(data not statically known)` |
| classify | docs_only | 93 | `docs_only(paths)` |
| docs_only | bool | 68 | `bool(paths)` |
| docs_only | all | 68 | `all(...)` |
| docs_only | is_documentation | 68 | `is_documentation(path)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| environment_read | `os.environ.get` | `main` | 98 |
| environment_read | `os.environ.get` | `main` | 99 |
| environment_read | `os.environ.get` | `main` | 100 |
| output | `print` | `main` | 102 |
| process | `subprocess.run` | `changed_paths` | 75 |
| output | `print` | `changed_paths` | 82 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `changed_paths` | `result.stdout.splitlines` | 84 |
| unresolved_call | `changed_paths` | `line.strip` | 84 |
| external_call | `docs_only` | `all` | 68 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
