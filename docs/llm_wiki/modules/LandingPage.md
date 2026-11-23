# LandingPage Module

**Path:** `frontend/src/pages/LandingPage.tsx`

## Description

_Auto-generated from `frontend/src/pages/LandingPage.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/common/ButtonLink` | `ButtonLink` | — | compiler-dependent |
| `../components/ui` | `PageHeader` | — | compiler-dependent |
| `../features/scope/useScopeLink` | `useScopeLink` | — | compiler-dependent |
| `../styles/landing.css` | — | — | present |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `STAGES` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/ButtonLink.tsx"]
    n1["frontend/src/components/ui/index.ts"]
    n2["frontend/src/features/scope/useScopeLink.ts"]
    n3["frontend/src/pages/LandingPage.test.tsx"]
    n4["frontend/src/pages/LandingPage.tsx"]
    n3 --> n4
    n4 --> n0
    n4 --> n1
    n4 --> n2
    click n0 "../modules/ButtonLink.md"
    click n1 "../modules/index.md"
    click n2 "../modules/useScopeLink.md"
    click n3 "../modules/LandingPage.test.md"
    click n4 "../modules/LandingPage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [LandingPage.test](../modules/LandingPage.test.md) |
| Outbound | [ButtonLink](../modules/ButtonLink.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [useScopeLink](../modules/useScopeLink.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
