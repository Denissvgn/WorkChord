# sampleProject.test Module

**Path:** `frontend/src/features/firstRun/sampleProject.test.tsx`

## Description

_Auto-generated from `frontend/src/features/firstRun/sampleProject.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/projects/RoadmapView` | `RoadmapView` | — | compiler-dependent |
| `../../components/tasks/DraftDismissalDialog` | `DraftDismissalDialog` | — | compiler-dependent |
| `../../components/tasks/useDraftDismissal` | `useDraftDismissal` | — | compiler-dependent |
| `../../i18n/i18n` | `changeAppLanguage`, `i18n` | — | compiler-dependent |
| `../../services/api` | `api` | — | compiler-dependent |
| `../../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../../test/renderWithProviders` | `createTestQueryClient`, `renderWithProviders` | — | compiler-dependent |
| `../../types/project` | `Project` | Declaration | erased |
| `../../utils/formatDate` | `formatDate` | — | compiler-dependent |
| `../identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../identity/identityService` | `WorkspaceIdentity` | Declaration | erased |
| `../scope/scopeStore` | `useScopeStore` | — | compiler-dependent |
| `../scope/useWorkScope` | `useWorkScope` | — | compiler-dependent |
| `./GetStartedPanel` | `GetStartedPanel` | — | compiler-dependent |
| `./SampleProjectAction` | `SampleProjectAction` | — | compiler-dependent |
| `./sampleProject` | `SampleManifest` | Specifier | compiler-dependent |
| `./sampleProject` | `loadSampleProject`, `removeSampleProject` | — | compiler-dependent |
| `./sampleProject.fixture` | `sampleProjectFixture` | — | compiler-dependent |
| `./sampleProjectStore` | `useSampleProject` | — | compiler-dependent |
| `./useFirstRunProgress` | `useFirstRunProgress` | — | compiler-dependent |
| `@tanstack/react-query` | `QueryClientProvider` | — | compiler-dependent |
| `@testing-library/react` | `render`, `act`, `cleanup`, `screen`, `waitFor`, `within` | — | compiler-dependent |
| `@testing-library/user-event` | `userEvent` | — | compiler-dependent |
| `react` | `useEffect` | — | compiler-dependent |
| `react-router-dom` | `createMemoryRouter`, `RouterProvider`, `useLocation` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `person`, `identity`, `queryClients` |
| Module calls | `mock`, `mock`, `queryClients = Set`, `beforeEach`, `afterEach`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/features/firstRun/sampleProject.test.tsx"]
    n1 --> n0
    click n1 "../modules/sampleProject.test.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `frontend` (19) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |

> All 19 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [Row](../entities/sampleProject.test_Row.md) | Type alias | 32 | `{ id: number; name?: string; title?: string; [key: string]: unknown }` | — |
