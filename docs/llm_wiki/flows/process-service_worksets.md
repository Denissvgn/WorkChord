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
    participant p8 as validate_declaration
    participant p9 as declaration.get (scripts/load/service_work…s.py:validate_declaration)
    participant p10 as type (scripts/load/service_work…s.py:validate_declaration)
    participant p11 as declaration.get(…).get
    participant p12 as ValueError (scripts/load/service_work…s.py:validate_declaration)
    participant p13 as source_binding
    participant p14 as Path(…).resolve (scripts/load/source_binding.py:source_binding)
    participant p15 as Path (scripts/load/source_binding.py:source_binding)
    participant p16 as sorted (scripts/load/source_binding.py:source_binding)
    participant p17 as root.glob
    participant p18 as str (scripts/load/source_binding.py:source_binding)
    participant p19 as path.relative_to
    participant p20 as hashlib.sha256(…).hexdigest (scripts/load/source_binding.py:source_binding, 1)
    participant p21 as hashlib.sha256 (scripts/load/source_binding.py:source_binding)
    participant p22 as path.read_bytes
    participant p23 as hashlib.sha256(…).hexdigest (scripts/load/source_binding.py:source_binding)
    p0-->>p1: argparse.ArgumentParser
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p3: parser.parse_args
    p0-->>p4: args.output.exists
    p0-->>p5: parser.error
    p0-->>p6: asyncio.run
    p0->>p7: run
    p7->>p8: validate_declaration
    p8-->>p9: declaration.get (scripts/load/service_work…s.py:validate_declaration)
    p8-->>p10: type (scripts/load/service_work…s.py:validate_declaration)
    p8-->>p9: declaration.get (scripts/load/service_work…s.py:validate_declaration)
    p8-->>p11: declaration.get(…).get
    p8-->>p9: declaration.get (scripts/load/service_work…s.py:validate_declaration)
    p8-->>p12: ValueError (scripts/load/service_work…s.py:validate_declaration)
    p7->>p13: source_binding
    p13-->>p14: Path(…).resolve (scripts/load/source_binding.py:source_binding)
    p13-->>p15: Path (scripts/load/source_binding.py:source_binding)
    p13-->>p16: sorted (scripts/load/source_binding.py:source_binding)
    p13-->>p17: root.glob
    p13-->>p17: root.glob
    p13-->>p17: root.glob
    p13-->>p18: str (scripts/load/source_binding.py:source_binding)
    p13-->>p19: path.relative_to
    p13-->>p20: hashlib.sha256(…).hexdigest (scripts/load/source_binding.py:source_binding, 1)
    p13-->>p21: hashlib.sha256 (scripts/load/source_binding.py:source_binding)
    p13-->>p22: path.read_bytes
    p13-->>p23: hashlib.sha256(…).hexdigest (scripts/load/source_binding.py:source_binding)
    p13-->>p21: hashlib.sha256 (scripts/load/source_binding.py:source_binding)
```

> Call sequence diagram shows 30 of 266 interactions; 236 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

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
