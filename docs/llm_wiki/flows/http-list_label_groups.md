# list_label_groups

**Entry point:** `list_label_groups` (`http`)
**Source:** [labels](../modules/labels.md)
**Modules touched:** [labels](../modules/labels.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_label_groups
    participant p1 as service.list_groups
    p0-->>p1: service.list_groups(include_inactive=include_inactive)
```

> Call sequence diagram shows 1 of 1 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 0 of 0 (0 omitted); unresolved 1 of 1 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 1; effect analysis evaluated: 1, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 3, emitted: 3, omitted: 0. Unavailable totals are excluded.

```mermaid
flowchart LR
    s1["1. list_label_groups"]
    s2["2. service.list_groups"]
    s1 -. "service.list_groups(include_inactive=include_inactive)" .-> s2
    click s1 "../modules/labels.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_label_groups` | `service: Annotated[LabelService, Depends(get_label_service)]`, `include_inactive: bool` | - | - | `...` |
| `service.list_groups` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_label_groups | service.list_groups | 35 | `service.list_groups(include_inactive=include_inactive)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_label_groups` | `service.list_groups` | 35 |

## Behavior

This flow starts at `list_label_groups` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
