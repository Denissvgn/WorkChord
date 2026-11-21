# MilestoneFormState

**Location:** `frontend/src/components/projects/projectDetailShared.ts:111`
**Kind:** Type alias
**Bases:** —
**Module:** [projectDetailShared](../modules/projectDetailShared.md)
**Target:**

```typescript
{
    name: string;
    description: string;
    target_date: string;
    completed_at: string;
    sort_order: string;
    status: ProjectMilestoneStatus;
}
```

## Description

_Auto-generated from `MilestoneFormState` in `frontend/src/components/projects/projectDetailShared.ts`._

## Attributes

*See the alias definition for its member types.*

## Methods

*See the alias definition for callable and member types.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["MilestoneFormState (frontend/src/components/projects/projectDetailShared.ts)"]
    n1["MilestoneFormDrawer (frontend/src/components/projects/MilestoneFormDrawer.tsx)"]
    n2["buildMilestonePayload (frontend/src/components/projects/projectDetailShared.ts)"]
    n3["createEmptyMilestoneForm (frontend/src/components/projects/projectDetailShared.ts)"]
    n4["createMilestoneFormFromRecord (frontend/src/components/projects/projectDetailShared.ts)"]
    n5["frontend/src/pages/ProjectDetailPage.tsx"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/projectDetailShared.md"
    click n1 "../modules/MilestoneFormDrawer.md"
    click n2 "../modules/projectDetailShared.md"
    click n3 "../modules/projectDetailShared.md"
    click n4 "../modules/projectDetailShared.md"
    click n5 "../modules/ProjectDetailPage.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [projectDetailShared](../modules/projectDetailShared.md) | 0 | — |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `MilestoneFormDrawer` | type_reference | [MilestoneFormDrawer](../modules/MilestoneFormDrawer.md) | — |
| `buildMilestonePayload` | type_reference | [projectDetailShared](../modules/projectDetailShared.md) | — |
| `createEmptyMilestoneForm` | type_reference | [projectDetailShared](../modules/projectDetailShared.md) | — |
| `createMilestoneFormFromRecord` | type_reference | [projectDetailShared](../modules/projectDetailShared.md) | — |
| `ProjectDetailPage` | import | [ProjectDetailPage](../modules/ProjectDetailPage.md) | — |
