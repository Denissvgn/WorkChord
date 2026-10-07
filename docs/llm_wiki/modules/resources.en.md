# resources.en Module

**Path:** `frontend/src/i18n/resources.en.ts`

## Description

_Auto-generated from `frontend/src/i18n/resources.en.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `./pagination` | `paginationEN` |
| `./teamwork.en` | `teamworkEnglish` |
| `./timeEntries` | `timeEntriesEN` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `englishResources` |
| Constants | `englishResources` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/i18n/i18n.test.ts"]
    n1["frontend/src/i18n/i18n.ts"]
    n2["frontend/src/i18n/pagination.ts"]
    n3["frontend/src/i18n/resources.en.ts"]
    n4["frontend/src/i18n/teamwork.en.ts"]
    n5["frontend/src/i18n/timeEntries.ts"]
    n6["frontend/src/pages/PlanMasterPage.test.tsx"]
    n0 --> n1
    n0 --> n3
    n1 --> n3
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n6 --> n1
    n6 --> n3
    click n0 "../modules/i18n.test.md"
    click n1 "../modules/i18n.md"
    click n2 "../modules/pagination.md"
    click n3 "../modules/resources.en.md"
    click n4 "../modules/teamwork.en.md"
    click n5 "../modules/timeEntries.md"
    click n6 "../modules/PlanMasterPage.test.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [i18n.test](../modules/i18n.test.md) |
| Inbound | [i18n](../modules/i18n.md) |
| Inbound | [PlanMasterPage.test](../modules/PlanMasterPage.test.md) |
| Outbound | [pagination](../modules/pagination.md) |
| Outbound | [teamwork.en](../modules/teamwork.en.md) |
| Outbound | [timeEntries](../modules/timeEntries.md) |
