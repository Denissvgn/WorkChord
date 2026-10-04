# ImportTeamModal Module

**Path:** `frontend/src/components/team/ImportTeamModal.tsx`

## Description

_Auto-generated from `frontend/src/components/team/ImportTeamModal.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/teamService` | `teamService` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../common/Button` | `Button` |
| `../common/Modal` | `Modal` |
| `@tanstack/react-query` | `useMutation`, `useQueryClient` |
| `lucide-react` | `Upload`, `FileText`, `AlertCircle` |
| `react` | `useEffect`, `useId`, `useRef`, `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ImportTeamModal` |
| Constants | `MAX_IMPORT_ROWS` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Modal.tsx"]
    n2["frontend/src/components/team/ImportTeamModal.test.tsx"]
    n3["frontend/src/components/team/ImportTeamModal.tsx"]
    n4["frontend/src/pages/TeamPage.tsx"]
    n5["frontend/src/services/teamService.ts"]
    n6["frontend/src/utils/apiError.ts"]
    n2 --> n3
    n3 --> n0
    n3 --> n1
    n3 --> n5
    n3 --> n6
    n4 --> n3
    n4 --> n5
    click n0 "../modules/Button.md"
    click n1 "../modules/Modal.md"
    click n2 "../modules/ImportTeamModal.test.md"
    click n3 "../modules/ImportTeamModal.md"
    click n4 "../modules/TeamPage.md"
    click n5 "../modules/teamService.md"
    click n6 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ImportTeamModal.test](../modules/ImportTeamModal.test.md) |
| Inbound | [TeamPage](../modules/TeamPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Modal](../modules/Modal.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [ImportTeamModalProps](../entities/ImportTeamModalProps.md) | Class | 12 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ImportTeamModal` | `({     iterationId,     onClose,     onSuccess: onImportSuccess,     onStateChange,     expectedRevision, }: ImportTeamModalProps)` | — | — |
