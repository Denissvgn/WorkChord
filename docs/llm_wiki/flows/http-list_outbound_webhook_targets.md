# list_outbound_webhook_targets

**Entry point:** `list_outbound_webhook_targets` (`http`)
**Source:** [outbound_webhooks](../modules/outbound_webhooks.md)
**Modules touched:** [outbound_webhooks](../modules/outbound_webhooks.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as list_outbound_webhook_targets
    participant p1 as service.list_targets
    p0-->>p1: service.list_targets
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. list_outbound_webhook_targets"]
    s2["2. service.list_targets"]
    s1 -. "service.list_targets(data not statically known)" .-> s2
    click s1 "../modules/outbound_webhooks.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `list_outbound_webhook_targets` | `service: Annotated[OutboundWebhookService, Depends(get_outbound_webhook_service)]` | - | - | `...` |
| `service.list_targets` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| list_outbound_webhook_targets | service.list_targets | 52 | `service.list_targets(data not statically known)` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `list_outbound_webhook_targets` | `service.list_targets` | 52 |

## Behavior

This flow starts at `list_outbound_webhook_targets` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
