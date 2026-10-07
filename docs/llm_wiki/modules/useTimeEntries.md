# useTimeEntries Module

**Path:** `frontend/src/features/timeEntries/useTimeEntries.ts`

## Description

_Auto-generated from `frontend/src/features/timeEntries/useTimeEntries.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/timeEntryService` | `timeEntryService` |
| `../identity/identityContext` | `useIdentity` |
| `@tanstack/react-query` | `useQuery` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `useTimeEntries` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/projects/TimeEntriesReport.tsx"]
    n1["frontend/src/components/tasks/TimeEntriesPanel.tsx"]
    n2["frontend/src/features/identity/identityContext.ts"]
    n3["frontend/src/features/timeEntries/useTimeEntries.ts"]
    n4["frontend/src/services/timeEntryService.ts"]
    n0 --> n1
    n0 --> n3
    n0 --> n4
    n1 --> n3
    n1 --> n4
    n3 --> n2
    n3 --> n4
    click n0 "../modules/TimeEntriesReport.md"
    click n1 "../modules/TimeEntriesPanel.md"
    click n2 "../modules/identityContext.md"
    click n3 "../modules/useTimeEntries.md"
    click n4 "../modules/timeEntryService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TimeEntriesReport](../modules/TimeEntriesReport.md) |
| Inbound | [TimeEntriesPanel](../modules/TimeEntriesPanel.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [timeEntryService](../modules/timeEntryService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useTimeEntries` | `()` | — | — |
