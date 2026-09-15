# GanttChartProps

**Location:** `frontend/src/components/gantt/GanttChart.tsx:22`
**Kind:** Class
**Bases:** —
**Module:** [GanttChart](../modules/GanttChart.md)

## Description

_Auto-generated from `GanttChartProps` in `frontend/src/components/gantt/GanttChart.tsx`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `iterationId` | `number` | *required* | — |
| `iterationRevision` | `number` | *required* | — |
| `startDate` | `string` | *required* | — |
| `endDate` | `string` | *required* | — |
| `tasks` | `GanttTask[]` | *required* | — |
| `weekends` | `string[]` | *required* | — |
| `holidays` | `string[]` | *required* | — |
| `memberVacations` | `Record<number, string[]>` | *required* | — |
| `sandboxMode` | `boolean` | *required* | — |
| `onSaveSandbox` | `(taskId: number, updatedData: Partial<GanttTask>) => void` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["GanttChartProps (frontend/src/components/gantt/GanttChart.tsx)"]
    n1["GanttChart (frontend/src/components/gantt/GanttChart.tsx)"]
    n1 --> n0
    click n0 "../modules/GanttChart.md"
    click n1 "../modules/GanttChart.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [GanttChart](../modules/GanttChart.md) | 0 | `endDate`, `holidays`, `iterationId`, `iterationRevision`, `memberVacations`, `onSaveSandbox`, `sandboxMode`, `startDate`, `tasks`, `weekends` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `GanttChart` | type_reference | [GanttChart](../modules/GanttChart.md) | — |
