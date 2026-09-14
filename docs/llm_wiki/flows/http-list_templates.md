# list_templates

**Entry point:** `list_templates` (`http`)
**Source:** [templates](../modules/templates.md)
**Modules touched:** [templates](../modules/templates.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_templates
    participant p1 as service.list_templates
    p0-->>p1: service.list_templates
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. list_templates"]
    s2["2. service.list_templates"]
    s1 -. "service.list_templates(template_type=template_type, include_inactive=include_inactive)" .-> s2
    click s1 "../modules/templates.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_templates` | `service: Annotated[TemplateService, Depends(get_template_service)]`, `template_type: Annotated[Optional[TemplateType], Query()]`, `include_inactive: bool` | - | - | `...` |
| `service.list_templates` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_templates | service.list_templates | 34 | `service.list_templates(template_type=template_type, include_inactive=include_inactive)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_templates` | `service.list_templates` | 34 |

## Behavior

This flow starts at `list_templates` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
