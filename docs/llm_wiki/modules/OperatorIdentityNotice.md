# OperatorIdentityNotice Module

**Path:** `frontend/src/features/identity/OperatorIdentityNotice.tsx`

## Description

_Auto-generated from `frontend/src/features/identity/OperatorIdentityNotice.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Button` | `Button` | — | compiler-dependent |
| `../../utils/adminAccess` | `clearAdminApiKey` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `OperatorIdentityNotice` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/settings/AdminAccessPanel.tsx"]
    n2["frontend/src/features/identity/LocalProfilePicker.tsx"]
    n3["frontend/src/features/identity/OperatorIdentityNotice.tsx"]
    n4["frontend/src/pages/MyWorkPage.tsx"]
    n5["frontend/src/utils/adminAccess.ts"]
    n1 --> n0
    n1 --> n3
    n1 --> n5
    n2 --> n0
    n2 --> n3
    n3 --> n0
    n3 --> n5
    n4 --> n0
    n4 --> n2
    n4 --> n3
    click n0 "../modules/Button.md"
    click n1 "../modules/AdminAccessPanel.md"
    click n2 "../modules/LocalProfilePicker.md"
    click n3 "../modules/OperatorIdentityNotice.md"
    click n4 "../modules/MyWorkPage.md"
    click n5 "../modules/adminAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AdminAccessPanel](../modules/AdminAccessPanel.md) |
| Inbound | [LocalProfilePicker](../modules/LocalProfilePicker.md) |
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [adminAccess](../modules/adminAccess.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `OperatorIdentityNotice` | `()` | — | — |
