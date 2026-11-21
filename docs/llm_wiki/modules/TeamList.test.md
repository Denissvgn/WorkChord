# TeamList.test Module

**Path:** `frontend/src/components/capacity/TeamList.test.tsx`

## Description

_Auto-generated from `frontend/src/components/capacity/TeamList.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/team` | `TeamMember` | Declaration | erased |
| `../iteration/IterationCapacityLine` | `IterationCapacityLine` | — | compiler-dependent |
| `./TeamList` | `TeamList` | — | compiler-dependent |
| `@testing-library/react` | `screen` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `team`, `iterations` |
| Module calls | `team = hoisted`, `mock`, `iterations = hoisted`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/capacity/TeamList.test.tsx"]
    n1["frontend/src/components/capacity/TeamList.tsx"]
    n2["frontend/src/components/iteration/IterationCapacityLine.tsx"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n4["frontend/src/types/team.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n1 --> n4
    click n0 "../modules/TeamList.test.md"
    click n1 "../modules/TeamList.md"
    click n2 "../modules/IterationCapacityLine.md"
    click n3 "../modules/renderWithProviders.md"
    click n4 "../modules/types_team.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [TeamList](../modules/TeamList.md) |
| Outbound | [IterationCapacityLine](../modules/IterationCapacityLine.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_team](../modules/types_team.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
