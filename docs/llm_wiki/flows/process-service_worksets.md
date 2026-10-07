# service_worksets

**Entry point:** `main` (`process`)
**Source:** [service_worksets](../modules/service_worksets.md)
**Modules touched:** [agent_service](../modules/agent_service.md), [delivery](../modules/delivery.md), [load_common](../modules/load_common.md), [local_baseline](../modules/local_baseline.md), and 11 more

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
- [support_database](../modules/support_database.md)
- [team_member](../modules/team_member.md)
- [user_session](../modules/user_session.md)

**Related modules:** [app_database](../modules/app_database.md), [authority](../modules/authority.md), [capacity_service](../modules/capacity_service.md), [delivery](../modules/delivery.md), and 11 more

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
- [support_database](../modules/support_database.md)
- [task_detail_service](../modules/task_detail_service.md)
- [task_service](../modules/task_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as argparse.ArgumentParser
    participant p2 as parser.add_argument
    participant p3 as parser.parse_args
    participant p4 as args.output.exists
    participant p5 as parser.error
    participant p6 as asyncio.run
    participant p7 as run
    participant p8 as assert_safe_test_database_url
    participant p9 as _deployment_environment
    participant p10 as os.environ.get
    participant p11 as UnsafeDatabaseTarget
    participant p12 as make_url
    participant p13 as url.get_backend_name
    participant p14 as TEST_DATABASE_PATTERN.fullmatch
    participant p15 as Path(…).resolve
    participant p16 as Path
    participant p17 as (…).resolve
    participant p18 as tempfile.gettempdir
    participant p19 as database_path.is_relative_to
    participant p20 as database_path.name.startswith
    participant p21 as url.startswith
    participant p22 as create_async_engine
    p0-->>p1: argparse.ArgumentParser
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p3: parser.parse_args
    p0-->>p4: args.output.exists
    p0-->>p5: parser.error
    p0-->>p6: asyncio.run
    p0->>p7: run
    p7->>p8: assert_safe_test_database_url
    p8->>p9: _deployment_environment
    p9-->>p10: os.environ.get
    p8->>p11: UnsafeDatabaseTarget
    p8-->>p12: make_url
    p8-->>p13: url.get_backend_name
    p8->>p11: UnsafeDatabaseTarget
    p8-->>p14: TEST_DATABASE_PATTERN.fullmatch
    p8->>p11: UnsafeDatabaseTarget
    p8-->>p15: Path(…).resolve
    p8-->>p16: Path
    p8-->>p17: (…).resolve
    p8-->>p16: Path
    p8-->>p18: tempfile.gettempdir
    p8-->>p19: database_path.is_relative_to
    p8->>p11: UnsafeDatabaseTarget
    p8-->>p20: database_path.name.startswith
    p8->>p11: UnsafeDatabaseTarget
    p8->>p11: UnsafeDatabaseTarget
    p7-->>p21: url.startswith
    p7-->>p22: create_async_engine
```

> Call sequence diagram shows 30 of 201 interactions; 171 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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
    s11["11. assert_safe_test_database_url"]
    s12["12. _deployment_environment"]
    s1 -. "argparse.ArgumentParser(description=__doc__)" .-> s2
    s1 -. "parser.add_argument('--database-url', required=True)" .-> s3
    s1 -. "parser.add_argument('--declaration', type=Path, required=True)" .-> s4
    s1 -. "parser.add_argument('--output', type=Path, required=True)" .-> s5
    s1 -. "parser.parse_args(data not statically known)" .-> s6
    s1 -. "args.output.exists(data not statically known)" .-> s7
    s1 -. "parser.error('Output already exists')" .-> s8
    s1 -. "asyncio.run(run(...))" .-> s9
    s1 -->|"run(args.database_url, json.loads(...))"| s10
    s10 -->|"assert_safe_test_database_url(url)"| s11
    s11 -->|"_deployment_environment(deployment_environment)"| s12
    b0["filesystem_read args.declaration.read_text"]
    s1 -. "filesystem_read args.declaration.read_text" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["mutation db.add"]
    s10 -. "mutation db.add" .-> b2
    b3["mutation db.add"]
    s10 -. "mutation db.add" .-> b3
    b4["environment_read os.environ.get"]
    s12 -. "environment_read os.environ.get" .-> b4
    click s1 "../modules/service_worksets.md"
    click s10 "../modules/service_worksets.md"
    click s11 "../modules/support_database.md"
    click s12 "../modules/support_database.md"
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
| `run` | `url`, `declaration` | `Base`, `Task`, `Task`, `Task` | `task.title`, `result[...]` | `result` |
| `assert_safe_test_database_url` | `database_url: str \| URL`, `deployment_environment: str \| None`, `allowed_postgres_hosts: frozenset[str]`, `allowed_sqlite_root: Path \| None` | `TEST_DATABASE_PREFIX`, `TEST_DATABASE_PREFIX` | - | `url`, `url`, `url` |
| `_deployment_environment` | `explicit: str \| None` | - | - | `...` |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 74 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.add_argument | 75 | `parser.add_argument('--database-url', required=True)` |
| main | parser.add_argument | 75 | `parser.add_argument('--declaration', type=Path, required=True)` |
| main | parser.add_argument | 76 | `parser.add_argument('--output', type=Path, required=True)` |
| main | parser.parse_args | 76 | `parser.parse_args(data not statically known)` |
| main | args.output.exists | 77 | `args.output.exists(data not statically known)` |
| main | parser.error | 77 | `parser.error('Output already exists')` |
| main | asyncio.run | 78 | `asyncio.run(run(...))` |
| main | run | 78 | `run(args.database_url, json.loads(...))` |
| run | assert_safe_test_database_url | 25 | `assert_safe_test_database_url(url)` |
| assert_safe_test_database_url | _deployment_environment | 49 | `_deployment_environment(deployment_environment)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| filesystem_read | `args.declaration.read_text` | `main` | 78 |
| output | `print` | `main` | 79 |
| mutation | `db.add` | `run` | 32 |
| mutation | `db.add` | `run` | 36 |
| environment_read | `os.environ.get` | `_deployment_environment` | 32 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 74 |
| unresolved_call | `main` | `parser.add_argument` | 75 |
| unresolved_call | `main` | `parser.add_argument` | 76 |
| unresolved_call | `main` | `parser.parse_args` | 76 |
| unresolved_call | `main` | `args.output.exists` | 77 |
| unresolved_call | `main` | `parser.error` | 77 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
