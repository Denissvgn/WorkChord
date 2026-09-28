# FrontendSavedViewService

**Location:** `frontend/src/services/savedViewService.ts:17`
**Kind:** Class
**Bases:** —
**Module:** [savedViewService](../modules/savedViewService.md)

## Description

_Auto-generated from `FrontendSavedViewService` in `frontend/src/services/savedViewService.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `getAll` | `(params: SavedViewListParams) => Promise<SavedView[]>` | Yes | — | — |
| `getById` | `(savedViewId: number) => Promise<SavedView>` | Yes | — | — |
| `getDashboardCards` | `(iterationId: number) => Promise<SavedViewDashboardCard[]>` | Yes | — | — |
| `create` | `(data: SavedViewCreate) => Promise<SavedView>` | Yes | — | — |
| `update` | `(savedViewId: number, data: SavedViewUpdate) => Promise<SavedView>` | Yes | — | — |
| `delete` | `(savedViewId: number) => Promise<void>` | Yes | — | — |
| `duplicate` | `(savedViewId: number, data?: SavedViewDuplicate) => Promise<SavedView>` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [savedViewService](../modules/savedViewService.md) | 0 | `create`, `delete`, `duplicate`, `getAll`, `getById`, `getDashboardCards`, `update` |
