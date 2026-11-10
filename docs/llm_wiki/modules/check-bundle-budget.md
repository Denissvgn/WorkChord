# check-bundle-budget Module

**Path:** `frontend/scripts/check-bundle-budget.mjs`

## Description

_Auto-generated from `frontend/scripts/check-bundle-budget.mjs`._

## Imports

| Source | Symbols |
|--------|---------|
| `node:fs` | `readFileSync`, `writeFileSync` |
| `node:path` | `dirname`, `resolve` |
| `node:url` | `fileURLToPath`, `pathToFileURL` |
| `node:zlib` | `gzipSync` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `BUDGETS`, `isCli` |
| Module calls | `BUDGETS = freeze` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `classifyChunk` | `(manifestEntry)` | — | — |
| `evaluateBudget` | `(assets, budgets = BUDGETS)` | — | — |
| `inspectBundle` | `(distDirectory)` | — | — |
| `run` | `(distDirectory)` | — | — |
