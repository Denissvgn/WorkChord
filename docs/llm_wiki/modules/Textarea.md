# Textarea Module

**Path:** `frontend/src/components/common/Textarea.tsx`

## Description

_Auto-generated from `frontend/src/components/common/Textarea.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./Input` | `RequiredIndicator` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `react` | `ReactNode`, `TextareaHTMLAttributes` | Declaration | erased |
| `react` | `forwardRef`, `useId` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `Textarea` |
| Constants | `Textarea` |
| Module calls | `Textarea = forwardRef` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/common/Input.tsx"]
    n1["frontend/src/components/common/Select.test.tsx"]
    n2["frontend/src/components/common/Textarea.tsx"]
    n3["frontend/src/components/projects/InitiativeForm.tsx"]
    n4["frontend/src/components/projects/ProjectForm.tsx"]
    n5["frontend/src/components/settings/QualificationKeysPanel.tsx"]
    n6["frontend/src/components/tasks/TaskPostponeForm.tsx"]
    n7["frontend/src/components/tasks/TaskPostponementPanel.tsx"]
    n8["frontend/src/components/tasks/useSavedViewManager.tsx"]
    n9["frontend/src/components/triage/CreateTriageDrawer.tsx"]
    n1 --> n2
    n2 --> n0
    n3 --> n0
    n3 --> n2
    n4 --> n0
    n4 --> n2
    n5 --> n0
    n5 --> n2
    n6 --> n2
    n7 --> n2
    n8 --> n0
    n8 --> n2
    n9 --> n0
    n9 --> n2
    click n0 "../modules/Input.md"
    click n1 "../modules/Select.test.md"
    click n2 "../modules/Textarea.md"
    click n3 "../modules/InitiativeForm.md"
    click n4 "../modules/ProjectForm.md"
    click n5 "../modules/QualificationKeysPanel.md"
    click n6 "../modules/TaskPostponeForm.md"
    click n7 "../modules/TaskPostponementPanel.md"
    click n8 "../modules/useSavedViewManager.md"
    click n9 "../modules/CreateTriageDrawer.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [Select.test](../modules/Select.test.md) |
| Inbound | [InitiativeForm](../modules/InitiativeForm.md) |
| Inbound | [ProjectForm](../modules/ProjectForm.md) |
| Inbound | [QualificationKeysPanel](../modules/QualificationKeysPanel.md) |
| Inbound | [TaskPostponeForm](../modules/TaskPostponeForm.md) |
| Inbound | [TaskPostponementPanel](../modules/TaskPostponementPanel.md) |
| Inbound | [useSavedViewManager](../modules/useSavedViewManager.md) |
| Inbound | [CreateTriageDrawer](../modules/CreateTriageDrawer.md) |
| Outbound | [Input](../modules/Input.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [TextareaProps](../entities/TextareaProps.md) | Interface | 6 | `TextareaHTMLAttributes<HTMLTextAreaElement>` | — |
