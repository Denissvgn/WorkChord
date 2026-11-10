# AgentPipelinePage Module

**Path:** `frontend/src/pages/AgentPipelinePage.tsx`

## Description

_Auto-generated from `frontend/src/pages/AgentPipelinePage.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/agent/TaskRoutingPanel` | `TaskRoutingPanel` | — | compiler-dependent |
| `../components/feedback/QueryState` | `QueryEmptyState`, `QueryErrorState`, `QueryLoadingState`, `QueryStaleState` | — | compiler-dependent |
| `../components/settings/AdminAccessGate` | `AdminAccessGate` | — | compiler-dependent |
| `../components/ui` | `MetricGrid`, `PageHeader`, `PageLayout` | — | compiler-dependent |
| `../components/ui/SlideOverDrawer` | `SlideOverDrawer` | — | compiler-dependent |
| `../hooks/useAdminAccess` | `useAdminAccess` | — | compiler-dependent |
| `../hooks/useAgentAccess` | `useAgentAccess` | — | compiler-dependent |
| `../services/agentService` | `agentService` | — | compiler-dependent |
| `../types/agent` | `AgentModelTrustState`, `TaskTimelineItem` | Declaration | erased |
| `../types/task` | `Task`, `TaskStatus` | Declaration | erased |
| `../utils/apiError` | `getApiErrorStatus` | — | compiler-dependent |
| `../utils/formatDate` | `formatDateTime` | — | compiler-dependent |
| `../utils/protectedQueries` | `protectedQueryRetry` | — | compiler-dependent |
| `@tanstack/react-query` | `useQuery` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `framer-motion` | `motion` | — | compiler-dependent |
| `lucide-react` | `CheckCircle2`, `User`, `Calendar`, `Folder`, `RefreshCw`, `Terminal`, `Search`, `Clock`, `AlertTriangle` | — | compiler-dependent |
| `react` | `useMemo`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `EMPTY_PIPELINE`, `TIMELINE_ITEM_LABELS`, `RUN_STATUSES`, `MODEL_TRUST_STATES`, `TASK_STATUSES` |
| Module calls | `RUN_STATUSES = Set`, `MODEL_TRUST_STATES = Set`, `TASK_STATUSES = Set` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/AgentPipelinePage.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/AgentPipelinePage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (1) |
| Outbound | `frontend` (13) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 6 | 0 |

> All 14 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `AgentPipelinePage` | `()` | — | — |
