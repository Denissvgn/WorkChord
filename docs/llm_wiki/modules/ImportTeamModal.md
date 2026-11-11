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
| `../common/DisabledReason` | `DisabledReason` | — | compiler-dependent |
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
    n1["frontend/src/components/common/DisabledReason.tsx"]
    n2["frontend/src/components/common/Modal.tsx"]
    n3["frontend/src/components/team/ImportTeamModal.test.tsx"]
    n4["frontend/src/components/team/ImportTeamModal.tsx"]
    n5["frontend/src/features/mutationFeedback.ts"]
    n6["frontend/src/features/usePlanningObservation.ts"]
    n7["frontend/src/pages/TeamPage.tsx"]
    n8["frontend/src/services/teamService.ts"]
    n9["frontend/src/utils/apiError.ts"]
    n3 --> n4
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n5
    n4 --> n6
    n4 --> n8
    n4 --> n9
    n6 --> n9
    n7 --> n4
    n7 --> n8
    click n0 "../modules/Button.md"
    click n1 "../modules/DisabledReason.md"
    click n2 "../modules/Modal.md"
    click n3 "../modules/ImportTeamModal.test.md"
    click n4 "../modules/ImportTeamModal.md"
    click n5 "../modules/mutationFeedback.md"
    click n6 "../modules/usePlanningObservation.md"
    click n7 "../modules/TeamPage.md"
    click n8 "../modules/teamService.md"
    click n9 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ImportTeamModal.test](../modules/ImportTeamModal.test.md) |
| Inbound | [TeamPage](../modules/TeamPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [DisabledReason](../modules/DisabledReason.md) |
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
| [ImportTeamModalProps](../entities/ImportTeamModalProps.md) | Interface | 15 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ImportTeamModal` | <pre><code>&#40;&#123;&#10;    iterationId&#44;&#10;    onClose&#44;&#10;    onSuccess&#58; onImportSuccess&#44;&#10;    onStateChange&#44;&#10;&#125;&#58; ImportTeamModalProps&#41;</code></pre> | — | — |
