# RoadmapRow

**Location:** `frontend/src/components/projects/RoadmapView.tsx:42`
**Kind:** Type alias
**Bases:** —
**Module:** [RoadmapView](../modules/RoadmapView.md)
**Target:**

```typescript
{
    project: Project;
    milestones: ProjectMilestone[];
    markers: RoadmapMarker[];
    startDate: Date | null;
    endDate: Date | null;
    spanSource: 'project' | 'single-project-date' | 'milestones' | 'none';
    /** Nothing to draw: no project dates and no dated milestones. */
    isUnscheduled: boolean;
    /** The project has neither a start nor a target date, even if its milestones give it a span. */
    needsDates: boolean;
}
```

## Description

_Auto-generated from `RoadmapRow` in `frontend/src/components/projects/RoadmapView.tsx`._

## Attributes

*See the alias definition for its member types.*

## Methods

*See the alias definition for callable and member types.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [RoadmapView](../modules/RoadmapView.md) | 0 | — |
