# modelAwareRouting Module

**Path:** `frontend/src/test/fixtures/modelAwareRouting.ts`

## Description

_Auto-generated from `frontend/src/test/fixtures/modelAwareRouting.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/agent` | `AgentActorRosterItem`, `AgentRoutingCandidate`, `AgentRoutingExclusion`, `AgentRoutingPreviewResponse` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `eligibleRoutingCandidate`, `excludedRoutingCandidate`, `modelAwareRoutingPreview`, `modelAwareRoutingRoster` |
| Constants | `eligibleRoutingCandidate`, `excludedRoutingCandidate`, `modelAwareRoutingPreview`, `modelAwareRoutingRoster` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/agent/RoutingCandidateComparison.test.tsx"]
    n1["frontend/src/components/agent/TaskRoutingPanel.test.tsx"]
    n2["frontend/src/pages/TeamPage.transport.test.tsx"]
    n3["frontend/src/test/fixtures/modelAwareRouting.ts"]
    n4["frontend/src/types/agent.ts"]
    n0 --> n3
    n1 --> n3
    n1 --> n4
    n2 --> n3
    n2 --> n4
    n3 --> n4
    click n0 "../modules/RoutingCandidateComparison.test.md"
    click n1 "../modules/TaskRoutingPanel.test.md"
    click n2 "../modules/TeamPage.transport.test.md"
    click n3 "../modules/modelAwareRouting.md"
    click n4 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [RoutingCandidateComparison.test](../modules/RoutingCandidateComparison.test.md) |
| Inbound | [TaskRoutingPanel.test](../modules/TaskRoutingPanel.test.md) |
| Inbound | [TeamPage.transport.test](../modules/TeamPage.transport.test.md) |
| Outbound | [types_agent](../modules/types_agent.md) |
