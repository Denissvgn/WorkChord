# claimTime Module

**Path:** `frontend/src/components/tasks/KanbanBoard/claimTime.ts`

## Description

/** "18:42" for a claim that ends today, a short date and time otherwise, in the reader's time zone. */

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `formatClaimUntil` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/KanbanBoard/claimTime.ts"]
    n1["frontend/src/components/tasks/KanbanBoard/KanbanCard.tsx"]
    n2["frontend/src/components/tasks/KanbanBoard/KanbanColumn.test.tsx"]
    n1 --> n0
    n2 --> n0
    n2 --> n1
    click n0 "../modules/claimTime.md"
    click n1 "../modules/KanbanCard.md"
    click n2 "../modules/KanbanColumn.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [KanbanCard](../modules/KanbanCard.md) |
| Inbound | [KanbanColumn.test](../modules/KanbanColumn.test.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `formatClaimUntil` | `(value: string, locale: string, now = new Date())` | — | "18:42" for a claim that ends today, a short date and time otherwise, in the reader's time zone. |
