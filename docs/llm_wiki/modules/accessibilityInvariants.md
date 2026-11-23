# accessibilityInvariants Module

**Path:** `frontend/src/test/accessibilityInvariants.ts`

## Description

_Auto-generated from `frontend/src/test/accessibilityInvariants.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `@testing-library/dom` | `getRoles` | — | compiler-dependent |
| `dom-accessibility-api` | `computeAccessibleName` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `accessibleNameViolations`, `headingOrderViolations`, `summaryNameViolations` |
| Constants | `UNIQUE_NAME_ROLES` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/team/AgentManifestWorkflow.test.tsx"]
    n1["frontend/src/test/accessibilityInvariants.test.tsx"]
    n2["frontend/src/test/accessibilityInvariants.ts"]
    n0 --> n2
    n1 --> n2
    click n0 "../modules/AgentManifestWorkflow.test.md"
    click n1 "../modules/accessibilityInvariants.test.md"
    click n2 "../modules/accessibilityInvariants.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AgentManifestWorkflow.test](../modules/AgentManifestWorkflow.test.md) |
| Inbound | [accessibilityInvariants.test](../modules/accessibilityInvariants.test.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [AccessibleNameViolation](../entities/AccessibleNameViolation.md) | Interface | 16 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `accessibleNameViolations` | `(container: HTMLElement) -> AccessibleNameViolation[]` | — | — |
| `headingOrderViolations` | `(container: HTMLElement) -> string[]` | — | Heading levels that skip a level on the way down, in document order. |
| `summaryNameViolations` | `(container: HTMLElement) -> string[]` | — | — |
