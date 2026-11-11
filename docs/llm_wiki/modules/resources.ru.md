# resources.ru Module

**Path:** `frontend/src/i18n/resources.ru.ts`

## Description

_Auto-generated from `frontend/src/i18n/resources.ru.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./agentTeamSetup.ru` | `agentTeamSetupRussian` | — | compiler-dependent |
| `./pagination` | `paginationRU` | — | compiler-dependent |
| `./plan.ru` | `planRussian` | — | compiler-dependent |
| `./planningInputMessages` | `planningInputRussian` | — | compiler-dependent |
| `./teamwork.ru` | `teamworkRussian` | — | compiler-dependent |
| `./timeEntries` | `timeEntriesRU` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `russianResources` |
| Constants | `russianResources` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/i18n/agentTeamSetup.ru.ts"]
    n1["frontend/src/i18n/i18n.test.ts"]
    n2["frontend/src/i18n/pagination.ts"]
    n3["frontend/src/i18n/plan.ru.ts"]
    n4["frontend/src/i18n/planningInputMessages.ts"]
    n5["frontend/src/i18n/resources.ru.ts"]
    n6["frontend/src/i18n/teamwork.ru.ts"]
    n7["frontend/src/i18n/timeEntries.ts"]
    n8["frontend/src/i18n/workflowVocabulary.test.ts"]
    n9["frontend/src/pages/PlanMasterPage.test.tsx"]
    n1 --> n5
    n5 --> n0
    n5 --> n2
    n5 --> n3
    n5 --> n4
    n5 --> n6
    n5 --> n7
    n8 --> n5
    n9 --> n5
    click n0 "../modules/agentTeamSetup.ru.md"
    click n1 "../modules/i18n.test.md"
    click n2 "../modules/pagination.md"
    click n3 "../modules/plan.ru.md"
    click n4 "../modules/planningInputMessages.md"
    click n5 "../modules/resources.ru.md"
    click n6 "../modules/teamwork.ru.md"
    click n7 "../modules/timeEntries.md"
    click n8 "../modules/workflowVocabulary.test.md"
    click n9 "../modules/PlanMasterPage.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [i18n.test](../modules/i18n.test.md) |
| Inbound | [workflowVocabulary.test](../modules/workflowVocabulary.test.md) |
| Inbound | [PlanMasterPage.test](../modules/PlanMasterPage.test.md) |
| Outbound | [agentTeamSetup.ru](../modules/agentTeamSetup.ru.md) |
| Outbound | [pagination](../modules/pagination.md) |
| Outbound | [plan.ru](../modules/plan.ru.md) |
| Outbound | [planningInputMessages](../modules/planningInputMessages.md) |
| Outbound | [teamwork.ru](../modules/teamwork.ru.md) |
| Outbound | [timeEntries](../modules/timeEntries.md) |
