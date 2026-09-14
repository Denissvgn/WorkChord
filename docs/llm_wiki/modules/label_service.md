# label_service Module

**Path:** `backend/app/services/label_service.py`

## Description

Service for governed label taxonomy and built-in defaults.

## Imports

| Source | Symbols |
|--------|---------|
| `app.models.label` | `Label`, `LabelGroup` |
| `app.schemas.label` | `LabelCreate`, `LabelGroupCreate`, `LabelGroupUpdate`, `LabelUpdate` |
| `app.services.agent_routing_policy` | `CAPABILITY_LABEL_SKILL_KEYS` |
| `app.services.language_service` | `backend_error_message`, `entity_not_found_message`, `resolve_runtime_ui_language` |
| `app.sql_semantics` | `portable_contains` |
| `sqlalchemy` | `Select`, `or_`, `select` |
| `sqlalchemy.exc` | `IntegrityError` |
| `sqlalchemy.ext.asyncio` | `AsyncSession` |
| `sqlalchemy.orm` | `selectinload`, `with_loader_criteria` |
| `typing` | `Any`, `Optional`, `Sequence` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/models/label.py"]
    n2["backend/app/routers/labels.py"]
    n3["backend/app/schemas/label.py"]
    n4["backend/app/services/agent_routing_policy.py"]
    n5["backend/app/services/label_service.py"]
    n6["backend/app/services/language_service.py"]
    n7["backend/app/services/upgrade_service.py"]
    n8["backend/app/sql_semantics.py"]
    n9["backend/tests/test_agent_routing_contract.py"]
    n0 --> n3
    n0 --> n5
    n2 --> n3
    n2 --> n5
    n2 --> n6
    n5 --> n1
    n5 --> n3
    n5 --> n4
    n5 --> n6
    n5 --> n8
    n7 --> n5
    n9 --> n4
    n9 --> n5
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/models_label.md"
    click n2 "../modules/labels.md"
    click n3 "../modules/schemas_label.md"
    click n4 "../modules/agent_routing_policy.md"
    click n5 "../modules/label_service.md"
    click n6 "../modules/language_service.md"
    click n7 "../modules/upgrade_service.md"
    click n8 "../modules/sql_semantics.md"
    click n9 "../modules/test_agent_routing_contract.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [labels](../modules/labels.md) |
| Inbound | [upgrade_service](../modules/upgrade_service.md) |
| Inbound | [test_agent_routing_contract](../modules/test_agent_routing_contract.md) |
| Outbound | [models_label](../modules/models_label.md) |
| Outbound | [schemas_label](../modules/schemas_label.md) |
| Outbound | [agent_routing_policy](../modules/agent_routing_policy.md) |
| Outbound | [language_service](../modules/language_service.md) |
| Outbound | [sql_semantics](../modules/sql_semantics.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [LabelService](../entities/LabelService.md) | 110 | — | Service for label group and label CRUD plus built-in label seeding. |
| [LabelConflictError](../entities/LabelConflictError.md) | 317 | `ValueError` | Raised when label taxonomy uniqueness constraints are violated. |
