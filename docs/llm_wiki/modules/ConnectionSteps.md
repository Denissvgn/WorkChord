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
| `./RuntimeIdentity` | `RuntimeIdentity` | — | compiler-dependent |
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
    n2["frontend/src/components/team/ConnectionSteps.test.tsx"]
    n3["frontend/src/components/team/ConnectionSteps.tsx"]
    n4["frontend/src/components/team/RuntimeIdentity.tsx"]
    n5["frontend/src/components/team/TeamProfileManager.tsx"]
    n6["frontend/src/features/agentTeamSetup/connectAgent.ts"]
    n7["frontend/src/types/agent.ts"]
    n1 --> n0
    n1 --> n3
    n1 --> n6
    n1 --> n7
    n2 --> n3
    n2 --> n7
    n3 --> n0
    n3 --> n4
    n3 --> n6
    n3 --> n7
    n4 --> n7
    n5 --> n0
    n5 --> n3
    n5 --> n6
    n5 --> n7
    n6 --> n7
    click n0 "../modules/Button.md"
    click n1 "../modules/ConnectAgentSteps.md"
    click n2 "../modules/ConnectionSteps.test.md"
    click n3 "../modules/ConnectionSteps.md"
    click n4 "../modules/RuntimeIdentity.md"
    click n5 "../modules/TeamProfileManager.md"
    click n6 "../modules/connectAgent.md"
    click n7 "../modules/types_agent.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [ConnectAgentSteps](../modules/ConnectAgentSteps.md) |
| Inbound | [ConnectionSteps.test](../modules/ConnectionSteps.test.md) |
| Inbound | [TeamProfileManager](../modules/TeamProfileManager.md) |
| Outbound | [Button](../modules/Button.md) |
| Outbound | [RuntimeIdentity](../modules/RuntimeIdentity.md) |
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
