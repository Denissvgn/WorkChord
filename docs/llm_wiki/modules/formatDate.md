# formatDate Module

**Path:** `frontend/src/utils/formatDate.ts`

## Description

_Auto-generated from `frontend/src/utils/formatDate.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../i18n/dateLocale` | `dateFnsLocale` |
| `date-fns` | `format`, `isValid`, `parseISO` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `DateInput`, `EMPTY_DATE`, `formatDate`, `formatDateTime` |
| Constants | `EMPTY_DATE`, `DATE_ONLY` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/utils/formatDate.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/formatDate.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (28) |
| Outbound | `frontend` (1) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

> All 29 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [DateInput](../entities/DateInput.md) | Type alias | 4 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `formatDate` | `(value: DateInput, language: string) -> string` | — | Format a date using the active application language. |
| `formatDateTime` | `(value: DateInput, language: string) -> string` | — | Format an instant in UTC using the active application language. Date-only |
