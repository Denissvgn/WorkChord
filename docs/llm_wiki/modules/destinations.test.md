# destinations.test Module

**Path:** `frontend/src/navigation/destinations.test.ts`

## Description

_Auto-generated from `frontend/src/navigation/destinations.test.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../i18n/resources.en` | `englishResources` | — | compiler-dependent |
| `../i18n/resources.ru` | `russianResources` | — | compiler-dependent |
| `./destinations` | `DESTINATION_GROUPS`, `DESTINATIONS`, `destinationsOwningPath`, `formatDestinationCounter`, `getCounterSource`, `getDestination`, `getDestinationForPath` | — | compiler-dependent |
| `./routeModules` | `metadataForPath`, `routeMetadata` | — | compiler-dependent |
| `node:fs` | `readFileSync` | — | compiler-dependent |
| `node:path` | `resolve` | — | compiler-dependent |
| `vitest` | `describe`, `expect`, `it` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `vocabulary`, `catalogs` |
| Module calls | `describe`, `describe`, `describe`, `describe` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/i18n/resources.en.ts"]
    n1["frontend/src/i18n/resources.ru.ts"]
    n2["frontend/src/navigation/destinations.test.ts"]
    n3["frontend/src/navigation/destinations.ts"]
    n4["frontend/src/navigation/routeModules.ts"]
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n4 --> n3
    click n0 "../modules/resources.en.md"
    click n1 "../modules/resources.ru.md"
    click n2 "../modules/destinations.test.md"
    click n3 "../modules/destinations.md"
    click n4 "../modules/routeModules.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [resources.en](../modules/resources.en.md) |
| Outbound | [resources.ru](../modules/resources.ru.md) |
| Outbound | [destinations](../modules/destinations.md) |
| Outbound | [routeModules](../modules/routeModules.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [Vocabulary](../entities/destinations.test_Vocabulary.md) | Type alias | 19 | `{ destinations: Array<{ id: string; name: { en: string; ru: string } }> }` | — |
