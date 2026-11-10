# OutboundWebhooksPanel Module

**Path:** `frontend/src/components/settings/OutboundWebhooksPanel.tsx`

## Description

_Auto-generated from `frontend/src/components/settings/OutboundWebhooksPanel.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../hooks/useAdminAccess` | `useAdminAccess` | — | compiler-dependent |
| `../../services/outboundWebhookService` | `outboundWebhookService` | — | compiler-dependent |
| `../../types/outboundWebhook` | `OutboundWebhookDelivery`, `OutboundWebhookDeliveryStatus`, `OutboundWebhookTarget`, `OutboundWebhookTargetCreate`, `OutboundWebhookTargetUpdate` | Declaration | erased |
| `../../utils/adminAccess` | `getAdminAccessErrorMessage` | — | compiler-dependent |
| `../../utils/formatDate` | `formatDateTime` | — | compiler-dependent |
| `../../utils/protectedQueries` | `protectedQueryRetry` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/Checkbox` | `Checkbox` | — | compiler-dependent |
| `../common/Input` | `Input` | — | compiler-dependent |
| `../common/useConfirmDialog` | `useConfirmDialog` | — | compiler-dependent |
| `../feedback/QueryState` | `QueryErrorState` | — | compiler-dependent |
| `../feedback/toast` | `useToast` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQuery`, `useQueryClient` | — | compiler-dependent |
| `lucide-react` | `Edit2`, `Loader2`, `Plus`, `RefreshCw`, `Save`, `Send`, `Trash2`, `Webhook`, `X` | — | compiler-dependent |
| `react` | `FormEvent` | Declaration | erased |
| `react` | `useId`, `useMemo`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `OutboundWebhooksPanel` |
| Constants | `eventGroups`, `emptyForm`, `statusClasses` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

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
| [TargetFormState](../entities/TargetFormState.md) | Interface | 35 | — | — |
| [TargetFormErrors](../entities/TargetFormErrors.md) | Interface | 46 | — | — |
| [EventOption](../entities/EventOption.md) | Interface | 53 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `OutboundWebhooksPanel` | `()` | — | — |
