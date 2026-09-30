# TaskAgentReadinessBadge Module

**Path:** `frontend/src/components/tasks/TaskAgentReadinessBadge.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskAgentReadinessBadge.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../i18n/i18n` | `i18n` |
| `../../types/task` | `TaskAgentReadiness` |
| `clsx` | `clsx` |
| `lucide-react` | `AlertTriangle`, `Bot`, `CheckCircle2`, `XCircle` |
| `react` | `useState`, `useRef`, `useEffect`, `useCallback`, `useId` |
| `react-dom` | `createPortal` |
| `react-router-dom` | `useLocation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskAgentReadinessBadge` |
| Constants | `t` |
| Module calls | `t = bind` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskAgentReadinessBadge.test.tsx"]
    n1["frontend/src/components/tasks/TaskAgentReadinessBadge.tsx"]
    n2["frontend/src/components/tasks/TaskForm.tsx"]
    n3["frontend/src/components/tasks/TaskList.tsx"]
    n4["frontend/src/i18n/i18n.ts"]
    n5["frontend/src/types/task.ts"]
    n0 --> n1
    n0 --> n5
    n1 --> n4
    n1 --> n5
    n2 --> n1
    n2 --> n5
    n3 --> n1
    n3 --> n5
    click n0 "../modules/TaskAgentReadinessBadge.test.md"
    click n1 "../modules/TaskAgentReadinessBadge.md"
    click n2 "../modules/TaskForm.md"
    click n3 "../modules/TaskList.md"
    click n4 "../modules/i18n.md"
    click n5 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskAgentReadinessBadge.test](../modules/TaskAgentReadinessBadge.test.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TaskList](../modules/TaskList.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskAgentReadinessBadgeProps](../entities/TaskAgentReadinessBadgeProps.md) | Class | 11 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskAgentReadinessBadge` | `({ readiness, mode = 'compact' }: TaskAgentReadinessBadgeProps)` | — | — |
