# Modal Module

**Path:** `frontend/src/components/common/Modal.tsx`

## Description

_Auto-generated from `frontend/src/components/common/Modal.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./dialogLayer` | `useDialogLayer` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `X` | — | compiler-dependent |
| `react` | `ReactNode`, `RefObject` | Declaration | erased |
| `react` | `useId` | — | compiler-dependent |
| `react-dom` | `createPortal` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `Modal`, `ModalProps` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/common/Modal.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/Modal.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (19) |
| Outbound | `frontend` (1) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 20 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ModalProps](../entities/ModalProps.md) | Interface | 8 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `Modal` | <pre><code>&#40;&#123;&#10;    open&#44;&#10;    title&#44;&#10;    description&#44;&#10;    children&#44;&#10;    footer&#44;&#10;    onClose&#44;&#10;    closeLabel&#44;&#10;    initialFocusRef&#44;&#10;    closeOnBackdropClick &#61; false&#44;&#10;    closeDisabled &#61; false&#44;&#10;    fullScreen &#61; false&#44;&#10;    className&#44;&#10;    contentClassName&#44;&#10;&#125;&#58; ModalProps&#41;</code></pre> | — | — |
