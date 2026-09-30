# AdminAccessPanel Module

**Path:** `frontend/src/components/settings/AdminAccessPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/AdminAccessPanel.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../hooks/useAdminAccess` | `useAdminAccess` |
| `../../utils/adminAccess` | `clearAdminApiKey`, `setAdminApiKey` |
| `../common/Button` | `Button` |
| `../common/Input` | `Input` |
| `@tanstack/react-query` | `useQueryClient` |
| `lucide-react` | `KeyRound`, `ShieldCheck`, `Trash2` |
| `react` | `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AdminAccessPanel` |
| Constants | `protectedQueryKeys` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Input.tsx"]
    n2["frontend/src/components/settings/AdminAccessGate.tsx"]
    n3["frontend/src/components/settings/AdminAccessPanel.test.tsx"]
    n4["frontend/src/components/settings/AdminAccessPanel.tsx"]
    n5["frontend/src/hooks/useAdminAccess.ts"]
    n6["frontend/src/pages/SettingsPage.tsx"]
    n7["frontend/src/utils/adminAccess.ts"]
    n2 --> n4
    n2 --> n5
    n3 --> n4
    n4 --> n0
    n4 --> n1
    n4 --> n5
    n4 --> n7
    n5 --> n7
    n6 --> n2
    n6 --> n4
    n6 --> n5
    click n0 "../modules/Button.md"
    click n1 "../modules/Input.md"
    click n2 "../modules/AdminAccessGate.md"
    click n3 "../modules/AdminAccessPanel.test.md"
    click n4 "../modules/AdminAccessPanel.md"
    click n5 "../modules/useAdminAccess.md"
    click n6 "../modules/SettingsPage.md"
    click n7 "../modules/adminAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AdminAccessGate](../modules/AdminAccessGate.md) |
| Inbound | [AdminAccessPanel.test](../modules/AdminAccessPanel.test.md) |
| Inbound | [SettingsPage](../modules/SettingsPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Input](../modules/Input.md) |
| Outbound | [useAdminAccess](../modules/useAdminAccess.md) |
| Outbound | [adminAccess](../modules/adminAccess.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `AdminAccessPanel` | `({     headingLevel = 2, }: {     headingLevel?: 2 \| 3; })` | — | — |
