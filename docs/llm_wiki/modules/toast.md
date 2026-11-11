# toast Module

**Path:** `frontend/src/components/feedback/toast.ts`

## Description

_Auto-generated from `frontend/src/components/feedback/toast.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `react` | `createContext`, `useContext` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ToastApi`, `ToastContext`, `ToastInput`, `ToastTone`, `ToneToastOptions`, `useToast` |
| Constants | `ToastContext` |
| Module calls | `ToastContext = createContext` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/feedback/toast.ts"]
    n0 --> n1
    click n1 "../modules/toast.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (19) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

> All 19 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ToastInput](../entities/ToastInput.md) | Interface | 5 | — | — |
| [ToastApi](../entities/ToastApi.md) | Interface | 17 | — | — |
| [ToastTone](../entities/ToastTone.md) | Type alias | 3 | `'success' \| 'error' \| 'info'` | — |
| [ToneToastOptions](../entities/ToneToastOptions.md) | Type alias | 15 | `Omit<ToastInput, 'message' \| 'tone'>` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useToast` | `()` | — | — |
