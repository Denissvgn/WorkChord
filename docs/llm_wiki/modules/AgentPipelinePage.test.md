# AgentPipelinePage.test Module

**Path:** `frontend/src/pages/AgentPipelinePage.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/AgentPipelinePage.test.tsx`._

## Imports

| Source | Symbols |
|--------|---------|
| `../i18n/i18n` | `i18n` |
| `../test/renderWithProviders` | `renderWithProviders` |
| `../types/agent` | `AgentPipeline`, `AgentRun`, `TaskTimelineResponse` |
| `../types/task` | `Task` |
| `./AgentPipelinePage` | `AgentPipelinePage` |
| `@testing-library/react` | `screen`, `waitFor` |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `agentServiceMock`, `useAdminAccessMock`, `useAgentAccessMock`, `sensitive`, `taskFixture`, `pipelineFixture`, `timelineFixture` |
| Module calls | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `useAgentAccessMock = hoisted`, `mock`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/i18n/i18n.ts"]
    n1["frontend/src/pages/AgentPipelinePage.test.tsx"]
    n2["frontend/src/pages/AgentPipelinePage.tsx"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n4["frontend/src/types/agent.ts"]
    n5["frontend/src/types/task.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n4
    n1 --> n5
    n2 --> n4
    n2 --> n5
    n4 --> n5
    click n0 "../modules/i18n.md"
    click n1 "../modules/AgentPipelinePage.test.md"
    click n2 "../modules/AgentPipelinePage.md"
    click n3 "../modules/renderWithProviders.md"
    click n4 "../modules/types_agent.md"
    click n5 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [AgentPipelinePage](../modules/AgentPipelinePage.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
