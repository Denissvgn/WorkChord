# list_github_status_automation_rules

**Entry point:** `list_github_status_automation_rules` (`http`)
**Source:** [routers_github](../modules/routers_github.md)
**Modules touched:** [routers_github](../modules/routers_github.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_github_status_automation_rules
    participant p1 as service.list_rules
    p0-->>p1: service.list_rules
```

> Call sequence diagram shows 1 of 1 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 0 of 0 (0 omitted); unresolved 1 of 1 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 1; effect analysis evaluated: 1, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 1 source steps with known totals: observed: 2, emitted: 2, omitted: 0. Unavailable totals are excluded.

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

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_github_status_automation_rules` | `service.list_rules` | 58 |

## Behavior

This flow starts at `list_github_status_automation_rules` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
