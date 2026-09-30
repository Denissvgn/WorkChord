# AdminAccessGate Module

**Path:** `frontend/src/components/settings/AdminAccessGate.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/AdminAccessGate.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../hooks/useAdminAccess` | `useAdminAccess` |
| `./AdminAccessPanel` | `AdminAccessPanel` |
| `lucide-react` | `LockKeyhole` |
| `react` | `ReactNode` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AdminAccessGate` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/settings/AdminAccessGate.tsx"]
    n1["frontend/src/components/settings/AdminAccessPanel.tsx"]
    n2["frontend/src/hooks/useAdminAccess.ts"]
    n3["frontend/src/pages/AgentPipelinePage.tsx"]
    n4["frontend/src/pages/AgentTeamSetupMasterPage.tsx"]
    n5["frontend/src/pages/SettingsPage.tsx"]
    n0 --> n1
    n0 --> n2
    n1 --> n2
    n3 --> n0
    n3 --> n2
    n4 --> n0
    n5 --> n0
    n5 --> n1
    n5 --> n2
    click n0 "../modules/AdminAccessGate.md"
    click n1 "../modules/AdminAccessPanel.md"
    click n2 "../modules/useAdminAccess.md"
    click n3 "../modules/AgentPipelinePage.md"
    click n4 "../modules/AgentTeamSetupMasterPage.md"
    click n5 "../modules/SettingsPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AgentPipelinePage](../modules/AgentPipelinePage.md) |
| Inbound | [AgentTeamSetupMasterPage](../modules/AgentTeamSetupMasterPage.md) |
| Inbound | [SettingsPage](../modules/SettingsPage.md) |
| Outbound | [AdminAccessPanel](../modules/AdminAccessPanel.md) |
| Outbound | [useAdminAccess](../modules/useAdminAccess.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [AdminAccessGateProps](../entities/AdminAccessGateProps.md) | Class | 7 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `AdminAccessGate` | `({     children,     showPanel = true,     recovery,     accessGranted,     headingLevel = 3, }: AdminAccessGateProps)` | — | — |
