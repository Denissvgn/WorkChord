# dateLocale Module

**Path:** `frontend/src/i18n/dateLocale.ts`

## Description

_Auto-generated from `frontend/src/i18n/dateLocale.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./i18n` | `i18n` | — | compiler-dependent |
| `date-fns` | `Locale` | Declaration | erased |
| `date-fns/locale` | `enUS`, `ru` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `dateFnsLocale`, `normalizedLanguage` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/calendar/InteractiveCalendar.tsx"]
    n1["frontend/src/components/gantt/GanttChart.tsx"]
    n2["frontend/src/components/projects/RoadmapView.tsx"]
    n3["frontend/src/components/settings/WorkCalendarSettings.tsx"]
    n4["frontend/src/i18n/dateLocale.ts"]
    n5["frontend/src/i18n/i18n.ts"]
    n6["frontend/src/utils/formatDate.ts"]
    n0 --> n4
    n1 --> n4
    n1 --> n6
    n2 --> n4
    n2 --> n6
    n3 --> n0
    n3 --> n4
    n4 --> n5
    n6 --> n4
    click n0 "../modules/InteractiveCalendar.md"
    click n1 "../modules/GanttChart.md"
    click n2 "../modules/RoadmapView.md"
    click n3 "../modules/WorkCalendarSettings.md"
    click n4 "../modules/dateLocale.md"
    click n5 "../modules/i18n.md"
    click n6 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [InteractiveCalendar](../modules/InteractiveCalendar.md) |
| Inbound | [GanttChart](../modules/GanttChart.md) |
| Inbound | [RoadmapView](../modules/RoadmapView.md) |
| Inbound | [WorkCalendarSettings](../modules/WorkCalendarSettings.md) |
| Inbound | [formatDate](../modules/formatDate.md) |
| Outbound | [i18n](../modules/i18n.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `normalizedLanguage` | `(language = i18n.language)` | — | — |
| `dateFnsLocale` | `(language = i18n.language) -> Locale` | — | — |
