# identityService Module

**Path:** `frontend/src/features/identity/identityService.ts`

## Description

_Auto-generated from `frontend/src/features/identity/identityService.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../services/api` | `api` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AccountSession`, `WorkProfile`, `WorkspaceIdentity`, `identityService` |
| Constants | `identityService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/settings/AdminAccessGate.test.tsx"]
    n1["frontend/src/components/settings/ConnectedReadersPanel.test.tsx"]
    n2["frontend/src/components/settings/ConnectedReadersPanel.tsx"]
    n3["frontend/src/features/identity/identityContext.ts"]
    n4["frontend/src/features/identity/IdentityProvider.tsx"]
    n5["frontend/src/features/identity/identityService.ts"]
    n6["frontend/src/features/identity/LocalProfilePicker.tsx"]
    n7["frontend/src/services/api.ts"]
    n0 --> n3
    n0 --> n5
    n1 --> n2
    n1 --> n3
    n1 --> n5
    n2 --> n3
    n2 --> n5
    n3 --> n5
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n4 --> n7
    n5 --> n7
    n6 --> n5
    click n0 "../modules/AdminAccessGate.test.md"
    click n1 "../modules/ConnectedReadersPanel.test.md"
    click n2 "../modules/ConnectedReadersPanel.md"
    click n3 "../modules/identityContext.md"
    click n4 "../modules/IdentityProvider.md"
    click n5 "../modules/identityService.md"
    click n6 "../modules/LocalProfilePicker.md"
    click n7 "../modules/api.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AdminAccessGate.test](../modules/AdminAccessGate.test.md) |
| Inbound | [ConnectedReadersPanel.test](../modules/ConnectedReadersPanel.test.md) |
| Inbound | [ConnectedReadersPanel](../modules/ConnectedReadersPanel.md) |
| Inbound | [identityContext](../modules/identityContext.md) |
| Inbound | [IdentityProvider](../modules/IdentityProvider.md) |
| Inbound | [LocalProfilePicker](../modules/LocalProfilePicker.md) |
| Outbound | [api](../modules/api.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [WorkProfile](../entities/WorkProfile.md) | Interface | 4 | — | A linked profile is verified; a trusted-local session's own choice is not. |
| [WorkspaceIdentity](../entities/WorkspaceIdentity.md) | Interface | 6 | — | — |
| [AccountSession](../entities/AccountSession.md) | Interface | 24 | — | One session of this account, or on a trusted-local server, one paired reader. |
