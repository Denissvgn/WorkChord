# RoutingQualificationKeyUsage

**Location:** `frontend/src/types/agent.ts:343`
**Kind:** Interface
**Bases:** —
**Module:** [types_agent](../modules/types_agent.md)

## Description

_Auto-generated from `RoutingQualificationKeyUsage` in `frontend/src/types/agent.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `catalog_entries` | `{ id: number; key: string; enabled: boolean }[]` | Yes | — | — |
| `task_ids` | `number[]` | Yes | — | — |
| `catalog_entries_omitted` | `number` | Yes | — | — |
| `task_ids_omitted` | `number` | Yes | — | — |
| `calibration_contracts` | `{ key: string; state: 'submitted' \| 'approved' }[]` | No | — | — |
| `calibration_contracts_omitted` | `number` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
*No generated relationships detected.*

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [types_agent](../modules/types_agent.md) | 0 | `calibration_contracts`, `calibration_contracts_omitted`, `catalog_entries`, `catalog_entries_omitted`, `task_ids`, `task_ids_omitted` |
