# PlanningWorkflowGuide Module

**Path:** `frontend/src/components/planning/PlanningWorkflowGuide.tsx`

## Description

_Auto-generated from `frontend/src/components/planning/PlanningWorkflowGuide.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../common/Button` | `Button` | — | compiler-dependent |
| `../ui/SlideOverDrawer` | `SlideOverDrawer` | — | compiler-dependent |
| `lucide-react` | `LucideIcon` | Declaration | erased |
| `lucide-react` | `CalendarClock`, `ChevronRight`, `CircleHelp`, `FlaskConical`, `History`, `ListChecks`, `LockKeyhole`, `Share2` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PlanningWorkflowGuide`, `PlanningWorkflowHelpContent` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/layout/ContextHelp.tsx"]
    n2["frontend/src/components/planning/PlanningWorkflowGuide.test.tsx"]
    n3["frontend/src/components/planning/PlanningWorkflowGuide.tsx"]
    n4["frontend/src/components/ui/SlideOverDrawer.tsx"]
    n1 --> n3
    n2 --> n3
    n3 --> n0
    n3 --> n4
    click n0 "../modules/Button.md"
    click n1 "../modules/ContextHelp.md"
    click n2 "../modules/PlanningWorkflowGuide.test.md"
    click n3 "../modules/PlanningWorkflowGuide.md"
    click n4 "../modules/SlideOverDrawer.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ContextHelp](../modules/ContextHelp.md) |
| Inbound | [PlanningWorkflowGuide.test](../modules/PlanningWorkflowGuide.test.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [SlideOverDrawer](../modules/SlideOverDrawer.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [PlanningSurface](../entities/PlanningSurface.md) | Type alias | 18 | `'plan' \| 'gantt'` | — |
| [GuideItem](../entities/GuideItem.md) | Type alias | 20 | <pre><code>&#123;&#10;    icon&#58; LucideIcon&#59;&#10;    title&#58; string&#59;&#10;    body&#58; string&#59;&#10;&#125;</code></pre> | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `PlanningWorkflowHelpContent` | <pre><code>&#40;&#123;&#10;    surface&#44;&#10;    showAction &#61; true&#44;&#10;    onNavigate&#44;&#10;&#125;&#58; &#123;&#10;    surface&#58; PlanningSurface&#59;&#10;    showAction&#63;&#58; boolean&#59;&#10;    onNavigate&#63;&#58; &#40;&#41; &#61;&#62; void&#59;&#10;&#125;&#41;</code></pre> | — | — |
| `PlanningWorkflowGuide` | `({ surface }: { surface: PlanningSurface })` | — | — |
