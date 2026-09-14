# workspaces Module

**Path:** `frontend/src/navigation/workspaces.ts`

## Description

_Auto-generated from `frontend/src/navigation/workspaces.ts`._

## Imports

| Source | Symbols |
|--------|---------|
| `lucide-react` | `LucideIcon`, `LayoutDashboard`, `Calendar`, `Inbox`, `Users`, `ListTodo`, `FolderOpen`, `Map`, `GanttChartSquare`, `Settings`, `Repeat`, `BarChart`, `Bot`, `MapPin`, `Network` |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `NavItem`, `PRIMARY_NAV_ITEMS`, `WORKSPACES`, `WorkspaceKey`, `WorkspaceMetadata`, `getWorkspaceForPath`, `getWorkspaceFromPath` |
| Constants | `WORKSPACES`, `PRIMARY_NAV_ITEMS` |
| Module calls | `PRIMARY_NAV_ITEMS = flatMap` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["frontend/src/components/layout/AppSidebar.tsx"]
    n1["frontend/src/components/layout/AppTopNav.tsx"]
    n2["frontend/src/components/layout/CommandMenu.tsx"]
    n3["frontend/src/navigation/helpContexts.ts"]
    n4["frontend/src/navigation/workspaces.test.ts"]
    n5["frontend/src/navigation/workspaces.ts"]
    n0 --> n5
    n1 --> n0
    n1 --> n5
    n2 --> n5
    n3 --> n5
    n4 --> n5
    click n0 "../modules/AppSidebar.md"
    click n1 "../modules/AppTopNav.md"
    click n2 "../modules/CommandMenu.md"
    click n3 "../modules/helpContexts.md"
    click n4 "../modules/workspaces.test.md"
    click n5 "../modules/workspaces.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AppSidebar](../modules/AppSidebar.md) |
| Inbound | [AppTopNav](../modules/AppTopNav.md) |
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
| [NavItem](../entities/NavItem.md) | Class | 21 | — | — |
| [WorkspaceMetadata](../entities/WorkspaceMetadata.md) | Class | 29 | — | — |
| [WorkspaceKey](../entities/WorkspaceKey.md) | Type alias | 19 | — | — |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `getWorkspaceFromPath` | `(pathname: string) -> WorkspaceKey` | — | — |
| `getWorkspaceForPath` | `(pathname: string) -> WorkspaceMetadata` | — | — |
