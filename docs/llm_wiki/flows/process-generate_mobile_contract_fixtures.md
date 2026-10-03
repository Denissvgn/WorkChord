# generate_mobile_contract_fixtures

**Entry point:** `main` (`process`)
**Source:** [generate_mobile_contract_fixtures](../modules/generate_mobile_contract_fixtures.md)
**Modules touched:** [config](../modules/config.md), [generate_mobile_contract_fixtures](../modules/generate_mobile_contract_fixtures.md), [schemas_task](../modules/schemas_task.md), and 5 more

**Complete modules touched:**

- [config](../modules/config.md)
- [generate_mobile_contract_fixtures](../modules/generate_mobile_contract_fixtures.md)
- [schemas_task](../modules/schemas_task.md)
- [schemas_task_brief](../modules/schemas_task_brief.md)
- [schemas_task_domain](../modules/schemas_task_domain.md)
- [session_service](../modules/session_service.md)
- [task_detail](../modules/task_detail.md)
- [task_service](../modules/task_service.md)

**Related modules:** [schemas_task](../modules/schemas_task.md), [schemas_task_brief](../modules/schemas_task_brief.md), [schemas_task_domain](../modules/schemas_task_domain.md), [session_service](../modules/session_service.md), and 2 more

**Complete related modules:**

- [schemas_task](../modules/schemas_task.md)
- [schemas_task_brief](../modules/schemas_task_brief.md)
- [schemas_task_domain](../modules/schemas_task_domain.md)
- [session_service](../modules/session_service.md)
- [task_detail](../modules/task_detail.md)
- [task_service](../modules/task_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as argparse.ArgumentParser
    participant p2 as parser.add_argument
    participant p3 as parser.parse_args
    participant p4 as serialized_examples
    participant p5 as json.dumps
    participant p6 as build_examples
    participant p7 as TaskBrief
    participant p8 as BriefCriterion
    participant p9 as TaskResponse
    participant p10 as leaf.model_copy
    participant p11 as TaskReference
    participant p12 as TaskReferencePage
    participant p13 as TaskDetailResponse
    participant p14 as reference.model_copy
    participant p15 as TaskActionsResponse
    participant p16 as TaskActionAvailability
    participant p17 as TaskStatusChangeResponse
    participant p18 as CascadeUpdateInfo
    participant p19 as TaskReviewResponse
    participant p20 as datetime
    participant p21 as leaf.model_dump
    participant p22 as legacy.pop
    participant p23 as legacy.update
    participant p24 as Response
    participant p25 as _cookie_options
    participant p26 as get_settings
    p0-->>p1: argparse.ArgumentParser
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p3: parser.parse_args
    p0->>p4: serialized_examples
    p4-->>p5: json.dumps
    p4->>p6: build_examples
    p6->>p7: TaskBrief
    p6->>p8: BriefCriterion
    p6->>p9: TaskResponse
    p6-->>p10: leaf.model_copy
    p6->>p11: TaskReference
    p6->>p12: TaskReferencePage
    p6->>p12: TaskReferencePage
    p6->>p13: TaskDetailResponse
    p6-->>p14: reference.model_copy
    p6->>p15: TaskActionsResponse
    p6->>p16: TaskActionAvailability
    p6->>p16: TaskActionAvailability
    p6-->>p10: leaf.model_copy
    p6->>p17: TaskStatusChangeResponse
    p6->>p18: CascadeUpdateInfo
    p6->>p19: TaskReviewResponse
    p6-->>p20: datetime
    p6-->>p21: leaf.model_dump
    p6-->>p22: legacy.pop
    p6-->>p23: legacy.update
    p6-->>p24: Response
    p6->>p25: _cookie_options
    p25->>p26: get_settings
```

> Call sequence diagram shows 30 of 47 interactions; 17 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. main"]
    s2["2. argparse.ArgumentParser"]
    s3["3. parser.add_argument"]
    s4["4. parser.add_argument"]
    s5["5. parser.parse_args"]
    s6["6. serialized_examples"]
    s7["7. json.dumps"]
    s8["8. build_examples"]
    s9["9. TaskBrief"]
    s10["10. BriefCriterion"]
    s11["11. TaskResponse"]
    s12["12. leaf.model_copy"]
    s1 -. "argparse.ArgumentParser(description=__doc__)" .-> s2
    s1 -. "parser.add_argument('--output', type=Path, default=OUTPUT)" .-> s3
    s1 -. "parser.add_argument('--check', action='store_true')" .-> s4
    s1 -. "parser.parse_args(data not statically known)" .-> s5
    s1 -->|"serialized_examples(data not statically known)"| s6
    s6 -. "json.dumps(build_examples(...), ensure_ascii=False, indent=2, sort_keys=True)" .-> s7
    s6 -->|"build_examples(data not statically known)"| s8
    s8 -->|"TaskBrief(…)"| s9
    s8 -->|"BriefCriterion(id='outline', revision=2, text='The outline identifies the next delivery', verification='Open the saved outline')"| s10
    s8 -->|"TaskResponse(…)"| s11
    s8 -. "leaf.model_copy(update={...})" .-> s12
    b0["filesystem_read args.output.read_text"]
    s1 -. "filesystem_read args.output.read_text" .-> b0
    b1["filesystem_write args.output.write_text"]
    s1 -. "filesystem_write args.output.write_text" .-> b1
    b2["mutation legacy.pop"]
    s8 -. "mutation legacy.pop" .-> b2
    b3["mutation legacy.update"]
    s8 -. "mutation legacy.update" .-> b3
    click s1 "../modules/generate_mobile_contract_fixtures.md"
    click s6 "../modules/generate_mobile_contract_fixtures.md"
    click s8 "../modules/generate_mobile_contract_fixtures.md"
    click s9 "../modules/schemas_task_brief.md"
    click s10 "../modules/schemas_task_brief.md"
    click s11 "../modules/schemas_task.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `Path`, `OUTPUT` | - | - |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `serialized_examples` | - | - | - | `...` |
| `json.dumps` | - | - | - | - |
| `build_examples` | - | `UTC` | - | `{...}` |
| `TaskBrief` | - | - | - | - |
| `BriefCriterion` | - | - | - | - |
| `TaskResponse` | - | - | - | - |
| `leaf.model_copy` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 72 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.add_argument | 73 | `parser.add_argument('--output', type=Path, default=OUTPUT)` |
| main | parser.add_argument | 74 | `parser.add_argument('--check', action='store_true')` |
| main | parser.parse_args | 75 | `parser.parse_args(data not statically known)` |
| main | serialized_examples | 76 | `serialized_examples(data not statically known)` |
| serialized_examples | json.dumps | 68 | `json.dumps(build_examples(...), ensure_ascii=False, indent=2, sort_keys=True)` |
| serialized_examples | build_examples | 68 | `build_examples(data not statically known)` |
| build_examples | TaskBrief | 24 | `TaskBrief(goal='Deliver a reviewed outline', context='Coordinate with the team', scope='Write the outline', exclusions='Publishing', verification='Read the saved artifact', artifact_expectations='A versioned outline', acceptance_criteria=[...])` |
| build_examples | BriefCriterion | 26 | `BriefCriterion(id='outline', revision=2, text='The outline identifies the next delivery', verification='Open the saved outline')` |
| build_examples | TaskResponse | 27 | `TaskResponse(id=72, title='Review the outline', iteration_id=None, project_id=9, parent_id=71, description='Legacy text is retained independently', priority=3, effort_days=None, effort_hours=None, start_date=None, end_date=None, status='active', version=7, owner_profile_id=4, blocked_reason='Waiting for feedback', execution_mode='manual', brief=brief, brief_revision=3, artifact_revision=2, progress={...})` |
| build_examples | leaf.model_copy | 33 | `leaf.model_copy(update={...})` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| filesystem_read | `args.output.read_text` | `main` | 78 |
| filesystem_write | `args.output.write_text` | `main` | 82 |
| mutation | `legacy.pop` | `build_examples` | 53 |
| mutation | `legacy.update` | `build_examples` | 54 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 72 |
| unresolved_call | `main` | `parser.add_argument` | 73 |
| unresolved_call | `main` | `parser.add_argument` | 74 |
| unresolved_call | `main` | `parser.parse_args` | 75 |
| external_call | `serialized_examples` | `json.dumps` | 68 |
| unresolved_call | `build_examples` | `leaf.model_copy` | 33 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

Builds deterministic sample payloads through the current backend models and includes the selected OpenAPI components. Check mode compares the complete serialized output to the committed mobile resource and fails on drift. Normal mode writes only the requested output. The caller supplies backend imports and controls the execution environment; no provider credential or live account is required.
