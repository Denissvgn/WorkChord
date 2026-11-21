# Scenario

**Location:** `frontend/src/pages/destinationEmptyStates.test.tsx:33`
**Kind:** Type alias
**Bases:** —
**Module:** [destinationEmptyStates.test](../modules/destinationEmptyStates.test.md)
**Target:**

```typescript
{
    /** A profile is chosen in this workspace, so the first setup step is past it. */
    profile?: boolean;
    iterations?: unknown[];
    projects?: unknown[];
    triage?: unknown[];
    tasks?: unknown[];
    pipeline?: Record<string, unknown[]>;
    /** The admin-key view of Team models: a key that may administer, and the two lists it shows. */
    models?: { catalog: unknown[]; bindings: unknown[] };
}
```

## Description

List destinations show one empty-state sentence and next step; Analytics shows empty reports.
Filtered lists with no results offer Clear filters and no create action, and empty states
must not link to paths that redirect.

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
| [destinationEmptyStates.test](../modules/destinationEmptyStates.test.md) | 0 | — |
