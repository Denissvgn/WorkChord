# LabelSelector Module

**Path:** `frontend/src/components/labels/LabelSelector.tsx`

## Description

_Auto-generated from `frontend/src/components/labels/LabelSelector.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Select` | `Select` | — | compiler-dependent |
| `../../i18n/seedDisplay` | `labelDisplay`, `labelGroupDisplay` | — | compiler-dependent |
| `../../services/labelService` | `labelService` | — | compiler-dependent |
| `../../types/label` | `Label` | Declaration | erased |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `./LabelChip` | `LabelChip` | — | compiler-dependent |
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
    n1["frontend/src/components/common/Select.tsx"]
    n2["frontend/src/components/feedback/QueryState.tsx"]
    n3["frontend/src/components/labels/LabelChip.tsx"]
    n4["frontend/src/components/labels/LabelSelector.tsx"]
    n5["frontend/src/components/settings/TemplateLabelSettings.tsx"]
    n6["frontend/src/components/tasks/TaskForm.tsx"]
    n7["frontend/src/components/triage/ConvertTriageDrawer.tsx"]
    n8["frontend/src/components/triage/CreateTriageDrawer.tsx"]
    n9["frontend/src/i18n/seedDisplay.ts"]
    n10["frontend/src/services/labelService.ts"]
    n11["frontend/src/types/label.ts"]
    n2 --> n0
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n9
    n4 --> n10
    n4 --> n11
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n4
    n5 --> n9
    n5 --> n10
    n5 --> n11
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n4
    n6 --> n9
    n7 --> n0
    n7 --> n1
    n7 --> n2
    n7 --> n4
    n7 --> n9
    n8 --> n0
    n8 --> n1
    n8 --> n2
    n8 --> n4
    n8 --> n9
    n9 --> n11
    n10 --> n11
    click n0 "../modules/Button.md"
    click n1 "../modules/Select.md"
    click n2 "../modules/QueryState.md"
    click n3 "../modules/LabelChip.md"
    click n4 "../modules/LabelSelector.md"
    click n5 "../modules/TemplateLabelSettings.md"
    click n6 "../modules/TaskForm.md"
    click n7 "../modules/ConvertTriageDrawer.md"
    click n8 "../modules/CreateTriageDrawer.md"
    click n9 "../modules/seedDisplay.md"
    click n10 "../modules/labelService.md"
    click n11 "../modules/types_label.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TemplateLabelSettings](../modules/TemplateLabelSettings.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [ConvertTriageDrawer](../modules/ConvertTriageDrawer.md) |
| Inbound | [CreateTriageDrawer](../modules/CreateTriageDrawer.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Select](../modules/Select.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [LabelChip](../modules/LabelChip.md) |
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
| [LabelSelectorProps](../entities/LabelSelectorProps.md) | Interface | 13 | — | — |
| [LabelOption](../entities/LabelOption.md) | Type alias | 22 | <pre><code>Label &#38; &#123;&#10;    groupName&#58; string&#59;&#10;&#125;</code></pre> | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `LabelSelector` | <pre><code>&#40;&#123;&#10;    value&#44;&#10;    onChange&#44;&#10;    label&#44;&#10;    placeholder&#44;&#10;    allowCustom &#61; true&#44;&#10;    className&#44;&#10;&#125;&#58; LabelSelectorProps&#41;</code></pre> | — | — |
