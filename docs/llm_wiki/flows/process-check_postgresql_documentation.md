# check_postgresql_documentation

**Entry point:** `main` (`process`)
**Source:** [check_postgresql_documentation](../modules/check_postgresql_documentation.md)
**Modules touched:** [check_postgresql_documentation](../modules/check_postgresql_documentation.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as check_documentation
    participant p2 as _read
    participant p3 as _require
    participant p4 as _local_link_count
    participant p5 as DocumentationContractError
    participant p6 as print
    participant p7 as '\n'.join
    participant p8 as texts.values
    participant p9 as forbidden.items
    participant p10 as snippet.lower
    participant p11 as combined.lower
    participant p12 as texts.items
    participant p13 as SHELL_FENCE_PATTERN.findall
    participant p14 as LIVE_SQLITE_COPY_PATTERN.search
    participant p15 as Path
    participant p16 as range
    participant p17 as sum
    participant p18 as len
    p0->>p1: check_documentation
    p1->>p2: _read
    p1->>p3: _require
    p1->>p4: _local_link_count
    p1->>p5: DocumentationContractError
    p0-->>p6: print(..., file=sys.stderr)
    p1-->>p7: '\n'.join(texts.values(...))
    p0-->>p6: print(...)
    p1-->>p8: texts.values
    p1-->>p9: forbidden.items
    p1-->>p10: snippet.lower
    p1-->>p11: combined.lower
    p1-->>p12: texts.items
    p1-->>p13: SHELL_FENCE_PATTERN.findall(text)
    p1-->>p14: LIVE_SQLITE_COPY_PATTERN.search(block)
    p1-->>p15: Path('README.md')
    p1-->>p15: Path('docs/runbooks/postgresql-operations.md')
    p1-->>p15: Path('.env.example')
    p1-->>p15: Path('docs/runbooks/postgresql-operations.md')
    p1-->>p15: Path('docs/runbooks/sqlite-to-postgresql-migration.md')
    p1-->>p15: Path('docs/runbooks/postgresql-backup-restore.md')
    p1-->>p15: Path('docs/runbooks/postgresql-qualification.md')
    p1-->>p15: Path('docs/runbooks/postgresql-rehearsal-cutover-evidence.md')
    p1-->>p15: Path('docs/runbooks/postgresql-postcutover-release-and-closeout.md')
    p1-->>p15: Path('docs/runbooks/sqlite-to-postgresql-cutover.md')
    p1-->>p15: Path('docs/runbooks/postgresql-cutover-checklist.md')
    p1-->>p16: range(1, 14)
    p1-->>p15: Path('docs/runbooks/postgresql-troubleshooting.md')
    p1-->>p17: sum(...)
    p1-->>p18: len(DOCUMENTS)
```

> Call sequence diagram shows 30 of 60 interactions; 30 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 17 of 17 (0 omitted); unresolved 8 of 21 (13 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `scripts/ci/check_postgresql_documentation.py:_read` | 3 | - | unresolved | 2 |
| `scripts/ci/check_postgresql_documentation.py:_read` | 3 | [scripts/ci/check_postgresql_documentation.py](../modules/check_postgresql_documentation.md) | internal | 1 |
| `scripts/ci/check_postgresql_documentation.py:check_documentation` | 2 | [scripts/ci/check_postgresql_documentation.py](../modules/check_postgresql_documentation.md) | internal | 12 |
| `scripts/ci/check_postgresql_documentation.py:_require` | 17 | [scripts/ci/check_postgresql_documentation.py](../modules/check_postgresql_documentation.md) | internal | 2 |
| `scripts/ci/check_postgresql_documentation.py:_require` | 17 | - | unresolved | 4 |
| `scripts/ci/check_postgresql_documentation.py:_local_link_count` | 49 | [scripts/ci/check_postgresql_documentation.py](../modules/check_postgresql_documentation.md) | internal | 2 |
| `scripts/ci/check_postgresql_documentation.py:_local_link_count` | 49 | - | unresolved | 7 |
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 23; effect analysis evaluated: 17, partial: 0, unavailable: 6. Counts include steps omitted from the displayed trace.

Collector observations for 17 source steps with known totals: observed: 47, emitted: 47, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `check_documentation` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `_read` | `available` | `evaluated` | `available` | `4` | `4` | `0` |
| `path.is_file` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `DocumentationContractError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `path.read_text` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `'\n'.join` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `texts.values` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `forbidden.items` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `snippet.lower` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `combined.lower` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `DocumentationContractError` | `unavailable` | `unavailable` | `unavailable` | — | — | — |

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. check_documentation"]
    s3["3. _read"]
    s4["4. path.is_file"]
    s5["5. DocumentationContractError"]
    s6["6. path.read_text"]
    s7["7. '\n'.join"]
    s8["8. texts.values"]
    s9["9. forbidden.items"]
    s10["10. snippet.lower"]
    s11["11. combined.lower"]
    s12["12. DocumentationContractError"]
    s1 -->|"check_documentation(data not statically known)"| s2
    s2 -->|"_read(path)"| s3
    s3 -. "path.is_file(data not statically known)" .-> s4
    s3 -->|"DocumentationContractError(...)"| s5
    s3 -. "path.read_text(encoding='utf-8')" .-> s6
    s2 -. "'\n'.join(texts.values(...))" .-> s7
    s2 -. "texts.values(data not statically known)" .-> s8
    s2 -. "forbidden.items(data not statically known)" .-> s9
    s2 -. "snippet.lower(data not statically known)" .-> s10
    s2 -. "snippet.lower(data not statically known)" .-> s11
    s2 -->|"DocumentationContractError(...)"| s12
    b0["output print"]
    s1 -. "output print" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["filesystem_read path.read_text"]
    s3 -. "filesystem_read path.read_text" .-> b2
    click s1 "../modules/check_postgresql_documentation.md"
    click s2 "../modules/check_postgresql_documentation.md"
    click s3 "../modules/check_postgresql_documentation.md"
    click s5 "../modules/check_postgresql_documentation.md"
    click s12 "../modules/check_postgresql_documentation.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `DocumentationContractError`, `sys` | - | `1`, `0` |
| `check_documentation` | - | `DOCUMENTS`, `DOCUMENTS`, `DOCUMENTS` | - | `(...)` |
| `_read` | `relative_path: Path` | `REPOSITORY_ROOT` | - | `path.read_text(...)` |
| `path.is_file` | - | - | - | - |
| `DocumentationContractError` | - | - | - | - |
| `path.read_text` | - | - | - | - |
| `'\n'.join` | - | - | - | - |
| `texts.values` | - | - | - | - |
| `forbidden.items` | - | - | - | - |
| `snippet.lower` | - | - | - | - |
| `combined.lower` | - | - | - | - |
| `DocumentationContractError` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | check_documentation | 229 | `check_documentation(data not statically known)` |
| check_documentation | _read | 84 | `_read(path)` |
| _read | path.is_file | 45 | `path.is_file(data not statically known)` |
| _read | DocumentationContractError | 46 | `DocumentationContractError(...)` |
| _read | path.read_text | 47 | `path.read_text(encoding='utf-8')` |
| check_documentation | '\n'.join | 85 | `'\n'.join(texts.values(...))` |
| check_documentation | texts.values | 85 | `texts.values(data not statically known)` |
| check_documentation | forbidden.items | 96 | `forbidden.items(data not statically known)` |
| check_documentation | snippet.lower | 97 | `snippet.lower(data not statically known)` |
| check_documentation | combined.lower | 97 | `snippet.lower(data not statically known)` |
| check_documentation | DocumentationContractError | 98 | `DocumentationContractError(...)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 231 |
| output | `print` | `main` | 233 |
| filesystem_read | `path.read_text` | `_read` | 47 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `_read` | `path.is_file` | 45 |
| unresolved_call | `check_documentation` | `'\n'.join` | 85 |
| unresolved_call | `check_documentation` | `texts.values` | 85 |
| unresolved_call | `check_documentation` | `forbidden.items` | 96 |
| unresolved_call | `check_documentation` | `snippet.lower` | 97 |
| unresolved_call | `check_documentation` | `combined.lower` | 97 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
