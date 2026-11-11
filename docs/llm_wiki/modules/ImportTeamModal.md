# ImportTeamModal Module

**Path:** `frontend/src/components/team/ImportTeamModal.tsx`

## Description

_Auto-generated from `frontend/src/components/team/ImportTeamModal.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/mutationFeedback` | `MutationFeedbackMeta` | Declaration | erased |
| `../../features/usePlanningObservation` | `usePlanningObservation` | — | compiler-dependent |
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Modal` | `Modal` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `Upload`, `FileText`, `AlertCircle` | — | compiler-dependent |
| `react` | `useEffect`, `useId`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ImportTeamModal` |
| Constants | `MAX_IMPORT_ROWS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Modal.tsx"]
    n2["frontend/src/components/team/ImportTeamModal.test.tsx"]
    n3["frontend/src/components/team/ImportTeamModal.tsx"]
    n4["frontend/src/features/mutationFeedback.ts"]
    n5["frontend/src/features/usePlanningObservation.ts"]
    n6["frontend/src/pages/TeamPage.tsx"]
    n7["frontend/src/services/teamService.ts"]
    n8["frontend/src/utils/apiError.ts"]
    n2 --> n3
    n3 --> n0
    n3 --> n1
    n3 --> n4
    n3 --> n5
    n3 --> n7
    n3 --> n8
    n5 --> n8
    n6 --> n3
    n6 --> n7
    click n0 "../modules/Button.md"
    click n1 "../modules/Modal.md"
    click n2 "../modules/ImportTeamModal.test.md"
    click n3 "../modules/ImportTeamModal.md"
    click n4 "../modules/mutationFeedback.md"
    click n5 "../modules/usePlanningObservation.md"
    click n6 "../modules/TeamPage.md"
    click n7 "../modules/teamService.md"
    click n8 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ImportTeamModal.test](../modules/ImportTeamModal.test.md) |
| Inbound | [TeamPage](../modules/TeamPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Modal](../modules/Modal.md) |
| Outbound | [mutationFeedback](../modules/mutationFeedback.md) |
| Outbound | [usePlanningObservation](../modules/usePlanningObservation.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ImportTeamModalProps](../entities/ImportTeamModalProps.md) | Interface | 14 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ImportTeamModal` | <pre><code>&#40;&#123;&#10;    iterationId&#44;&#10;    onClose&#44;&#10;    onSuccess&#58; onImportSuccess&#44;&#10;    onStateChange&#44;&#10;&#125;&#58; ImportTeamModalProps&#41;</code></pre> | — | — |
