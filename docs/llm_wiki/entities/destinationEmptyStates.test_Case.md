# Case

**Location:** `frontend/src/pages/destinationEmptyStates.test.tsx:169`
**Kind:** Type alias
**Bases:** —
**Module:** [destinationEmptyStates.test](../modules/destinationEmptyStates.test.md)
**Target:**

```typescript
{
    name: string;
    path: string;
    page: () => ReactElement;
    scenario?: Scenario;
    /** The copy key the page's (first) empty state must show. */
    copy?: string;
    /** Text typed into the page's search box before the empty state is read. */
    typeSearch?: string;
    /** A list that filters hide: it must offer Clear filters. */
    filtered?: boolean;
    adminKey?: boolean;
    /** The agent key the Models tab needs before it reads anything. */
    agentKey?: boolean;
    /** Copy keys of controls that must not appear on the page: competing actions of an empty workspace. */
    absent?: string[];
    /** Rendered with the shell's identity, so the first-run step decides the page's one next step. */
    setup?: boolean;
}
```

## Description

_Auto-generated from `Case` in `frontend/src/pages/destinationEmptyStates.test.tsx`._

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
