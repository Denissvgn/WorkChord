# RouteErrorBoundary Module

**Path:** `frontend/src/components/layout/RouteErrorBoundary.tsx`

## Description

_Auto-generated from `frontend/src/components/layout/RouteErrorBoundary.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/scope/useScopeLink` | `scopeLinkNow` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `lucide-react` | `AlertTriangle`, `Home`, `RefreshCw` | — | compiler-dependent |
| `react` | `ErrorInfo`, `ReactNode` | Specifier | compiler-dependent |
| `react` | `Component` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `RouteErrorBoundary` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/layout/AppShell.tsx"]
    n2["frontend/src/components/layout/BareLayout.tsx"]
    n3["frontend/src/components/layout/RouteErrorBoundary.tsx"]
    n4["frontend/src/features/scope/useScopeLink.ts"]
    n1 --> n3
    n2 --> n3
    n2 --> n4
    n3 --> n0
    n3 --> n4
    click n0 "../modules/Button.md"
    click n1 "../modules/AppShell.md"
    click n2 "../modules/BareLayout.md"
    click n3 "../modules/RouteErrorBoundary.md"
    click n4 "../modules/useScopeLink.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppShell](../modules/AppShell.md) |
| Inbound | [BareLayout](../modules/BareLayout.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [useScopeLink](../modules/useScopeLink.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [RouteErrorBoundary](../entities/RouteErrorBoundary.md) | Class | 19 | `Component<RouteErrorBoundaryProps, RouteErrorBoundaryState>` | — |
| [RouteErrorBoundaryProps](../entities/RouteErrorBoundaryProps.md) | Interface | 6 | — | — |
| [RouteErrorBoundaryState](../entities/RouteErrorBoundaryState.md) | Interface | 15 | — | — |
