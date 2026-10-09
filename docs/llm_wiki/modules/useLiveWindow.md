# useLiveWindow Module

**Path:** `frontend/src/features/useLiveWindow.ts`

## Description

Live paged work retains four pages with one separate foreground head-discovery read. Cursor progress and upper bounds are validated; missing or cyclic continuations fail visibly. Duplicate rows resolve to the highest observed version. Retired windows expose explicit latest-window navigation without replacing selected task state or editor drafts. Reset opens a fresh query generation rather than replaying an obsolete cursor.

## Imports

| Source | Symbols |
|--------|---------|
| `@tanstack/react-query` | `useInfiniteQuery`, `useQuery`, `useQueryClient`, `InfiniteData`, `QueryKey`, `UseInfiniteQueryOptions` |
| `react` | `useState` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `deduplicateWindow`, `useLiveWindow`, `validateWindowCursor` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/projects/TimeEntriesReport.tsx"]
    n1["frontend/src/components/tasks/BacklogPanel.tsx"]
    n2["frontend/src/components/tasks/PagedTaskBrowser.tsx"]
    n3["frontend/src/components/tasks/TaskDiscussion.tsx"]
    n4["frontend/src/components/tasks/TimeEntriesPanel.tsx"]
    n5["frontend/src/features/useLiveWindow.test.tsx"]
    n6["frontend/src/features/useLiveWindow.ts"]
    n7["frontend/src/pages/MyWorkPage.tsx"]
    n8["frontend/src/pages/RoadmapPage.tsx"]
    n0 --> n4
    n0 --> n6
    n1 --> n6
    n2 --> n6
    n3 --> n6
    n4 --> n6
    n5 --> n6
    n7 --> n6
    n8 --> n6
    click n0 "../modules/TimeEntriesReport.md"
    click n1 "../modules/BacklogPanel.md"
    click n2 "../modules/PagedTaskBrowser.md"
    click n3 "../modules/TaskDiscussion.md"
    click n4 "../modules/TimeEntriesPanel.md"
    click n5 "../modules/useLiveWindow.test.md"
    click n6 "../modules/useLiveWindow.md"
    click n7 "../modules/MyWorkPage.md"
    click n8 "../modules/RoadmapPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TimeEntriesReport](../modules/TimeEntriesReport.md) |
| Inbound | [BacklogPanel](../modules/BacklogPanel.md) |
| Inbound | [PagedTaskBrowser](../modules/PagedTaskBrowser.md) |
| Inbound | [TaskDiscussion](../modules/TaskDiscussion.md) |
| Inbound | [TimeEntriesPanel](../modules/TimeEntriesPanel.md) |
| Inbound | [useLiveWindow.test](../modules/useLiveWindow.test.md) |
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |
| Inbound | [RoadmapPage](../modules/RoadmapPage.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useLiveWindow` | `(options: UseInfiniteQueryOptions<T, Error, InfiniteData<T, P>, QueryKey, P>)` | — | — |
| `validateWindowCursor` | `(page: unknown, current: unknown, next: unknown)` | — | — |
| `deduplicateWindow` | `(data: InfiniteData<T, P>) -> InfiniteData<T, P>` | — | — |
