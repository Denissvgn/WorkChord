# check-tailwind-classes Module

**Path:** `frontend/scripts/check-tailwind-classes.mjs`

## Description

_Auto-generated from `frontend/scripts/check-tailwind-classes.mjs`._

## Imports

| Source | Symbols |
|--------|---------|
| `../tailwind.config.js` | `tailwindConfig` |
| `node:fs/promises` | `readdir`, `readFile` |
| `node:path` | `extname`, `resolve` |
| `node:url` | `fileURLToPath`, `pathToFileURL` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `semanticRoots`, `colorUtilityPrefixes`, `colorUtilitySource`, `semanticRootSource`, `paletteSource`, `variantSource`, `semanticClassPattern`, `legacyClassPattern`, `rawPaletteClassPattern`, `darkVariantClassPattern`, `arbitraryColorClassPattern`, `translucentSemanticTextPattern`, `configuredColors`, `semanticColorNames` |
| Module calls | `semanticRoots = Set`, `colorUtilityPrefixes = sort`, `colorUtilitySource = join`, `semanticRootSource = join`, `semanticClassPattern = RegExp`, `legacyClassPattern = RegExp`, `rawPaletteClassPattern = RegExp`, `darkVariantClassPattern = RegExp`, `arbitraryColorClassPattern = RegExp`, `translucentSemanticTextPattern = RegExp`, `semanticColorNames = Set` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/scripts/check-tailwind-classes.mjs"]
    n1["frontend/tailwind.config.js"]
    n0 --> n1
    click n0 "../modules/check-tailwind-classes.md"
    click n1 "../modules/tailwind.config.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Outbound | [tailwind.config](../modules/tailwind.config.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `findInvalidSemanticClasses` | `(source, validColorNames = semanticColorNames)` | — | — |
| `validateFiles` | *(async)* `(files)` | — | — |
