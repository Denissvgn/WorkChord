# BareLayout Module

**Path:** `frontend/src/components/layout/BareLayout.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/BareLayout.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/scope/useScopeLink` | `useScopeLink` | — | compiler-dependent |
| `../../store/themeStore` | `useThemeStore` | — | compiler-dependent |
| `./BrandMark` | `BrandMark` | — | compiler-dependent |
| `./DocumentMetadata` | `DocumentMetadata` | — | compiler-dependent |
| `./RouteErrorBoundary` | `RouteErrorBoundary` | — | compiler-dependent |
| `react` | `ReactNode` | Specifier | compiler-dependent |
| `react` | `useEffect` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |
| `react-router-dom` | `Link`, `useLocation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `BareLayout` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/App.tsx"]
    n1["frontend/src/components/layout/BareLayout.test.tsx"]
    n2["frontend/src/components/layout/BareLayout.tsx"]
    n3["frontend/src/components/layout/BrandMark.tsx"]
    n4["frontend/src/components/layout/DocumentMetadata.tsx"]
    n5["frontend/src/components/layout/RouteErrorBoundary.tsx"]
    n6["frontend/src/features/scope/useScopeLink.ts"]
    n7["frontend/src/store/themeStore.ts"]
    n0 --> n2
    n0 --> n4
    n1 --> n2
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n2 --> n6
    n2 --> n7
    n5 --> n6
    click n0 "../modules/App.md"
    click n1 "../modules/BareLayout.test.md"
    click n2 "../modules/BareLayout.md"
    click n3 "../modules/BrandMark.md"
    click n4 "../modules/DocumentMetadata.md"
    click n5 "../modules/RouteErrorBoundary.md"
    click n6 "../modules/useScopeLink.md"
    click n7 "../modules/themeStore.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [App](../modules/App.md) |
| Inbound | [BareLayout.test](../modules/BareLayout.test.md) |
| Outbound | [BrandMark](../modules/BrandMark.md) |
| Outbound | [DocumentMetadata](../modules/DocumentMetadata.md) |
| Outbound | [RouteErrorBoundary](../modules/RouteErrorBoundary.md) |
| Outbound | [useScopeLink](../modules/useScopeLink.md) |
| Outbound | [themeStore](../modules/themeStore.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `BareLayout` | `({ children }: { children: ReactNode })` | — | — |
