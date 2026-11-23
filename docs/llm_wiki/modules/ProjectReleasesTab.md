# ProjectReleasesTab Module

**Path:** `frontend/src/components/projects/ProjectReleasesTab.tsx`

## Description

_Auto-generated from `frontend/src/components/projects/ProjectReleasesTab.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/release` | `Release` | Declaration | erased |
| `../../utils/formatDate` | `formatDate` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../ui` | `SectionCard` | — | compiler-dependent |
| `./projectDetailShared` | `releaseBadgeClassName`, `releaseStatusLabelKeys`, `t` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `Package`, `Plus` | — | compiler-dependent |
| `react-router-dom` | `Link` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ProjectReleasesTab` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/projects/projectDetailShared.ts"]
    n2["frontend/src/components/projects/ProjectReleasesTab.tsx"]
    n3["frontend/src/components/ui/index.ts"]
    n4["frontend/src/pages/ProjectDetailPage.tsx"]
    n5["frontend/src/types/release.ts"]
    n6["frontend/src/utils/formatDate.ts"]
    n1 --> n5
    n2 --> n0
    n2 --> n1
    n2 --> n3
    n2 --> n5
    n2 --> n6
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    click n0 "../modules/Button.md"
    click n1 "../modules/projectDetailShared.md"
    click n2 "../modules/ProjectReleasesTab.md"
    click n3 "../modules/index.md"
    click n4 "../modules/ProjectDetailPage.md"
    click n5 "../modules/types_release.md"
    click n6 "../modules/formatDate.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ProjectDetailPage](../modules/ProjectDetailPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [projectDetailShared](../modules/projectDetailShared.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [types_release](../modules/types_release.md) |
| Outbound | [formatDate](../modules/formatDate.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 3 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ProjectReleasesTab` | <pre><code>&#40;&#123;&#10;    releases&#44;&#10;    isLoading&#44;&#10;    onCreate&#44;&#10;&#125;&#58; &#123;&#10;    releases&#58; Release&#91;&#93;&#59;&#10;    isLoading&#58; boolean&#59;&#10;    onCreate&#58; &#40;&#41; &#61;&#62; void&#59;&#10;&#125;&#41;</code></pre> | — | — |
