# browser_managed_work Module

**Path:** `scripts/ci/browser_managed_work.mjs`

## Description

_Auto-generated from `scripts/ci/browser_managed_work.mjs`._

## Imports

| Source | Symbols |
|--------|---------|
| `./browser_worker.mjs` | `dispatchInbox`, `backupBrowserDatabase` |
| `node:assert/strict` | `assert` |
| `node:fs/promises` | `writeFile` |
| `node:path` | `join` |
| `playwright` | `chromium` |
| Unresolved `dynamic-import` | — (line 425; deferred) |
| Unresolved `dynamic-import` | — (line 450; deferred) |
| Unresolved `dynamic-import` | — (line 453; deferred) |
| Unresolved `dynamic-import` | — (line 458; deferred) |
| Unresolved `dynamic-import` | — (line 496) |

## Module Signals

| Signal | Values |
|--------|--------|
| Constants | `baseURL`, `artifacts`, `issuer`, `browser`, `context`, `page`, `errors`, `steps` |
| Module calls | `on`, `on` |

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
| Outbound | [browser_worker](../modules/browser_worker.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 1 |
