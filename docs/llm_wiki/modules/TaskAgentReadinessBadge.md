# TaskAgentReadinessBadge Module

**Path:** `frontend/src/components/tasks/TaskAgentReadinessBadge.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskAgentReadinessBadge.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Button` | `Button` | — | compiler-dependent |
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../types/task` | `TaskAgentReadiness` | Declaration | erased |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `AlertTriangle`, `Bot`, `CheckCircle2`, `XCircle` | — | compiler-dependent |
| `react` | `useState`, `useRef`, `useEffect`, `useCallback`, `useId` | — | compiler-dependent |
| `react-dom` | `createPortal` | — | compiler-dependent |
| `react-router-dom` | `useLocation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskAgentReadinessBadge` |
| Constants | `t` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/tasks/TaskAgentReadinessBadge.test.tsx"]
    n2["frontend/src/components/tasks/TaskAgentReadinessBadge.tsx"]
    n3["frontend/src/components/tasks/TaskForm.tsx"]
    n4["frontend/src/components/tasks/TaskList.tsx"]
    n5["frontend/src/i18n/i18n.ts"]
    n6["frontend/src/types/task.ts"]
    n1 --> n2
    n1 --> n6
    n2 --> n0
    n2 --> n5
    n2 --> n6
    n3 --> n0
    n3 --> n2
    n3 --> n6
    n4 --> n0
    n4 --> n2
    n4 --> n6
    click n0 "../modules/Button.md"
    click n1 "../modules/TaskAgentReadinessBadge.test.md"
    click n2 "../modules/TaskAgentReadinessBadge.md"
    click n3 "../modules/TaskForm.md"
    click n4 "../modules/TaskList.md"
    click n5 "../modules/i18n.md"
    click n6 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskAgentReadinessBadge.test](../modules/TaskAgentReadinessBadge.test.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TaskList](../modules/TaskList.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskAgentReadinessBadgeProps](../entities/TaskAgentReadinessBadgeProps.md) | Interface | 12 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskAgentReadinessBadge` | `({ readiness, mode = 'compact' }: TaskAgentReadinessBadgeProps)` | — | — |
