# create_label_group

**Entry point:** `create_label_group` (`http`)
**Source:** [labels](../modules/labels.md)
**Modules touched:** [labels](../modules/labels.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_label_group
    participant p1 as service.create_group
    participant p2 as HTTPException
    participant p3 as str
    p0-->>p1: service.create_group(data)
    p0-->>p2: HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))
    p0-->>p3: str(exc)
```

> Call sequence diagram shows 3 of 3 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 2 of 2 (0 omitted); unresolved 1 of 1 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 1; effect analysis evaluated: 1, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 5, emitted: 5, omitted: 0. Unavailable totals are excluded.

```mermaid
flowchart LR
    s1["1. create_label_group"]
    s2["2. service.create_group"]
    s3["3. HTTPException"]
    s4["4. str"]
    s1 -. "service.create_group(data)" .-> s2
    s1 -. "HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))" .-> s3
    s1 -. "str(exc)" .-> s4
    click s1 "../modules/labels.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_label_group` | `data: LabelGroupCreate`, `service: Annotated[LabelService, Depends(get_label_service)]` | `LabelConflictError`, `status` | - | `...` |
| `service.create_group` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `str` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_label_group | service.create_group | 49 | `service.create_group(data)` |
| create_label_group | HTTPException | 51 | `HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(...))` |
| create_label_group | str | 51 | `str(exc)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_label_group` | `service.create_group` | 49 |
| external_call | `create_label_group` | `HTTPException` | 51 |

## Behavior

This flow starts at `create_label_group` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
