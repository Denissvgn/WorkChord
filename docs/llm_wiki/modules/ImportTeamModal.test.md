# ImportTeamModal.test Module

**Path:** `frontend/src/components/team/ImportTeamModal.test.tsx`

## Description

_Auto-generated from `frontend/src/components/team/ImportTeamModal.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `createTestQueryClient`, `renderWithProviders` | — | compiler-dependent |
| `../../types/team` | `TeamMember` | Declaration | erased |
| `./ImportTeamModal` | `ImportTeamModal` | — | compiler-dependent |
| `@testing-library/react` | `act`, `fireEvent`, `screen`, `waitFor` | — | compiler-dependent |
| `vitest` | `afterEach`, `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `planningMock`, `teamServiceMock` |
| Module calls | `planningMock = hoisted`, `mock`, `teamServiceMock = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/team/ImportTeamModal.test.tsx"]
    n1["frontend/src/components/team/ImportTeamModal.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/team.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    click n0 "../modules/ImportTeamModal.test.md"
    click n1 "../modules/ImportTeamModal.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/types_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [ImportTeamModal](../modules/ImportTeamModal.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_team](../modules/types_team.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [ControlledFileReader](../entities/ControlledFileReader.md) | 26 | — | — |
