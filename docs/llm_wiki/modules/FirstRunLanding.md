# FirstRunLanding Module

**Path:** `frontend/src/features/firstRun/FirstRunLanding.tsx`

## Description

_Auto-generated from `frontend/src/features/firstRun/FirstRunLanding.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/layout/setupGuideEvents` | `OPEN_SETUP_GUIDE_EVENT` | — | compiler-dependent |
| `../../services/projectService` | `projectService` | — | compiler-dependent |
| `../identity/credentialRemount` | `consumeCredentialRemount` | — | compiler-dependent |
| `./getStartedVisibility` | `useGetStartedVisibility` | — | compiler-dependent |
| `./setupReturn` | `useSetupReturn` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react` | `useEffect`, `useRef` | — | compiler-dependent |
| `react-router-dom` | `useLocation`, `useNavigate`, `useNavigationType` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `FirstRunLanding` |
| Constants | `OVERVIEW_PATH` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/AppShell.tsx"]
    n1["frontend/src/components/layout/setupGuideEvents.ts"]
    n2["frontend/src/features/firstRun/FirstRunLanding.tsx"]
    n3["frontend/src/features/firstRun/GetStartedFlow.test.tsx"]
    n4["frontend/src/features/firstRun/GetStartedPanel.test.tsx"]
    n5["frontend/src/features/firstRun/getStartedVisibility.ts"]
    n6["frontend/src/features/firstRun/setupReturn.ts"]
    n7["frontend/src/features/identity/credentialRemount.ts"]
    n8["frontend/src/features/identity/IdentityProvider.keepRoute.test.tsx"]
    n9["frontend/src/services/projectService.ts"]
    n0 --> n2
    n2 --> n1
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n2 --> n9
    n3 --> n2
    n3 --> n5
    n3 --> n6
    n4 --> n2
    n4 --> n5
    n8 --> n2
    click n0 "../modules/AppShell.md"
    click n1 "../modules/setupGuideEvents.md"
    click n2 "../modules/FirstRunLanding.md"
    click n3 "../modules/GetStartedFlow.test.md"
    click n4 "../modules/GetStartedPanel.test.md"
    click n5 "../modules/getStartedVisibility.md"
    click n6 "../modules/setupReturn.md"
    click n7 "../modules/credentialRemount.md"
    click n8 "../modules/IdentityProvider.keepRoute.test.md"
    click n9 "../modules/projectService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppShell](../modules/AppShell.md) |
| Inbound | [GetStartedFlow.test](../modules/GetStartedFlow.test.md) |
| Inbound | [GetStartedPanel.test](../modules/GetStartedPanel.test.md) |
| Inbound | [IdentityProvider.keepRoute.test](../modules/IdentityProvider.keepRoute.test.md) |
| Outbound | [setupGuideEvents](../modules/setupGuideEvents.md) |
| Outbound | [getStartedVisibility](../modules/getStartedVisibility.md) |
| Outbound | [setupReturn](../modules/setupReturn.md) |
| Outbound | [credentialRemount](../modules/credentialRemount.md) |
| Outbound | [projectService](../modules/projectService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `FirstRunLanding` | `()` | — | Two ways into the Get started panel on Overview. A workspace with no project opens on |
