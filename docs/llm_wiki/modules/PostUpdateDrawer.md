# PostUpdateDrawer Module

**Path:** `frontend/src/components/projects/PostUpdateDrawer.tsx`

## Description

_Auto-generated from `frontend/src/components/projects/PostUpdateDrawer.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/project` | `ProjectHealth` | Declaration | erased |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../common/DisabledReason` | `DisabledReason` | — | compiler-dependent |
| `../common/Input` | `RequiredIndicator` | — | compiler-dependent |
| `../ui` | `SlideOverDrawer` | — | compiler-dependent |
| `./projectDetailShared` | `ProjectUpdateFormState` | Specifier | compiler-dependent |
| `./projectDetailShared` | `healthDotClass`, `healthLabelKeys`, `healthToTone`, `t`, `textareaClassName` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `AlertTriangle`, `Send` | — | compiler-dependent |
| `react` | `FormEvent` | Declaration | erased |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PostUpdateDrawer` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/common/DisabledReason.tsx"]
    n2["frontend/src/components/common/Input.tsx"]
    n3["frontend/src/components/projects/PostUpdateDrawer.tsx"]
    n4["frontend/src/components/projects/projectDetailShared.ts"]
    n5["frontend/src/components/ui/index.ts"]
    n6["frontend/src/pages/ProjectDetailPage.tsx"]
    n7["frontend/src/types/project.ts"]
    n3 --> n0
    n3 --> n1
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n3 --> n7
    n4 --> n7
    n6 --> n0
    n6 --> n3
    n6 --> n4
    n6 --> n5
    n6 --> n7
    click n0 "../modules/Button.md"
    click n1 "../modules/DisabledReason.md"
    click n2 "../modules/Input.md"
    click n3 "../modules/PostUpdateDrawer.md"
    click n4 "../modules/projectDetailShared.md"
    click n5 "../modules/index.md"
    click n6 "../modules/ProjectDetailPage.md"
    click n7 "../modules/types_project.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [DisabledReason](../modules/DisabledReason.md) |
| Outbound | [Input](../modules/Input.md) |
| Outbound | [projectDetailShared](../modules/projectDetailShared.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [types_project](../modules/types_project.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `PostUpdateDrawer` | <pre><code>&#40;&#123;&#10;    open&#44;&#10;    onClose&#44;&#10;    form&#44;&#10;    error&#44;&#10;    isPending&#44;&#10;    setField&#44;&#10;    onSubmit&#44;&#10;    onDismissError&#44;&#10;    summaryIsBlank&#44;&#10;    projectName&#44;&#10;&#125;&#58; &#123;&#10;    open&#58; boolean&#59;&#10;    onClose&#58; &#40;&#41; &#61;&#62; void&#59;&#10;    form&#58; ProjectUpdateFormState&#59;&#10;    error&#58; string &#124; null&#59;&#10;    isPending&#58; boolean&#59;&#10;    setField&#58; &#60;K extends keyof ProjectUpdateFormState&#62;&#40;field&#58; K&#44; value&#58; ProjectUpdateFormState&#91;K&#93;&#41; &#61;&#62; void&#59;&#10;    onSubmit&#58; &#40;event&#58; FormEvent&#60;HTMLFormElement&#62;&#41; &#61;&#62; void&#59;&#10;    onDismissError&#58; &#40;&#41; &#61;&#62; void&#59;&#10;    summaryIsBlank&#58; boolean&#59;&#10;    projectName&#58; string&#59;&#10;&#125;&#41;</code></pre> | — | — |
