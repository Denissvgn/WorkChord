# single-page-toolbar Module

**Path:** `frontend/eslint-rules/single-page-toolbar.js`

## Description

/**
 * A page has at most one toolbar row. For every value a function returns, this rule works out
 * which `PageToolbar` elements can be on screen together and reports every one after the first.
 *
 * Which component is the toolbar is decided by its binding, not by the name written in JSX:
 * a named import with or without an alias, a default import, a namespace import (`ui.PageToolbar`),
 * a name the imported local module re-exports for it, and constants or wrappers that hold it.
 *
 * Where a toolbar element can be held, the rule follows it: JSX trees and fragments, attributes and
 * render props, variables (every assignment counts, because the rule does not follow control flow),
 * destructuring, object properties, array elements, values added later (`rows.a = …`, `push`),
 * local helper functions and their return values, local components rendered as JSX, and callbacks
 * passed to calls (a `map` or `flatMap` callback renders once per item, so its toolbar counts twice).
 *
 * Only two things are accepted as exclusive: the two arms of one conditional expression, and
 * separate return statements. One member read with a computed key (`views[mode]`) reads one value,
 * so it counts like a conditional over the values it can read. Everything else that the rule cannot
 * prove exclusive is reported, and the message says so.
 *
 * Toolbars inside a component imported from another file are not seen here; the page-chrome check
 * counts them in the rendered page.
 */

## Imports

| Source | Symbols |
|--------|---------|
| `node:fs` | `existsSync`, `readFileSync`, `statSync` |
| `node:path` | `dirname`, `resolve` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `default` |
| Constants | `MESSAGE`, `TOOLBAR`, `CALL`, `DYNAMIC`, `ALL`, `WRAPPERS`, `ELEMENT_FACTORIES`, `MUTATING_METHODS`, `PER_ITEM_METHODS`, `MODULE_EXTENSIONS`, `TOOLBAR_MODULE`, `exportCache`, `rule` |
| Module calls | `CALL = Symbol`, `DYNAMIC = Symbol`, `ALL = Symbol`, `WRAPPERS = Set`, `ELEMENT_FACTORIES = Set`, `MUTATING_METHODS = Set`, `PER_ITEM_METHODS = Set`, `exportCache = Map` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/eslint-rules/single-page-toolbar.js"]
    n1["frontend/eslint.config.js"]
    n1 --> n0
    click n0 "../modules/single-page-toolbar.md"
    click n1 "../modules/eslint.config.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [eslint.config](../modules/eslint.config.md) |
