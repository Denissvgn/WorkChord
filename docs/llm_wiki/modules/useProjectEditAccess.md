# useProjectEditAccess Module

**Path:** `frontend/src/features/identity/useProjectEditAccess.ts`

## Description

Hook that mirrors the server's edit rule for a project (operator or owner, trusted local mode, or an editor or manager project role; never an observer or an agent) so editing controls are offered only to people the server accepts, and exposes the server feature flags, including the one for retargeting a prerequisite. The server stays the authority.

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `./identityContext` | `useIdentity` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `PREREQUISITE_RETARGET_FEATURE`, `useProjectEditAccess`, `useProjectManageAccess` |
| Constants | `PREREQUISITE_RETARGET_FEATURE` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/tasks/DeliveryDependencies.tsx"]
    n1["frontend/src/components/tasks/GitHubReconciliationPanel.tsx"]
    n2["frontend/src/components/tasks/TaskWorkPanel.tsx"]
    n3["frontend/src/features/identity/identityContext.ts"]
    n4["frontend/src/features/identity/useProjectEditAccess.ts"]
    n0 --> n4
    n1 --> n4
    n2 --> n3
    n2 --> n4
    n4 --> n3
    click n0 "../modules/DeliveryDependencies.md"
    click n1 "../modules/GitHubReconciliationPanel.md"
    click n2 "../modules/TaskWorkPanel.md"
    click n3 "../modules/identityContext.md"
    click n4 "../modules/useProjectEditAccess.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [DeliveryDependencies](../modules/DeliveryDependencies.md) |
| Inbound | [GitHubReconciliationPanel](../modules/GitHubReconciliationPanel.md) |
| Inbound | [TaskWorkPanel](../modules/TaskWorkPanel.md) |
| Outbound | [identityContext](../modules/identityContext.md) |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `useProjectManageAccess` | `(projectId: number \| null \| undefined)` | — | Whether the signed-in person may decide in a project (replace or supersede work), mirroring the server rule: |
| `useProjectEditAccess` | `(projectId: number \| null \| undefined)` | — | Whether the signed-in person may edit in a project, mirroring the server rule so controls are |
