# AssigneeSelectProps

**Location:** `frontend/src/components/tasks/AssigneeSelect.tsx:5`
**Kind:** Interface
**Bases:** `Omit<ComponentProps<'select'>, 'value' | 'onChange' | 'children' | 'aria-label'>`
**Module:** [AssigneeSelect](../modules/AssigneeSelect.md)

## Description

_Auto-generated from `AssigneeSelectProps` in `frontend/src/components/tasks/AssigneeSelect.tsx`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `'aria-label'` | `string` | Yes | — | — |
| `value` | `number \| null \| undefined` | Yes | — | — |
| `options` | `TaskRowAssigneeOption[]` | Yes | — | — |
| `emptyLabel` | `string` | Yes | — | — |
| `onChange` | `(assigneeId: number \| null) => void` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["AssigneeSelectProps (frontend/src/components/tasks/AssigneeSelect.tsx)"]
    n1["Omit#60;ComponentProps#60;'select'#62;, 'value' | 'onChange' | 'children' | 'aria-label'#62;"]
    n2["AssigneeSelect (frontend/src/components/tasks/AssigneeSelect.tsx)"]
    n0 --> n1
    n2 --> n0
    click n0 "../modules/AssigneeSelect.md"
    click n2 "../modules/AssigneeSelect.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [AssigneeSelect](../modules/AssigneeSelect.md) | 0 | `'aria-label'`, `emptyLabel`, `onChange`, `options`, `value` |

### Structure

| Kind | Entity | Module |
|---|---|---|
| Base | `Omit<ComponentProps<'select'>, 'value' \| 'onChange' \| 'children' \| 'aria-label'>` | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `AssigneeSelect` | type_reference | [AssigneeSelect](../modules/AssigneeSelect.md) | — |
