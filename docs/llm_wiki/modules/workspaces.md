# workspaces Module

**Path:** `frontend/src/navigation/workspaces.ts`

## Description

_Auto-generated from `frontend/src/navigation/workspaces.ts`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `lucide-react` | `LucideIcon` | Declaration | erased |
| `lucide-react` | `LayoutDashboard`, `Calendar`, `Inbox`, `Users`, `ListTodo`, `FolderOpen`, `Map`, `GanttChartSquare`, `Settings`, `Repeat`, `BarChart`, `Bot`, `MapPin`, `Network`, `Truck`, `UserCheck` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `NavItem`, `PRIMARY_NAV_ITEMS`, `WORKSPACES`, `WorkspaceKey`, `WorkspaceMetadata`, `getWorkspaceForPath`, `getWorkspaceFromPath` |
| Constants | `WORKSPACES`, `PRIMARY_NAV_ITEMS` |
| Module calls | `PRIMARY_NAV_ITEMS = flatMap` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/layout/AppSidebar.tsx"]
    n1["frontend/src/components/layout/AppTopNav.tsx"]
    n2["frontend/src/components/layout/CommandMenu.test.tsx"]
    n3["frontend/src/components/layout/CommandMenu.tsx"]
    n4["frontend/src/navigation/helpContexts.ts"]
    n5["frontend/src/navigation/workspaces.test.ts"]
    n6["frontend/src/navigation/workspaces.ts"]
    n0 --> n6
    n1 --> n0
    n1 --> n6
    n2 --> n3
    n2 --> n6
    n3 --> n6
    n4 --> n6
    n5 --> n6
    click n0 "../modules/AppSidebar.md"
    click n1 "../modules/AppTopNav.md"
    click n2 "../modules/CommandMenu.test.md"
    click n3 "../modules/CommandMenu.md"
    click n4 "../modules/helpContexts.md"
    click n5 "../modules/workspaces.test.md"
    click n6 "../modules/workspaces.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppSidebar](../modules/AppSidebar.md) |
| Inbound | [AppTopNav](../modules/AppTopNav.md) |
| Inbound | [CommandMenu.test](../modules/CommandMenu.test.md) |
| Inbound | [CommandMenu](../modules/CommandMenu.md) |
| Inbound | [helpContexts](../modules/helpContexts.md) |
| Inbound | [workspaces.test](../modules/workspaces.test.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Classes

| Class | Kind | Line | Bases / Target | Description |
|-------|------|------|----------------|-------------|
| [NavItem](../entities/NavItem.md) | Interface | 23 | — | — |
| [WorkspaceMetadata](../entities/WorkspaceMetadata.md) | Interface | 31 | — | — |
| [WorkspaceKey](../entities/WorkspaceKey.md) | Type alias | 21 | `'delivery' \| 'planning' \| 'resource'` | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `getWorkspaceFromPath` | `(pathname: string) -> WorkspaceKey` | — | — |
| `getWorkspaceForPath` | `(pathname: string) -> WorkspaceMetadata` | — | — |
