# resources.ru Module

**Path:** `frontend/src/i18n/resources.ru.ts`

## Description

_Auto-generated from `frontend/src/i18n/resources.ru.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./agentTeamSetup.ru` | `agentTeamSetupRussian` | — | compiler-dependent |
| `./pagination` | `paginationRU` | — | compiler-dependent |
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
    n3["frontend/src/i18n/planningInputMessages.ts"]
    n4["frontend/src/i18n/resources.ru.ts"]
    n5["frontend/src/i18n/teamwork.ru.ts"]
    n6["frontend/src/i18n/timeEntries.ts"]
    n7["frontend/src/i18n/workflowVocabulary.test.ts"]
    n8["frontend/src/pages/PlanMasterPage.test.tsx"]
    n1 --> n4
    n4 --> n0
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n4 --> n6
    n7 --> n4
    n8 --> n4
    click n0 "../modules/agentTeamSetup.ru.md"
    click n1 "../modules/i18n.test.md"
    click n2 "../modules/pagination.md"
    click n3 "../modules/planningInputMessages.md"
    click n4 "../modules/resources.ru.md"
    click n5 "../modules/teamwork.ru.md"
    click n6 "../modules/timeEntries.md"
    click n7 "../modules/workflowVocabulary.test.md"
    click n8 "../modules/PlanMasterPage.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [i18n.test](../modules/i18n.test.md) |
| Inbound | [workflowVocabulary.test](../modules/workflowVocabulary.test.md) |
| Inbound | [PlanMasterPage.test](../modules/PlanMasterPage.test.md) |
| Outbound | [agentTeamSetup.ru](../modules/agentTeamSetup.ru.md) |
| Outbound | [pagination](../modules/pagination.md) |
| Outbound | [planningInputMessages](../modules/planningInputMessages.md) |
| Outbound | [teamwork.ru](../modules/teamwork.ru.md) |
| Outbound | [timeEntries](../modules/timeEntries.md) |
