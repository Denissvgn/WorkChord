# check_postgresql_documentation

**Entry point:** `main` (`process`)
**Source:** [check_postgresql_documentation](../modules/check_postgresql_documentation.md)
**Modules touched:** [check_postgresql_documentation](../modules/check_postgresql_documentation.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as check_documentation
    participant p2 as _read
    participant p3 as path.is_file
    participant p4 as DocumentationContractError
    participant p5 as path.read_text
    participant p6 as '\n'.join
    participant p7 as texts.values
    participant p8 as forbidden.items
    participant p9 as snippet.lower
    participant p10 as combined.lower
    participant p11 as texts.items
    participant p12 as SHELL_FENCE_PATTERN.findall
    participant p13 as LIVE_SQLITE_COPY_PATTERN.search
    participant p14 as _require
    participant p15 as ' '.join
    participant p16 as text.split
    participant p17 as snippet.split
    participant p18 as Path
    p0->>p1: check_documentation
    p1->>p2: _read
    p2-->>p3: path.is_file
    p2->>p4: DocumentationContractError
    p2-->>p5: path.read_text
    p1-->>p6: '\n'.join
    p1-->>p7: texts.values
    p1-->>p8: forbidden.items
    p1-->>p9: snippet.lower
    p1-->>p10: combined.lower
    p1->>p4: DocumentationContractError
    p1-->>p11: texts.items
    p1-->>p12: SHELL_FENCE_PATTERN.findall
    p1-->>p13: LIVE_SQLITE_COPY_PATTERN.search
    p1->>p4: DocumentationContractError
    p1->>p14: _require
    p14->>p2: _read
    p14-->>p15: ' '.join
    p14-->>p16: text.split
    p14-->>p15: ' '.join
    p14-->>p17: snippet.split
    p14->>p4: DocumentationContractError
    p1-->>p18: Path
    p1->>p14: _require
    p1-->>p18: Path
    p1->>p14: _require
    p1-->>p18: Path
    p1->>p14: _require
    p1-->>p18: Path
    p1->>p14: _require
```

> Call sequence diagram shows 30 of 58 interactions; 28 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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
| main | check_documentation | 226 | `check_documentation(data not statically known)` |
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
| output | `print` | `main` | 228 |
| output | `print` | `main` | 230 |
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
