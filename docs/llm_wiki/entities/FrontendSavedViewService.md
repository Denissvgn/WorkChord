# FrontendSavedViewService

**Location:** `frontend/src/services/savedViewService.ts:17`
**Kind:** Class
**Bases:** —
**Module:** [savedViewService](../modules/savedViewService.md)

## Description

_Auto-generated from `FrontendSavedViewService` in `frontend/src/services/savedViewService.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `getAll` | `(params: SavedViewListParams) => Promise<SavedView[]>` | *required* | — |
| `getById` | `(savedViewId: number) => Promise<SavedView>` | *required* | — |
| `getDashboardCards` | `(iterationId: number) => Promise<SavedViewDashboardCard[]>` | *required* | — |
| `create` | `(data: SavedViewCreate) => Promise<SavedView>` | *required* | — |
| `update` | `(savedViewId: number, data: SavedViewUpdate) => Promise<SavedView>` | *required* | — |
| `delete` | `(savedViewId: number) => Promise<void>` | *required* | — |
| `duplicate` | `(savedViewId: number, data?: SavedViewDuplicate) => Promise<SavedView>` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [savedViewService](../modules/savedViewService.md) | 0 | `create`, `delete`, `duplicate`, `getAll`, `getById`, `getDashboardCards`, `update` |
