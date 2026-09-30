# TaskRoutingPanel.test Module

**Path:** `frontend/src/components/agent/TaskRoutingPanel.test.tsx`

## Description

_Auto-generated from `frontend/src/components/agent/TaskRoutingPanel.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../../i18n/i18n` | `i18n` |
| `../../test/fixtures/modelAwareRouting` | `modelAwareRoutingPreview`, `modelAwareRoutingRoster` |
| `../../test/renderWithProviders` | `renderWithProviders` |
| `../../types/agent` | `AgentActorRosterItem`, `AgentCapabilities`, `AgentModelBinding`, `AgentModelCatalogEntry`, `AgentRoutingPreviewResponse`, `AgentTaskAssignment`, `TaskRoutingAssessment`, `TaskRoutingAssessmentState` |
| `../../types/task` | `Task` |
| `./TaskRoutingPanel` | `TaskRoutingPanel` |
| `@testing-library/react` | `screen`, `waitFor` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `agentServiceMock`, `useAgentAccessMock`, `taskFixture`, `currentAssessment`, `currentAssessmentState`, `modelCatalog`, `modelBinding`, `dispatchableRoster`, `pendingRecoveryAssignment`, `capabilities` |
| Module calls | `agentServiceMock = hoisted`, `useAgentAccessMock = hoisted`, `mock`, `mock`, `dispatchableRoster = map`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/agent/TaskRoutingPanel.test.tsx"]
    n1["frontend/src/components/agent/TaskRoutingPanel.tsx"]
    n2["frontend/src/i18n/i18n.ts"]
    n3["frontend/src/test/fixtures/modelAwareRouting.ts"]
    n4["frontend/src/test/renderWithProviders.tsx"]
    n5["frontend/src/types/agent.ts"]
    n6["frontend/src/types/task.ts"]
    n0 --> n1
    n0 --> n2
    n0 --> n3
    n0 --> n4
    n0 --> n5
    n0 --> n6
    n1 --> n5
    n1 --> n6
    n3 --> n5
    n5 --> n6
    click n0 "../modules/TaskRoutingPanel.test.md"
    click n1 "../modules/TaskRoutingPanel.md"
    click n2 "../modules/i18n.md"
    click n3 "../modules/modelAwareRouting.md"
    click n4 "../modules/renderWithProviders.md"
    click n5 "../modules/types_agent.md"
    click n6 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [TaskRoutingPanel](../modules/TaskRoutingPanel.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [modelAwareRouting](../modules/modelAwareRouting.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
