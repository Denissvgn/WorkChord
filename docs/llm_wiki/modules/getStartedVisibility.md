# getStartedVisibility Module

**Path:** `frontend/src/features/firstRun/getStartedVisibility.ts`

## Description

_Auto-generated from `frontend/src/features/firstRun/getStartedVisibility.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `zustand` | `create` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `GET_STARTED_DISMISSED_KEY`, `GetStartedRequest`, `readGetStartedDismissed`, `useGetStartedVisibility` |
| Constants | `GET_STARTED_DISMISSED_KEY`, `useGetStartedVisibility` |
| Module calls | `useGetStartedVisibility = create` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/features/firstRun/FirstRunLanding.tsx"]
    n1["frontend/src/features/firstRun/GetStartedFlow.test.tsx"]
    n2["frontend/src/features/firstRun/GetStartedPanel.test.tsx"]
    n3["frontend/src/features/firstRun/GetStartedPanel.tsx"]
    n4["frontend/src/features/firstRun/getStartedVisibility.ts"]
    n5["frontend/src/features/firstRun/useGetStarted.ts"]
    n6["frontend/src/pages/destinationEmptyStates.test.tsx"]
    n7["frontend/src/pages/OverviewPage.test.tsx"]
    n0 --> n4
    n1 --> n0
    n1 --> n4
    n2 --> n0
    n2 --> n4
    n3 --> n4
    n5 --> n4
    n6 --> n4
    n7 --> n4
    click n0 "../modules/FirstRunLanding.md"
    click n1 "../modules/GetStartedFlow.test.md"
    click n2 "../modules/GetStartedPanel.test.md"
    click n3 "../modules/GetStartedPanel.md"
    click n4 "../modules/getStartedVisibility.md"
    click n5 "../modules/useGetStarted.md"
    click n6 "../modules/destinationEmptyStates.test.md"
    click n7 "../modules/OverviewPage.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [FirstRunLanding](../modules/FirstRunLanding.md) |
| Inbound | [GetStartedFlow.test](../modules/GetStartedFlow.test.md) |
| Inbound | [GetStartedPanel.test](../modules/GetStartedPanel.test.md) |
| Inbound | [GetStartedPanel](../modules/GetStartedPanel.md) |
| Inbound | [useGetStarted](../modules/useGetStarted.md) |
| Inbound | [destinationEmptyStates.test](../modules/destinationEmptyStates.test.md) |
| Inbound | [OverviewPage.test](../modules/OverviewPage.test.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [GetStartedVisibility](../entities/GetStartedVisibility.md) | Interface | 39 | — | — |
| [GetStartedRequest](../entities/GetStartedRequest.md) | Type alias | 37 | `false \| 'pending' \| 'incomplete' \| 'complete'` | Reopened from Help. `pending` until the steps are known; `incomplete` lasts until setup is |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `readGetStartedDismissed` | `() -> boolean` | — | — |
