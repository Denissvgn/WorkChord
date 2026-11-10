# AgentTeamSetupMasterPage Module

**Path:** `frontend/src/pages/AgentTeamSetupMasterPage.tsx`

## Description

The responsive setup workflow keeps current blockers and recovery actions reachable outside the desktop rail. Known mobile blocker codes have English and Russian recovery labels; raw codes remain secondary diagnostics. Unknown codes retain a general recovery instruction and their original diagnostic value. Configuration, package acknowledgment and observed runtime readiness remain distinct. Without a readable status the page shows topology and member counts as unknown, not as empty, and a 401 or 403 becomes a plain key-required message without a retry.

_Auto-generated from `frontend/src/pages/AgentTeamSetupMasterPage.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/layout/Breadcrumbs` | `Breadcrumbs` | — | compiler-dependent |
| `../components/settings/AdminAccessGate` | `AdminAccessGate` | — | compiler-dependent |
| `../components/settings/AgentTeamStepList` | `AgentTeamStepList` | — | compiler-dependent |
| `../components/ui/MasterProgress` | `MasterProgress` | — | compiler-dependent |
| `../features/agentTeamSetup/manifest` | `parseAgentTeamMasterEditor` | — | compiler-dependent |
| `../features/agentTeamSetup/masters` | `AGENT_TEAM_STEP_DEFINITIONS`, `stateTone` | — | compiler-dependent |
| `../features/agentTeamSetup/statusScopes` | `RuntimeReadinessState`, `SessionAuthorityState`, `TopologyConfigurationState` | Specifier | compiler-dependent |
| `../features/agentTeamSetup/statusScopes` | `deriveAgentTeamStatusScopes` | — | compiler-dependent |
| `../features/agentTeamSetup/useAgentTeamReadiness` | `useAgentTeamReadiness` | — | compiler-dependent |
| `../services/agentService` | `agentService` | — | compiler-dependent |
| `../types/agent` | `AgentTeamApplyResponse`, `AgentTeamMaster`, `AgentTeamPlan`, `AgentTeamPlanAction`, `AgentTeamValidation` | Declaration | erased |
| `../utils/focusLifecycle` | `captureFocusOrigin`, `focusOwnedTarget` | — | compiler-dependent |
| `../utils/formatDate` | `formatDateTime` | — | compiler-dependent |
| `@tanstack/react-query` | `useMutation`, `useQueryClient` | — | compiler-dependent |
| `axios` | `axios` | — | compiler-dependent |
| `lucide-react` | `ChevronDown`, `CircleAlert`, `FileJson`, `KeyRound`, `LoaderCircle`, `RefreshCw`, `ShieldCheck` | — | compiler-dependent |
| `react` | `useEffect`, `useMemo`, `useRef`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `topologyTone`, `authorityTone`, `runtimeTone`, `AGENT_TEAM_OPERATION_KEYS`, `AGENT_TEAM_RECONCILIATION_KEYS`, `AGENT_TEAM_APPLY_STATUS_KEYS`, `AGENT_TEAM_APPLY_STATUS_TONES`, `AGENT_TEAM_ACTION_STATUS_KEYS`, `AGENT_TEAM_ACTION_STATUS_TONES` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/pages/AgentTeamSetupMasterPage.tsx"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/AgentTeamSetupMasterPage.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (1) |
| Outbound | `frontend` (12) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 5 | 0 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [WorkflowFocusIntent](../entities/WorkflowFocusIntent.md) | Interface | 130 | — | — |
| [StatusTone](../entities/StatusTone.md) | Type alias | 60 | `'done' \| 'warn' \| 'blocked' \| 'opt' \| 'accent'` | — |
| [AgentTeamActionReceiptStatus](../entities/AgentTeamActionReceiptStatus.md) | Type alias | 127 | `AgentTeamApplyResponse['receipts'][number]['status']` | — |
| [WorkflowFocusTarget](../entities/WorkflowFocusTarget.md) | Type alias | 128 | `'plan' \| 'receipt'` | — |