# emptyStates Module

**Path:** `frontend/src/i18n/emptyStates.ts`

## Description

/**
 * Copy for the empty states of each destination and view. Each state says what appears there in
 * one sentence; its one button comes from the first-run order (see useNextSetupAction).
 */

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `emptyStatesEnglish`, `emptyStatesRussian` |
| Constants | `emptyStatesEnglish`, `emptyStatesRussian` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/i18n/emptyStates.test.ts"]
    n1["frontend/src/i18n/emptyStates.ts"]
    n2["frontend/src/i18n/resources.en.ts"]
    n3["frontend/src/i18n/resources.ru.ts"]
    n0 --> n1
    n2 --> n1
    n3 --> n1
    click n0 "../modules/emptyStates.test.md"
    click n1 "../modules/emptyStates.md"
    click n2 "../modules/resources.en.md"
    click n3 "../modules/resources.ru.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [emptyStates.test](../modules/emptyStates.test.md) |
| Inbound | [resources.en](../modules/resources.en.md) |
| Inbound | [resources.ru](../modules/resources.ru.md) |
