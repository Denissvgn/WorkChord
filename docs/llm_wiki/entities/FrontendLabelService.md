# FrontendLabelService

**Location:** `frontend/src/services/labelService.ts:41`
**Kind:** Class
**Bases:** —
**Module:** [labelService](../modules/labelService.md)

## Description

_Auto-generated from `FrontendLabelService` in `frontend/src/services/labelService.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `getGroups` | `(params?: LabelGroupListParams) => Promise<LabelGroup[]>` | *required* | — |
| `getLabels` | `(params?: LabelListParams) => Promise<Label[]>` | *required* | — |
| `createGroup` | `(data: LabelGroupCreate) => Promise<LabelGroup>` | *required* | — |
| `updateGroup` | `(groupId: number, data: LabelGroupUpdate) => Promise<LabelGroup>` | *required* | — |
| `createLabel` | `(data: LabelCreate) => Promise<Label>` | *required* | — |
| `updateLabel` | `(labelId: number, data: LabelUpdate) => Promise<Label>` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [labelService](../modules/labelService.md) | 0 | `createGroup`, `createLabel`, `getGroups`, `getLabels`, `updateGroup`, `updateLabel` |
