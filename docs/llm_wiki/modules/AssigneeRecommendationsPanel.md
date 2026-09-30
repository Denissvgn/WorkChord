# AssigneeRecommendationsPanel Module

**Path:** `frontend/src/components/team/AssigneeRecommendationsPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/team/AssigneeRecommendationsPanel.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/taskService` | `taskService` |
| `../../services/triageService` | `triageService` |
| `../common/Button` | `Button` |
| `../feedback/QueryState` | `QueryErrorState` |
| `@tanstack/react-query` | `useQuery` |
| `lucide-react` | `AlertTriangle`, `CheckCircle2`, `UserCheck` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AssigneeRecommendationsPanel` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/feedback/QueryState.tsx"]
    n2["frontend/src/components/tasks/TaskForm.tsx"]
    n3["frontend/src/components/team/AssigneeRecommendationsPanel.tsx"]
    n4["frontend/src/pages/TriagePage.tsx"]
    n5["frontend/src/services/taskService.ts"]
    n6["frontend/src/services/triageService.ts"]
    n1 --> n0
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n5
    n2 --> n6
    n3 --> n0
    n3 --> n1
    n3 --> n5
    n3 --> n6
    n4 --> n0
    n4 --> n1
    n4 --> n3
    n4 --> n5
    n4 --> n6
    click n0 "../modules/Button.md"
    click n1 "../modules/QueryState.md"
    click n2 "../modules/TaskForm.md"
    click n3 "../modules/AssigneeRecommendationsPanel.md"
    click n4 "../modules/TriagePage.md"
    click n5 "../modules/taskService.md"
    click n6 "../modules/triageService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [taskService](../modules/taskService.md) |
| Outbound | [triageService](../modules/triageService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [AssigneeRecommendationsPanelProps](../entities/AssigneeRecommendationsPanelProps.md) | Class | 9 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `AssigneeRecommendationsPanel` | `({     targetType,     taskId,     triageItemId,     iterationId,     selectedAssigneeId,     onSelectAssignee, }: AssigneeRecommendationsPanelProps)` | — | — |
