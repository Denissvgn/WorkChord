# IterationEditorDrawer Module

**Path:** `frontend/src/components/iteration/IterationEditorDrawer.tsx`

## Description

_Auto-generated from `frontend/src/components/iteration/IterationEditorDrawer.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/iteration` | `Iteration` | Declaration | erased |
| `../common/useConfirmDialog` | `useConfirmDialog` | — | compiler-dependent |
| `../ui` | `SlideOverDrawer` | — | compiler-dependent |
| `./IterationForm` | `IterationForm` | — | compiler-dependent |
| `react` | `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `IterationEditorDrawer` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/useConfirmDialog.tsx"]
    n1["frontend/src/components/iteration/IterationEditorDrawer.tsx"]
    n2["frontend/src/components/iteration/IterationForm.tsx"]
    n3["frontend/src/components/planning/PlanIterationDrawers.tsx"]
    n4["frontend/src/components/ui/index.ts"]
    n5["frontend/src/types/iteration.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n4
    n1 --> n5
    n2 --> n0
    n2 --> n5
    n3 --> n1
    n3 --> n5
    click n0 "../modules/useConfirmDialog.md"
    click n1 "../modules/IterationEditorDrawer.md"
    click n2 "../modules/IterationForm.md"
    click n3 "../modules/PlanIterationDrawers.md"
    click n4 "../modules/index.md"
    click n5 "../modules/types_iteration.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [PlanIterationDrawers](../modules/PlanIterationDrawers.md) |
| Outbound | [useConfirmDialog](../modules/useConfirmDialog.md) |
| Outbound | [IterationForm](../modules/IterationForm.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [IterationEditorDrawerProps](../entities/IterationEditorDrawerProps.md) | Interface | 8 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `IterationEditorDrawer` | `({ iteration, defaultProjectId, onClose, onSaved }: IterationEditorDrawerProps)` | — | The iteration form in the slide-over drawer, the one place an iteration is created or edited. |
