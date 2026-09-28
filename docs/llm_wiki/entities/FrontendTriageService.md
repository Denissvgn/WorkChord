# FrontendTriageService

**Location:** `frontend/src/services/triageService.ts:47`
**Kind:** Class
**Bases:** —
**Module:** [triageService](../modules/triageService.md)

## Description

_Auto-generated from `FrontendTriageService` in `frontend/src/services/triageService.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `getAll` | `(params?: TriageListParams) => Promise<TriageItem[]>` | Yes | — | — |
| `create` | `(data: TriageItemCreate) => Promise<TriageItem>` | Yes | — | — |
| `getById` | `(triageItemId: number) => Promise<TriageItem>` | Yes | — | — |
| `update` | `(triageItemId: number, data: TriageItemUpdate) => Promise<TriageItem>` | Yes | — | — |
| `accept` | `(triageItemId: number, data?: TriageActionRequest) => Promise<TriageItem>` | Yes | — | — |
| `decline` | `(triageItemId: number, data?: TriageActionRequest) => Promise<TriageItem>` | Yes | — | — |
| `snooze` | `(triageItemId: number, data: TriageSnoozeRequest) => Promise<TriageItem>` | Yes | — | — |
| `markDuplicate` | `(triageItemId: number, data: TriageDuplicateRequest) => Promise<TriageItem>` | Yes | — | — |
| `getDuplicateSuggestions` | `(         triageItemId: number,         params?: { limitPerType?: number; minScore?: number }     ) => Promise<TriageDuplicateSuggestionsResponse>` | Yes | — | — |
| `getAssigneeRecommendations` | `(         triageItemId: number,         iterationId?: number \| null     ) => Promise<AssigneeRecommendation[]>` | Yes | — | — |
| `getClassificationSuggestions` | `(         triageItemId: number,         limit?: number     ) => Promise<TriageClassificationSuggestion[]>` | Yes | — | — |
| `classify` | `(triageItemId: number) => Promise<TriageClassificationSuggestion>` | Yes | — | — |
| `draftTask` | `(triageItemId: number, data?: TriageTaskDraftRequest) => Promise<TriageTaskDraftResponse>` | Yes | — | — |
| `convertToTask` | `(triageItemId: number, data: TriageConvertToTaskRequest) => Promise<TriageConvertToTaskResponse>` | Yes | — | — |

## Methods

*No public methods. Inherits from base classes.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [triageService](../modules/triageService.md) | 0 | `accept`, `classify`, `convertToTask`, `create`, `decline`, `draftTask`, `getAll`, `getAssigneeRecommendations`, `getById`, `getClassificationSuggestions`, `getDuplicateSuggestions`, `markDuplicate` |
