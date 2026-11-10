# check-query-feedback Module

**Path:** `frontend/scripts/check-query-feedback.mjs`

## Description

_Auto-generated from `frontend/scripts/check-query-feedback.mjs`._

## Imports

| Source | Symbols |
|--------|---------|
| `node:crypto` | `crypto` |
| `node:fs` | `fs` |
| `node:path` | `path` |
| `node:url` | `fileURLToPath`, `pathToFileURL` |
| `typescript` | `ts` |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `REVIEWED_HOOK_COUNTS`, `HOOK_KINDS`, `REVIEWED_HOOK_FINGERPRINTS`, `isMain` |
| Module calls | `HOOK_KINDS = Map` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
*No internal module dependencies detected.*

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `findHookCalls` | `(source, fileName = 'source.tsx')` | — | Locate React Query hooks through the TypeScript AST so generics, multiline |
| `hookInventoryFingerprint` | `(source, fileName = 'source.tsx')` | — | — |
| `validateNewHookAnnotations` | `(source)` | — | — |
| `checkQueryFeedback` | `(root)` | — | — |
