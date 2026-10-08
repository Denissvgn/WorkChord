# planningInputMessages Module

**Path:** `frontend/src/i18n/planningInputMessages.ts`

## Description

Planning observation and import messages form a small independent translation namespace. Both locale resources reference it, preserving key parity while keeping the existing route bundle limits unchanged.

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `planningInputEnglish`, `planningInputRussian` |
| Constants | `planningInputEnglish`, `planningInputRussian` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/i18n/planningInputMessages.ts"]
    n1["frontend/src/i18n/resources.en.ts"]
    n2["frontend/src/i18n/resources.ru.ts"]
    n1 --> n0
    n2 --> n0
    click n0 "../modules/planningInputMessages.md"
    click n1 "../modules/resources.en.md"
    click n2 "../modules/resources.ru.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [resources.en](../modules/resources.en.md) |
| Inbound | [resources.ru](../modules/resources.ru.md) |
