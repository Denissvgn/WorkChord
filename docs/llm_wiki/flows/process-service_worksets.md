# service_worksets

**Entry point:** `main` (`process`)
**Source:** [service_worksets](../modules/service_worksets.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [delivery](../modules/delivery.md), [load_common](../modules/load_common.md), [local_baseline](../modules/local_baseline.md), and 12 more

**Complete modules touched:**

- [agent_service](../modules/agent_service.md)
- [delivery](../modules/delivery.md)
- [load_common](../modules/load_common.md)
- [local_baseline](../modules/local_baseline.md)
- [models_agent](../modules/models_agent.md)
- [models_calendar](../modules/models_calendar.md)
- [models_iteration](../modules/models_iteration.md)
- [models_project](../modules/models_project.md)
- [models_task](../modules/models_task.md)
- [result](../modules/result.md)
- [run](../modules/run.md)
- [service_worksets](../modules/service_worksets.md)
- [source_binding](../modules/source_binding.md)
- [support_database](../modules/support_database.md)
- [team_member](../modules/team_member.md)
- [user_session](../modules/user_session.md)

**Related modules:** [app_database](../modules/app_database.md), [authority](../modules/authority.md), [capacity_service](../modules/capacity_service.md), [delivery](../modules/delivery.md), and 12 more

**Complete related modules:**

- [app_database](../modules/app_database.md)
- [authority](../modules/authority.md)
- [capacity_service](../modules/capacity_service.md)
- [delivery](../modules/delivery.md)
- [delivery_metrics_service](../modules/delivery_metrics_service.md)
- [load_common](../modules/load_common.md)
- [local_baseline](../modules/local_baseline.md)
- [models_agent](../modules/models_agent.md)
- [models_iteration](../modules/models_iteration.md)
- [models_task](../modules/models_task.md)
- [project_service](../modules/project_service.md)
- [query_limits](../modules/query_limits.md)
- [source_binding](../modules/source_binding.md)
- [support_database](../modules/support_database.md)
- [task_detail_service](../modules/task_detail_service.md)
- [task_service](../modules/task_service.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as run
    participant p2 as atomic_write_json
    participant p3 as seal_document
    participant p4 as assert_safe_test_database_url
    participant p5 as seed_delivery_scenario
    participant p6 as summarize
    participant p7 as verify_binding
    participant p8 as latency_summary
    participant p9 as percentile
    participant p10 as validate_declaration
    participant p11 as source_binding
    participant p12 as Iteration
    participant p13 as Task
    participant p14 as AgentRun
    participant p15 as _deployment_environment
    participant p16 as Calendar
    participant p17 as QualificationInputError
    participant p18 as UnsafeDatabaseTarget
    participant p19 as Project
    participant p20 as sha256_bytes
    participant p21 as canonical_json_bytes
    participant p22 as TeamMemberProfile
    participant p23 as TeamMember
    participant p24 as AgentActor
    participant p25 as Recorder
    participant p26 as hash_api_key
    participant p27 as UserSession
    participant p28 as Attempt
    participant p29 as argparse.ArgumentParser
    participant p30 as parser.add_argument
    p0->>p1: run
    p0->>p2: atomic_write_json
    p2->>p3: seal_document
    p1->>p4: assert_safe_test_database_url
    p1->>p5: seed_delivery_scenario
    p1->>p6: summarize
    p1->>p7: verify_binding
    p6->>p8: latency_summary
    p8->>p9: percentile
    p1->>p10: validate_declaration
    p1->>p11: source_binding
    p1->>p12: Iteration
    p1->>p13: Task
    p1->>p14: AgentRun
    p4->>p15: _deployment_environment
    p5->>p16: Calendar
    p3->>p17: QualificationInputError
    p4->>p18: UnsafeDatabaseTarget
    p5->>p19: Project
    p3->>p20: sha256_bytes
    p3->>p21: canonical_json_bytes
    p5->>p22: TeamMemberProfile
    p5->>p23: TeamMember
    p5->>p24: AgentActor
    p6->>p25: Recorder
    p5->>p26: hash_api_key
    p5->>p27: UserSession
    p6->>p28: Attempt
    p0-->>p29: argparse.ArgumentParser(description=__doc__)
    p0-->>p30: parser.add_argument('--database-url', required=True)
```

> Call sequence diagram shows 30 of 266 interactions; 236 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 105 (104 omitted); unresolved 1 of 108 (107 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `scripts/load/service_worksets.py:main` | 1 | - | unresolved | 6 |
| `scripts/load/service_worksets.py:main` | 1 | - | external | 3 |
| `scripts/load/service_worksets.py:validate_declaration` | 11 | - | unresolved | 4 |
| `scripts/load/service_worksets.py:validate_declaration` | 11 | - | external | 2 |
| `scripts/load/source_binding.py:source_binding` | 18 | - | unresolved | 9 |
| `scripts/load/source_binding.py:source_binding` | 18 | - | external | 9 |
| `backend/tests/support/database.py:_deployment_environment` | 38 | - | external | 1 |
| `backend/tests/support/database.py:assert_safe_test_database_url` | 37 | - | external | 4 |
> Omission summary shows 8 of 38 groups; 30 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 54; effect analysis evaluated: 20, partial: 0, unavailable: 34. Counts include steps omitted from the displayed trace.

Collector observations for 20 source steps with known totals: observed: 85, emitted: 85, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `5` | `5` | `0` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.parse_args` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `args.output.exists` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.error` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `asyncio.run` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `run` | `available` | `evaluated` | `available` | `16` | `16` | `0` |
| `validate_declaration` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `declaration.get (scripts/load/service_work…s.py:validate_declaration)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. argparse.ArgumentParser"]
    s3["3. parser.add_argument"]
    s4["4. parser.add_argument"]
    s5["5. parser.add_argument"]
    s6["6. parser.parse_args"]
    s7["7. args.output.exists"]
    s8["8. parser.error"]
    s9["9. asyncio.run"]
    s10["10. run"]
    s11["11. validate_declaration"]
    s12["12. declaration.get (scripts/load/service_work…s.py:validate_declaration)"]
    s1 -. "argparse.ArgumentParser(description=__doc__)" .-> s2
    s1 -. "parser.add_argument('--database-url', required=True)" .-> s3
    s1 -. "parser.add_argument('--declaration', type=Path, required=True)" .-> s4
    s1 -. "parser.add_argument('--output', type=Path, required=True)" .-> s5
    s1 -. "parser.parse_args(data not statically known)" .-> s6
    s1 -. "args.output.exists(data not statically known)" .-> s7
    s1 -. "parser.error('Output already exists')" .-> s8
    s1 -. "asyncio.run(run(...))" .-> s9
    s1 -->|"run(args.database_url, json.loads(...))"| s10
    s10 -->|"validate_declaration(declaration)"| s11
    s11 -. "declaration.get (scripts/load/service_work…s.py:validate_declaration)('concurrency')" .-> s12
    b0["filesystem_read args.declaration.read_text"]
    s1 -. "filesystem_read args.declaration.read_text" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["mutation db.add"]
    s10 -. "mutation db.add" .-> b2
    b3["mutation db.add"]
    s10 -. "mutation db.add" .-> b3
    b4["mutation plans.append"]
    s10 -. "mutation plans.append" .-> b4
    click s1 "../modules/service_worksets.md"
    click s10 "../modules/service_worksets.md"
    click s11 "../modules/service_worksets.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
    class b4 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `Path`, `Path` | - | `...` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `args.output.exists` | - | - | - | - |
| `parser.error` | - | - | - | - |
| `asyncio.run` | - | - | - | - |
| `run` | `url`, `declaration` | `Base`, `Task`, `Task`, `Task` | `task.title`, `result[...]`, `result[...]`, `result[...]`, `result[...]`, `result[...]` | `result` |
| `validate_declaration` | `declaration` | - | - | - |
| `declaration.get (scripts/load/service_work…s.py:validate_declaration)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 122 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.add_argument | 123 | `parser.add_argument('--database-url', required=True)` |
| main | parser.add_argument | 123 | `parser.add_argument('--declaration', type=Path, required=True)` |
| main | parser.add_argument | 124 | `parser.add_argument('--output', type=Path, required=True)` |
| main | parser.parse_args | 124 | `parser.parse_args(data not statically known)` |
| main | args.output.exists | 125 | `args.output.exists(data not statically known)` |
| main | parser.error | 125 | `parser.error('Output already exists')` |
| main | asyncio.run | 126 | `asyncio.run(run(...))` |
| main | run | 126 | `run(args.database_url, json.loads(...))` |
| run | validate_declaration | 34 | `validate_declaration(declaration)` |
| validate_declaration | declaration.get (scripts/load/service_work…s.py:validate_declaration) | 27 | `declaration.get('concurrency')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| filesystem_read | `args.declaration.read_text` | `main` | 126 |
| output | `print` | `main` | 127 |
| mutation | `db.add` | `run` | 56 |
| mutation | `db.add` | `run` | 60 |
| mutation | `plans.append` | `run` | 95 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 122 |
| unresolved_call | `main` | `parser.add_argument` | 123 |
| unresolved_call | `main` | `parser.add_argument` | 124 |
| unresolved_call | `main` | `parser.parse_args` | 124 |
| unresolved_call | `main` | `args.output.exists` | 125 |
| unresolved_call | `main` | `parser.error` | 125 |
| unresolved_call | `validate_declaration` | `declaration.get` | 27 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
