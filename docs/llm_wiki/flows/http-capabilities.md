# capabilities

**Entry point:** `capabilities` (`http`)
**Source:** [time_entries](../modules/time_entries.md)
**Modules touched:** [config](../modules/config.md), [time_entries](../modules/time_entries.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as capabilities
    participant p1 as db.info.get
    participant p2 as bool
    participant p3 as get_settings
    participant p4 as Settings
    p0-->>p1: db.info.get
    p0-->>p2: bool
    p0->>p3: get_settings
    p3->>p4: Settings
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. capabilities"]
    s2["2. db.info.get"]
    s3["3. bool"]
    s4["4. get_settings"]
    s5["5. Settings"]
    s1 -. "db.info.get('authority')" .-> s2
    s1 -. "bool(...)" .-> s3
    s1 -->|"get_settings(data not statically known)"| s4
    s4 -->|"Settings(data not statically known)"| s5
    click s1 "../modules/time_entries.md"
    click s4 "../modules/config.md"
    click s5 "../modules/config.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `capabilities` | `db: DB` | - | - | `{...}` |
| `db.info.get` | - | - | - | - |
| `bool` | - | - | - | - |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| capabilities | db.info.get | 21 | `db.info.get('authority')` |
| capabilities | bool | 22 | `bool(...)` |
| capabilities | get_settings | 23 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `capabilities` | `db.info.get` | 21 |

## Behavior

This flow starts at `capabilities` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
