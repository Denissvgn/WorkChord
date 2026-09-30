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
    n0["frontend/src/pages/AgentTeamSetupMasterPage.tsx"]
    n1["frontend/src/pages/PlanMasterPage.tsx"]
    n2["frontend/src/utils/focusLifecycle.test.ts"]
    n3["frontend/src/utils/focusLifecycle.ts"]
    n0 --> n3
    n1 --> n3
    n2 --> n3
    click n0 "../modules/AgentTeamSetupMasterPage.md"
    click n1 "../modules/PlanMasterPage.md"
    click n2 "../modules/focusLifecycle.test.md"
    click n3 "../modules/focusLifecycle.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AgentTeamSetupMasterPage](../modules/AgentTeamSetupMasterPage.md) |
| Inbound | [PlanMasterPage](../modules/PlanMasterPage.md) |
| Inbound | [focusLifecycle.test](../modules/focusLifecycle.test.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `captureFocusOrigin` | `() -> HTMLElement \| null` | — | — |
| `focusOwnedTarget` | `(origin: HTMLElement \| null, target: HTMLElement \| null) -> boolean` | — | — |
