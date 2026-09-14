# dateLocale Module

**Path:** `frontend/src/i18n/dateLocale.ts`

## Description

_Auto-generated from `frontend/src/i18n/dateLocale.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./i18n` | `i18n` |
| `date-fns` | `Locale` |
| `date-fns/locale` | `enUS`, `ru` |

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
    n2["frontend/src/i18n/dateLocale.ts"]
    n3["frontend/src/i18n/i18n.ts"]
    n4["frontend/src/pages/CalendarPage.tsx"]
    n5["frontend/src/pages/RoadmapPage.tsx"]
    n6["frontend/src/utils/formatDate.ts"]
    n0 --> n2
    n1 --> n2
    n1 --> n6
    n2 --> n3
    n4 --> n0
    n4 --> n2
    n5 --> n2
    n5 --> n3
    n5 --> n6
    n6 --> n2
    click n0 "../modules/InteractiveCalendar.md"
    click n1 "../modules/GanttChart.md"
    click n2 "../modules/dateLocale.md"
    click n3 "../modules/i18n.md"
    click n4 "../modules/CalendarPage.md"
    click n5 "../modules/RoadmapPage.md"
    click n6 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [InteractiveCalendar](../modules/InteractiveCalendar.md) |
| Inbound | [GanttChart](../modules/GanttChart.md) |
| Inbound | [CalendarPage](../modules/CalendarPage.md) |
| Inbound | [RoadmapPage](../modules/RoadmapPage.md) |
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
