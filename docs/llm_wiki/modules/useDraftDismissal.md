# useDraftDismissal Module

**Path:** `frontend/src/components/tasks/useDraftDismissal.ts`

## Description

Mounted-scope guards suppress obsolete close, discard and pending callbacks after an editor is removed. Existing dirty and pending confirmation, before-unload and sign-out controls retain their behavior. The reusable active-mount check also protects late write completions in task, comment and time editors.

## Imports

| Source | Symbols |
|--------|---------|
| `react` | `useCallback`, `useEffect`, `useRef`, `useState` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `useActiveMount`, `useDraftDismissal` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/tasks/useDraftDismissal.ts"]
    n0 --> n1
    click n1 "../modules/useDraftDismissal.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (13) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

> All 13 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useActiveMount` | `()` | — | — |
| `useDraftDismissal` | `(onClose: () => void)` | — | — |