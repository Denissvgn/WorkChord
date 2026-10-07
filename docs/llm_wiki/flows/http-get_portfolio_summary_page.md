# get_portfolio_summary_page

**Entry point:** `get_portfolio_summary_page` (`http`)
**Source:** [projects](../modules/projects.md)
**Modules touched:** [projects](../modules/projects.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as get_portfolio_summary_page
    participant p1 as service.portfolio_page
    p0-->>p1: service.portfolio_page
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. get_portfolio_summary_page"]
    s2["2. service.portfolio_page"]
    s1 -. "service.portfolio_page(limit=limit, after_id=after_id, upper_id=upper_id)" .-> s2
    click s1 "../modules/projects.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `get_portfolio_summary_page` | `service: Annotated[ProjectService, Depends(get_project_service)]`, `limit: int`, `after_id: int`, `upper_id: int \| None` | - | - | `...` |
| `service.portfolio_page` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| get_portfolio_summary_page | service.portfolio_page | 91 | `service.portfolio_page(limit=limit, after_id=after_id, upper_id=upper_id)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `get_portfolio_summary_page` | `service.portfolio_page` | 91 |

## Behavior

This flow starts at `get_portfolio_summary_page` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
