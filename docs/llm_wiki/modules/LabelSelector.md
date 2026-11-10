# LabelSelector Module

**Path:** `frontend/src/components/labels/LabelSelector.tsx`

## Description

_Auto-generated from `frontend/src/components/labels/LabelSelector.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../i18n/seedDisplay` | `labelDisplay`, `labelGroupDisplay` | — | compiler-dependent |
| `../../services/labelService` | `labelService` | — | compiler-dependent |
| `../../types/label` | `Label` | Declaration | erased |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `lucide-react` | `Plus`, `X` | — | compiler-dependent |
| `react` | `useMemo`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `LabelSelector` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/labels/LabelSelector.tsx"]
    n3["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n4["frontend/src/components/tasks/TaskForm.tsx"]
    n5["frontend/src/i18n/seedDisplay.ts"]
    n6["frontend/src/pages/TriagePage.tsx"]
    n7["frontend/src/services/labelService.ts"]
    n8["frontend/src/types/label.ts"]
    n1 --> n0
    n2 --> n0
    n2 --> n1
    n2 --> n5
    n2 --> n7
    n2 --> n8
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n5
    n3 --> n7
    n3 --> n8
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n5
    n5 --> n8
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n5
    n7 --> n8
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/LabelSelector.md"
    click n3 "../modules/TemplateLabelSettings.md"
    click n4 "../modules/TaskForm.md"
    click n5 "../modules/seedDisplay.md"
    click n6 "../modules/TriagePage.md"
    click n7 "../modules/labelService.md"
    click n8 "../modules/types_label.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [seedDisplay](../modules/seedDisplay.md) |
| Outbound | [labelService](../modules/labelService.md) |
| Outbound | [types_label](../modules/types_label.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [LabelSelectorProps](../entities/LabelSelectorProps.md) | Interface | 11 | — | — |
| [LabelOption](../entities/LabelOption.md) | Type alias | 20 | <pre><code>Label &#38; &#123;&#10;    groupName&#58; string&#59;&#10;&#125;</code></pre> | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `LabelSelector` | <pre><code>&#40;&#123;&#10;    value&#44;&#10;    onChange&#44;&#10;    label&#44;&#10;    placeholder&#44;&#10;    allowCustom &#61; true&#44;&#10;    className&#44;&#10;&#125;&#58; LabelSelectorProps&#41;</code></pre> | — | — |
