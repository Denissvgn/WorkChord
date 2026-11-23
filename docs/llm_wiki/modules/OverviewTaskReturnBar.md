# OverviewTaskReturnBar Module

**Path:** `frontend/src/components/overview/OverviewTaskReturnBar.tsx`

## Description

_Auto-generated from `frontend/src/components/overview/OverviewTaskReturnBar.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/overview/overviewTaskThread` | `overviewTaskReturnFocusId` | — | compiler-dependent |
| `../../features/scope/useScopeLink` | `useScopeLink` | — | compiler-dependent |
| `../common/ButtonLink` | `ButtonLink` | — | compiler-dependent |
| `lucide-react` | `ArrowLeft`, `Waypoints` | — | compiler-dependent |
| `react` | `RefObject` | Declaration | erased |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `OverviewTaskReturnBar` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/ButtonLink.tsx"]
    n1["frontend/src/components/overview/OverviewTaskReturnBar.tsx"]
    n2["frontend/src/features/overview/overviewTaskThread.ts"]
    n3["frontend/src/features/scope/useScopeLink.ts"]
    n4["frontend/src/pages/TasksPage.tsx"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    click n0 "../modules/ButtonLink.md"
    click n1 "../modules/OverviewTaskReturnBar.md"
    click n2 "../modules/overviewTaskThread.md"
    click n3 "../modules/useScopeLink.md"
    click n4 "../modules/TasksPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [ButtonLink](../modules/ButtonLink.md) |
| Outbound | [overviewTaskThread](../modules/overviewTaskThread.md) |
| Outbound | [useScopeLink](../modules/useScopeLink.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `OverviewTaskReturnBar` | <pre><code>&#40;&#123;&#10;    active&#44;&#10;    taskId&#44;&#10;    taskTitle&#44;&#10;    returnActionRef&#44;&#10;&#125;&#58; &#123;&#10;    active&#58; boolean&#59;&#10;    taskId&#58; number &#124; null&#59;&#10;    taskTitle&#63;&#58; string &#124; null&#59;&#10;    returnActionRef&#63;&#58; RefObject&#60;HTMLAnchorElement &#124; null&#62;&#59;&#10;&#125;&#41;</code></pre> | — | — |
