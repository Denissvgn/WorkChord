# TaskWorkflowGuide Module

**Path:** `frontend/src/components/tasks/TaskWorkflowGuide.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskWorkflowGuide.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../common/Button` | `Button` | — | compiler-dependent |
| `../ui/SlideOverDrawer` | `SlideOverDrawer` | — | compiler-dependent |
| `lucide-react` | `Bot`, `CalendarRange`, `CheckCircle2`, `ChevronRight`, `CircleHelp`, `UserRoundCheck` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskWorkflowGuide`, `TaskWorkflowHelpContent` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/layout/ContextHelp.tsx"]
    n2["frontend/src/components/tasks/TaskWorkflowGuide.tsx"]
    n3["frontend/src/components/ui/SlideOverDrawer.tsx"]
    n1 --> n2
    n2 --> n0
    n2 --> n3
    click n0 "../modules/Button.md"
    click n1 "../modules/ContextHelp.md"
    click n2 "../modules/TaskWorkflowGuide.md"
    click n3 "../modules/SlideOverDrawer.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ContextHelp](../modules/ContextHelp.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [SlideOverDrawer](../modules/SlideOverDrawer.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskWorkflowHelpContent` | <pre><code>&#40;&#123;&#10;    showAction &#61; true&#44;&#10;    onNavigate&#44;&#10;&#125;&#58; &#123;&#10;    showAction&#63;&#58; boolean&#59;&#10;    onNavigate&#63;&#58; &#40;&#41; &#61;&#62; void&#59;&#10;&#125;&#41;</code></pre> | — | — |
| `TaskWorkflowGuide` | `()` | — | — |
