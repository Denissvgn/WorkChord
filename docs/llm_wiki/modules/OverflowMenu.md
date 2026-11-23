# OverflowMenu Module

**Path:** `frontend/src/components/ui/OverflowMenu.tsx`

## Description

_Auto-generated from `frontend/src/components/ui/OverflowMenu.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/buttonStyles` | `ButtonSize`, `ButtonVariant` | Declaration | erased |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `MoreHorizontal` | — | compiler-dependent |
| `react` | `KeyboardEvent`, `ReactNode` | Declaration | erased |
| `react` | `useEffect`, `useId`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `OverflowMenu`, `OverflowMenuItem` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/capacity/CapacitySection.tsx"]
    n1["frontend/src/components/capacity/CapacityTable.tsx"]
    n2["frontend/src/components/common/Button.tsx"]
    n3["frontend/src/components/common/buttonStyles.ts"]
    n4["frontend/src/components/gantt/GanttChart.tsx"]
    n5["frontend/src/components/tasks/TaskBulkOperationsPanel.tsx"]
    n6["frontend/src/components/tasks/TaskRow.tsx"]
    n7["frontend/src/components/team/AgentModelAdministration.tsx"]
    n8["frontend/src/components/ui/OverflowMenu.test.tsx"]
    n9["frontend/src/components/ui/OverflowMenu.tsx"]
    n10["frontend/src/components/ui/PageLayout.tsx"]
    n11["frontend/src/pages/GanttPage.tsx"]
    n0 --> n2
    n0 --> n9
    n1 --> n9
    n2 --> n3
    n4 --> n2
    n4 --> n9
    n5 --> n2
    n5 --> n9
    n6 --> n2
    n6 --> n9
    n7 --> n2
    n7 --> n9
    n8 --> n9
    n9 --> n2
    n9 --> n3
    n10 --> n9
    n11 --> n2
    n11 --> n4
    n11 --> n9
    click n0 "../modules/CapacitySection.md"
    click n1 "../modules/CapacityTable.md"
    click n2 "../modules/Button.md"
    click n3 "../modules/buttonStyles.md"
    click n4 "../modules/GanttChart.md"
    click n5 "../modules/TaskBulkOperationsPanel.md"
    click n6 "../modules/TaskRow.md"
    click n7 "../modules/AgentModelAdministration.md"
    click n8 "../modules/OverflowMenu.test.md"
    click n9 "../modules/OverflowMenu.md"
    click n10 "../modules/PageLayout.md"
    click n11 "../modules/GanttPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [CapacitySection](../modules/CapacitySection.md) |
| Inbound | [CapacityTable](../modules/CapacityTable.md) |
| Inbound | [GanttChart](../modules/GanttChart.md) |
| Inbound | [TaskBulkOperationsPanel](../modules/TaskBulkOperationsPanel.md) |
| Inbound | [TaskRow](../modules/TaskRow.md) |
| Inbound | [AgentModelAdministration](../modules/AgentModelAdministration.md) |
| Inbound | [OverflowMenu.test](../modules/OverflowMenu.test.md) |
| Inbound | [PageLayout](../modules/PageLayout.md) |
| Inbound | [GanttPage](../modules/GanttPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [buttonStyles](../modules/buttonStyles.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [OverflowMenuItem](../entities/OverflowMenuItem.md) | Type alias | 9 | <pre><code>&#123;&#10;    label&#58; ReactNode&#59;&#10;    icon&#63;&#58; ReactNode&#59;&#10;    onSelect&#58; &#40;&#41; &#61;&#62; void&#59;&#10;    tone&#63;&#58; &#39;default&#39; &#124; &#39;danger&#39;&#59;&#10;    disabled&#63;&#58; boolean&#59;&#10;&#125;</code></pre> | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `OverflowMenu` | <pre><code>&#40;&#123;&#10;    items&#44;&#10;    label&#44;&#10;    className&#44;&#10;    alwaysMenu &#61; false&#44;&#10;    align &#61; &#39;end&#39;&#44;&#10;    trigger&#44;&#10;    triggerClassName&#44;&#10;    triggerVariant &#61; &#39;outline&#39;&#44;&#10;    triggerSize &#61; &#39;md&#39;&#44;&#10;    triggerIconOnly &#61; true&#44;&#10;&#125;&#58; &#123;&#10;    items&#58; OverflowMenuItem&#91;&#93;&#59;&#10;    label&#63;&#58; string&#59;&#10;    className&#63;&#58; string&#59;&#10;    &#47;&#42;&#42; Keep the menu button even for one item&#44; so a page header never gains a visible extra action&#46; &#42;&#47;&#10;    alwaysMenu&#63;&#58; boolean&#59;&#10;    &#47;&#42;&#42; Which edge of the button the menu lines up with&#46; &#42;&#47;&#10;    align&#63;&#58; &#39;start&#39; &#124; &#39;end&#39;&#59;&#10;    &#47;&#42;&#42; Replaces the three&#45;dot icon&#44; such as a status icon that opens its moves&#46; &#42;&#47;&#10;    trigger&#63;&#58; ReactNode&#59;&#10;    triggerClassName&#63;&#58; string&#59;&#10;    triggerVariant&#63;&#58; ButtonVariant&#59;&#10;    triggerSize&#63;&#58; ButtonSize&#59;&#10;    triggerIconOnly&#63;&#58; boolean&#59;&#10;&#125;&#41;</code></pre> | — | — |
