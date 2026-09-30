# dialogLayer Module

**Path:** `frontend/src/components/common/dialogLayer.ts`

## Description

_Auto-generated from `frontend/src/components/common/dialogLayer.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `react` | `useCallback`, `useEffect`, `useRef`, `RefObject` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `useDialogLayer` |
| Constants | `focusableSelector`, `dialogLayerStack` |
| Module calls | `focusableSelector = join` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/dialogLayer.ts"]
    n1["frontend/src/components/common/FullscreenWorkspace.tsx"]
    n2["frontend/src/components/common/Modal.tsx"]
    n3["frontend/src/components/layout/AppTopNav.tsx"]
    n4["frontend/src/components/ui/SlideOverDrawer.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    click n0 "../modules/dialogLayer.md"
    click n1 "../modules/FullscreenWorkspace.md"
    click n2 "../modules/Modal.md"
    click n3 "../modules/AppTopNav.md"
    click n4 "../modules/SlideOverDrawer.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [FullscreenWorkspace](../modules/FullscreenWorkspace.md) |
| Inbound | [Modal](../modules/Modal.md) |
| Inbound | [AppTopNav](../modules/AppTopNav.md) |
| Inbound | [SlideOverDrawer](../modules/SlideOverDrawer.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [DialogLayerOptions](../entities/DialogLayerOptions.md) | Class | 57 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useDialogLayer` | `({     open,     onClose,     initialFocusRef,     restoreFocusRef,     closeDisabled = false, }: DialogLayerOptions)` | — | Share modal-layer behavior without coupling a dialog to a visual layout. |
