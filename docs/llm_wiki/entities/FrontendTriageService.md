# FrontendTriageService

**Location:** `frontend/src/services/triageService.ts:47`
**Kind:** Class
**Bases:** —
**Module:** [triageService](../modules/triageService.md)

## Description

_Auto-generated from `FrontendTriageService` in `frontend/src/services/triageService.ts`._

## Attributes

| Name | Type | Default | Description |
|------|------|---------|-------------|
| `getAll` | `(params?: TriageListParams) => Promise<TriageItem[]>` | *required* | — |
| `create` | `(data: TriageItemCreate) => Promise<TriageItem>` | *required* | — |
| `getById` | `(triageItemId: number) => Promise<TriageItem>` | *required* | — |
| `update` | `(triageItemId: number, data: TriageItemUpdate) => Promise<TriageItem>` | *required* | — |
| `accept` | `(triageItemId: number, data?: TriageActionRequest) => Promise<TriageItem>` | *required* | — |
| `decline` | `(triageItemId: number, data?: TriageActionRequest) => Promise<TriageItem>` | *required* | — |
| `snooze` | `(triageItemId: number, data: TriageSnoozeRequest) => Promise<TriageItem>` | *required* | — |
| `markDuplicate` | `(triageItemId: number, data: TriageDuplicateRequest) => Promise<TriageItem>` | *required* | — |
| `getDuplicateSuggestions` | `(         triageItemId: number,         params?: { limitPerType?: number; minScore?: number }     ) => Promise<TriageDuplicateSuggestionsResponse>` | *required* | — |
| `getAssigneeRecommendations` | `(         triageItemId: number,         iterationId?: number \| null     ) => Promise<AssigneeRecommendation[]>` | *required* | — |
| `getClassificationSuggestions` | `(         triageItemId: number,         limit?: number     ) => Promise<TriageClassificationSuggestion[]>` | *required* | — |
| `classify` | `(triageItemId: number) => Promise<TriageClassificationSuggestion>` | *required* | — |
| `draftTask` | `(triageItemId: number, data?: TriageTaskDraftRequest) => Promise<TriageTaskDraftResponse>` | *required* | — |
| `convertToTask` | `(triageItemId: number, data: TriageConvertToTaskRequest) => Promise<TriageConvertToTaskResponse>` | *required* | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [triageService](../modules/triageService.md) | 0 | `accept`, `classify`, `convertToTask`, `create`, `decline`, `draftTask`, `getAll`, `getAssigneeRecommendations`, `getById`, `getClassificationSuggestions`, `getDuplicateSuggestions`, `markDuplicate` |
