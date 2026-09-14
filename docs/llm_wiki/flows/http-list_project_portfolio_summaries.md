# list_project_portfolio_summaries

**Entry point:** `list_project_portfolio_summaries` (`http`)
**Source:** [projects](../modules/projects.md)
**Modules touched:** [projects](../modules/projects.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_project_portfolio_summaries
    participant p1 as service.list_portfolio_summaries
    p0-->>p1: service.list_portfolio_summaries
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. list_project_portfolio_summaries"]
    s2["2. service.list_portfolio_summaries"]
    s1 -. "service.list_portfolio_summaries(data not statically known)" .-> s2
    click s1 "../modules/projects.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_project_portfolio_summaries` | `service: Annotated[ProjectService, Depends(get_project_service)]` | - | - | `...` |
| `service.list_portfolio_summaries` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_project_portfolio_summaries | service.list_portfolio_summaries | 102 | `service.list_portfolio_summaries(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_project_portfolio_summaries` | `service.list_portfolio_summaries` | 102 |

## Behavior

This flow starts at `list_project_portfolio_summaries` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
