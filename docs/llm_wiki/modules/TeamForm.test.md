# TeamForm.test Module

**Path:** `frontend/src/components/team/TeamForm.test.tsx`

## Description

_Auto-generated from `frontend/src/components/team/TeamForm.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../test/renderWithProviders` | `renderWithProviders` |
| `../../types/team` | `TeamMember`, `TeamMemberCreate` |
| `./TeamForm` | `TeamForm` |
| `@testing-library/react` | `act`, `screen`, `waitFor` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `planningMock`, `teamServiceMock` |
| Module calls | `planningMock = hoisted`, `mock`, `teamServiceMock = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/team/TeamForm.test.tsx"]
    n1["frontend/src/components/team/TeamForm.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/team.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n3
    click n0 "../modules/TeamForm.test.md"
    click n1 "../modules/TeamForm.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/types_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [TeamForm](../modules/TeamForm.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_team](../modules/types_team.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
