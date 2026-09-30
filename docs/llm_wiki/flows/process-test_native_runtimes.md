# test_native_runtimes

**Entry point:** `__main__` (`process`)
**Source:** [test_native_runtimes](../modules/test_native_runtimes.md)
**Modules touched:** [test_native_runtimes](../modules/test_native_runtimes.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as __main__
    participant p1 as unittest.main
    p0-->>p1: unittest.main
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. __main__"]
    s2["2. unittest.main"]
    s1 -. "unittest.main(data not statically known)" .-> s2
    click s1 "../modules/test_native_runtimes.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `__main__` | - | - | - | - |
| `unittest.main` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| __main__ | unittest.main | 365 | `unittest.main(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `__main__` | `unittest.main` | 365 |

## Behavior

This flow starts at `__main__` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
