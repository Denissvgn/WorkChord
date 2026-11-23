# useGetStarted Module

**Path:** `frontend/src/features/firstRun/useGetStarted.ts`

## Description

_Auto-generated from `frontend/src/features/firstRun/useGetStarted.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./getStartedVisibility` | `useGetStartedVisibility` | — | compiler-dependent |
| `./sampleProjectStore` | `useSampleProject` | — | compiler-dependent |
| `./useFirstRunProgress` | `useFirstRunProgress` | — | compiler-dependent |
| `react` | `useEffect` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `useGetStarted` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/firstRun/getStartedVisibility.ts"]
    n1["frontend/src/features/firstRun/sampleProjectStore.ts"]
    n2["frontend/src/features/firstRun/useFirstRunProgress.ts"]
    n3["frontend/src/features/firstRun/useGetStarted.ts"]
    n4["frontend/src/pages/OverviewPage.tsx"]
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n4 --> n3
    click n0 "../modules/getStartedVisibility.md"
    click n1 "../modules/sampleProjectStore.md"
    click n2 "../modules/useFirstRunProgress.md"
    click n3 "../modules/useGetStarted.md"
    click n4 "../modules/OverviewPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [OverviewPage](../modules/OverviewPage.md) |
| Outbound | [getStartedVisibility](../modules/getStartedVisibility.md) |
| Outbound | [sampleProjectStore](../modules/sampleProjectStore.md) |
| Outbound | [useFirstRunProgress](../modules/useFirstRunProgress.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useGetStarted` | `()` | — | Whether Overview shows the Get started panel: once every step's state is known, while setup |
