# TaskRowAssigneeOption

**Location:** `frontend/src/components/tasks/TaskRow.tsx:18`
**Kind:** Interface
**Bases:** —
**Module:** [TaskRow](../modules/TaskRow.md)

## Description

_Auto-generated from `TaskRowAssigneeOption` in `frontend/src/components/tasks/TaskRow.tsx`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `id` | `number` | Yes | — | — |
| `name` | `string` | Yes | — | — |
| `kind` | `'human' \| 'agent' \| 'hybrid'` | No | — | — |
| `profileId` | `number \| null` | No | — | — |
| `agentConnected` | `boolean` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["TaskRowAssigneeOption (frontend/src/components/tasks/TaskRow.tsx)"]
    n1["frontend/src/components/tasks/AssigneeSelect.tsx"]
    n2["frontend/src/components/tasks/TaskList.tsx"]
    n3["agentRowValues (frontend/src/components/tasks/useAgentRowFacts.ts)"]
    n4["assigneeKind (frontend/src/components/tasks/useAgentRowFacts.ts)"]
    n5["frontend/src/components/tasks/useIterationRowData.ts"]
    n6["assigneeOptionsFrom (frontend/src/components/tasks/useTaskRowEdits.ts)"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    n6 --> n0
    click n0 "../modules/TaskRow.md"
    click n1 "../modules/AssigneeSelect.md"
    click n2 "../modules/TaskList.md"
    click n3 "../modules/useAgentRowFacts.md"
    click n4 "../modules/useAgentRowFacts.md"
    click n5 "../modules/useIterationRowData.md"
    click n6 "../modules/useTaskRowEdits.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [TaskRow](../modules/TaskRow.md) | 0 | `agentConnected`, `id`, `kind`, `name`, `profileId` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AssigneeSelect` | import | [AssigneeSelect](../modules/AssigneeSelect.md) | — |
| `TaskList` | import | [TaskList](../modules/TaskList.md) | — |
| `agentRowValues` | type_reference | [useAgentRowFacts](../modules/useAgentRowFacts.md) | — |
| `assigneeKind` | type_reference | [useAgentRowFacts](../modules/useAgentRowFacts.md) | — |
| `useIterationRowData` | import | [useIterationRowData](../modules/useIterationRowData.md) | — |
| `assigneeOptionsFrom` | type_reference | [useTaskRowEdits](../modules/useTaskRowEdits.md) | — |
