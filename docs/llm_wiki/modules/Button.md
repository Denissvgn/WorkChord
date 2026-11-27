# Button Module

**Path:** `frontend/src/components/common/Button.tsx`

## Description

_Auto-generated from `frontend/src/components/common/Button.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./buttonStyles` | `ButtonSize`, `ButtonVariant` | Specifier | compiler-dependent |
| `./buttonStyles` | `buttonClassName` | — | compiler-dependent |
| `lucide-react` | `Loader2` | — | compiler-dependent |
| `react` | `ButtonHTMLAttributes` | Declaration | erased |
| `react` | `Children`, `forwardRef` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `Button` |
| Constants | `Button` |
| Module calls | `Button = forwardRef` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/common/Button.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/Button.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (166) |
| Outbound | `frontend` (1) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

> All 167 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ButtonProps](../entities/ButtonProps.md) | Interface | 6 | `ButtonHTMLAttributes<HTMLButtonElement>` | — |
