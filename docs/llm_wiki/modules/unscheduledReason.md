# unscheduledReason Module

**Path:** `frontend/src/components/gantt/unscheduledReason.ts`

## Description

_Auto-generated from `frontend/src/components/gantt/unscheduledReason.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/gantt` | `KeptDatesTask`, `UnscheduledTask` | Declaration | erased |
| `i18next` | `TFunction` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `unscheduledReasonText` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/gantt/unscheduledReason.ts"]
    n1["frontend/src/components/gantt/UnscheduledTasks.tsx"]
    n2["frontend/src/components/planning/PlanScheduleSection.tsx"]
    n3["frontend/src/types/gantt.ts"]
    n0 --> n3
    n1 --> n0
    n1 --> n3
    n2 --> n0
    n2 --> n3
    click n0 "../modules/unscheduledReason.md"
    click n1 "../modules/UnscheduledTasks.md"
    click n2 "../modules/PlanScheduleSection.md"
    click n3 "../modules/types_gantt.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [UnscheduledTasks](../modules/UnscheduledTasks.md) |
| Inbound | [PlanScheduleSection](../modules/PlanScheduleSection.md) |
| Outbound | [types_gantt](../modules/types_gantt.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `unscheduledReasonText` | `(t: TFunction, item: UnscheduledTask \| KeptDatesTask) -> string` | — | The translated reason a schedule run left a task unplaced, naming any postponed work it waits on. |
