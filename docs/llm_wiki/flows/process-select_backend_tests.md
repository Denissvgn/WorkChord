# select_backend_tests

**Entry point:** `main` (`process`)
**Source:** [select_backend_tests](../modules/select_backend_tests.md)
**Modules touched:** [select_backend_tests](../modules/select_backend_tests.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as select
    participant p2 as changed_paths
    participant p3 as require_checkout_at
    participant p4 as selection_for
    participant p5 as wiki_selection
    participant p6 as _rev_parse
    participant p7 as wiki_revision
    participant p8 as is_ancestor
    participant p9 as _require_clean
    participant p10 as Repository
    participant p11 as module_name
    participant p12 as is_test_file
    participant p13 as FullSuite
    participant p14 as _git
    participant p15 as is_shared_ground
    participant p16 as WikiGraph
    participant p17 as reverse_closure
    participant p18 as argparse.ArgumentParser
    participant p19 as parser.add_argument
    participant p20 as __doc__.splitlines
    participant p21 as os.environ.get
    participant p22 as parser.parse_args
    participant p23 as print
    participant p24 as json.dumps
    participant p25 as (…).exists
    participant p26 as sorted (scripts/ci/select_backend_tests.py:select)
    p0->>p1: select
    p1->>p2: changed_paths
    p1->>p3: require_checkout_at
    p1->>p4: selection_for
    p1->>p5: wiki_selection
    p3->>p6: _rev_parse
    p5->>p7: wiki_revision
    p5->>p8: is_ancestor
    p5->>p9: _require_clean
    p1->>p10: Repository
    p1->>p11: module_name
    p1->>p12: is_test_file
    p1->>p13: FullSuite
    p2->>p14: _git
    p4->>p15: is_shared_ground
    p5->>p16: WikiGraph
    p5->>p17: reverse_closure
    p0-->>p18: argparse.ArgumentParser(description=...)
    p0-->>p19: parser.add_argument('--base', default=os.environ.get(...))
    p0-->>p20: __doc__.splitlines
    p0-->>p21: os.environ.get('BASE_SHA', '')
    p0-->>p19: parser.add_argument('--head', default=os.environ.get(...))
    p0-->>p21: os.environ.get('HEAD_SHA', '')
    p0-->>p19: parser.add_argument('--root', type=Path, default=REPOSITORY_ROOT)
    p0-->>p19: parser.add_argument('--engine', choices=(...), default='ast', help='ast: static graph only (default) wiki: static graph unioned with llm-wiki')
    p0-->>p22: parser.parse_args(argv)
    p0-->>p23: print(json.dumps(...))
    p0-->>p24: json.dumps(select(...), indent=2)
    p1-->>p25: (…).exists
    p1-->>p26: sorted (scripts/ci/select_backend_tests.py:select)(...)
```

> Call sequence diagram shows 30 of 143 interactions; 113 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 7 of 41 (34 omitted); unresolved 6 of 60 (54 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `scripts/ci/select_backend_tests.py:changed_paths` | 15 | [scripts/ci/select_backend_tests.py](../modules/select_backend_tests.md) | internal | 3 |
| `scripts/ci/select_backend_tests.py:_git` | 17 | - | external | 2 |
| `scripts/ci/select_backend_tests.py:changed_paths` | 15 | - | unresolved | 2 |
| `scripts/ci/select_backend_tests.py:changed_paths` | 15 | - | external | 1 |
| `scripts/ci/select_backend_tests.py:_rev_parse` | 26 | [scripts/ci/select_backend_tests.py](../modules/select_backend_tests.md) | internal | 1 |
| `scripts/ci/select_backend_tests.py:_rev_parse` | 26 | - | unresolved | 1 |
| `scripts/ci/select_backend_tests.py:require_checkout_at` | 25 | [scripts/ci/select_backend_tests.py](../modules/select_backend_tests.md) | internal | 2 |
| `scripts/ci/select_backend_tests.py:selection_for` | 32 | - | external | 6 |
> Omission summary shows 8 of 30 groups; 22 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 43; effect analysis evaluated: 24, partial: 0, unavailable: 19. Counts include steps omitted from the displayed trace.

Collector observations for 24 source steps with known totals: observed: 119, emitted: 119, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `7` | `7` | `0` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `__doc__.splitlines` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `os.environ.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `os.environ.get` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.parse_args` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `print` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `json.dumps` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. argparse.ArgumentParser"]
    s3["3. __doc__.splitlines"]
    s4["4. parser.add_argument"]
    s5["5. os.environ.get"]
    s6["6. parser.add_argument"]
    s7["7. os.environ.get"]
    s8["8. parser.add_argument"]
    s9["9. parser.add_argument"]
    s10["10. parser.parse_args"]
    s11["11. print"]
    s12["12. json.dumps"]
    s1 -. "argparse.ArgumentParser(description=...)" .-> s2
    s1 -. "__doc__.splitlines(data not statically known)" .-> s3
    s1 -. "parser.add_argument('--base', default=os.environ.get(...))" .-> s4
    s1 -. "os.environ.get('BASE_SHA', '')" .-> s5
    s1 -. "parser.add_argument('--head', default=os.environ.get(...))" .-> s6
    s1 -. "os.environ.get('HEAD_SHA', '')" .-> s7
    s1 -. "parser.add_argument('--root', type=Path, default=REPOSITORY_ROOT)" .-> s8
    s1 -. "parser.add_argument('--engine', choices=(...), default='ast', help='ast: static graph only (default); wiki: static graph unioned with llm-wiki')" .-> s9
    s1 -. "parser.parse_args(argv)" .-> s10
    s1 -. "print(json.dumps(...))" .-> s11
    s1 -. "json.dumps(select(...), indent=2)" .-> s12
    b0["environment_read os.environ.get"]
    s1 -. "environment_read os.environ.get" .-> b0
    b1["environment_read os.environ.get"]
    s1 -. "environment_read os.environ.get" .-> b1
    b2["output print"]
    s1 -. "output print" .-> b2
    click s1 "../modules/select_backend_tests.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | `argv: list[str] \| None` | `Path`, `REPOSITORY_ROOT` | - | `0` |
| `argparse.ArgumentParser` | - | - | - | - |
| `__doc__.splitlines` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `os.environ.get` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `os.environ.get` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `print` | - | - | - | - |
| `json.dumps` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 656 | `argparse.ArgumentParser(description=...)` |
| main | __doc__.splitlines | 656 | `__doc__.splitlines(data not statically known)` |
| main | parser.add_argument | 657 | `parser.add_argument('--base', default=os.environ.get(...))` |
| main | os.environ.get | 657 | `os.environ.get('BASE_SHA', '')` |
| main | parser.add_argument | 658 | `parser.add_argument('--head', default=os.environ.get(...))` |
| main | os.environ.get | 658 | `os.environ.get('HEAD_SHA', '')` |
| main | parser.add_argument | 659 | `parser.add_argument('--root', type=Path, default=REPOSITORY_ROOT)` |
| main | parser.add_argument | 660 | `parser.add_argument('--engine', choices=(...), default='ast', help='ast: static graph only (default); wiki: static graph unioned with llm-wiki')` |
| main | parser.parse_args | 666 | `parser.parse_args(argv)` |
| main | print | 667 | `print(json.dumps(...))` |
| main | json.dumps | 667 | `json.dumps(select(...), indent=2)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| environment_read | `os.environ.get` | `main` | 657 |
| environment_read | `os.environ.get` | `main` | 658 |
| output | `print` | `main` | 667 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 656 |
| external_call | `main` | `__doc__.splitlines` | 656 |
| unresolved_call | `main` | `parser.add_argument` | 659 |
| unresolved_call | `main` | `parser.add_argument` | 660 |
| unresolved_call | `main` | `parser.parse_args` | 666 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
