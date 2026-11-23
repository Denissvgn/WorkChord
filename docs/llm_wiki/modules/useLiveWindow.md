# useLiveWindow Module

**Path:** `frontend/src/features/useLiveWindow.ts`

## Description

Live paged work retains four pages with one separate foreground head-discovery read. Cursor progress and upper bounds are validated; missing or cyclic continuations fail visibly. Duplicate rows resolve to the highest observed version. Retired windows expose explicit latest-window navigation without replacing selected task state or editor drafts. Reset opens a fresh query generation rather than replaying an obsolete cursor.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `@tanstack/react-query` | `InfiniteData`, `QueryKey`, `UseInfiniteQueryOptions` | Specifier | compiler-dependent |
| `@tanstack/react-query` | `useInfiniteQuery`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `deduplicateWindow`, `useLiveWindow`, `validateWindowCursor` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/projects/RoadmapView.tsx"]
    n1["frontend/src/components/projects/TimeEntriesReport.tsx"]
    n2["frontend/src/components/tasks/BacklogPanel.tsx"]
    n3["frontend/src/components/tasks/PagedTaskBrowser.tsx"]
    n4["frontend/src/components/tasks/TaskDiscussion.tsx"]
    n5["frontend/src/components/tasks/TimeEntriesPanel.tsx"]
    n6["frontend/src/features/useLiveWindow.test.tsx"]
    n7["frontend/src/features/useLiveWindow.ts"]
    n8["frontend/src/pages/MyWorkPage.tsx"]
    n0 --> n7
    n1 --> n5
    n1 --> n7
    n2 --> n7
    n3 --> n7
    n4 --> n7
    n5 --> n7
    n6 --> n7
    n8 --> n7
    click n0 "../modules/RoadmapView.md"
    click n1 "../modules/TimeEntriesReport.md"
    click n2 "../modules/BacklogPanel.md"
    click n3 "../modules/PagedTaskBrowser.md"
    click n4 "../modules/TaskDiscussion.md"
    click n5 "../modules/TimeEntriesPanel.md"
    click n6 "../modules/useLiveWindow.test.md"
    click n7 "../modules/useLiveWindow.md"
    click n8 "../modules/MyWorkPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [RoadmapView](../modules/RoadmapView.md) |
| Inbound | [TimeEntriesReport](../modules/TimeEntriesReport.md) |
| Inbound | [BacklogPanel](../modules/BacklogPanel.md) |
| Inbound | [PagedTaskBrowser](../modules/PagedTaskBrowser.md) |
| Inbound | [TaskDiscussion](../modules/TaskDiscussion.md) |
| Inbound | [TimeEntriesPanel](../modules/TimeEntriesPanel.md) |
| Inbound | [useLiveWindow.test](../modules/useLiveWindow.test.md) |
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useLiveWindow` | `<T, P>(options: UseInfiniteQueryOptions<T, Error, InfiniteData<T, P>, QueryKey, P>)` | — | — |
| `validateWindowCursor` | `(page: unknown, current: unknown, next: unknown)` | — | — |
| `deduplicateWindow` | `<T, P>(data: InfiniteData<T, P>) -> InfiniteData<T, P>` | — | — |