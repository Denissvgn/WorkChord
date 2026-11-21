# destinationEmptyStates.test Module

**Path:** `frontend/src/pages/destinationEmptyStates.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/destinationEmptyStates.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../features/firstRun/getStartedVisibility` | `useGetStartedVisibility` | — | compiler-dependent |
| `../features/identity/identityContext` | `IdentityContext` | — | compiler-dependent |
| `../features/identity/identityService` | `WorkspaceIdentity` | Declaration | erased |
| `../features/scope/scopeStore` | `useScopeStore` | — | compiler-dependent |
| `../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../navigation/legacyPaths` | `mapLegacyPath` | — | compiler-dependent |
| `../services/api` | `api` | — | compiler-dependent |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../test/workspaceApi` | `installWorkspaceApi` | — | compiler-dependent |
| `../types/project` | `Project` | Declaration | erased |
| `../utils/adminAccess` | `clearAdminApiKey`, `setAdminApiKey` | — | compiler-dependent |
| `../utils/agentAccess` | `clearAgentApiKey`, `setAgentApiKey` | — | compiler-dependent |
| `./AnalyticsPage` | `AnalyticsPage` | — | compiler-dependent |
| `./GanttPage` | `GanttPage` | — | compiler-dependent |
| `./MyWorkPage` | `MyWorkPage` | — | compiler-dependent |
| `./OverviewPage` | `OverviewPage` | — | compiler-dependent |
| `./PlanPage` | `PlanPage` | — | compiler-dependent |
| `./ProjectsPage` | `ProjectsPage` | — | compiler-dependent |
| `./TasksPage` | `TasksPage` | — | compiler-dependent |
| `./TeamPage` | `TeamPage` | — | compiler-dependent |
| `./TriagePage` | `TriagePage` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor` | — | compiler-dependent |
| `axios` | `AxiosResponse`, `InternalAxiosRequestConfig` | Declaration | erased |
| `react` | `ReactElement` | Declaration | erased |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `MODEL`, `BINDING`, `ITERATION`, `TRIAGE`, `PROJECT`, `PAGE`, `GUEST`, `originalAdapter`, `CASES`, `LANGUAGES` |
| Module calls | `beforeEach`, `afterEach`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/destinationEmptyStates.test.tsx"]
    n1 --> n0
    click n1 "../modules/destinationEmptyStates.test.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | `frontend` (21) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 21 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [Scenario](../entities/Scenario.md) | Type alias | 33 | <pre><code>&#123;&#10;    &#47;&#42;&#42; A profile is chosen in this workspace&#44; so the first setup step is past it&#46; &#42;&#47;&#10;    profile&#63;&#58; boolean&#59;&#10;    iterations&#63;&#58; unknown&#91;&#93;&#59;&#10;    projects&#63;&#58; unknown&#91;&#93;&#59;&#10;    triage&#63;&#58; unknown&#91;&#93;&#59;&#10;    tasks&#63;&#58; unknown&#91;&#93;&#59;&#10;    pipeline&#63;&#58; Record&#60;string&#44; unknown&#91;&#93;&#62;&#59;&#10;    &#47;&#42;&#42; The admin&#45;key view of Team models&#58; a key that may administer&#44; and the two lists it shows&#46; &#42;&#47;&#10;    models&#63;&#58; &#123; catalog&#58; unknown&#91;&#93;&#59; bindings&#58; unknown&#91;&#93; &#125;&#59;&#10;&#125;</code></pre> | List destinations show one empty-state sentence and next step; Analytics shows empty reports. |
| [Case](../entities/destinationEmptyStates.test_Case.md) | Type alias | 169 | <pre><code>&#123;&#10;    name&#58; string&#59;&#10;    path&#58; string&#59;&#10;    page&#58; &#40;&#41; &#61;&#62; ReactElement&#59;&#10;    scenario&#63;&#58; Scenario&#59;&#10;    &#47;&#42;&#42; The copy key the page&#39;s &#40;first&#41; empty state must show&#46; &#42;&#47;&#10;    copy&#63;&#58; string&#59;&#10;    &#47;&#42;&#42; Text typed into the page&#39;s search box before the empty state is read&#46; &#42;&#47;&#10;    typeSearch&#63;&#58; string&#59;&#10;    &#47;&#42;&#42; A list that filters hide&#58; it must offer Clear filters&#46; &#42;&#47;&#10;    filtered&#63;&#58; boolean&#59;&#10;    adminKey&#63;&#58; boolean&#59;&#10;    &#47;&#42;&#42; The agent key the Models tab needs before it reads anything&#46; &#42;&#47;&#10;    agentKey&#63;&#58; boolean&#59;&#10;    &#47;&#42;&#42; Copy keys of controls that must not appear on the page&#58; competing actions of an empty workspace&#46; &#42;&#47;&#10;    absent&#63;&#58; string&#91;&#93;&#59;&#10;    &#47;&#42;&#42; Rendered with the shell&#39;s identity&#44; so the first&#45;run step decides the page&#39;s one next step&#46; &#42;&#47;&#10;    setup&#63;&#58; boolean&#59;&#10;&#125;</code></pre> | — |
| [Language](../entities/Language.md) | Type alias | 252 | `(typeof LANGUAGES)[number]` | — |
