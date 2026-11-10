# SystemLanguageProvider Module

**Path:** `frontend/src/i18n/SystemLanguageProvider.tsx`

## Description

_Auto-generated from `frontend/src/i18n/SystemLanguageProvider.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/feedback/QueryState` | `QueryErrorState`, `QueryLoadingState` | — | compiler-dependent |
| `../hooks/useAdminAccess` | `useAdminAccess` | — | compiler-dependent |
| `../services/systemSettingsService` | `systemSettingsService` | — | compiler-dependent |
| `./i18n` | `changeAppLanguage` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `react` | `ReactNode` | Specifier | compiler-dependent |
| `react` | `useEffect` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `SystemLanguageProvider` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/feedback/QueryState.tsx"]
    n1["frontend/src/hooks/useAdminAccess.ts"]
    n2["frontend/src/i18n/i18n.ts"]
    n3["frontend/src/i18n/SystemLanguageProvider.tsx"]
    n4["frontend/src/main.tsx"]
    n5["frontend/src/services/systemSettingsService.ts"]
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n5
    n4 --> n2
    n4 --> n3
    click n0 "../modules/QueryState.md"
    click n1 "../modules/useAdminAccess.md"
    click n2 "../modules/i18n.md"
    click n3 "../modules/SystemLanguageProvider.md"
    click n4 "../modules/src_main.md"
    click n5 "../modules/systemSettingsService.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [src_main](../modules/src_main.md) |
| Outbound | [QueryState](../modules/QueryState.md) |
| Outbound | [useAdminAccess](../modules/useAdminAccess.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [systemSettingsService](../modules/systemSettingsService.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [SystemLanguageProviderProps](../entities/SystemLanguageProviderProps.md) | Interface | 9 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `SystemLanguageProvider` | `({ children }: SystemLanguageProviderProps)` | — | — |
