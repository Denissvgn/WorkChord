# isolated_rehearsal

**Entry point:** `main` (`process`)
**Source:** [isolated_rehearsal](../modules/isolated_rehearsal.md)
**Modules touched:** [isolated_rehearsal](../modules/isolated_rehearsal.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as prepare
    participant p2 as cleanup
    participant p3 as verify
    participant p4 as verify_images
    participant p5 as ownership_override
    participant p6 as resources
    participant p7 as load_marker
    participant p8 as docker
    participant p9 as argparse.ArgumentParser
    participant p10 as parser.add_argument
    participant p11 as parser.parse_args
    participant p12 as os.environ.items
    participant p13 as environment.update
    participant p14 as free_port
    participant p15 as subprocess.run
    participant p16 as str (scripts/server/isolated_rehearsal.py:main)
    participant p17 as RuntimeError
    participant p18 as print
    participant p19 as json.dumps (scripts/server/isolated_rehearsal.py:main)
    participant p20 as SystemExit
    participant p21 as ValueError (scripts/server/isolated_rehearsal.py:main)
    participant p22 as json.load
    participant p23 as __import__
    participant p24 as path.write_text (scripts/server/isolated_rehearsal.py:main)
    p0->>p1: prepare
    p0->>p2: cleanup
    p0->>p3: verify
    p0->>p4: verify_images
    p0->>p5: ownership_override
    p1->>p6: resources
    p2->>p7: load_marker
    p4->>p8: docker
    p0-->>p9: argparse.ArgumentParser(description=__doc__)
    p0-->>p10: parser.add_argument('action', choices=[...])
    p0-->>p10: parser.add_argument('--runtime-root', type=Path, required=True)
    p0-->>p10: parser.add_argument('--project')
    p0-->>p10: parser.add_argument('--platform', default='linux/arm64')
    p0-->>p11: parser.parse_args
    p0-->>p12: os.environ.items
    p0-->>p13: environment.update(WORKCHORD_HTTP_PORT=free_port(...), POSTGRES_HOST_PORT=free_port(...))
    p0-->>p14: free_port
    p0-->>p14: free_port
    p0-->>p13: environment.update(…)
    p0-->>p15: subprocess.run([...], cwd=ROOT, env=environment, check=True)
    p0-->>p16: str (scripts/server/isolated_rehearsal.py:main)(...)
    p0-->>p17: RuntimeError('Owned cleanup incomplete inspect cleanup-results.json')
    p0-->>p18: print(json.dumps(...))
    p0-->>p19: json.dumps (scripts/server/isolated_rehearsal.py:main)(result)
    p0-->>p20: SystemExit(1)
    p0-->>p21: ValueError (scripts/server/isolated_rehearsal.py:main)('Project identity mismatch')
    p0-->>p22: json.load(...)
    p0-->>p23: __import__('sys')
    p0-->>p24: path.write_text (scripts/server/isolated_rehearsal.py:main)(...)
    p0-->>p19: json.dumps (scripts/server/isolated_rehearsal.py:main)(ownership_override(...))
```

> Call sequence diagram shows 30 of 122 interactions; 92 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 12 of 50 (38 omitted); unresolved 10 of 54 (44 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `scripts/server/isolated_rehearsal.py:prepare` | 8 | - | external | 15 |
| `scripts/server/isolated_rehearsal.py:prepare` | 8 | - | unresolved | 10 |
| `scripts/server/isolated_rehearsal.py:resources` | 22 | - | unresolved | 7 |
| `scripts/server/isolated_rehearsal.py:resources` | 22 | [scripts/server/isolated_rehearsal.py](../modules/isolated_rehearsal.md) | internal | 2 |
| `scripts/server/isolated_rehearsal.py:docker` | 24 | - | unresolved | 1 |
| `scripts/server/isolated_rehearsal.py:docker` | 24 | - | external | 1 |
| `scripts/server/isolated_rehearsal.py:resources` | 22 | - | external | 1 |
| `scripts/server/isolated_rehearsal.py:prepare` | 8 | [scripts/server/isolated_rehearsal.py](../modules/isolated_rehearsal.md) | internal | 1 |
> Omission summary shows 8 of 22 groups; 14 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 19; effect analysis evaluated: 19, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 19 source steps with known totals: observed: 80, emitted: 80, omitted: 0. Unavailable totals are excluded.

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. argparse.ArgumentParser"]
    s3["3. parser.add_argument"]
    s4["4. parser.add_argument"]
    s5["5. parser.add_argument"]
    s6["6. parser.add_argument"]
    s7["7. parser.parse_args"]
    s8["8. prepare"]
    s9["9. Path (scripts/server/isolated_rehearsal.py:prepare)"]
    s10["10. re.fullmatch (scripts/server/isolated_rehearsal.py:prepare)"]
    s11["11. str (scripts/server/isolated_rehearsal.py:prepare)"]
    s12["12. ValueError (scripts/server/isolated_rehearsal.py:prepare)"]
    s1 -. "argparse.ArgumentParser(description=__doc__)" .-> s2
    s1 -. "parser.add_argument('action', choices=[...])" .-> s3
    s1 -. "parser.add_argument('--runtime-root', type=Path, required=True)" .-> s4
    s1 -. "parser.add_argument('--project')" .-> s5
    s1 -. "parser.add_argument('--platform', default='linux/arm64')" .-> s6
    s1 -. "parser.parse_args(data not statically known)" .-> s7
    s1 -->|"prepare(args.runtime_root, ..., args.platform)"| s8
    s8 -. "Path (scripts/server/isolated_rehearsal.py:prepare)(root)" .-> s9
    s8 -. "re.fullmatch (scripts/server/isolated_rehearsal.py:prepare)('/[A-Za-z0-9_./-]+', str(...))" .-> s10
    s8 -. "str (scripts/server/isolated_rehearsal.py:prepare)(root)" .-> s11
    s8 -. "ValueError (scripts/server/isolated_rehearsal.py:prepare)('Use a shell-safe absolute runtime path without spaces or control characters')" .-> s12
    b0["mutation environment.update"]
    s1 -. "mutation environment.update" .-> b0
    b1["mutation environment.update"]
    s1 -. "mutation environment.update" .-> b1
    b2["process subprocess.run"]
    s1 -. "process subprocess.run" .-> b2
    b3["output print"]
    s1 -. "output print" .-> b3
    b4["filesystem_read json.load"]
    s1 -. "filesystem_read json.load" .-> b4
    b5["filesystem_write path.write_text"]
    s1 -. "filesystem_write path.write_text" .-> b5
    b6["filesystem_write path.write_text"]
    s1 -. "filesystem_write path.write_text" .-> b6
    b7["filesystem_write path.write_text"]
    s8 -. "filesystem_write path.write_text" .-> b7
    click s1 "../modules/isolated_rehearsal.md"
    click s8 "../modules/isolated_rehearsal.md"
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
| `main` | - | `Path`, `ROOT` | - | - |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `prepare` | `root`, `project`, `platform` | `MARKER` | - | `marker` |
| `Path (scripts/server/isolated_rehearsal.py:prepare)` | - | - | - | - |
| `re.fullmatch (scripts/server/isolated_rehearsal.py:prepare)` | - | - | - | - |
| `str (scripts/server/isolated_rehearsal.py:prepare)` | - | - | - | - |
| `ValueError (scripts/server/isolated_rehearsal.py:prepare)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 127 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.add_argument | 128 | `parser.add_argument('action', choices=[...])` |
| main | parser.add_argument | 129 | `parser.add_argument('--runtime-root', type=Path, required=True)` |
| main | parser.add_argument | 130 | `parser.add_argument('--project')` |
| main | parser.add_argument | 131 | `parser.add_argument('--platform', default='linux/arm64')` |
| main | parser.parse_args | 132 | `parser.parse_args(data not statically known)` |
| main | prepare | 134 | `prepare(args.runtime_root, ..., args.platform)` |
| prepare | Path (scripts/server/isolated_rehearsal.py:prepare) | 57 | `Path(root)` |
| prepare | re.fullmatch (scripts/server/isolated_rehearsal.py:prepare) | 58 | `re.fullmatch('/[A-Za-z0-9_./-]+', str(...))` |
| prepare | str (scripts/server/isolated_rehearsal.py:prepare) | 58 | `str(root)` |
| prepare | ValueError (scripts/server/isolated_rehearsal.py:prepare) | 59 | `ValueError('Use a shell-safe absolute runtime path without spaces or control characters')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `environment.update` | `main` | 139 |
| mutation | `environment.update` | `main` | 140 |
| process | `subprocess.run` | `main` | 143 |
| output | `print` | `main` | 149 |
| filesystem_read | `json.load` | `main` | 156 |
| filesystem_write | `path.write_text` | `main` | 157 |
| filesystem_write | `path.write_text` | `main` | 160 |
| filesystem_write | `path.write_text` | `prepare` | 76 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 127 |
| unresolved_call | `main` | `parser.add_argument` | 128 |
| unresolved_call | `main` | `parser.add_argument` | 129 |
| unresolved_call | `main` | `parser.add_argument` | 130 |
| unresolved_call | `main` | `parser.add_argument` | 131 |
| unresolved_call | `main` | `parser.parse_args` | 132 |
| external_call | `prepare` | `re.fullmatch` | 58 |
| external_call | `prepare` | `ValueError` | 59 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
