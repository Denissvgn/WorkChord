# local_baseline

**Entry point:** `main` (`process`)
**Source:** [local_baseline](../modules/local_baseline.md)
**Modules touched:** [load_common](../modules/load_common.md), [local_baseline](../modules/local_baseline.md), [result](../modules/result.md), [run](../modules/run.md), [source_binding](../modules/source_binding.md)

**Related modules:** [load_common](../modules/load_common.md), [result](../modules/result.md), [run](../modules/run.md), [source_binding](../modules/source_binding.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as measure
    participant p2 as summarize
    participant p3 as verify_binding
    participant p4 as source_binding
    participant p5 as QualificationInputError
    participant p6 as sha256_file
    participant p7 as atomic_write_json
    participant p8 as authorized_base_url
    participant p9 as latency_summary
    participant p10 as seal_document
    participant p11 as percentile
    participant p12 as Recorder
    participant p13 as Attempt
    participant p14 as utc_now_text
    participant p15 as sha256_bytes
    participant p16 as canonical_json_bytes
    participant p17 as argparse.ArgumentParser
    participant p18 as parser.add_argument
    participant p19 as parser.parse_args
    participant p20 as args.output.exists
    participant p21 as parser.error
    participant p22 as json.loads (scripts/load/local_baseline.py:main)
    p0->>p1: measure
    p0->>p2: summarize
    p0->>p3: verify_binding
    p0->>p4: source_binding
    p0->>p5: QualificationInputError
    p0->>p6: sha256_file
    p0->>p7: atomic_write_json
    p1->>p8: authorized_base_url
    p2->>p9: latency_summary
    p7->>p10: seal_document
    p9->>p11: percentile
    p2->>p12: Recorder
    p2->>p13: Attempt
    p2->>p14: utc_now_text
    p10->>p15: sha256_bytes
    p10->>p16: canonical_json_bytes
    p0-->>p17: argparse.ArgumentParser(description=__doc__)
    p0-->>p18: parser.add_argument('--observations', type=Path)
    p0-->>p18: parser.add_argument('--base-url')
    p0-->>p18: parser.add_argument('--nonce')
    p0-->>p18: parser.add_argument('--session-state', type=Path)
    p0-->>p18: parser.add_argument('--agent-key-env', default='WORKCHORD_BENCHMARK_AGENT_KEY')
    p0-->>p18: parser.add_argument('--declaration', type=Path, required=True)
    p0-->>p18: parser.add_argument('--source-revision')
    p0-->>p18: parser.add_argument('--source-sha256')
    p0-->>p18: parser.add_argument('--output', type=Path, required=True)
    p0-->>p19: parser.parse_args
    p0-->>p20: args.output.exists
    p0-->>p21: parser.error('Use a new output path historical observations are immutable')
    p0-->>p22: json.loads (scripts/load/local_baseline.py:main)(args.declaration.read_text(...))
```

> Call sequence diagram shows 30 of 230 interactions; 200 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 2 of 87 (85 omitted); unresolved 12 of 96 (84 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `scripts/load/source_binding.py:source_binding` | 15 | - | unresolved | 9 |
| `scripts/load/source_binding.py:source_binding` | 15 | - | external | 9 |
| `scripts/load/local_baseline.py:main` | 1 | - | unresolved | 6 |
| `scripts/load/local_baseline.py:main` | 1 | - | external | 6 |
| `scripts/load/common.py:authorized_base_url` | 41 | - | external | 3 |
| `scripts/load/common.py:authorized_base_url` | 41 | [scripts/load/common.py](../modules/load_common.md) | internal | 6 |
| `scripts/load/common.py:authorized_base_url` | 41 | - | unresolved | 2 |
| `scripts/load/local_baseline.py:measure` | 40 | - | external | 15 |
> Omission summary shows 8 of 32 groups; 24 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 48; effect analysis evaluated: 19, partial: 0, unavailable: 29. Counts include steps omitted from the displayed trace.

Collector observations for 19 source steps with known totals: observed: 87, emitted: 87, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `17` | `17` | `0` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.parse_args` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

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
| `main` | - | `Path`, `Path`, `Path`, `Path`, `QualificationInputError` | `result[...]`, `result[...]`, `result[...]`, `result[...]`, `result[...]`, `result[...]`, `result[...]`, `result[...]` | `...` |
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
| main | argparse.ArgumentParser | 172 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.add_argument | 173 | `parser.add_argument('--observations', type=Path)` |
| main | parser.add_argument | 174 | `parser.add_argument('--base-url')` |
| main | parser.add_argument | 175 | `parser.add_argument('--nonce')` |
| main | parser.add_argument | 176 | `parser.add_argument('--session-state', type=Path)` |
| main | parser.add_argument | 177 | `parser.add_argument('--agent-key-env', default='WORKCHORD_BENCHMARK_AGENT_KEY')` |
| main | parser.add_argument | 178 | `parser.add_argument('--declaration', type=Path, required=True)` |
| main | parser.add_argument | 179 | `parser.add_argument('--source-revision')` |
| main | parser.add_argument | 180 | `parser.add_argument('--source-sha256')` |
| main | parser.add_argument | 181 | `parser.add_argument('--output', type=Path, required=True)` |
| main | parser.parse_args | 182 | `parser.parse_args(data not statically known)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| filesystem_read | `args.declaration.read_text` | `main` | 186 |
| filesystem_read | `args.observations.read_text` | `main` | 188 |
| output | `print` | `main` | 206 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 172 |
| unresolved_call | `main` | `parser.add_argument` | 173 |
| unresolved_call | `main` | `parser.add_argument` | 174 |
| unresolved_call | `main` | `parser.add_argument` | 175 |
| unresolved_call | `main` | `parser.add_argument` | 176 |
| unresolved_call | `main` | `parser.add_argument` | 177 |
| unresolved_call | `main` | `parser.add_argument` | 178 |
| unresolved_call | `main` | `parser.add_argument` | 179 |
| unresolved_call | `main` | `parser.add_argument` | 180 |
| unresolved_call | `main` | `parser.add_argument` | 181 |
| unresolved_call | `main` | `parser.parse_args` | 182 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
