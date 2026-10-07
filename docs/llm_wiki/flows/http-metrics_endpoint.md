# metrics_endpoint

**Entry point:** `metrics_endpoint` (`http`)
**Source:** [app_main](../modules/app_main.md)
**Modules touched:** [app_database](../modules/app_database.md), [app_main](../modules/app_main.md), [config](../modules/config.md), [database_config](../modules/database_config.md), and 4 more

**Complete modules touched:**

- [app_database](../modules/app_database.md)
- [app_main](../modules/app_main.md)
- [config](../modules/config.md)
- [database_config](../modules/database_config.md)
- [maintenance](../modules/maintenance.md)
- [observability](../modules/observability.md)
- [time](../modules/time.md)
- [upgrade_service](../modules/upgrade_service.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as metrics_endpoint
    participant p1 as collect_metrics
    participant p2 as readiness_snapshot
    participant p3 as get_settings
    participant p4 as Settings
    participant p5 as head_revision
    participant p6 as ScriptDirectory.from_config
    participant p7 as alembic_config
    participant p8 as migrations_dir
    participant p9 as Path(…).resolve
    participant p10 as Path (backend/app/services/upgr…service.py:migrations_dir)
    participant p11 as Config
    participant p12 as str (backend/app/services/upgr…service.py:alembic_config)
    participant p13 as config.set_main_option
    participant p14 as alembic_safe_url
    participant p15 as isinstance
    participant p16 as make_url
    participant p17 as url.render_as_string(…).replace
    participant p18 as url.render_as_string
    participant p19 as database_configuration
    participant p20 as parse_database_configuration
    participant p21 as script.get_heads
    participant p22 as len (backend/app/services/upgr…_service.py:head_revision)
    participant p23 as UpgradeError
    participant p24 as ', '.join
    participant p25 as asyncio.timeout
    participant p26 as async_session_maker
    participant p27 as db.execute (backend/app/observability.py:readiness_snapshot)
    p0->>p1: collect_metrics
    p1->>p2: readiness_snapshot
    p2->>p3: get_settings
    p3->>p4: Settings
    p2->>p5: head_revision
    p5-->>p6: ScriptDirectory.from_config
    p5->>p7: alembic_config
    p7->>p8: migrations_dir
    p8-->>p9: Path(…).resolve
    p8-->>p10: Path (backend/app/services/upgr…service.py:migrations_dir)
    p7-->>p11: Config
    p7-->>p12: str (backend/app/services/upgr…service.py:alembic_config)
    p7-->>p13: config.set_main_option
    p7-->>p12: str (backend/app/services/upgr…service.py:alembic_config)
    p7-->>p13: config.set_main_option
    p7->>p14: alembic_safe_url
    p14-->>p15: isinstance
    p14-->>p16: make_url
    p14-->>p17: url.render_as_string(…).replace
    p14-->>p18: url.render_as_string
    p7->>p19: database_configuration
    p19->>p20: parse_database_configuration
    p19->>p3: get_settings
    p5-->>p21: script.get_heads
    p5-->>p22: len (backend/app/services/upgr…_service.py:head_revision)
    p5->>p23: UpgradeError
    p5-->>p24: ', '.join
    p2-->>p25: asyncio.timeout
    p2-->>p26: async_session_maker
    p2-->>p27: db.execute (backend/app/observability.py:readiness_snapshot)
```

> Call sequence diagram shows 30 of 126 interactions; 96 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. metrics_endpoint"]
    s2["2. collect_metrics"]
    s3["3. readiness_snapshot"]
    s4["4. get_settings"]
    s5["5. Settings"]
    s6["6. head_revision"]
    s7["7. ScriptDirectory.from_config"]
    s8["8. alembic_config"]
    s9["9. migrations_dir"]
    s10["10. Path(…).resolve"]
    s11["11. Path (backend/app/services/upgr…service.py:migrations_dir)"]
    s12["12. Config"]
    s1 -->|"collect_metrics(data not statically known)"| s2
    s2 -->|"readiness_snapshot(data not statically known)"| s3
    s3 -->|"get_settings(data not statically known)"| s4
    s4 -->|"Settings(data not statically known)"| s5
    s3 -->|"head_revision(data not statically known)"| s6
    s6 -. "ScriptDirectory.from_config(alembic_config(...))" .-> s7
    s6 -->|"alembic_config(data not statically known)"| s8
    s8 -->|"migrations_dir(data not statically known)"| s9
    s9 -. "Path(…).resolve(data not statically known)" .-> s10
    s9 -. "Path (backend/app/services/upgr…service.py:migrations_dir)(__file__)" .-> s11
    s8 -. "Config(str(...))" .-> s12
    click s1 "../modules/app_main.md"
    click s2 "../modules/observability.md"
    click s3 "../modules/observability.md"
    click s4 "../modules/config.md"
    click s5 "../modules/config.md"
    click s6 "../modules/upgrade_service.md"
    click s8 "../modules/upgrade_service.md"
    click s9 "../modules/upgrade_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `metrics_endpoint` | - | - | - | `PlainTextResponse(...)` |
| `collect_metrics` | - | - | - | - |
| `readiness_snapshot` | - | `SQLAlchemyError`, `SQLAlchemyError`, `SQLAlchemyError`, `SQLAlchemyError` | - | `(...)`, `(...)` |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `head_revision` | - | - | - | `heads[...]` |
| `ScriptDirectory.from_config` | - | - | - | - |
| `alembic_config` | `connection: Connection \| None` | - | `config.attributes[...]` | `config` |
| `migrations_dir` | - | - | - | `...` |
| `Path(…).resolve` | - | - | - | - |
| `Path (backend/app/services/upgr…service.py:migrations_dir)` | - | - | - | - |
| `Config` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| metrics_endpoint | collect_metrics | 278 | `collect_metrics(data not statically known)` |
| collect_metrics | readiness_snapshot | 399 | `readiness_snapshot(data not statically known)` |
| readiness_snapshot | get_settings | 252 | `get_settings(data not statically known)` |
| get_settings | Settings | 481 | `Settings(data not statically known)` |
| readiness_snapshot | head_revision | 253 | `head_revision(data not statically known)` |
| head_revision | ScriptDirectory.from_config | 90 | `ScriptDirectory.from_config(alembic_config(...))` |
| head_revision | alembic_config | 90 | `alembic_config(data not statically known)` |
| alembic_config | migrations_dir | 70 | `migrations_dir(data not statically known)` |
| migrations_dir | Path(…).resolve | 59 | `Path(__file__).resolve(data not statically known)` |
| migrations_dir | Path (backend/app/services/upgr…service.py:migrations_dir) | 59 | `Path(__file__)` |
| alembic_config | Config | 71 | `Config(str(...))` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `head_revision` | `ScriptDirectory.from_config` | 90 |
| unresolved_call | `migrations_dir` | `Path(__file__).resolve` | 59 |
| external_call | `alembic_config` | `Config` | 71 |
| step_limit | `metrics_endpoint` | `first 12 steps` | 0 |
| truncated_flow | `metrics_endpoint` | `depth limit` | 0 |

## Behavior

This flow starts at `metrics_endpoint` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
