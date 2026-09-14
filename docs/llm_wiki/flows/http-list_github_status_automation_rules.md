# list_github_status_automation_rules

**Entry point:** `list_github_status_automation_rules` (`http`)
**Source:** [routers_github](../modules/routers_github.md)
**Modules touched:** [routers_github](../modules/routers_github.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_github_status_automation_rules
    participant p1 as service.list_rules
    p0-->>p1: service.list_rules
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. list_github_status_automation_rules"]
    s2["2. service.list_rules"]
    s1 -. "service.list_rules(data not statically known)" .-> s2
    click s1 "../modules/routers_github.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_github_status_automation_rules` | `service: Annotated[GitHubStatusAutomationService, Depends(get_github_status_automation_service)]` | - | - | `...` |
| `service.list_rules` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_github_status_automation_rules | service.list_rules | 58 | `service.list_rules(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_github_status_automation_rules` | `service.list_rules` | 58 |

## Behavior

This flow starts at `list_github_status_automation_rules` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
