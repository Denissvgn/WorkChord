# OutboundWebhooksPanel Module

**Path:** `frontend/src/components/settings/OutboundWebhooksPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/OutboundWebhooksPanel.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../hooks/useAdminAccess` | `useAdminAccess` |
| `../../services/outboundWebhookService` | `outboundWebhookService` |
| `../../types/outboundWebhook` | `OutboundWebhookDelivery`, `OutboundWebhookDeliveryStatus`, `OutboundWebhookTarget`, `OutboundWebhookTargetCreate`, `OutboundWebhookTargetUpdate` |
| `../../utils/adminAccess` | `getAdminAccessErrorMessage` |
| `../../utils/formatDate` | `formatDateTime` |
| `../../utils/protectedQueries` | `protectedQueryRetry` |
| `../common/Button` | `Button` |
| `../common/Checkbox` | `Checkbox` |
| `../common/Input` | `Input` |
| `../common/useConfirmDialog` | `useConfirmDialog` |
| `../feedback/QueryState` | `QueryErrorState` |
| `../feedback/toast` | `useToast` |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` |
| `lucide-react` | `Edit2`, `Loader2`, `Plus`, `RefreshCw`, `Save`, `Send`, `Trash2`, `Webhook`, `X` |
| `react` | `useId`, `useMemo`, `useState`, `FormEvent` |
| `react-i18next` | `useTranslation` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `OutboundWebhooksPanel` |
| Constants | `eventGroups`, `emptyForm`, `statusClasses` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/settings/OutboundWebhooksPanel.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/OutboundWebhooksPanel.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (2) |
| Outbound | `frontend` (12) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

> All 14 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TargetFormState](../entities/TargetFormState.md) | Class | 35 | — | — |
| [TargetFormErrors](../entities/TargetFormErrors.md) | Class | 46 | — | — |
| [EventOption](../entities/EventOption.md) | Class | 53 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `OutboundWebhooksPanel` | `()` | — | — |
