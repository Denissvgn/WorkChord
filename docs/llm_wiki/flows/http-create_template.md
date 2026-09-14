# create_template

**Entry point:** `create_template` (`http`)
**Source:** [templates](../modules/templates.md)
**Modules touched:** [templates](../modules/templates.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as create_template
    participant p1 as service.create
    p0-->>p1: service.create
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. create_template"]
    s2["2. service.create"]
    s1 -. "service.create(data)" .-> s2
    click s1 "../modules/templates.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `create_template` | `data: WorkTemplateCreate`, `service: Annotated[TemplateService, Depends(get_template_service)]` | - | - | `...` |
| `service.create` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| create_template | service.create | 50 | `service.create(data)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `create_template` | `service.create` | 50 |

## Behavior

This flow starts at `create_template` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
