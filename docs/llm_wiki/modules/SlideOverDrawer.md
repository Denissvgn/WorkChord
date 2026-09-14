# SlideOverDrawer Module

**Path:** `frontend/src/components/ui/SlideOverDrawer.tsx`

## Description

_Auto-generated from `frontend/src/components/ui/SlideOverDrawer.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../common/dialogLayer` | `useDialogLayer` |
| `lucide-react` | `X` |
| `react` | `useId`, `ReactNode`, `RefObject` |
| `react-dom` | `createPortal` |
| `react-i18next` | `useTranslation` |
| `tailwind-merge` | `twMerge` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `SlideOverDrawer` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/dialogLayer.ts"]
    n1["frontend/src/components/gantt/TaskEditModal.tsx"]
    n2["frontend/src/components/planning/PlanningWorkflowGuide.tsx"]
    n3["frontend/src/components/tasks/TaskEditorDrawer.tsx"]
    n4["frontend/src/components/tasks/TaskWorkflowGuide.tsx"]
    n5["frontend/src/components/ui/SlideOverDrawer.tsx"]
    n6["frontend/src/pages/AgentPipelinePage.tsx"]
    n1 --> n5
    n2 --> n5
    n3 --> n5
    n4 --> n5
    n5 --> n0
    n6 --> n5
    click n0 "../modules/dialogLayer.md"
    click n1 "../modules/TaskEditModal.md"
    click n2 "../modules/PlanningWorkflowGuide.md"
    click n3 "../modules/TaskEditorDrawer.md"
    click n4 "../modules/TaskWorkflowGuide.md"
    click n5 "../modules/SlideOverDrawer.md"
    click n6 "../modules/AgentPipelinePage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskEditModal](../modules/TaskEditModal.md) |
| Inbound | [PlanningWorkflowGuide](../modules/PlanningWorkflowGuide.md) |
| Inbound | [TaskEditorDrawer](../modules/TaskEditorDrawer.md) |
| Inbound | [TaskWorkflowGuide](../modules/TaskWorkflowGuide.md) |
| Inbound | [AgentPipelinePage](../modules/AgentPipelinePage.md) |
| Outbound | [dialogLayer](../modules/dialogLayer.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `SlideOverDrawer` | `({     open,     title,     subtitle,     icon,     children,     footer,     onClose,     ariaLabel,     className,     initialFocusRef,     restoreFocusRef,     closeOnBackdropClick = true,     closeDisabled = false,     closeLabel: closeLabelProp, }: {     open: boolean;     title: ReactNode;     subtitle?: ReactNode;     icon?: ReactNode;     children: ReactNode;     footer?: ReactNode;     onClose: () => void;     ariaLabel?: string;     className?: string;     initialFocusRef?: RefObject<HTMLElement \| null>;     restoreFocusRef?: RefObject<HTMLElement \| null>;     closeOnBackdropClick?: boolean;     closeDisabled?: boolean;     closeLabel?: string; })` | — | — |
