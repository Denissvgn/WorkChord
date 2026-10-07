# list_initiatives

**Entry point:** `list_initiatives` (`http`)
**Source:** [projects](../modules/projects.md)
**Modules touched:** [projects](../modules/projects.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_initiatives
    participant p1 as service.list_initiatives
    p0-->>p1: service.list_initiatives
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. list_initiatives"]
    s2["2. service.list_initiatives"]
    s1 -. "service.list_initiatives(data not statically known)" .-> s2
    click s1 "../modules/projects.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_initiatives` | `service: Annotated[ProjectService, Depends(get_project_service)]` | - | - | `...` |
| `service.list_initiatives` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_initiatives | service.list_initiatives | 139 | `service.list_initiatives(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_initiatives` | `service.list_initiatives` | 139 |

## Behavior

This flow starts at `list_initiatives` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
