# browser_worker Module

**Path:** `scripts/ci/browser_worker.mjs`

## Description

_Auto-generated from `scripts/ci/browser_worker.mjs`._

## Imports

| Source | Symbols |
|--------|---------|
| `node:child_process` | `execFile` |
| `node:path` | `isAbsolute` |
| `node:util` | `promisify` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["scripts/ci/browser_managed_work.mjs"]
    n1["scripts/ci/browser_worker.mjs"]
    n0 --> n1
    click n0 "../modules/browser_managed_work.md"
    click n1 "../modules/browser_worker.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [browser_managed_work](../modules/browser_managed_work.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `dispatchInbox` | *(async)* `()` | — | — |
| `backupBrowserDatabase` | *(async)* `()` | — | — |
