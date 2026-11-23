# ModelBindings Module

**Path:** `frontend/src/components/team/ModelBindings.tsx`

## Description

_Auto-generated from `frontend/src/components/team/ModelBindings.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../types/agent` | `AgentModelBinding`, `AgentModelCatalogEntry` | Declaration | erased |
| `../common/Button` | `Button` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ModelBindings` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/team/AgentModelAdministration.tsx"]
    n2["frontend/src/components/team/ModelBindings.tsx"]
    n3["frontend/src/types/agent.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n3
    n2 --> n0
    n2 --> n3
    click n0 "../modules/Button.md"
    click n1 "../modules/AgentModelAdministration.md"
    click n2 "../modules/ModelBindings.md"
    click n3 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [AgentModelAdministration](../modules/AgentModelAdministration.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [types_agent](../modules/types_agent.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 1 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ModelBindings` | <pre><code>&#40;&#123; bindings&#44; actorNames&#44; catalog&#44; canAdminister&#44; busy&#44; onEdit&#44; onToggle &#125;&#58; &#123;&#10;    bindings&#58; AgentModelBinding&#91;&#93;&#59; actorNames&#58; Map&#60;number&#44; string&#62;&#59; catalog&#58; Map&#60;number&#44; AgentModelCatalogEntry&#62;&#59;&#10;    canAdminister&#58; boolean&#59; busy&#58; boolean&#59; onEdit&#58; &#40;binding&#58; AgentModelBinding&#41; &#61;&#62; void&#59; onToggle&#58; &#40;binding&#58; AgentModelBinding&#41; &#61;&#62; void&#59;&#10;&#125;&#41;</code></pre> | — | — |
