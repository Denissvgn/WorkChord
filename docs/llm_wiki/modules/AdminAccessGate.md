# AdminAccessGate Module

**Path:** `frontend/src/components/settings/AdminAccessGate.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/AdminAccessGate.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../hooks/useAdminAccess` | `useAdminAccess`, `useKeylessReader` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `./AdminAccessPanel` | `AdminAccessPanel` | — | compiler-dependent |
| `./sharedUnlock` | `SettingsReadOnlyContext`, `useSharedUnlock` | — | compiler-dependent |
| `lucide-react` | `LockKeyhole` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `react` | `useId`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AdminAccessGate` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/settings/AdminAccessGate.test.tsx"]
    n2["frontend/src/components/settings/AdminAccessGate.tsx"]
    n3["frontend/src/components/settings/AdminAccessPanel.tsx"]
    n4["frontend/src/components/settings/GitHubSettingsPanel.tsx"]
    n5["frontend/src/components/settings/sharedUnlock.ts"]
    n6["frontend/src/components/tasks/PipelineView.tsx"]
    n7["frontend/src/components/team/AgentManifestWorkflow.tsx"]
    n8["frontend/src/hooks/useAdminAccess.ts"]
    n9["frontend/src/pages/SettingsPage.tsx"]
    n1 --> n2
    n2 --> n0
    n2 --> n3
    n2 --> n5
    n2 --> n8
    n3 --> n0
    n3 --> n8
    n4 --> n0
    n4 --> n2
    n4 --> n5
    n6 --> n0
    n6 --> n2
    n7 --> n0
    n7 --> n2
    n9 --> n0
    n9 --> n2
    n9 --> n3
    n9 --> n4
    n9 --> n5
    n9 --> n8
    click n0 "../modules/Button.md"
    click n1 "../modules/AdminAccessGate.test.md"
    click n2 "../modules/AdminAccessGate.md"
    click n3 "../modules/AdminAccessPanel.md"
    click n4 "../modules/GitHubSettingsPanel.md"
    click n5 "../modules/sharedUnlock.md"
    click n6 "../modules/PipelineView.md"
    click n7 "../modules/AgentManifestWorkflow.md"
    click n8 "../modules/useAdminAccess.md"
    click n9 "../modules/SettingsPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AdminAccessGate.test](../modules/AdminAccessGate.test.md) |
| Inbound | [GitHubSettingsPanel](../modules/GitHubSettingsPanel.md) |
| Inbound | [PipelineView](../modules/PipelineView.md) |
| Inbound | [AgentManifestWorkflow](../modules/AgentManifestWorkflow.md) |
| Inbound | [SettingsPage](../modules/SettingsPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [AdminAccessPanel](../modules/AdminAccessPanel.md) |
| Outbound | [sharedUnlock](../modules/sharedUnlock.md) |
| Outbound | [useAdminAccess](../modules/useAdminAccess.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [AdminAccessGateProps](../entities/AdminAccessGateProps.md) | Interface | 10 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `AdminAccessGate` | <pre><code>&#40;&#123;&#10;    children&#44;&#10;    showPanel &#61; true&#44;&#10;    recovery&#44;&#10;    accessGranted&#44;&#10;    headingLevel &#61; 3&#44;&#10;    saveVariant &#61; &#39;primary&#39;&#44;&#10;    readable &#61; false&#44;&#10;    managesReadOnly &#61; false&#44;&#10;&#125;&#58; AdminAccessGateProps&#41;</code></pre> | — | — |
