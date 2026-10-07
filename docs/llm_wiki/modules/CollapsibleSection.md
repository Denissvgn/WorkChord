# CollapsibleSection Module

**Path:** `frontend/src/components/common/CollapsibleSection.tsx`

## Description

_Auto-generated from `frontend/src/components/common/CollapsibleSection.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `clsx` | `clsx` |
| `lucide-react` | `ChevronDown` |
| `react` | `useId`, `useState` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `CollapsibleSection` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/CollapsibleSection.tsx"]
    n1["frontend/src/components/iteration/IterationForm.tsx"]
    n2["frontend/src/components/projects/InitiativeForm.tsx"]
    n3["frontend/src/components/projects/ProjectForm.tsx"]
    n4["frontend/src/components/projects/TimeEntriesReport.tsx"]
    n5["frontend/src/components/releases/ReleaseForm.tsx"]
    n6["frontend/src/components/tasks/TaskForm.tsx"]
    n7["frontend/src/components/tasks/TimeEntriesPanel.tsx"]
    n8["frontend/src/components/team/TeamForm.tsx"]
    n9["frontend/src/pages/TriagePage.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n4 --> n7
    n5 --> n0
    n6 --> n0
    n6 --> n7
    n7 --> n0
    n8 --> n0
    n9 --> n0
    click n0 "../modules/CollapsibleSection.md"
    click n1 "../modules/IterationForm.md"
    click n2 "../modules/InitiativeForm.md"
    click n3 "../modules/ProjectForm.md"
    click n4 "../modules/TimeEntriesReport.md"
    click n5 "../modules/ReleaseForm.md"
    click n6 "../modules/TaskForm.md"
    click n7 "../modules/TimeEntriesPanel.md"
    click n8 "../modules/TeamForm.md"
    click n9 "../modules/TriagePage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [IterationForm](../modules/IterationForm.md) |
| Inbound | [InitiativeForm](../modules/InitiativeForm.md) |
| Inbound | [ProjectForm](../modules/ProjectForm.md) |
| Inbound | [TimeEntriesReport](../modules/TimeEntriesReport.md) |
| Inbound | [ReleaseForm](../modules/ReleaseForm.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TimeEntriesPanel](../modules/TimeEntriesPanel.md) |
| Inbound | [TeamForm](../modules/TeamForm.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [CollapsibleSectionProps](../entities/CollapsibleSectionProps.md) | Class | 5 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `CollapsibleSection` | `({ title, defaultOpen = false, children }: CollapsibleSectionProps)` | — | — |
