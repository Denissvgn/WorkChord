# check_markdown_links

**Entry point:** `main` (`process`)
**Source:** [check_markdown_links](../modules/check_markdown_links.md)
**Modules touched:** [check_markdown_links](../modules/check_markdown_links.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as Path.cwd
    participant p2 as changed_paths
    participant p3 as os.environ.get
    participant p4 as print
    participant p5 as broken_links
    participant p6 as p.endswith
    participant p7 as p.startswith
    participant p8 as len
    participant p9 as relative.endswith
    participant p10 as relative.startswith
    participant p11 as source.is_file
    participant p12 as LINK_PATTERN.findall
    participant p13 as source.read_text
    participant p14 as target.startswith
    participant p15 as target.split
    participant p16 as path_part.startswith
    participant p17 as path_part.lstrip
    participant p18 as resolved.exists
    participant p19 as problems.append
    p0-->>p1: Path.cwd
    p0-->>p2: changed_paths(os.environ.get(...), os.environ.get(...))
    p0-->>p3: os.environ.get('BASE_SHA', '')
    p0-->>p3: os.environ.get('HEAD_SHA', '')
    p0-->>p4: print('Could not determine the changed files', file=sys.stderr)
    p0->>p5: broken_links
    p0-->>p4: print(problem, file=sys.stderr)
    p0-->>p6: p.endswith('.md')
    p0-->>p7: p.startswith(WIKI_PREFIX)
    p0-->>p4: print(...)
    p0-->>p8: len(checked)
    p0-->>p8: len(problems)
    p5-->>p9: relative.endswith('.md')
    p5-->>p10: relative.startswith(WIKI_PREFIX)
    p5-->>p11: source.is_file
    p5-->>p12: LINK_PATTERN.findall(source.read_text(...))
    p5-->>p13: source.read_text(encoding='utf-8')
    p5-->>p14: target.startswith(SKIPPED_PREFIXES)
    p5-->>p15: target.split(' ', 1)
    p5-->>p16: path_part.startswith('/')
    p5-->>p17: path_part.lstrip('/')
    p5-->>p18: resolved.exists
    p5-->>p19: problems.append(...)
```

> Call sequence diagram shows 23 of 23 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 9 of 9 (0 omitted); unresolved 13 of 13 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 2; effect analysis evaluated: 2, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 2 source steps with known totals: observed: 17, emitted: 17, omitted: 0. Unavailable totals are excluded.

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. Path.cwd"]
    s3["3. changed_paths"]
    s4["4. os.environ.get"]
    s5["5. os.environ.get"]
    s6["6. print"]
    s7["7. broken_links"]
    s8["8. relative.endswith"]
    s9["9. relative.startswith"]
    s10["10. source.is_file"]
    s11["11. LINK_PATTERN.findall"]
    s12["12. source.read_text"]
    s1 -. "Path.cwd(data not statically known)" .-> s2
    s1 -. "changed_paths(os.environ.get(...), os.environ.get(...))" .-> s3
    s1 -. "os.environ.get('BASE_SHA', '')" .-> s4
    s1 -. "os.environ.get('HEAD_SHA', '')" .-> s5
    s1 -. "print('Could not determine the changed files', file=sys.stderr)" .-> s6
    s1 -->|"broken_links(root, paths)"| s7
    s7 -. "relative.endswith('.md')" .-> s8
    s7 -. "relative.startswith(WIKI_PREFIX)" .-> s9
    s7 -. "source.is_file(data not statically known)" .-> s10
    s7 -. "LINK_PATTERN.findall(source.read_text(...))" .-> s11
    s7 -. "source.read_text(encoding='utf-8')" .-> s12
    b0["environment_read os.environ.get"]
    s1 -. "environment_read os.environ.get" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["output print"]
    s1 -. "output print" .-> b2
    b3["output print"]
    s1 -. "output print" .-> b3
    b4["filesystem_read source.read_text"]
    s7 -. "filesystem_read source.read_text" .-> b4
    b5["mutation problems.append"]
    s7 -. "mutation problems.append" .-> b5
    click s1 "../modules/check_markdown_links.md"
    click s7 "../modules/check_markdown_links.md"
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
| `main` | `argv: list[str]` | `sys`, `sys`, `WIKI_PREFIX` | - | `1`, `...` |
| `Path.cwd` | - | - | - | - |
| `changed_paths` | - | - | - | - |
| `os.environ.get` | - | - | - | - |
| `os.environ.get` | - | - | - | - |
| `print` | - | - | - | - |
| `broken_links` | `root: Path`, `relative_paths: list[str]` | `WIKI_PREFIX`, `SKIPPED_PREFIXES` | - | `problems` |
| `relative.endswith` | - | - | - | - |
| `relative.startswith` | - | - | - | - |
| `source.is_file` | - | - | - | - |
| `LINK_PATTERN.findall` | - | - | - | - |
| `source.read_text` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | Path.cwd | 45 | `Path.cwd(data not statically known)` |
| main | changed_paths | 49 | `changed_paths(os.environ.get(...), os.environ.get(...))` |
| main | os.environ.get | 49 | `os.environ.get('BASE_SHA', '')` |
| main | os.environ.get | 49 | `os.environ.get('HEAD_SHA', '')` |
| main | print | 51 | `print('Could not determine the changed files', file=sys.stderr)` |
| main | broken_links | 53 | `broken_links(root, paths)` |
| broken_links | relative.endswith | 27 | `relative.endswith('.md')` |
| broken_links | relative.startswith | 27 | `relative.startswith(WIKI_PREFIX)` |
| broken_links | source.is_file | 30 | `source.is_file(data not statically known)` |
| broken_links | LINK_PATTERN.findall | 32 | `LINK_PATTERN.findall(source.read_text(...))` |
| broken_links | source.read_text | 32 | `source.read_text(encoding='utf-8')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| environment_read | `os.environ.get` | `main` | 49 |
| output | `print` | `main` | 51 |
| output | `print` | `main` | 55 |
| output | `print` | `main` | 57 |
| filesystem_read | `source.read_text` | `broken_links` | 32 |
| mutation | `problems.append` | `broken_links` | 40 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `Path.cwd` | 45 |
| unresolved_call | `broken_links` | `relative.endswith` | 27 |
| unresolved_call | `broken_links` | `relative.startswith` | 27 |
| unresolved_call | `broken_links` | `source.is_file` | 30 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
