# GetStartedPanel.test Module

**Path:** `frontend/src/features/firstRun/GetStartedPanel.test.tsx`

## Description

_Auto-generated from `frontend/src/features/firstRun/GetStartedPanel.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/layout/ContextHelp` | `ContextHelp` | — | compiler-dependent |
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../pages/OverviewPage` | `OverviewPage` | — | compiler-dependent |
| `../../services/iterationService` | `iterationService` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/iteration` | `Iteration`, `PlanCheckpoint` | Declaration | erased |
| `../../types/project` | `Project` | Declaration | erased |
| `../identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../identity/identityService` | `WorkspaceIdentity` | Declaration | erased |
| `../planningMasters/usePlanningNavigationSummary` | `planningNavigationSummaryKey` | — | compiler-dependent |
| `../scope/scopeStore` | `useScopeStore` | — | compiler-dependent |
| `./FirstRunLanding` | `FirstRunLanding` | — | compiler-dependent |
| `./firstRunSteps` | `firstRunSteps` | — | compiler-dependent |
| `./getStartedVisibility` | `GET_STARTED_DISMISSED_KEY`, `useGetStartedVisibility` | — | compiler-dependent |
| `./sampleProjectStore` | `useSampleProject` | — | compiler-dependent |
| `@testing-library/react` | `act`, `fireEvent`, `screen`, `waitFor`, `within` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `react` | `useState` | — | compiler-dependent |
| `react-router-dom` | `Route`, `Routes`, `useLocation` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `server` |
| Module calls | `server = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `afterEach`, `describe`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/features/firstRun/GetStartedPanel.test.tsx"]
    n1 --> n0
    click n1 "../modules/GetStartedPanel.test.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `frontend` (15) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.
