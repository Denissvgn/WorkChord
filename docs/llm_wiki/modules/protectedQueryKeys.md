# protectedQueryKeys Module

**Path:** `frontend/src/components/settings/protectedQueryKeys.ts`

## Description

/** Query keys whose data needs the admin key: they are dropped on unlock and lock, and refetched after an unlock. */

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `protectedQueryKeys` |
| Constants | `protectedQueryKeys` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/AdminAccessPanel.test.tsx"]
    n1["frontend/src/components/settings/AdminAccessPanel.tsx"]
    n2["frontend/src/components/settings/protectedQueryKeys.ts"]
    n3["frontend/src/features/identity/AccountMenu.tsx"]
    n0 --> n1
    n0 --> n2
    n1 --> n2
    n3 --> n2
    click n0 "../modules/AdminAccessPanel.test.md"
    click n1 "../modules/AdminAccessPanel.md"
    click n2 "../modules/protectedQueryKeys.md"
    click n3 "../modules/AccountMenu.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AdminAccessPanel.test](../modules/AdminAccessPanel.test.md) |
| Inbound | [AdminAccessPanel](../modules/AdminAccessPanel.md) |
| Inbound | [AccountMenu](../modules/AccountMenu.md) |
