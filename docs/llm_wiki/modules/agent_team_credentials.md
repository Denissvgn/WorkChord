# agent_team_credentials Module

**Path:** `backend/app/services/agent_team_credentials.py`

## Description

This one-way delivery boundary owns private-directory checks, exclusive no-follow writes and nonsecret receipt digests. Setup reconciliation retains planning, authorization and transaction ownership; old sink/error imports remain available through the setup facade.

One-way credential delivery, independent of setup planning and transactions.

## Imports

| Source | Symbols |
|--------|---------|
| `hashlib` | `hashlib` |
| `json` | `json` |
| `os` | `os` |
| `pathlib` | `Path` |
| `stat` | `stat` |
| `typing` | `Protocol` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/services/agent_team_credentials.py"]
    n1["backend/app/services/agent_team_setup_service.py"]
    n1 --> n0
    click n0 "../modules/agent_team_credentials.md"
    click n1 "../modules/agent_team_setup_service.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [agent_team_setup_service](../modules/agent_team_setup_service.md) |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [CredentialDeliveryError](../entities/CredentialDeliveryError.md) | 9 | `RuntimeError` | Raised when a one-time actor key did not reach the approved sink. |
| [AgentTeamCredentialSink](../entities/AgentTeamCredentialSink.md) | 13 | `Protocol` | One-way sink boundary; implementations never return credential material. |
| [FilesystemAgentTeamCredentialSink](../entities/FilesystemAgentTeamCredentialSink.md) | 33 | — | Write one-time credentials to an operator-owned mode-0700 directory. |