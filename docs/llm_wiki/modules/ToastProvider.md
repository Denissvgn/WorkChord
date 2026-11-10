# ToastProvider Module

**Path:** `frontend/src/components/feedback/ToastProvider.tsx`

## Description

_Auto-generated from `frontend/src/components/feedback/ToastProvider.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../common/Button` | `Button` | — | compiler-dependent |
| `./toast` | `ToastApi`, `ToastInput`, `ToastTone` | Specifier | compiler-dependent |
| `./toast` | `ToastContext` | — | compiler-dependent |
| `lucide-react` | `AlertTriangle`, `CheckCircle2`, `Info`, `X` | — | compiler-dependent |
| `react` | `ReactNode` | Specifier | compiler-dependent |
| `react` | `useCallback`, `useEffect`, `useMemo`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ToastProvider` |
| Constants | `toastClasses`, `toastIcons`, `iconClasses` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/toast.ts"]
    n2["frontend/src/components/feedback/ToastProvider.tsx"]
    n3["frontend/src/main.tsx"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n2 --> n0
    n2 --> n1
    n3 --> n2
    n4 --> n2
    click n0 "../modules/Button.md"
    click n1 "../modules/toast.md"
    click n2 "../modules/ToastProvider.md"
    click n3 "../modules/src_main.md"
    click n4 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [src_main](../modules/src_main.md) |
| Inbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [toast](../modules/toast.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ToastRecord](../entities/ToastRecord.md) | Interface | 13 | `Required<Pick<ToastInput, 'message' \| 'tone' \| 'durationMs'>>` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ToastProvider` | `({ children }: { children: ReactNode })` | — | — |
