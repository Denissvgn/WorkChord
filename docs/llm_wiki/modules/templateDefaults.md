# templateDefaults Module

**Path:** `frontend/src/utils/templateDefaults.ts`

## Description

_Auto-generated from `frontend/src/utils/templateDefaults.ts`._

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `appendChecklistToDescription`, `getPayloadBoolean`, `getPayloadNumber`, `getPayloadString`, `mergeLabels` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/projects/ProjectForm.tsx"]
    n1["frontend/src/components/tasks/TaskForm.tsx"]
    n2["frontend/src/pages/TriagePage.tsx"]
    n3["frontend/src/utils/templateDefaults.ts"]
    n0 --> n3
    n1 --> n3
    n2 --> n3
    click n0 "../modules/ProjectForm.md"
    click n1 "../modules/TaskForm.md"
    click n2 "../modules/TriagePage.md"
    click n3 "../modules/templateDefaults.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectForm](../modules/ProjectForm.md) |
| Inbound | [TaskForm](../modules/TaskForm.md) |
| Inbound | [TriagePage](../modules/TriagePage.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `mergeLabels` | `(current: string[] = [], incoming: string[] = [])` | — | — |
| `appendChecklistToDescription` | `(description: string \| null \| undefined, checklist: string[] = [])` | — | — |
| `getPayloadString` | `(payload: Record<string, unknown>, key: string, fallback: string \| null = null)` | — | — |
| `getPayloadBoolean` | `(payload: Record<string, unknown>, key: string, fallback: boolean)` | — | — |
| `getPayloadNumber` | `(payload: Record<string, unknown>, key: string, fallback: number)` | — | — |
