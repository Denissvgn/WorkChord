# PlanQuickAddCapacity.test Module

**Path:** `frontend/src/components/planning/PlanQuickAddCapacity.test.tsx`

## Description

_Auto-generated from `frontend/src/components/planning/PlanQuickAddCapacity.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/iteration` | `Iteration` | Declaration | erased |
| `../../types/team` | `TeamMember` | Declaration | erased |
| `./PlanQuickAddCapacity` | `PlanQuickAddCapacity` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `team`, `planning`, `iteration` |
| Module calls | `team = hoisted`, `planning = hoisted`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/planning/PlanQuickAddCapacity.test.tsx"]
    n1["frontend/src/components/planning/PlanQuickAddCapacity.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/iteration.ts"]
    n4["frontend/src/types/team.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n1 --> n3
    n1 --> n4
    click n0 "../modules/PlanQuickAddCapacity.test.md"
    click n1 "../modules/PlanQuickAddCapacity.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/types_iteration.md"
    click n4 "../modules/types_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [PlanQuickAddCapacity](../modules/PlanQuickAddCapacity.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_iteration](../modules/types_iteration.md) |
| Outbound | [types_team](../modules/types_team.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
