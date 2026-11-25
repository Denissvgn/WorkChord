# wiki_lock_root_preflight

**Entry point:** `main` (`process`)
**Source:** [wiki_lock_root_preflight](../modules/wiki_lock_root_preflight.md)
**Modules touched:** [wiki_lock_root_preflight](../modules/wiki_lock_root_preflight.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as check
    participant p2 as own_repository_git_dir
    participant p3 as selected_lock_git_dir
    participant p4 as _git_path
    participant p5 as _is_real_git_directory
    participant p6 as argparse.ArgumentParser
    participant p7 as parser.add_argument
    participant p8 as __doc__.splitlines
    participant p9 as Path.cwd
    participant p10 as parser.parse_args
    participant p11 as print
    participant p12 as checkout.resolve
    participant p13 as wiki_directory.is_dir
    participant p14 as lines.append
    participant p15 as '\n'.join
    participant p16 as wiki_directory.resolve
    participant p17 as candidate.resolve
    participant p18 as subprocess.run
    participant p19 as candidate.is_dir
    participant p20 as str
    participant p21 as candidate.is_symlink
    participant p22 as RuntimeError
    p0->>p1: check
    p1->>p2: own_repository_git_dir
    p1->>p3: selected_lock_git_dir
    p2->>p4: _git_path
    p3->>p5: _is_real_git_directory
    p0-->>p6: argparse.ArgumentParser(description=...)
    p0-->>p7: parser.add_argument('--checkout', type=Path, default=Path.cwd(...), help='checkout or linked worktree to check (default: current directory)')
    p0-->>p8: __doc__.splitlines
    p0-->>p9: Path.cwd
    p0-->>p10: parser.parse_args(argv)
    p0-->>p11: print(..., file=sys.stderr)
    p0-->>p11: print(report)
    p1-->>p12: checkout.resolve
    p1-->>p13: wiki_directory.is_dir
    p1-->>p14: lines.append(...)
    p1-->>p15: '\n'.join(lines)
    p1-->>p14: lines.append(...)
    p1-->>p14: lines.append('REFUSE: no .git directory found above the wiki directory the writer would use the wiki directory as its lock root.')
    p1-->>p15: '\n'.join(lines)
    p1-->>p14: lines.append(…)
    p1-->>p15: '\n'.join(lines)
    p1-->>p14: lines.append('OK: the effective lock root belongs to this repository.')
    p1-->>p15: '\n'.join(lines)
    p3-->>p16: wiki_directory.resolve
    p3-->>p17: candidate.resolve
    p4-->>p18: subprocess.run([...], check=False, capture_output=True, text=True)
    p5-->>p19: candidate.is_dir
    p4-->>p20: str(checkout)
    p5-->>p21: candidate.is_symlink
    p4-->>p22: RuntimeError(...)
```

> Call sequence diagram shows 30 of 34 interactions; 4 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 8 of 9 (1 omitted); unresolved 17 of 20 (3 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `scripts/ci/wiki_lock_root_preflight.py:_git_path` | 9 | - | unresolved | 3 |
| `scripts/ci/wiki_lock_root_preflight.py:_git_path` | 9 | - | external | 1 |
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
    s2["2. argparse.ArgumentParser"]
    s3["3. __doc__.splitlines"]
    s4["4. parser.add_argument"]
    s5["5. Path.cwd"]
    s6["6. parser.parse_args"]
    s7["7. check"]
    s8["8. own_repository_git_dir"]
    s9["9. _git_path"]
    s10["10. subprocess.run"]
    s11["11. str"]
    s12["12. RuntimeError"]
    s1 -. "argparse.ArgumentParser(description=...)" .-> s2
    s1 -. "__doc__.splitlines(data not statically known)" .-> s3
    s1 -. "parser.add_argument('--checkout', type=Path, default=Path.cwd(...), help='checkout or linked worktree to check (default: current directory)')" .-> s4
    s1 -. "Path.cwd(data not statically known)" .-> s5
    s1 -. "parser.parse_args(argv)" .-> s6
    s1 -->|"check(args.checkout)"| s7
    s7 -->|"own_repository_git_dir(checkout)"| s8
    s8 -->|"_git_path(checkout, '--git-common-dir')"| s9
    s9 -. "subprocess.run([...], check=False, capture_output=True, text=True)" .-> s10
    s9 -. "str(checkout)" .-> s11
    s9 -. "RuntimeError(...)" .-> s12
    b0["output print"]
    s1 -. "output print" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["mutation lines.append"]
    s7 -. "mutation lines.append" .-> b2
    b3["mutation lines.append"]
    s7 -. "mutation lines.append" .-> b3
    b4["mutation lines.append"]
    s7 -. "mutation lines.append" .-> b4
    b5["mutation lines.append"]
    s7 -. "mutation lines.append" .-> b5
    b6["mutation lines.append"]
    s7 -. "mutation lines.append" .-> b6
    b7["process subprocess.run"]
    s9 -. "process subprocess.run" .-> b7
    click s1 "../modules/wiki_lock_root_preflight.md"
    click s7 "../modules/wiki_lock_root_preflight.md"
    click s8 "../modules/wiki_lock_root_preflight.md"
    click s9 "../modules/wiki_lock_root_preflight.md"
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
| `main` | `argv: list[str] \| None` | `Path`, `sys` | - | `1`, `...` |
| `argparse.ArgumentParser` | - | - | - | - |
| `__doc__.splitlines` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `Path.cwd` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `check` | `checkout: Path` | `WIKI_DIRECTORY` | - | `(...)`, `(...)`, `(...)`, `(...)` |
| `own_repository_git_dir` | `checkout: Path` | - | - | `_git_path(...)` |
| `_git_path` | `checkout: Path`, `args: str` | - | - | `...` |
| `subprocess.run` | - | - | - | - |
| `str` | - | - | - | - |
| `RuntimeError` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 92 | `argparse.ArgumentParser(description=...)` |
| main | __doc__.splitlines | 92 | `__doc__.splitlines(data not statically known)` |
| main | parser.add_argument | 93 | `parser.add_argument('--checkout', type=Path, default=Path.cwd(...), help='checkout or linked worktree to check (default: current directory)')` |
| main | Path.cwd | 96 | `Path.cwd(data not statically known)` |
| main | parser.parse_args | 99 | `parser.parse_args(argv)` |
| main | check | 101 | `check(args.checkout)` |
| check | own_repository_git_dir | 63 | `own_repository_git_dir(checkout)` |
| own_repository_git_dir | _git_path | 43 | `_git_path(checkout, '--git-common-dir')` |
| _git_path | subprocess.run | 26 | `subprocess.run([...], check=False, capture_output=True, text=True)` |
| _git_path | str | 27 | `str(checkout)` |
| _git_path | RuntimeError | 33 | `RuntimeError(...)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 103 |
| output | `print` | `main` | 105 |
| mutation | `lines.append` | `check` | 70 |
| mutation | `lines.append` | `check` | 73 |
| mutation | `lines.append` | `check` | 75 |
| mutation | `lines.append` | `check` | 81 |
| mutation | `lines.append` | `check` | 87 |
| process | `subprocess.run` | `_git_path` | 26 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 92 |
| external_call | `main` | `__doc__.splitlines` | 92 |
| unresolved_call | `main` | `parser.add_argument` | 93 |
| external_call | `main` | `Path.cwd` | 96 |
| unresolved_call | `main` | `parser.parse_args` | 99 |
| external_call | `_git_path` | `RuntimeError` | 33 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

Reads Git metadata only and never opens a lock or runs the wiki writer. It resolves the nearest real directory named `.git` above the wiki directory, as the installed writer does, and compares it with the checkout's own repository directory. Exit 0 means the writer's locks stay inside this repository; exit 1 means they would not or cannot be determined, and the writer must then be run from an isolated clone.
