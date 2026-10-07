# local_baseline

**Entry point:** `main` (`process`)
**Source:** [local_baseline](../modules/local_baseline.md)
**Modules touched:** [load_common](../modules/load_common.md), [local_baseline](../modules/local_baseline.md), [result](../modules/result.md), [run](../modules/run.md)

**Related modules:** [load_common](../modules/load_common.md), [result](../modules/result.md), [run](../modules/run.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as argparse.ArgumentParser
    participant p2 as parser.add_argument
    participant p3 as parser.parse_args
    participant p4 as args.output.exists
    participant p5 as parser.error
    participant p6 as json.loads (scripts/load/local_baseline.py:main)
    participant p7 as args.declaration.read_text
    participant p8 as args.observations.read_text
    participant p9 as asyncio.run
    participant p10 as measure
    participant p11 as authorized_base_url
    participant p12 as urlsplit (scripts/load/common.py:authorized_base_url)
    participant p13 as QualificationInputError
    participant p14 as os.getenv
    participant p15 as len (scripts/load/common.py:authorized_base_url)
    participant p16 as change_id.strip
    p0-->>p1: argparse.ArgumentParser
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p3: parser.parse_args
    p0-->>p4: args.output.exists
    p0-->>p5: parser.error
    p0-->>p6: json.loads (scripts/load/local_baseline.py:main)
    p0-->>p7: args.declaration.read_text
    p0-->>p6: json.loads (scripts/load/local_baseline.py:main)
    p0-->>p8: args.observations.read_text
    p0-->>p5: parser.error
    p0-->>p9: asyncio.run
    p0->>p10: measure
    p10->>p11: authorized_base_url
    p11-->>p12: urlsplit (scripts/load/common.py:authorized_base_url)
    p11->>p13: QualificationInputError
    p11->>p13: QualificationInputError
    p11->>p13: QualificationInputError
    p11->>p13: QualificationInputError
    p11-->>p14: os.getenv
    p11-->>p15: len (scripts/load/common.py:authorized_base_url)
    p11-->>p16: change_id.strip
    p11->>p13: QualificationInputError
```

> Call sequence diagram shows 30 of 173 interactions; 143 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

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
    s7["7. parser.add_argument"]
    s8["8. parser.add_argument"]
    s9["9. parser.add_argument"]
    s10["10. parser.add_argument"]
    s11["11. parser.add_argument"]
    s12["12. parser.parse_args"]
    s1 -. "argparse.ArgumentParser(description=__doc__)" .-> s2
    s1 -. "parser.add_argument('--observations', type=Path)" .-> s3
    s1 -. "parser.add_argument('--base-url')" .-> s4
    s1 -. "parser.add_argument('--nonce')" .-> s5
    s1 -. "parser.add_argument('--session-state', type=Path)" .-> s6
    s1 -. "parser.add_argument('--agent-key-env', default='WORKCHORD_BENCHMARK_AGENT_KEY')" .-> s7
    s1 -. "parser.add_argument('--declaration', type=Path, required=True)" .-> s8
    s1 -. "parser.add_argument('--source-revision')" .-> s9
    s1 -. "parser.add_argument('--source-sha256')" .-> s10
    s1 -. "parser.add_argument('--output', type=Path, required=True)" .-> s11
    s1 -. "parser.parse_args(data not statically known)" .-> s12
    b0["filesystem_read args.declaration.read_text"]
    s1 -. "filesystem_read args.declaration.read_text" .-> b0
    b1["filesystem_read args.observations.read_text"]
    s1 -. "filesystem_read args.observations.read_text" .-> b1
    b2["output print"]
    s1 -. "output print" .-> b2
    click s1 "../modules/local_baseline.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `Path`, `Path`, `Path`, `Path`, `QualificationInputError` | `result[...]`, `result[...]`, `result[...]`, `result[...]`, `result[...]` | `...` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 121 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.add_argument | 122 | `parser.add_argument('--observations', type=Path)` |
| main | parser.add_argument | 123 | `parser.add_argument('--base-url')` |
| main | parser.add_argument | 124 | `parser.add_argument('--nonce')` |
| main | parser.add_argument | 125 | `parser.add_argument('--session-state', type=Path)` |
| main | parser.add_argument | 126 | `parser.add_argument('--agent-key-env', default='WORKCHORD_BENCHMARK_AGENT_KEY')` |
| main | parser.add_argument | 127 | `parser.add_argument('--declaration', type=Path, required=True)` |
| main | parser.add_argument | 128 | `parser.add_argument('--source-revision')` |
| main | parser.add_argument | 129 | `parser.add_argument('--source-sha256')` |
| main | parser.add_argument | 130 | `parser.add_argument('--output', type=Path, required=True)` |
| main | parser.parse_args | 131 | `parser.parse_args(data not statically known)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| filesystem_read | `args.declaration.read_text` | `main` | 134 |
| filesystem_read | `args.observations.read_text` | `main` | 136 |
| output | `print` | `main` | 148 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 121 |
| unresolved_call | `main` | `parser.add_argument` | 122 |
| unresolved_call | `main` | `parser.add_argument` | 123 |
| unresolved_call | `main` | `parser.add_argument` | 124 |
| unresolved_call | `main` | `parser.add_argument` | 125 |
| unresolved_call | `main` | `parser.add_argument` | 126 |
| unresolved_call | `main` | `parser.add_argument` | 127 |
| unresolved_call | `main` | `parser.add_argument` | 128 |
| unresolved_call | `main` | `parser.add_argument` | 129 |
| unresolved_call | `main` | `parser.add_argument` | 130 |
| unresolved_call | `main` | `parser.parse_args` | 131 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
