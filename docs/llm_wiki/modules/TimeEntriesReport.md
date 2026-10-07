# TimeEntriesReport Module

**Path:** `frontend/src/components/projects/TimeEntriesReport.tsx`

## Description

_Auto-generated from `frontend/src/components/projects/TimeEntriesReport.tsx`._

Project reports expose work-date filters, own versus authorized manager totals, recorded coverage and current hour estimates. Unknown values remain distinct from zero. Personal entry controls inherit the same date range; exported totals never reveal another author's notes. Capability, read and export failures provide localized recovery and withhold cached private contents. Existing design primitives and responsive grids preserve the task/project interface.

## Imports

| Source | Symbols |
|--------|---------|
| `../../features/timeEntries/useTimeEntries` | `useTimeEntries` |
| `../../services/timeEntryService` | `timeEntryService`, `timeAccessDenied` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../common/Button` | `Button` |
| `../common/CollapsibleSection` | `CollapsibleSection` |
| `../common/Input` | `Input` |
| `../feedback/QueryState` | `QueryErrorState` |
| `../tasks/TimeEntriesPanel` | `TimeEntriesPanel` |
| `@tanstack/react-query` | `useInfiniteQuery`, `useMutation` |
| `date-fns` | `format`, `startOfMonth` |
| `react` | `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TimeEntriesReport` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/CollapsibleSection.tsx"]
    n2["frontend/src/components/common/Input.tsx"]
    n3["frontend/src/components/feedback/QueryState.tsx"]
    n4["frontend/src/components/projects/TimeEntriesReport.test.tsx"]
    n5["frontend/src/components/projects/TimeEntriesReport.tsx"]
    n6["frontend/src/components/tasks/TimeEntriesPanel.tsx"]
    n7["frontend/src/features/timeEntries/useTimeEntries.ts"]
    n8["frontend/src/pages/ProjectDetailPage.tsx"]
    n9["frontend/src/services/timeEntryService.ts"]
    n10["frontend/src/utils/apiError.ts"]
    n3 --> n0
    n3 --> n10
    n4 --> n5
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n6
    n5 --> n7
    n5 --> n9
    n5 --> n10
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n7
    n6 --> n9
    n6 --> n10
    n7 --> n9
    n8 --> n0
    n8 --> n2
    n8 --> n3
    n8 --> n5
    n8 --> n10
    click n0 "../modules/Button.md"
    click n1 "../modules/CollapsibleSection.md"
    click n2 "../modules/Input.md"
    click n3 "../modules/QueryState.md"
    click n4 "../modules/TimeEntriesReport.test.md"
    click n5 "../modules/TimeEntriesReport.md"
    click n6 "../modules/TimeEntriesPanel.md"
    click n7 "../modules/useTimeEntries.md"
    click n8 "../modules/ProjectDetailPage.md"
    click n9 "../modules/timeEntryService.md"
    click n10 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TimeEntriesReport.test](../modules/TimeEntriesReport.test.md) |
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [CollapsibleSection](../modules/CollapsibleSection.md) |
| Outbound | [Input](../modules/Input.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [TimeEntriesPanel](../modules/TimeEntriesPanel.md) |
| Outbound | [useTimeEntries](../modules/useTimeEntries.md) |
| Outbound | [timeEntryService](../modules/timeEntryService.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TimeEntriesReport` | `({ projectId }: { projectId: number })` | — | — |
