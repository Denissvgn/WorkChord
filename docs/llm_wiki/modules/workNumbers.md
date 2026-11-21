# workNumbers Module

**Path:** `frontend/src/utils/workNumbers.ts`

## Description

/**
 * One way to write work numbers everywhere: counts, decimals, percent and effort
 * in days, in the reader's locale. A missing value returns null so the caller says
 * "unknown" in words instead of showing 0.
 */

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `formatCount`, `formatDecimal`, `formatEffortDays`, `formatPercent` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/utils/workNumbers.ts"]
    n0 --> n1
    click n1 "../modules/workNumbers.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (14) |

> All 14 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `formatCount` | `(value: number \| null \| undefined, locale: string)` | — | — |
| `formatDecimal` | `(value: number \| null \| undefined, locale: string, digits = 1)` | — | — |
| `formatPercent` | `(value: number \| null \| undefined, locale: string)` | — | `value` is 0–100, as the server reports completion. |
| `formatEffortDays` | `(value: number \| null \| undefined, locale: string)` | — | — |
