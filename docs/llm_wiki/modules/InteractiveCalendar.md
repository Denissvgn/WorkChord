# InteractiveCalendar Module

**Path:** `frontend/src/components/calendar/InteractiveCalendar.tsx`

## Description

_Auto-generated from `frontend/src/components/calendar/InteractiveCalendar.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Button` | `Button` | — | compiler-dependent |
| `../../components/common/Select` | `Select` | — | compiler-dependent |
| `../../i18n/dateLocale` | `dateFnsLocale` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `date-fns` | `format`, `startOfMonth`, `endOfMonth`, `eachDayOfInterval`, `getDay` | — | compiler-dependent |
| `lucide-react` | `ChevronLeft`, `ChevronRight` | — | compiler-dependent |
| `react` | `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `CalendarPeriodNavigator`, `InteractiveCalendar` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/calendar/InteractiveCalendar.test.tsx"]
    n1["frontend/src/components/calendar/InteractiveCalendar.tsx"]
    n2["frontend/src/components/common/Button.tsx"]
    n3["frontend/src/components/common/Select.tsx"]
    n4["frontend/src/components/settings/WorkCalendarSettings.tsx"]
    n5["frontend/src/i18n/dateLocale.ts"]
    n0 --> n1
    n0 --> n4
    n1 --> n2
    n1 --> n3
    n1 --> n5
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n5
    click n0 "../modules/InteractiveCalendar.test.md"
    click n1 "../modules/InteractiveCalendar.md"
    click n2 "../modules/Button.md"
    click n3 "../modules/Select.md"
    click n4 "../modules/WorkCalendarSettings.md"
    click n5 "../modules/dateLocale.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [InteractiveCalendar.test](../modules/InteractiveCalendar.test.md) |
| Inbound | [WorkCalendarSettings](../modules/WorkCalendarSettings.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Select](../modules/Select.md) |
| Outbound | [dateLocale](../modules/dateLocale.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [CalendarPeriodNavigatorProps](../entities/CalendarPeriodNavigatorProps.md) | Interface | 13 | — | — |
| [InteractiveCalendarProps](../entities/InteractiveCalendarProps.md) | Interface | 23 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `CalendarPeriodNavigator` | <pre><code>&#40;&#123;&#10;    year&#44;&#10;    month&#44;&#10;    holidays&#44;&#10;    weekendDays&#44;&#10;    onYearChange&#44;&#10;    onMonthChange&#44;&#10;    className&#44;&#10;&#125;&#58; CalendarPeriodNavigatorProps&#41;</code></pre> | — | — |
| `InteractiveCalendar` | <pre><code>&#40;&#123;&#10;    year&#44;&#10;    month&#44;&#10;    holidays&#44;&#10;    shortDays&#44;&#10;    weekendDays&#44;&#10;    onYearChange&#44;&#10;    onMonthChange&#44;&#10;    onAddHoliday&#44;&#10;    onRemoveHoliday&#44;&#10;    onAddShortDay&#44;&#10;    onRemoveShortDay&#10;&#125;&#58; InteractiveCalendarProps&#41;</code></pre> | — | — |
