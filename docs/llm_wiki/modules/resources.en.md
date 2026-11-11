# resources.en Module

**Path:** `frontend/src/i18n/resources.en.ts`

## Description

_Auto-generated from `frontend/src/i18n/resources.en.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./landing.en` | `landingEnglish` | — | compiler-dependent |
| `./pagination` | `paginationEN` | — | compiler-dependent |
| `./planningInputMessages` | `planningInputEnglish` | — | compiler-dependent |
| `./teamwork.en` | `teamworkEnglish` | — | compiler-dependent |
| `./timeEntries` | `timeEntriesEN` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `englishResources` |
| Constants | `englishResources` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/i18n/formatsAndWording.test.ts"]
    n1["frontend/src/i18n/i18n.test.ts"]
    n2["frontend/src/i18n/i18n.ts"]
    n3["frontend/src/i18n/landing.en.ts"]
    n4["frontend/src/i18n/pagination.ts"]
    n5["frontend/src/i18n/planningInputMessages.ts"]
    n6["frontend/src/i18n/resources.en.ts"]
    n7["frontend/src/i18n/teamwork.en.ts"]
    n8["frontend/src/i18n/timeEntries.ts"]
    n9["frontend/src/i18n/workflowVocabulary.test.ts"]
    n10["frontend/src/pages/PlanMasterPage.test.tsx"]
    n0 --> n2
    n0 --> n6
    n1 --> n2
    n1 --> n6
    n2 --> n6
    n6 --> n3
    n6 --> n4
    n6 --> n5
    n6 --> n7
    n6 --> n8
    n9 --> n6
    n10 --> n2
    n10 --> n6
    click n0 "../modules/formatsAndWording.test.md"
    click n1 "../modules/i18n.test.md"
    click n2 "../modules/i18n.md"
    click n3 "../modules/landing.en.md"
    click n4 "../modules/pagination.md"
    click n5 "../modules/planningInputMessages.md"
    click n6 "../modules/resources.en.md"
    click n7 "../modules/teamwork.en.md"
    click n8 "../modules/timeEntries.md"
    click n9 "../modules/workflowVocabulary.test.md"
    click n10 "../modules/PlanMasterPage.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [formatsAndWording.test](../modules/formatsAndWording.test.md) |
| Inbound | [i18n.test](../modules/i18n.test.md) |
| Inbound | [i18n](../modules/i18n.md) |
| Inbound | [workflowVocabulary.test](../modules/workflowVocabulary.test.md) |
| Inbound | [PlanMasterPage.test](../modules/PlanMasterPage.test.md) |
| Outbound | [landing.en](../modules/landing.en.md) |
| Outbound | [pagination](../modules/pagination.md) |
| Outbound | [planningInputMessages](../modules/planningInputMessages.md) |
| Outbound | [teamwork.en](../modules/teamwork.en.md) |
| Outbound | [timeEntries](../modules/timeEntries.md) |
