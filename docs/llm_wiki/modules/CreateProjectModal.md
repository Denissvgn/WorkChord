# CreateProjectModal Module

**Path:** `frontend/src/features/firstRun/CreateProjectModal.tsx`

## Description

_Auto-generated from `frontend/src/features/firstRun/CreateProjectModal.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Button` | `Button` | — | compiler-dependent |
| `../../components/common/Input` | `Input` | — | compiler-dependent |
| `../../components/common/Modal` | `Modal` | — | compiler-dependent |
| `../../services/projectService` | `projectService` | — | compiler-dependent |
| `../../types/project` | `Project` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../mutationFeedback` | `MutationFeedbackMeta` | Declaration | erased |
| `../mutationFeedback` | `feedbackMessage` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQueryClient` | — | compiler-dependent |
| `react` | `FormEvent` | Declaration | erased |
| `react` | `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `CreateProjectModal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Input.tsx"]
    n2["frontend/src/components/common/Modal.tsx"]
    n3["frontend/src/features/firstRun/CreateProjectModal.tsx"]
    n4["frontend/src/features/firstRun/GetStartedPanel.tsx"]
    n5["frontend/src/features/mutationFeedback.ts"]
    n6["frontend/src/services/projectService.ts"]
    n7["frontend/src/types/project.ts"]
    n8["frontend/src/utils/apiError.ts"]
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n4 --> n0
    n4 --> n3
    n6 --> n7
    click n0 "../modules/Button.md"
    click n1 "../modules/Input.md"
    click n2 "../modules/Modal.md"
    click n3 "../modules/CreateProjectModal.md"
    click n4 "../modules/GetStartedPanel.md"
    click n5 "../modules/mutationFeedback.md"
    click n6 "../modules/projectService.md"
    click n7 "../modules/types_project.md"
    click n8 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GetStartedPanel](../modules/GetStartedPanel.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Input](../modules/Input.md) |
| Outbound | [Modal](../modules/Modal.md) |
| Outbound | [mutationFeedback](../modules/mutationFeedback.md) |
| Outbound | [projectService](../modules/projectService.md) |
| Outbound | [types_project](../modules/types_project.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `CreateProjectModal` | `({ onClose, onCreated }: { onClose: () => void; onCreated: (project: Project) => void })` | — | The short way to a first project: a name and, optionally, its start and target dates. |
