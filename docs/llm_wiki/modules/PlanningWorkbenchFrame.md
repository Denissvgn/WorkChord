# PlanningWorkbenchFrame Module

**Path:** `frontend/src/components/planning/PlanningWorkbenchFrame.tsx`

## Description

_Auto-generated from `frontend/src/components/planning/PlanningWorkbenchFrame.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../ui` | `PageHeader`, `PageLayout` |
| `./PlanReturnBar` | `PlanReturnBar` |
| `clsx` | `clsx` |
| `react` | `ReactNode` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PlanningWorkbenchFact`, `PlanningWorkbenchFrame` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/planning/PlanningWorkbenchFrame.test.tsx"]
    n1["frontend/src/components/planning/PlanningWorkbenchFrame.tsx"]
    n2["frontend/src/components/planning/PlanReturnBar.tsx"]
    n3["frontend/src/components/ui/index.ts"]
    n4["frontend/src/pages/CalendarPage.tsx"]
    n5["frontend/src/pages/GanttPage.tsx"]
    n6["frontend/src/pages/RoadmapPage.tsx"]
    n0 --> n1
    n1 --> n2
    n1 --> n3
    n4 --> n1
    n4 --> n3
    n5 --> n1
    n5 --> n3
    n6 --> n1
    n6 --> n3
    click n0 "../modules/PlanningWorkbenchFrame.test.md"
    click n1 "../modules/PlanningWorkbenchFrame.md"
    click n2 "../modules/PlanReturnBar.md"
    click n3 "../modules/index.md"
    click n4 "../modules/CalendarPage.md"
    click n5 "../modules/GanttPage.md"
    click n6 "../modules/RoadmapPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanningWorkbenchFrame.test](../modules/PlanningWorkbenchFrame.test.md) |
| Inbound | [CalendarPage](../modules/CalendarPage.md) |
| Inbound | [GanttPage](../modules/GanttPage.md) |
| Inbound | [RoadmapPage](../modules/RoadmapPage.md) |
| Outbound | [PlanReturnBar](../modules/PlanReturnBar.md) |
| Outbound | [index](../modules/index.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [PlanningWorkbenchFact](../entities/PlanningWorkbenchFact.md) | Type alias | 6 | — | — |
| [PlanningWorkbenchFrameProps](../entities/PlanningWorkbenchFrameProps.md) | Type alias | 12 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `PlanningWorkbenchFrame` | `({     title,     description,     facts = [],     contextControl,     secondaryActions,     primaryAction,     overflowAction,     state,     children,     variant = 'default',     className,     headerClassName,     canvasClassName,     testId, }: PlanningWorkbenchFrameProps)` | — | — |
