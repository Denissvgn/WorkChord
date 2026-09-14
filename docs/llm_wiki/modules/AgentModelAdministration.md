# AgentModelAdministration Module

**Path:** `frontend/src/components/settings/AgentModelAdministration.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/AgentModelAdministration.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../hooks/useAgentAccess` | `useAgentAccess` |
| `../../services/agentService` | `agentService` |
| `../../types/agent` | `AgentModelBinding`, `AgentModelBindingCreate`, `AgentModelCatalogCreate`, `AgentModelCatalogEntry` |
| `../../utils/apiError` | `normalizeApiError` |
| `../../utils/formatDate` | `formatDateTime` |
| `../../utils/modelRouting` | `createAgentCommandMetadata`, `formatRoutingCode`, `parseRoutingTags` |
| `../../utils/protectedQueries` | `protectedQueryRetry` |
| `../common/Button` | `Button` |
| `../common/Checkbox` | `Checkbox` |
| `../common/Input` | `Input`, `RequiredIndicator` |
| `../common/useConfirmDialog` | `useConfirmDialog` |
| `../feedback/QueryState` | `QueryEmptyState`, `QueryErrorState`, `QueryLoadingState` |
| `../feedback/toast` | `useToast` |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` |
| `lucide-react` | `AlertTriangle`, `Bot`, `Database`, `Link2`, `Pencil`, `Plus`, `RefreshCw`, `ShieldCheck`, `X` |
| `react` | `useMemo`, `useState`, `FormEvent` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `AgentModelAdministration` |
| Constants | `EMPTY_CATALOG_FORM`, `EMPTY_BINDING_FORM` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/settings/AgentModelAdministration.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/AgentModelAdministration.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (2) |
| Outbound | `frontend` (13) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 15 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [CatalogForm](../entities/CatalogForm.md) | Class | 39 | — | — |
| [BindingForm](../entities/BindingForm.md) | Class | 53 | — | — |
| [ConflictResolution](../entities/ConflictResolution.md) | Class | 63 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `AgentModelAdministration` | `()` | — | — |
