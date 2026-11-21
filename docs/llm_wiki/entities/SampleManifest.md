# SampleManifest

**Location:** `frontend/src/features/firstRun/sampleProject.ts:13`
**Kind:** Interface
**Bases:** —
**Module:** [sampleProject](../modules/sampleProject.md)

## Description

_Auto-generated from `SampleManifest` in `frontend/src/features/firstRun/sampleProject.ts`._

## Attributes

| Name | Type | Required | Default | Description |
|------|------|----------|---------|-------------|
| `owner` | `string` | Yes | — | — |
| `records` | `SampleRecord[]` | Yes | — | — |
| `complete` | `boolean` | Yes | — | — |
| `previousScope` | `WorkScope` | No | — | — |

## Methods

*No declared methods.*

## Relationships

<!-- Auto-generated relationship summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["SampleManifest (frontend/src/features/firstRun/sampleProject.ts)"]
    n1["frontend/src/features/firstRun/sampleProject.test.tsx"]
    n2["loadSampleProject (frontend/src/features/firstRun/sampleProject.ts)"]
    n3["removeSampleProject (frontend/src/features/firstRun/sampleProject.ts)"]
    n4["frontend/src/features/firstRun/SampleProjectAction.tsx"]
    n5["frontend/src/features/firstRun/sampleProjectStore.ts"]
    n1 --> n0
    n2 --> n0
    n3 --> n0
    n4 --> n0
    n5 --> n0
    click n0 "../modules/sampleProject.md"
    click n1 "../modules/sampleProject.test.md"
    click n2 "../modules/sampleProject.md"
    click n3 "../modules/sampleProject.md"
    click n4 "../modules/SampleProjectAction.md"
    click n5 "../modules/sampleProjectStore.md"
```

### Summary

| Module | Methods | Attributes |
|---|---:|---|
| [sampleProject](../modules/sampleProject.md) | 0 | `complete`, `owner`, `previousScope`, `records` |

### References

| Reference | Kind | Source | Call sites |
|---|---|---|---:|
| `sampleProject.test` | import | [sampleProject.test](../modules/sampleProject.test.md) | — |
| `loadSampleProject` | type_reference | [sampleProject](../modules/sampleProject.md) | — |
| `removeSampleProject` | type_reference | [sampleProject](../modules/sampleProject.md) | — |
| `SampleProjectAction` | import | [SampleProjectAction](../modules/SampleProjectAction.md) | — |
| `sampleProjectStore` | import | [sampleProjectStore](../modules/sampleProjectStore.md) | — |
