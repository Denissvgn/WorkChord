# get_project_page

**Entry point:** `get_project_page` (`http`)
**Source:** [projects](../modules/projects.md)
**Modules touched:** [projects](../modules/projects.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_project_page
    participant p1 as service.project_page
    p0-->>p1: service.project_page
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_project_page"]
    s2["2. service.project_page"]
    s1 -. "service.project_page(limit=limit, after_id=after_id, upper_id=upper_id)" .-> s2
    click s1 "../modules/projects.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_project_page` | `service: Annotated[ProjectService, Depends(get_project_service)]`, `limit: int`, `after_id: int`, `upper_id: int \| None` | - | - | `...` |
| `service.project_page` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_project_page | service.project_page | 98 | `service.project_page(limit=limit, after_id=after_id, upper_id=upper_id)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_project_page` | `service.project_page` | 98 |

## Behavior

This flow starts at `get_project_page` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
