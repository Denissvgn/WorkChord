# timeEntryService Module

**Path:** `frontend/src/services/timeEntryService.ts`

## Description

_Auto-generated from `frontend/src/services/timeEntryService.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./api` | `api` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TimeEntry`, `TimeFilters`, `TimePage`, `TimeReport`, `TimeRevision`, `TimeValues`, `timeAccessDenied`, `timeEntryService` |
| Constants | `timeEntryService` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/projects/TimeEntriesReport.tsx"]
    n1["frontend/src/components/tasks/TimeEntriesPanel.tsx"]
    n2["frontend/src/features/timeEntries/useTimeEntries.ts"]
    n3["frontend/src/services/api.ts"]
    n4["frontend/src/services/timeEntryService.test.ts"]
    n5["frontend/src/services/timeEntryService.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n5
    n1 --> n2
    n1 --> n5
    n2 --> n5
    n4 --> n5
    n5 --> n3
    click n0 "../modules/TimeEntriesReport.md"
    click n1 "../modules/TimeEntriesPanel.md"
    click n2 "../modules/useTimeEntries.md"
    click n3 "../modules/api.md"
    click n4 "../modules/timeEntryService.test.md"
    click n5 "../modules/timeEntryService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TimeEntriesReport](../modules/TimeEntriesReport.md) |
| Inbound | [TimeEntriesPanel](../modules/TimeEntriesPanel.md) |
| Inbound | [useTimeEntries](../modules/useTimeEntries.md) |
| Inbound | [timeEntryService.test](../modules/timeEntryService.test.md) |
| Outbound | [api](../modules/api.md) |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TimeValues](../entities/timeEntryService_TimeValues.md) | Class | 3 | — | — |
| [TimeEntry](../entities/timeEntryService_TimeEntry.md) | Class | 4 | `TimeValues` | — |
| [TimePage](../entities/TimePage.md) | Class | 8 | — | — |
| [TimeRevision](../entities/TimeRevision.md) | Class | 9 | `TimeValues` | — |
| [TimeReport](../entities/TimeReport.md) | Class | 10 | — | — |
| [TimeFilters](../entities/TimeFilters.md) | Class | 18 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `timeAccessDenied` | `(error: unknown)` | — | — |
