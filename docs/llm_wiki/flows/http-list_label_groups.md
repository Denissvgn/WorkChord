# list_label_groups

**Entry point:** `list_label_groups` (`http`)
**Source:** [labels](../modules/labels.md)
**Modules touched:** [labels](../modules/labels.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_label_groups
    participant p1 as service.list_groups
    p0-->>p1: service.list_groups
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_label_groups` | `service.list_groups` | 35 |

## Behavior

This flow starts at `list_label_groups` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
