# VacationManager Module

**Path:** `frontend/src/components/team/VacationManager.tsx`

## Description

_Auto-generated from `frontend/src/components/team/VacationManager.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../services/planningInputService` | `planningInputService`, `ObservedRevisions` |
| `../../services/teamService` | `teamService` |
| `../../types/team` | `Vacation`, `TeamMember` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../../utils/formatDate` | `formatDate` |
| `../common/Button` | `Button` |
| `../common/Input` | `Input` |
| `../common/Modal` | `Modal` |
| `../common/useConfirmDialog` | `useConfirmDialog` |
| `../planning/PlanningInputBoundary` | `PlanningInputBoundary` |
| `./VacationCsvImport` | `VacationCsvImport` |
| `@tanstack/react-query` | `useMutation`, `useQueryClient` |
| `lucide-react` | `Plane`, `Trash2`, `Plus`, `Calendar` |
| `react` | `ReactNode`, `useState` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `VacationManager` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/team/VacationManager.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/VacationManager.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (1) |
| Outbound | `frontend` (11) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 12 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [VacationManagerProps](../entities/VacationManagerProps.md) | Class | 18 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `VacationManager` | `(props: VacationManagerProps)` | — | — |
