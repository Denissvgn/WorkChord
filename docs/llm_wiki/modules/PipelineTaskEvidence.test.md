# PipelineTaskEvidence.test Module

**Path:** `frontend/src/pages/PipelineTaskEvidence.test.tsx`

## Description

_Auto-generated from `frontend/src/pages/PipelineTaskEvidence.test.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../components/tasks/PipelineTaskEvidence` | `PipelineTaskEvidence` | — | compiler-dependent |
| `../i18n/i18n` | `i18n` | — | compiler-dependent |
| `../test/renderWithProviders` | `renderWithProviders` | — | compiler-dependent |
| `../types/agent` | `AgentRun`, `TaskTimelineResponse` | Declaration | erased |
| `../types/task` | `Task` | Declaration | erased |
| `@testing-library/react` | `screen`, `waitFor` | — | compiler-dependent |
| `vitest` | `beforeEach`, `describe`, `expect`, `it`, `vi` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `agentServiceMock`, `useAdminAccessMock`, `useAgentAccessMock`, `useKeylessReaderMock`, `sensitive`, `taskFixture`, `timelineFixture` |
| Module calls | `agentServiceMock = hoisted`, `useAdminAccessMock = hoisted`, `useAgentAccessMock = hoisted`, `mock`, `useKeylessReaderMock = hoisted`, `mock`, `mock`, `mock`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/tasks/PipelineTaskEvidence.tsx"]
    n1["frontend/src/i18n/i18n.ts"]
    n2["frontend/src/pages/PipelineTaskEvidence.test.tsx"]
    n3["frontend/src/test/renderWithProviders.tsx"]
    n4["frontend/src/types/agent.ts"]
    n5["frontend/src/types/task.ts"]
    n0 --> n4
    n0 --> n5
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n5
    n3 --> n1
    n4 --> n5
    click n0 "../modules/PipelineTaskEvidence.md"
    click n1 "../modules/i18n.md"
    click n2 "../modules/PipelineTaskEvidence.test.md"
    click n3 "../modules/renderWithProviders.md"
    click n4 "../modules/types_agent.md"
    click n5 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [PipelineTaskEvidence](../modules/PipelineTaskEvidence.md) |
| Outbound | [i18n](../modules/i18n.md) |
| Outbound | [renderWithProviders](../modules/renderWithProviders.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
| Outbound | [types_task](../modules/types_task.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |
