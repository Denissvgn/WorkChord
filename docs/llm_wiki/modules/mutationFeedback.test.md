# mutationFeedback.test Module

**Path:** `frontend/src/features/mutationFeedback.test.tsx`

## Description

_Auto-generated from `frontend/src/features/mutationFeedback.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `./MutationSuccessFeedback` | `MutationSuccessFeedback` | — | compiler-dependent |
| `./mutationFeedback` | `MutationFeedbackMeta` | Declaration | erased |
| `./mutationFeedback` | `feedbackMessage` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation` | — | compiler-dependent |
| `@testing-library/react` | `screen`, `waitFor` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/features/mutationFeedback.test.tsx"]
    n1["frontend/src/features/mutationFeedback.ts"]
    n2["frontend/src/features/MutationSuccessFeedback.tsx"]
    n3["frontend/src/i18n/i18n.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n2 --> n1
    n4 --> n3
    click n0 "../modules/mutationFeedback.test.md"
    click n1 "../modules/mutationFeedback.md"
    click n2 "../modules/MutationSuccessFeedback.md"
    click n3 "../modules/i18n.md"
    click n4 "../modules/renderWithProviders.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [mutationFeedback](../modules/mutationFeedback.md) |
| Outbound | [MutationSuccessFeedback](../modules/MutationSuccessFeedback.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |
