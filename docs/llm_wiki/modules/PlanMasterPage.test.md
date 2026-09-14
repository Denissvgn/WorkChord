# PlanMasterPage.test Module

**Path:** `frontend/src/pages/PlanMasterPage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/PlanMasterPage.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../features/planningMasters/masters` | `deriveStatus`, `EMPTY_READINESS`, `nextStep`, `readiness`, `PlanReadiness` |
| `../features/planningMasters/usePlanningReadiness` | `PlanningQueryFeedback` |
| `../i18n/i18n` | `i18n` |
| `../i18n/resources.en` | `englishResources` |
| `../i18n/resources.ru` | `russianResources` |
| `../test/accessibilityInvariants` | `accessibleNameViolations` |
| `../test/renderWithProviders` | `renderWithProviders` |
| `../types/iteration` | `Iteration` |
| `../types/task` | `Task` |
| `./PlanMasterPage` | `PlanMasterPage` |
| `./PlanMasterPage.tsx?raw` | `planMasterSource` |
| `@testing-library/react` | `act`, `screen`, `waitFor`, `within` |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `planningReadinessMock`, `planShareServiceMock`, `iteration`, `member` |
| Module calls | `planningReadinessMock = hoisted`, `planShareServiceMock = hoisted`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/planningMasters/masters.ts"]
    n1["frontend/src/features/planningMasters/usePlanningReadiness.ts"]
    n2["frontend/src/i18n/i18n.ts"]
    n3["frontend/src/i18n/resources.en.ts"]
    n4["frontend/src/i18n/resources.ru.ts"]
    n5["frontend/src/pages/PlanMasterPage.test.tsx"]
    n6["frontend/src/pages/PlanMasterPage.tsx"]
    n7["frontend/src/test/accessibilityInvariants.ts"]
    n8["frontend/src/test/renderWithProviders.tsx"]
    n9["frontend/src/types/iteration.ts"]
    n10["frontend/src/types/task.ts"]
    n1 --> n0
    n1 --> n9
    n1 --> n10
    n2 --> n3
    n5 --> n0
    n5 --> n1
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n6
    n5 --> n7
    n5 --> n8
    n5 --> n9
    n5 --> n10
    n6 --> n0
    n6 --> n1
    click n0 "../modules/planningMasters_masters.md"
    click n1 "../modules/usePlanningReadiness.md"
    click n2 "../modules/i18n.md"
    click n3 "../modules/resources.en.md"
    click n4 "../modules/resources.ru.md"
    click n5 "../modules/PlanMasterPage.test.md"
    click n6 "../modules/PlanMasterPage.md"
    click n7 "../modules/accessibilityInvariants.md"
    click n8 "../modules/renderWithProviders.md"
    click n9 "../modules/types_iteration.md"
    click n10 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [planningMasters_masters](../modules/planningMasters_masters.md) |
| Outbound | [usePlanningReadiness](../modules/usePlanningReadiness.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [resources.en](../modules/resources.en.md) |
| Outbound | [resources.ru](../modules/resources.ru.md) |
| Outbound | [PlanMasterPage](../modules/PlanMasterPage.md) |
| Outbound | [accessibilityInvariants](../modules/accessibilityInvariants.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [QueryKey](../entities/QueryKey.md) | Type alias | 35 | — | — |
| [PlanningMember](../entities/PlanningMember.md) | Type alias | 36 | — | — |
