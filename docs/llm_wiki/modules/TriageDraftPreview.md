# TriageDraftPreview Module

**Path:** `frontend/src/components/triage/TriageDraftPreview.tsx`

## Description

_Auto-generated from `frontend/src/components/triage/TriageDraftPreview.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/task` | `TaskBrief` | Declaration | erased |
| `../../types/triage` | `TriageTaskDraftResponse` | Declaration | erased |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../tasks/taskEditorContract` | `newCriterion` | — | compiler-dependent |
| `./triageUtils` | `t` | — | compiler-dependent |
| `lucide-react` | `AlertCircle`, `Plus` | — | compiler-dependent |
| `react` | `Dispatch`, `SetStateAction` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `TriageDraftPreview` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/tasks/taskEditorContract.ts"]
    n2["frontend/src/components/triage/ConvertTriageDrawer.tsx"]
    n3["frontend/src/components/triage/TriageDraftPreview.tsx"]
    n4["frontend/src/components/triage/triageUtils.ts"]
    n5["frontend/src/types/task.ts"]
    n6["frontend/src/types/triage.ts"]
    n1 --> n5
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n4
    n2 --> n6
    n3 --> n0
    n3 --> n1
    n3 --> n4
    n3 --> n5
    n3 --> n6
    n4 --> n5
    n4 --> n6
    n5 --> n6
    n6 --> n5
    click n0 "../modules/Button.md"
    click n1 "../modules/taskEditorContract.md"
    click n2 "../modules/ConvertTriageDrawer.md"
    click n3 "../modules/TriageDraftPreview.md"
    click n4 "../modules/triageUtils.md"
    click n5 "../modules/types_task.md"
    click n6 "../modules/types_triage.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ConvertTriageDrawer](../modules/ConvertTriageDrawer.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [taskEditorContract](../modules/taskEditorContract.md) |
| Outbound | [triageUtils](../modules/triageUtils.md) |
| Outbound | [types_task](../modules/types_task.md) |
| Outbound | [types_triage](../modules/types_triage.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `TriageDraftPreview` | <pre><code>&#40;&#123; draftPreview&#44; applyDraft&#44; setBrief&#44; description&#44; setDescription&#44; title&#44; setTitle&#44; draftErrorMessage &#125;&#58; &#123;&#10;    draftPreview&#58; TriageTaskDraftResponse &#124; null&#59; applyDraft&#58; &#40;&#41; &#61;&#62; void&#59; setBrief&#58; Dispatch&#60;SetStateAction&#60;TaskBrief&#62;&#62;&#59;&#10;    description&#58; string&#59; setDescription&#58; &#40;value&#58; string &#124; &#40;&#40;previous&#58; string&#41; &#61;&#62; string&#41;&#41; &#61;&#62; void&#59;&#10;    title&#58; string&#59; setTitle&#58; &#40;value&#58; string&#41; &#61;&#62; void&#59; draftErrorMessage&#58; string &#124; null&#59;&#10;&#125;&#41;</code></pre> | — | — |
