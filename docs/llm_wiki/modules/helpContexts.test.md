# helpContexts.test Module

**Path:** `frontend/src/navigation/helpContexts.test.ts`

## Description

_Auto-generated from `frontend/src/navigation/helpContexts.test.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../i18n/resources.en` | `englishResources` | — | compiler-dependent |
| `../i18n/resources.ru` | `russianResources` | — | compiler-dependent |
| `./destinations` | `DESTINATIONS` | — | compiler-dependent |
| `./helpContexts` | `getHelpContext` | — | compiler-dependent |
| `node:fs` | `readFileSync` | — | compiler-dependent |
| `node:path` | `resolve` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `vocabulary`, `catalogs` |
| Module calls | `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/i18n/resources.en.ts"]
    n1["frontend/src/i18n/resources.ru.ts"]
    n2["frontend/src/navigation/destinations.ts"]
    n3["frontend/src/navigation/helpContexts.test.ts"]
    n4["frontend/src/navigation/helpContexts.ts"]
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n4 --> n2
    click n0 "../modules/resources.en.md"
    click n1 "../modules/resources.ru.md"
    click n2 "../modules/destinations.md"
    click n3 "../modules/helpContexts.test.md"
    click n4 "../modules/helpContexts.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [resources.en](../modules/resources.en.md) |
| Outbound | [resources.ru](../modules/resources.ru.md) |
| Outbound | [destinations](../modules/destinations.md) |
| Outbound | [helpContexts](../modules/helpContexts.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [Localized](../entities/helpContexts.test_Localized.md) | Type alias | 11 | `{ en: string; ru: string }` | — |
| [VocabularyEntry](../entities/VocabularyEntry.md) | Type alias | 12 | `{ id: string; name: Localized \| string }` | — |
