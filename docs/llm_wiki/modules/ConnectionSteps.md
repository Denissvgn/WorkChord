# ConnectionSteps Module

**Path:** `frontend/src/components/team/ConnectionSteps.tsx`

## Description

_Auto-generated from `frontend/src/components/team/ConnectionSteps.tsx`._

## Imports

| Source | Symbols | Type-only | Runtime emission |
|--------|---------|-----------|------------------|
| `../../features/agentTeamSetup/connectAgent` | `RUNTIME_PRODUCT_NAMES`, `credentialFilename`, `runtimeOfMember`, `runtimeSnippet` | — | compiler-dependent |
| `../../types/agent` | `AgentTeamMaster`, `AgentTeamMemberSpec`, `AgentTeamMemberStatus` | Declaration | erased |
| `../common/Button` | `Button` | — | compiler-dependent |
| `react` | `useEffect`, `useState` | — | compiler-dependent |
| `react-i18next` | `useTranslation` | — | compiler-dependent |

## Module Signals

| Signal | Values |
|--------|--------|
| Exports | `ConnectionSteps` |
| Constants | `P` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
This graph shows full source coupling. Type dependencies can be erased; compiler-dependent cycle groups are runtime candidates, not confirmed initialization cycles.

```mermaid
flowchart LR
    n0["frontend/src/components/common/Button.tsx"]
    n1["frontend/src/components/team/ConnectAgentSteps.tsx"]
    n2["frontend/src/components/team/ConnectionSteps.tsx"]
    n3["frontend/src/components/team/TeamProfileManager.tsx"]
    n4["frontend/src/features/agentTeamSetup/connectAgent.ts"]
    n5["frontend/src/types/agent.ts"]
    n1 --> n0
    n1 --> n2
    n1 --> n4
    n1 --> n5
    n2 --> n0
    n2 --> n4
    n2 --> n5
    n3 --> n0
    n3 --> n2
    n3 --> n4
    n3 --> n5
    n4 --> n5
    click n0 "../modules/Button.md"
    click n1 "../modules/ConnectAgentSteps.md"
    click n2 "../modules/ConnectionSteps.md"
    click n3 "../modules/TeamProfileManager.md"
    click n4 "../modules/connectAgent.md"
    click n5 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ConnectAgentSteps](../modules/ConnectAgentSteps.md) |
| Inbound | [TeamProfileManager](../modules/TeamProfileManager.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [connectAgent](../modules/connectAgent.md) |
| Outbound | [types_agent](../modules/types_agent.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| typescript | 2 | 0 |

## Functions

| Function | Signature | Decorators | Description |
|----------|-----------|------------|-------------|
| `ConnectionSteps` | <pre><code>&#40;&#123; manifest&#44; member&#44; memberStatus&#44; connected&#44; checking &#61; false&#44; onCheck &#125;&#58; &#123;&#10;    manifest&#58; AgentTeamMaster&#59;&#10;    member&#58; AgentTeamMemberSpec&#59;&#10;    memberStatus&#58; AgentTeamMemberStatus &#124; undefined&#59;&#10;    connected&#58; boolean&#59;&#10;    checking&#63;&#58; boolean&#59;&#10;    onCheck&#58; &#40;&#41; &#61;&#62; void&#59;&#10;&#125;&#41;</code></pre> | — | What the Connect steps show once a member exists: the credential file, the skill package, the runtime |
