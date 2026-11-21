# InitiativeGroupHeader Module

**Path:** `frontend/src/components/projects/InitiativeGroupHeader.tsx`

## Description

_Auto-generated from `frontend/src/components/projects/InitiativeGroupHeader.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/project` | `ProjectHealth` | Declaration | erased |
| `../../utils/formatDate` | `formatDate` | — | compiler-dependent |
| `../../utils/teamMemberLabels` | `formatPortfolioOwnerLabel` | — | compiler-dependent |
| `../common/Button` | `Button` | — | compiler-dependent |
| `../ui` | `OverflowMenu` | — | compiler-dependent |
| `./projectPortfolio` | `InitiativeGroupInfo` | Declaration | erased |
| `./projectStatusStyles` | `projectHealthBadgeClassName` | — | compiler-dependent |
| `clsx` | `clsx` | — | compiler-dependent |
| `lucide-react` | `Pencil` | — | compiler-dependent |
| `react` | `useId` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `InitiativeGroupHeader` |
| Constants | `healthLabelKeys` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/projects/InitiativeGroupHeader.tsx"]
    n2["frontend/src/components/projects/projectPortfolio.ts"]
    n3["frontend/src/components/projects/projectStatusStyles.ts"]
    n4["frontend/src/components/projects/RoadmapView.tsx"]
    n5["frontend/src/components/ui/index.ts"]
    n6["frontend/src/pages/ProjectsPage.tsx"]
    n7["frontend/src/types/project.ts"]
    n8["frontend/src/utils/formatDate.ts"]
    n9["frontend/src/utils/teamMemberLabels.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n1 --> n5
    n1 --> n7
    n1 --> n8
    n1 --> n9
    n2 --> n7
    n3 --> n7
    n4 --> n0
    n4 --> n1
    n4 --> n2
    n4 --> n3
    n4 --> n5
    n4 --> n7
    n4 --> n8
    n6 --> n0
    n6 --> n1
    n6 --> n2
    n6 --> n3
    n6 --> n4
    n6 --> n5
    n6 --> n7
    n6 --> n8
    n6 --> n9
    click n0 "../modules/Button.md"
    click n1 "../modules/InitiativeGroupHeader.md"
    click n2 "../modules/projectPortfolio.md"
    click n3 "../modules/projectStatusStyles.md"
    click n4 "../modules/RoadmapView.md"
    click n5 "../modules/index.md"
    click n6 "../modules/ProjectsPage.md"
    click n7 "../modules/types_project.md"
    click n8 "../modules/formatDate.md"
    click n9 "../modules/teamMemberLabels.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [RoadmapView](../modules/RoadmapView.md) |
| Inbound | [ProjectsPage](../modules/ProjectsPage.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [projectPortfolio](../modules/projectPortfolio.md) |
| Outbound | [projectStatusStyles](../modules/projectStatusStyles.md) |
| Outbound | [index](../modules/index.md) |
| Outbound | [types_project](../modules/types_project.md) |
| Outbound | [formatDate](../modules/formatDate.md) |
| Outbound | [teamMemberLabels](../modules/teamMemberLabels.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 4 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `InitiativeGroupHeader` | <pre><code>&#40;&#123;&#10;    initiative&#44;&#10;    projectCount&#44;&#10;    headingLevel&#44;&#10;    headingId&#44;&#10;    onEdit&#44;&#10;    onDelete&#44;&#10;    className&#44;&#10;&#125;&#58; &#123;&#10;    initiative&#58; InitiativeGroupInfo &#124; null&#59;&#10;    projectCount&#58; number&#59;&#10;    &#47;&#42;&#42; A heading in the roadmap rail&#59; plain text inside a table header cell&#46; &#42;&#47;&#10;    headingLevel&#63;&#58; 3&#59;&#10;    headingId&#63;&#58; string&#59;&#10;    onEdit&#63;&#58; &#40;&#41; &#61;&#62; void&#59;&#10;    onDelete&#63;&#58; &#40;&#41; &#61;&#62; void&#59;&#10;    className&#63;&#58; string&#59;&#10;&#125;&#41;</code></pre> | — | The header row of one initiative group: its name, owner, health and target |
