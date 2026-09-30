# FullscreenWorkspace Module

**Path:** `frontend/src/components/common/FullscreenWorkspace.tsx`

## Description

_Auto-generated from `frontend/src/components/common/FullscreenWorkspace.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `./dialogLayer` | `useDialogLayer` |
| `clsx` | `clsx` |
| `react` | `ReactNode`, `RefObject` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `FullscreenWorkspace` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/dialogLayer.ts"]
    n1["frontend/src/components/common/FullscreenWorkspace.tsx"]
    n2["frontend/src/pages/GanttPage.tsx"]
    n3["frontend/src/pages/TasksPage.tsx"]
    n1 --> n0
    n2 --> n1
    n3 --> n1
    click n0 "../modules/dialogLayer.md"
    click n1 "../modules/FullscreenWorkspace.md"
    click n2 "../modules/GanttPage.md"
    click n3 "../modules/TasksPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GanttPage](../modules/GanttPage.md) |
| Inbound | [TasksPage](../modules/TasksPage.md) |
| Outbound | [dialogLayer](../modules/dialogLayer.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `FullscreenWorkspace` | `({     open,     onClose,     ariaLabel,     children,     className,     fullscreenClassName,     initialFocusRef, }: {     open: boolean;     onClose: () => void;     ariaLabel: string;     children: ReactNode;     className?: string;     fullscreenClassName?: string;     initialFocusRef?: RefObject<HTMLElement \| null>; })` | — | — |
