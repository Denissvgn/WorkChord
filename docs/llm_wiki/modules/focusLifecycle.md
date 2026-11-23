# focusLifecycle Module

**Path:** `frontend/src/utils/focusLifecycle.ts`

## Description

_Auto-generated from `frontend/src/utils/focusLifecycle.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `captureFocusOrigin`, `focusOwnedTarget` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/team/AgentManifestWorkflow.tsx"]
    n1["frontend/src/utils/focusLifecycle.test.ts"]
    n2["frontend/src/utils/focusLifecycle.ts"]
    n0 --> n2
    n1 --> n2
    click n0 "../modules/AgentManifestWorkflow.md"
    click n1 "../modules/focusLifecycle.test.md"
    click n2 "../modules/focusLifecycle.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AgentManifestWorkflow](../modules/AgentManifestWorkflow.md) |
| Inbound | [focusLifecycle.test](../modules/focusLifecycle.test.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `captureFocusOrigin` | `() -> HTMLElement \| null` | — | — |
| `focusOwnedTarget` | `(origin: HTMLElement \| null, target: HTMLElement \| null) -> boolean` | — | — |
