# adminAccessService Module

**Path:** `frontend/src/services/adminAccessService.ts`

## Description

_Auto-generated from `frontend/src/services/adminAccessService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./api` | `api` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `verifyAdminApiKey` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/AdminAccessPanel.tsx"]
    n1["frontend/src/features/identity/AccountMenu.tsx"]
    n2["frontend/src/services/adminAccessService.ts"]
    n3["frontend/src/services/api.ts"]
    n0 --> n2
    n1 --> n2
    n1 --> n3
    n2 --> n3
    click n0 "../modules/AdminAccessPanel.md"
    click n1 "../modules/AccountMenu.md"
    click n2 "../modules/adminAccessService.md"
    click n3 "../modules/api.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AdminAccessPanel](../modules/AdminAccessPanel.md) |
| Inbound | [AccountMenu](../modules/AccountMenu.md) |
| Outbound | [api](../modules/api.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `verifyAdminApiKey` | *(async)* `(key: string)` | — | Check a candidate key without changing the credential stored in this tab. |
