# ConfirmDialog Module

**Path:** `frontend/src/components/common/ConfirmDialog.tsx`

## Description

_Auto-generated from `frontend/src/components/common/ConfirmDialog.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./Button` | `Button` | — | compiler-dependent |
| `./Modal` | `Modal` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `AlertTriangle` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `react` | `useRef` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ConfirmDialog`, `ConfirmDialogProps`, `ConfirmDialogTone` |
| Constants | `toneTitleClassName` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/common/ConfirmDialog.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/ConfirmDialog.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (10) |
| Outbound | `frontend` (2) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ConfirmDialogProps](../entities/ConfirmDialogProps.md) | Interface | 10 | — | — |
| [ConfirmDialogTone](../entities/ConfirmDialogTone.md) | Type alias | 8 | `'danger' \| 'warning'` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ConfirmDialog` | <pre><code>&#40;&#123;&#10;    open&#44;&#10;    title&#44;&#10;    description&#44;&#10;    confirmLabel&#44;&#10;    cancelLabel&#44;&#10;    closeLabel&#44;&#10;    onConfirm&#44;&#10;    onCancel&#44;&#10;    tone &#61; &#39;danger&#39;&#44;&#10;    pending &#61; false&#44;&#10;    confirmDisabled &#61; false&#44;&#10;&#125;&#58; ConfirmDialogProps&#41;</code></pre> | — | A deliberately small destructive-action contract layered on the shared |
