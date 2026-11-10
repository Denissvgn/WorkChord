# TeamProfileManager.test Module

**Path:** `frontend/src/components/team/TeamProfileManager.test.tsx`

## Description

_Auto-generated from `frontend/src/components/team/TeamProfileManager.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/team` | `TeamMemberProfile`, `TeamMemberProfileCreate`, `TeamMemberProfileUpdate` | Declaration | erased |
| `./TeamProfileManager` | `TeamProfileManager` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor`, `within` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `teamServiceMock`, `planningMock` |
| Module calls | `teamServiceMock = hoisted`, `planningMock = hoisted`, `mock`, `mock`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/team/TeamProfileManager.test.tsx"]
    n1["frontend/src/components/team/TeamProfileManager.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/team.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n3
    click n0 "../modules/TeamProfileManager.test.md"
    click n1 "../modules/TeamProfileManager.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/types_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [TeamProfileManager](../modules/TeamProfileManager.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_team](../modules/types_team.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
