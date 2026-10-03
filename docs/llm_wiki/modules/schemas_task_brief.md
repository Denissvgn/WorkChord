# task_brief Module

**Path:** `backend/app/schemas/task_brief.py`

## Description

Canonical brief inputs and separate execution evidence/review contracts.

## Imports

| Source | Symbols |
|--------|---------|
| `datetime` | `datetime` |
| `pydantic` | `BaseModel`, `ConfigDict`, `Field`, `field_validator`, `model_validator` |
| `typing` | `Literal` |
| `uuid` | `uuid4` |

## Local dependency map

<!-- Auto-generated local dependency summary. Do not edit by hand. -->
```mermaid
flowchart LR
    n0["backend/app/mcp_agent_tools.py"]
    n1["backend/app/routers/task_domain.py"]
    n2["backend/app/schemas/agent.py"]
    n3["backend/app/schemas/llm.py"]
    n4["backend/app/schemas/task.py"]
    n5["backend/app/schemas/task_brief.py"]
    n6["backend/app/schemas/template.py"]
    n7["backend/app/schemas/triage.py"]
    n8["backend/app/services/task_brief_service.py"]
    n9["backend/tests/test_task_domain.py"]
    n10["backend/tests/test_task_domain_integrity.py"]
    n11["scripts/generate_mobile_contract_fixtures.py"]
    n0 --> n2
    n0 --> n4
    n0 --> n5
    n0 --> n6
    n0 --> n7
    n0 --> n8
    n1 --> n4
    n1 --> n5
    n1 --> n8
    n2 --> n4
    n2 --> n5
    n2 --> n7
    n3 --> n5
    n4 --> n5
    n6 --> n5
    n7 --> n4
    n7 --> n5
    n7 --> n8
    n8 --> n5
    n9 --> n0
    n9 --> n2
    n9 --> n4
    n9 --> n5
    n9 --> n7
    n9 --> n8
    n10 --> n4
    n10 --> n5
    n10 --> n8
    n10 --> n9
    n11 --> n4
    n11 --> n5
    click n0 "../modules/mcp_agent_tools.md"
    click n1 "../modules/routers_task_domain.md"
    click n2 "../modules/schemas_agent.md"
    click n3 "../modules/schemas_llm.md"
    click n4 "../modules/schemas_task.md"
    click n5 "../modules/schemas_task_brief.md"
    click n6 "../modules/schemas_template.md"
    click n7 "../modules/schemas_triage.md"
    click n8 "../modules/task_brief_service.md"
    click n9 "../modules/test_task_domain.md"
    click n10 "../modules/test_task_domain_integrity.md"
    click n11 "../modules/generate_mobile_contract_fixtures.md"
```

### Internal neighbors

| Direction | Module |
|---|---|
| Inbound | [mcp_agent_tools](../modules/mcp_agent_tools.md) |
| Inbound | [routers_task_domain](../modules/routers_task_domain.md) |
| Inbound | [schemas_agent](../modules/schemas_agent.md) |
| Inbound | [schemas_llm](../modules/schemas_llm.md) |
| Inbound | [schemas_task](../modules/schemas_task.md) |
| Inbound | [schemas_template](../modules/schemas_template.md) |
| Inbound | [schemas_triage](../modules/schemas_triage.md) |
| Inbound | [task_brief_service](../modules/task_brief_service.md) |
| Inbound | [test_task_domain](../modules/test_task_domain.md) |
| Inbound | [test_task_domain_integrity](../modules/test_task_domain_integrity.md) |
| Inbound | [generate_mobile_contract_fixtures](../modules/generate_mobile_contract_fixtures.md) |

### External packages

| Language | Used packages | Undeclared packages |
|---|---:|---:|
| python | 1 | 0 |

## Classes

| Class | Line | Bases | Description |
|-------|------|-------|-------------|
| [BriefCriterion](../entities/schemas_task_brief_BriefCriterion.md) | 10 | `BaseModel` | — |
| [TaskBrief](../entities/schemas_task_brief_TaskBrief.md) | 25 | `BaseModel` | — |
| [BriefWrite](../entities/BriefWrite.md) | 44 | `BaseModel` | — |
| [BriefConvert](../entities/BriefConvert.md) | 50 | `BaseModel` | — |
| [CriterionProgress](../entities/schemas_task_brief_CriterionProgress.md) | 56 | `BaseModel` | — |
| [ProgressWrite](../entities/ProgressWrite.md) | 64 | `BaseModel` | — |
| [TaskReviewWrite](../entities/TaskReviewWrite.md) | 80 | `BaseModel` | — |
| [TaskReviewResponse](../entities/TaskReviewResponse.md) | 90 | `BaseModel` | — |
