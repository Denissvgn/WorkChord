# dataset

**Entry point:** `dataset` (`http`)
**Source:** [serve_disposable_api](../modules/serve_disposable_api.md)
**Modules touched:** [serve_disposable_api](../modules/serve_disposable_api.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as dataset
    participant p1 as request.headers.get
    participant p2 as HTTPException
    p0-->>p1: request.headers.get('X-Fixture-Key')
    p0-->>p2: HTTPException(404)
```

> Call sequence diagram shows 2 of 2 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 0 of 0 (0 omitted); unresolved 2 of 2 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 1; effect analysis evaluated: 1, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 3, emitted: 3, omitted: 0. Unavailable totals are excluded.

```mermaid
flowchart LR
    s1["1. dataset"]
    s2["2. request.headers.get"]
    s3["3. HTTPException"]
    s1 -. "request.headers.get('X-Fixture-Key')" .-> s2
    s1 -. "HTTPException(404)" .-> s3
    click s1 "../modules/serve_disposable_api.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `dataset` | `request: Request`, `task_id: int` | - | - | `dataset_counts` |
| `request.headers.get` | - | - | - | - |
| `HTTPException` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| dataset | request.headers.get | 90 | `request.headers.get('X-Fixture-Key')` |
| dataset | HTTPException | 91 | `HTTPException(404)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `dataset` | `request.headers.get` | 90 |
| unresolved_call | `dataset` | `HTTPException` | 91 |

## Behavior

This flow starts at `dataset` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
