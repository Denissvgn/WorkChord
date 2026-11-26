# taskEditorContract Module

**Path:** `frontend/src/components/tasks/taskEditorContract.ts`

## Description

_Auto-generated from `frontend/src/components/tasks/taskEditorContract.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/task` | `Task`, `TaskBrief`, `TaskCreate`, `TaskStatus`, `TaskUpdate` | Declaration | erased |
| `../../utils/apiError` | `getApiErrorMessage` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TASK_EDITOR_FIELD_SCHEMA`, `TaskConflictMetadata`, `TaskEditorAvailability`, `TaskEditorSection`, `TaskEditorServerError`, `TaskEditorValidationCode`, `TaskEditorValidationIssue`, `TaskEditorValues`, `buildTaskEditorDefaults`, `emptyTaskBrief`, `mapTaskEditorServerError`, `newCriterion`, `toTaskCreate`, `toTaskUpdate`, `validateTaskEditor` |
| Constants | `TASK_EDITOR_FIELD_SCHEMA` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend"]
    n1["frontend/src/components/tasks/taskEditorContract.ts"]
    n0 --> n1
    n1 --> n0
    click n1 "../modules/taskEditorContract.md"
```

> Module-level dependencies exceed the generated-diagram limits, so the diagram and table below group them by top-level package. Counts report the number of module neighbors in each package.

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | `frontend` (15) |
| Outbound | `frontend` (2) |

> All 17 module neighbor(s) are summarized by package because the module-level view exceeds the 12-node limit.

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TaskEditorValues](../entities/TaskEditorValues.md) | Interface | 10 | — | — |
| [TaskEditorDefaultsContext](../entities/TaskEditorDefaultsContext.md) | Interface | 38 | — | — |
| [TaskEditorFieldDefinition](../entities/TaskEditorFieldDefinition.md) | Interface | 46 | — | — |
| [TaskEditorValidationIssue](../entities/TaskEditorValidationIssue.md) | Interface | 197 | — | — |
| [TaskConflictMetadata](../entities/TaskConflictMetadata.md) | Interface | 266 | — | — |
| [TaskEditorSection](../entities/TaskEditorSection.md) | Type alias | 4 | `'essential' \| 'planning' \| 'advanced' \| 'internal'` | — |
| [TaskEditorAvailability](../entities/TaskEditorAvailability.md) | Type alias | 5 | <pre><code>&#124; &#39;all&#45;editors&#39;&#10;    &#124; &#39;existing&#45;task&#39;&#10;    &#124; &#39;preserved&#45;metadata&#39;</code></pre> | — |
| [TaskEditorValidationCode](../entities/TaskEditorValidationCode.md) | Type alias | 190 | <pre><code>&#124; &#39;titleRequired&#39;&#10;    &#124; &#39;priorityRange&#39;&#10;    &#124; &#39;effortRequired&#39;&#10;    &#124; &#39;dateOrder&#39;&#10;    &#124; &#39;assigneeOutsideIteration&#39;</code></pre> | — |
| [TaskEditorServerError](../entities/TaskEditorServerError.md) | Type alias | 274 | <pre><code>&#124; &#123;&#10;        kind&#58; &#39;version&#45;conflict&#39;&#59;&#10;        expectedVersion&#58; number&#59;&#10;        currentTask&#58; TaskConflictMetadata&#59;&#10;    &#125;&#10;    &#124; &#123; kind&#58; &#39;generic&#39;&#59; message&#58; string &#125;</code></pre> | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `emptyTaskBrief` | `() -> TaskBrief` | — | — |
| `buildTaskEditorDefaults` | `(context: TaskEditorDefaultsContext = {}) -> TaskEditorValues` | — | — |
| `validateTaskEditor` | `(values: TaskEditorValues, iterationAssigneeIds?: ReadonlySet<number>) -> TaskEditorValidationIssue[]` | — | — |
| `toTaskCreate` | `(values: TaskEditorValues) -> TaskCreate` | — | — |
| `toTaskUpdate` | `(values: TaskEditorValues, options: { includeStatus?: boolean } = {}) -> TaskUpdate` | — | — |
| `mapTaskEditorServerError` | `(error: unknown, fallback: string) -> TaskEditorServerError` | — | — |
| `newCriterion` | `(text = '')` | — | — |
