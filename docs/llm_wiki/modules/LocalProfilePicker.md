# LocalProfilePicker Module

**Path:** `frontend/src/features/identity/LocalProfilePicker.tsx`

## Description

Lets a trusted-local browser choose the person profile it works as, or add one with only a name ("Add me"), and clear the choice. It lists person profiles only, saves through `PUT /auth/local-profile`, and calls `onChosen` so the identity is re-read. Used by the account menu in `IdentityProvider.tsx` and by My Work when the queue has no profile. The choice is a label for that browser's queue, never a verified identity.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../components/common/Button` | `Button` | — | compiler-dependent |
| `../../components/common/Select` | `Select` | — | compiler-dependent |
| `../../hooks/useAdminAccess` | `useAdminAccess` | — | compiler-dependent |
| `../../services/teamService` | `teamService` | — | compiler-dependent |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |
| `./OperatorIdentityNotice` | `OperatorIdentityNotice` | — | compiler-dependent |
| `./identityService` | `WorkProfile` | Declaration | erased |
| `./identityService` | `identityService` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery` | — | compiler-dependent |
| `react` | `FormEvent` | Declaration | erased |
| `react` | `useId`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `LocalProfilePicker` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/Select.tsx"]
    n2["frontend/src/features/firstRun/GetStartedPanel.tsx"]
    n3["frontend/src/features/identity/AccountMenu.tsx"]
    n4["frontend/src/features/identity/identityService.ts"]
    n5["frontend/src/features/identity/LocalProfilePicker.tsx"]
    n6["frontend/src/features/identity/OperatorIdentityNotice.tsx"]
    n7["frontend/src/hooks/useAdminAccess.ts"]
    n8["frontend/src/pages/MyWorkPage.tsx"]
    n9["frontend/src/services/teamService.ts"]
    n10["frontend/src/utils/apiError.ts"]
    n2 --> n0
    n2 --> n5
    n3 --> n0
    n3 --> n1
    n3 --> n4
    n3 --> n5
    n3 --> n7
    n3 --> n9
    n3 --> n10
    n5 --> n0
    n5 --> n1
    n5 --> n4
    n5 --> n6
    n5 --> n7
    n5 --> n9
    n5 --> n10
    n6 --> n0
    n8 --> n0
    n8 --> n5
    n8 --> n6
    n8 --> n7
    n8 --> n10
    click n0 "../modules/Button.md"
    click n1 "../modules/Select.md"
    click n2 "../modules/GetStartedPanel.md"
    click n3 "../modules/AccountMenu.md"
    click n4 "../modules/identityService.md"
    click n5 "../modules/LocalProfilePicker.md"
    click n6 "../modules/OperatorIdentityNotice.md"
    click n7 "../modules/useAdminAccess.md"
    click n8 "../modules/MyWorkPage.md"
    click n9 "../modules/teamService.md"
    click n10 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [GetStartedPanel](../modules/GetStartedPanel.md) |
| Inbound | [AccountMenu](../modules/AccountMenu.md) |
| Inbound | [MyWorkPage](../modules/MyWorkPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [Select](../modules/Select.md) |
| Outbound | [identityService](../modules/identityService.md) |
| Outbound | [OperatorIdentityNotice](../modules/OperatorIdentityNotice.md) |
| Outbound | [useAdminAccess](../modules/useAdminAccess.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `LocalProfilePicker` | `({ current, onChosen }: { current: WorkProfile \| null; onChosen: () => void })` | — | Lets a trusted-local session say which person it works as. The choice is |
