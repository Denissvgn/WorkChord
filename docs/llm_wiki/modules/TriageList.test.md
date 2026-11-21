# TriageList.test Module

**Path:** `frontend/src/components/triage/TriageList.test.tsx`

## Description

_Auto-generated from `frontend/src/components/triage/TriageList.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../../types/triage` | `TriageItem` | Declaration | erased |
| `./TriageList` | `TriageList` | — | compiler-dependent |
| `@testing-library/react` | `screen` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `item` |
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/triage/TriageList.test.tsx"]
    n1["frontend/src/components/triage/TriageList.tsx"]
    n2["frontend/src/test/renderWithProviders.tsx"]
    n3["frontend/src/types/triage.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n1 --> n3
    click n0 "../modules/TriageList.test.md"
    click n1 "../modules/TriageList.md"
    click n2 "../modules/renderWithProviders.md"
    click n3 "../modules/types_triage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [TriageList](../modules/TriageList.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_triage](../modules/types_triage.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
