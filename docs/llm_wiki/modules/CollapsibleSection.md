# CollapsibleSection Module

**Path:** `frontend/src/components/common/CollapsibleSection.tsx`

## Description

_Auto-generated from `frontend/src/components/common/CollapsibleSection.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `ChevronDown` | — | compiler-dependent |
| `react` | `useId`, `useState` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `CollapsibleSection` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/capacity/TeamForm.tsx"]
    n1["frontend/src/components/common/CollapsibleSection.tsx"]
    n2["frontend/src/components/iteration/IterationForm.tsx"]
    n3["frontend/src/components/projects/InitiativeForm.tsx"]
    n4["frontend/src/components/projects/ProjectForm.tsx"]
    n5["frontend/src/components/projects/TimeEntriesReport.tsx"]
    n6["frontend/src/components/releases/ReleaseForm.tsx"]
    n7["frontend/src/components/tasks/TaskCreateSections.tsx"]
    n8["frontend/src/components/tasks/TaskForm.tsx"]
    n9["frontend/src/components/tasks/TimeEntriesPanel.tsx"]
    n10["frontend/src/components/triage/ConvertTriageDrawer.tsx"]
    n0 --> n1
    n2 --> n1
    n3 --> n1
    n4 --> n1
    n5 --> n1
    n5 --> n9
    n6 --> n1
    n7 --> n1
    n8 --> n1
    n8 --> n7
    n8 --> n9
    n9 --> n1
    n10 --> n1
    n10 --> n7
    click n0 "../modules/TeamForm.md"
    click n1 "../modules/CollapsibleSection.md"
    click n2 "../modules/IterationForm.md"
    click n3 "../modules/InitiativeForm.md"
    click n4 "../modules/ProjectForm.md"
    click n5 "../modules/TimeEntriesReport.md"
    click n6 "../modules/ReleaseForm.md"
    click n7 "../modules/TaskCreateSections.md"
    click n8 "../modules/TaskForm.md"
    click n9 "../modules/TimeEntriesPanel.md"
    click n10 "../modules/ConvertTriageDrawer.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TeamForm](../modules/TeamForm.md) |
| Inbound | [IterationForm](../modules/IterationForm.md) |
| Inbound | [InitiativeForm](../modules/InitiativeForm.md) |
| Inbound | [ProjectForm](../modules/ProjectForm.md) |
| Inbound | [TimeEntriesReport](../modules/TimeEntriesReport.md) |
| Inbound | [ReleaseForm](../modules/ReleaseForm.md) |
| Inbound | [TaskCreateSections](../modules/TaskCreateSections.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TimeEntriesPanel](../modules/TimeEntriesPanel.md) |
| Inbound | [ConvertTriageDrawer](../modules/ConvertTriageDrawer.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [CollapsibleSectionProps](../entities/CollapsibleSectionProps.md) | Interface | 5 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `CollapsibleSection` | `({ title, defaultOpen = false, open, onOpenChange, children }: CollapsibleSectionProps)` | — | — |
