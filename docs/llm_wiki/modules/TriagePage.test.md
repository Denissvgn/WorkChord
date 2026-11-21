# TriagePage.test Module

**Path:** `frontend/src/pages/TriagePage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/TriagePage.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/tasks/TaskForm` | `TaskForm` | — | compiler-dependent |
| `../components/triage/ConvertTriageDrawer` | `ConvertTriageDrawer` | — | compiler-dependent |
| `../components/triage/TriageActionModal` | `TriageActionModal` | — | compiler-dependent |
| `../test/pageChrome` | `expectPageChrome` | — | compiler-dependent |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../types/iteration` | `Iteration` | Declaration | erased |
| `../types/project` | `Project` | Declaration | erased |
| `../types/triage` | `TriageItem` | Declaration | erased |
| `./TriagePage` | `TriagePage` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `node:fs` | `readdirSync`, `readFileSync` | — | compiler-dependent |
| `node:path` | `resolve` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `api`, `project`, `iteration`, `item`, `secondItem` |
| Module calls | `api = hoisted`, `mock`, `beforeEach`, `describe`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/TaskForm.tsx"]
    n1["frontend/src/components/triage/ConvertTriageDrawer.tsx"]
    n2["frontend/src/components/triage/TriageActionModal.tsx"]
    n3["frontend/src/pages/TriagePage.test.tsx"]
    n4["frontend/src/pages/TriagePage.tsx"]
    n5["frontend/src/test/pageChrome.ts"]
    n6["frontend/src/test/renderWithProviders.tsx"]
    n7["frontend/src/types/iteration.ts"]
    n8["frontend/src/types/project.ts"]
    n9["frontend/src/types/triage.ts"]
    n0 --> n7
    n0 --> n9
    n1 --> n7
    n1 --> n8
    n1 --> n9
    n2 --> n7
    n2 --> n9
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n4 --> n1
    n4 --> n2
    n4 --> n9
    click n0 "../modules/TaskForm.md"
    click n1 "../modules/ConvertTriageDrawer.md"
    click n2 "../modules/TriageActionModal.md"
    click n3 "../modules/TriagePage.test.md"
    click n4 "../modules/TriagePage.md"
    click n5 "../modules/pageChrome.md"
    click n6 "../modules/renderWithProviders.md"
    click n7 "../modules/types_iteration.md"
    click n8 "../modules/types_project.md"
    click n9 "../modules/types_triage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [TaskForm](../modules/TaskForm.md) |
| Outbound | [ConvertTriageDrawer](../modules/ConvertTriageDrawer.md) |
| Outbound | [TriageActionModal](../modules/TriageActionModal.md) |
| Outbound | [TriagePage](../modules/TriagePage.md) |
| Outbound | [pageChrome](../modules/pageChrome.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [types_project](../modules/types_project.md) |
| Outbound | [types_triage](../modules/types_triage.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
