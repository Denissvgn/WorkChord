# scheduleEvidence Module

**Path:** `frontend/src/features/planningMasters/scheduleEvidence.ts`

## Description

_Auto-generated from `frontend/src/features/planningMasters/scheduleEvidence.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/gantt` | `GanttTask` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `scheduleLeaves` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/planning/PlanReviewSection.tsx"]
    n1["frontend/src/components/planning/PlanScheduleSection.tsx"]
    n2["frontend/src/features/planningMasters/scheduleEvidence.ts"]
    n3["frontend/src/types/gantt.ts"]
    n0 --> n2
    n0 --> n3
    n1 --> n2
    n1 --> n3
    n2 --> n3
    click n0 "../modules/PlanReviewSection.md"
    click n1 "../modules/PlanScheduleSection.md"
    click n2 "../modules/scheduleEvidence.md"
    click n3 "../modules/types_gantt.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanReviewSection](../modules/PlanReviewSection.md) |
| Inbound | [PlanScheduleSection](../modules/PlanScheduleSection.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `scheduleLeaves` | `(tasks: GanttTask[], deferred = false) -> GanttTask[]` | — | — |
