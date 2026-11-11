# TaskBriefEditor Module

**Path:** `frontend/src/components/tasks/TaskBriefEditor.tsx`

## Description

_Auto-generated from `frontend/src/components/tasks/TaskBriefEditor.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/task` | `TaskBrief` | Declaration | erased |
| `../common/Button` | `Button` | — | compiler-dependent |
| `./taskEditorContract` | `newCriterion` | — | compiler-dependent |
| `lucide-react` | `ArrowDown`, `ArrowUp`, `Plus`, `Trash2` | — | compiler-dependent |
| `react` | `useId` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TaskBriefEditor` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/tasks/TaskBriefEditor.test.tsx"]
    n2["frontend/src/components/tasks/TaskBriefEditor.tsx"]
    n3["frontend/src/components/tasks/taskEditorContract.ts"]
    n4["frontend/src/components/tasks/TaskForm.tsx"]
    n5["frontend/src/components/tasks/TaskReadView.tsx"]
    n6["frontend/src/pages/TriagePage.tsx"]
    n7["frontend/src/types/task.ts"]
    n1 --> n2
    n1 --> n3
    n2 --> n0
    n2 --> n3
    n2 --> n7
    n3 --> n7
    n4 --> n0
    n4 --> n2
    n4 --> n3
    n4 --> n7
    n5 --> n0
    n5 --> n2
    n5 --> n7
    n6 --> n0
    n6 --> n2
    n6 --> n3
    n6 --> n7
    click n0 "../modules/Button.md"
    click n1 "../modules/TaskBriefEditor.test.md"
    click n2 "../modules/TaskBriefEditor.md"
    click n3 "../modules/taskEditorContract.md"
    click n4 "../modules/TaskForm.md"
    click n5 "../modules/TaskReadView.md"
    click n6 "../modules/TriagePage.md"
    click n7 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskBriefEditor.test](../modules/TaskBriefEditor.test.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TaskReadView](../modules/TaskReadView.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [taskEditorContract](../modules/taskEditorContract.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TaskBriefEditor` | <pre><code>&#40;&#123; value&#44; onChange&#44; disabled &#61; false&#44; hideContext &#61; false &#125;&#58; &#123;&#10;    value&#58; TaskBrief&#59; onChange&#58; &#40;value&#58; TaskBrief&#41; &#61;&#62; void&#59; disabled&#63;&#58; boolean&#59; hideContext&#63;&#58; boolean&#59;&#10;&#125;&#41;</code></pre> | — | — |
