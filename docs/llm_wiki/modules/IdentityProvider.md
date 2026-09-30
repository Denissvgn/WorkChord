# IdentityProvider Module

**Path:** `frontend/src/features/identity/IdentityProvider.tsx`

## Description

_Auto-generated from `frontend/src/features/identity/IdentityProvider.tsx`._

The web shell exposes managed identity, profile and access state. Work queries are partitioned by principal and grants, cleared across account changes, and periodically refreshed. Expiry retains a same-account draft; a task editor provides a reachable sign-in path even when a modal covers the shell.

## Imports

| Source | Symbols |
|--------|---------|
| `../../components/common/Button` | `Button` |
| `../../services/api` | `setSessionIntegrity`, `IDENTITY_EXPIRED_EVENT`, `api` |
| `../../services/teamService` | `teamService` |
| `../../utils/adminAccess` | `clearAdminApiKey`, `ADMIN_API_KEY_CHANGED_EVENT` |
| `../../utils/agentAccess` | `clearAgentApiKey`, `AGENT_API_KEY_CHANGED_EVENT` |
| `../../utils/apiError` | `getApiErrorMessage` |
| `../workQueryFreshness` | `installWorkFreshness` |
| `./identityContext` | `IdentityContext`, `useIdentity` |
| `./identityService` | `identityService`, `WorkspaceIdentity` |
| `@tanstack/react-query` | `QueryClient`, `QueryClientProvider`, `useQuery`, `useQueryClient` |
| `lucide-react` | `LogIn`, `LogOut`, `ShieldCheck`, `User` |
| `react` | `useCallback`, `useEffect`, `useMemo`, `useRef`, `useState`, `ReactNode` |
| `react-i18next` | `useTranslation` |
| `react-router-dom` | `useLocation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `IdentityBadge`, `IdentityProvider` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/UserSessionBadge.tsx"]
    n2["frontend/src/features/identity/identityContext.ts"]
    n3["frontend/src/features/identity/IdentityProvider.tsx"]
    n4["frontend/src/features/identity/identityService.ts"]
    n5["frontend/src/features/workQueryFreshness.ts"]
    n6["frontend/src/main.tsx"]
    n7["frontend/src/services/api.ts"]
    n8["frontend/src/services/teamService.ts"]
    n9["frontend/src/utils/adminAccess.ts"]
    n10["frontend/src/utils/agentAccess.ts"]
    n11["frontend/src/utils/apiError.ts"]
    n1 --> n2
    n1 --> n3
    n2 --> n4
    n3 --> n0
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n3 --> n7
    n3 --> n8
    n3 --> n9
    n3 --> n10
    n3 --> n11
    n4 --> n7
    n6 --> n3
    n6 --> n5
    n7 --> n9
    n7 --> n10
    n8 --> n7
    n9 --> n11
    click n0 "../modules/Button.md"
    click n1 "../modules/UserSessionBadge.md"
    click n2 "../modules/identityContext.md"
    click n3 "../modules/IdentityProvider.md"
    click n4 "../modules/identityService.md"
    click n5 "../modules/workQueryFreshness.md"
    click n6 "../modules/src_main.md"
    click n7 "../modules/api.md"
    click n8 "../modules/teamService.md"
    click n9 "../modules/adminAccess.md"
    click n10 "../modules/agentAccess.md"
    click n11 "../modules/apiError.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [UserSessionBadge](../modules/UserSessionBadge.md) |
| Inbound | [src_main](../modules/src_main.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [identityContext](../modules/identityContext.md) |
| Outbound | [identityService](../modules/identityService.md) |
| Outbound | [workQueryFreshness](../modules/workQueryFreshness.md) |
| Outbound | [api](../modules/api.md) |
| Outbound | [teamService](../modules/teamService.md) |
| Outbound | [adminAccess](../modules/adminAccess.md) |
| Outbound | [agentAccess](../modules/agentAccess.md) |
| Outbound | [apiError](../modules/apiError.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `IdentityProvider` | `({ children }: { children: ReactNode })` | — | — |
| `IdentityBadge` | `()` | — | — |