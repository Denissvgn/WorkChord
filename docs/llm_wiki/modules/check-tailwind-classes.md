# check-tailwind-classes Module

**Path:** `frontend/scripts/check-tailwind-classes.mjs`

## Description

_Auto-generated from `frontend/scripts/check-tailwind-classes.mjs`._

## Imports

| Source | Symbols |
|--------|---------|
| `node:fs` | `readFileSync` |
| `node:fs/promises` | `readdir`, `readFile` |
| `node:path` | `extname`, `resolve` |
| `node:url` | `pathToFileURL` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `semanticRoots`, `colorUtilityPrefixes`, `colorUtilitySource`, `semanticRootSource`, `paletteSource`, `variantSource`, `semanticClassPattern`, `legacyClassPattern`, `rawPaletteClassPattern`, `darkVariantClassPattern`, `arbitraryColorClassPattern`, `translucentSemanticTextPattern`, `globalsCss`, `semanticColorNames` |
| Module calls | `semanticRoots = Set`, `colorUtilityPrefixes = sort`, `colorUtilitySource = join`, `semanticRootSource = join`, `semanticClassPattern = RegExp`, `legacyClassPattern = RegExp`, `rawPaletteClassPattern = RegExp`, `darkVariantClassPattern = RegExp`, `arbitraryColorClassPattern = RegExp`, `translucentSemanticTextPattern = RegExp`, `globalsCss = readFileSync`, `semanticColorNames = Set` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `themeColorNames` | `(stylesheet)` | — | — |
| `findInvalidSemanticClasses` | `(source, validColorNames = semanticColorNames)` | — | — |
| `validateFiles` | *(async)* `(files)` | — | — |
