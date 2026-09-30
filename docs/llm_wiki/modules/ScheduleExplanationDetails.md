# ScheduleExplanationDetails Module

**Path:** `frontend/src/components/gantt/ScheduleExplanationDetails.tsx`

## Description

_Auto-generated from `frontend/src/components/gantt/ScheduleExplanationDetails.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../i18n/i18n` | `i18n` |
| `../../types/gantt` | `GanttTask`, `ScheduleDecisionExplanation` |
| `../../utils/formatDate` | `formatDate` |
| `../common/Button` | `Button` |
| `clsx` | `clsx` |
| `date-fns` | `addDays`, `format`, `parseISO` |
| `lucide-react` | `AlertTriangle`, `ChevronDown`, `ChevronRight`, `ExternalLink` |
| `react` | `useState` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ScheduleExplanationDetails` |
| Constants | `t`, `DECISION_BADGE_CLASSES` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/gantt/ScheduleExplanationDetails.tsx"]
    n2["frontend/src/i18n/i18n.ts"]
    n3["frontend/src/pages/GanttPage.tsx"]
    n4["frontend/src/types/gantt.ts"]
    n5["frontend/src/utils/formatDate.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n4
    n1 --> n5
    n3 --> n0
    n3 --> n1
    n3 --> n4
    n3 --> n5
    click n0 "../modules/Button.md"
    click n1 "../modules/ScheduleExplanationDetails.md"
    click n2 "../modules/i18n.md"
    click n3 "../modules/GanttPage.md"
    click n4 "../modules/types_gantt.md"
    click n5 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GanttPage](../modules/GanttPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ScheduleExplanationDetailsProps](../entities/ScheduleExplanationDetailsProps.md) | Class | 12 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ScheduleExplanationDetails` | `({     decisions,     taskLookup,     memberVacations,     workloadBalanced,     workloadIssues,     onOpenTask, }: ScheduleExplanationDetailsProps)` | — | — |
