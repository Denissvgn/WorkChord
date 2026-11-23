# GetStartedFlow.test Module

**Path:** `frontend/src/features/firstRun/GetStartedFlow.test.tsx`

## Description

_Auto-generated from `frontend/src/features/firstRun/GetStartedFlow.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/layout/ScopeBar` | `ScopeBar` | — | compiler-dependent |
| `../../components/planning/PlanReturnBar` | `PlanReturnBar` | — | compiler-dependent |
| `../../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../../pages/OverviewPage` | `OverviewPage` | — | compiler-dependent |
| `../../pages/PlanPage` | `PlanPage` | — | compiler-dependent |
| `../../pages/TasksPage` | `TasksPage` | — | compiler-dependent |
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/iteration` | `Iteration`, `PlanCheckpoint` | Declaration | erased |
| `../../types/project` | `Project` | Declaration | erased |
| `../../types/task` | `Task` | Declaration | erased |
| `../../types/team` | `TeamMember` | Declaration | erased |
| `../identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../identity/identityService` | `WorkspaceIdentity` | Declaration | erased |
| `../scope/scopeStore` | `useScopeStore` | — | compiler-dependent |
| `./FirstRunLanding` | `FirstRunLanding` | — | compiler-dependent |
| `./getStartedVisibility` | `useGetStartedVisibility` | — | compiler-dependent |
| `./setupReturn` | `SETUP_RETURN_KEY`, `useSetupReturn` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `react` | `ReactNode` | Declaration | erased |
| `react` | `useState` | — | compiler-dependent |
| `react-router-dom` | `Route`, `Routes`, `useLocation` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `server` |
| Module calls | `server = hoisted`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `mock`, `beforeEach`, `afterEach`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/features/firstRun/GetStartedFlow.test.tsx"]
    n1 --> n0
    click n1 "../modules/GetStartedFlow.test.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `frontend` (17) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 17 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [User](../entities/User.md) | Type alias | 238 | `ReturnType<typeof renderWorkspace>['user']` | — |
