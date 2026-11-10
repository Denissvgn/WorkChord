# FrontendTriageService

**Location:** `frontend/src/services/triageService.ts:47`
**Kind:** Interface
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
| `getDuplicateSuggestions` | <pre><code>&#40;&#10;        triageItemId&#58; number&#44;&#10;        params&#63;&#58; &#123; limitPerType&#63;&#58; number&#59; minScore&#63;&#58; number &#125;&#10;    &#41; &#61;&#62; Promise&#60;TriageDuplicateSuggestionsResponse&#62;</code></pre> | Yes | — | — |
| `getAssigneeRecommendations` | <pre><code>&#40;&#10;        triageItemId&#58; number&#44;&#10;        iterationId&#63;&#58; number &#124; null&#10;    &#41; &#61;&#62; Promise&#60;AssigneeRecommendation&#91;&#93;&#62;</code></pre> | Yes | — | — |
| `getClassificationSuggestions` | <pre><code>&#40;&#10;        triageItemId&#58; number&#44;&#10;        limit&#63;&#58; number&#10;    &#41; &#61;&#62; Promise&#60;TriageClassificationSuggestion&#91;&#93;&#62;</code></pre> | Yes | — | — |
| `classify` | `(triageItemId: number) => Promise<TriageClassificationSuggestion>` | Yes | — | — |
| `draftTask` | `(triageItemId: number, data?: TriageTaskDraftRequest) => Promise<TriageTaskDraftResponse>` | Yes | — | — |
| `convertToTask` | `(triageItemId: number, data: TriageConvertToTaskRequest) => Promise<TriageConvertToTaskResponse>` | Yes | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [triageService](../modules/triageService.md) | 0 | `accept`, `classify`, `convertToTask`, `create`, `decline`, `draftTask`, `getAll`, `getAssigneeRecommendations`, `getById`, `getClassificationSuggestions`, `getDuplicateSuggestions`, `markDuplicate` |
