# sampleProject.fixture Module

**Path:** `frontend/src/features/firstRun/sampleProject.fixture.ts`

## Description

_Auto-generated from `frontend/src/features/firstRun/sampleProject.fixture.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/task` | `TaskBrief` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `sampleProjectFixture` |
| Constants | `english`, `russian` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/features/firstRun/sampleProject.fixture.ts"]
    n1["frontend/src/features/firstRun/sampleProject.test.tsx"]
    n2["frontend/src/features/firstRun/sampleProject.ts"]
    n3["frontend/src/types/task.ts"]
    n0 --> n3
    n1 --> n0
    n1 --> n2
    n2 --> n0
    click n0 "../modules/sampleProject.fixture.md"
    click n1 "../modules/sampleProject.test.md"
    click n2 "../modules/sampleProject.md"
    click n3 "../modules/types_task.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [sampleProject.test](../modules/sampleProject.test.md) |
| Inbound | [sampleProject](../modules/sampleProject.md) |
| Outbound | [types_task](../modules/types_task.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `sampleProjectFixture` | `(language: string, now = new Date())` | — | — |
