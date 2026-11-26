# readiness_check

**Entry point:** `readiness_check` (`http`)
**Source:** [app_main](../modules/app_main.md)
**Modules touched:** [app_database](../modules/app_database.md), [app_main](../modules/app_main.md), [app_maintenance](../modules/app_maintenance.md), [config](../modules/config.md), and 4 more

**Complete modules touched:**

- [app_database](../modules/app_database.md)
- [app_main](../modules/app_main.md)
- [app_maintenance](../modules/app_maintenance.md)
- [config](../modules/config.md)
- [database_config](../modules/database_config.md)
- [observability](../modules/observability.md)
- [time](../modules/time.md)
- [upgrade_service](../modules/upgrade_service.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as readiness_check
    participant p1 as readiness_snapshot
    participant p2 as get_settings
    participant p3 as _readiness_detail_authorized
    participant p4 as head_revision
    participant p5 as _queue_snapshot
    participant p6 as maintenance_state
    participant p7 as alembic_config
    participant p8 as maintenance_configuration_fingerprint
    participant p9 as database_configuration
    participant p10 as parse_database_configuration
    participant p11 as _postgresql_snapshot
    participant p12 as database_runtime_summary
    participant p13 as _resident_set_size_bytes
    participant p14 as Settings
    participant p15 as utc_now
    participant p16 as UpgradeError
    participant p17 as as_utc
    participant p18 as migrations_dir
    participant p19 as alembic_safe_url
    participant p20 as _settings_value
    participant p21 as DatabaseConfigurationError
    participant p22 as DatabaseConfiguration
    participant p23 as redact_database_url
    participant p24 as _certificate_path
    participant p25 as JSONResponse
    participant p26 as request.headers.get
    participant p27 as hmac.compare_digest
    participant p28 as asyncio.timeout
    participant p29 as presented.encode
    participant p30 as async_session_maker
    p0->>p1: readiness_snapshot
    p0->>p2: get_settings
    p0->>p3: _readiness_detail_authorized
    p1->>p4: head_revision
    p1->>p5: _queue_snapshot
    p1->>p6: maintenance_state
    p4->>p7: alembic_config
    p6->>p8: maintenance_configuration_fingerprint
    p7->>p9: database_configuration
    p9->>p10: parse_database_configuration
    p1->>p11: _postgresql_snapshot
    p1->>p12: database_runtime_summary
    p1->>p13: _resident_set_size_bytes
    p2->>p14: Settings
    p5->>p15: utc_now
    p4->>p16: UpgradeError
    p5->>p17: as_utc
    p7->>p18: migrations_dir
    p7->>p19: alembic_safe_url
    p10->>p20: _settings_value
    p10->>p21: DatabaseConfigurationError
    p10->>p22: DatabaseConfiguration
    p10->>p23: redact_database_url
    p10->>p24: _certificate_path
    p0-->>p25: JSONResponse(status_code=..., content=payload)
    p3-->>p26: request.headers.get('x-readiness-detail-token', '')
    p3-->>p27: hmac.compare_digest(presented.encode(...), expected.encode(...))
    p1-->>p28: asyncio.timeout(settings.database_readiness_timeout_seconds)
    p3-->>p29: presented.encode('utf-8')
    p1-->>p30: async_session_maker
```

> Call sequence diagram shows 30 of 210 interactions; 180 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 3 of 75 (72 omitted); unresolved 3 of 65 (62 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/observability.py:readiness_snapshot` | 2 | [backend/app/config.py](../modules/config.md) | internal | 1 |
| `backend/app/services/upgrade_service.py:head_revision` | 5 | - | external | 2 |
| `backend/app/services/upgrade_service.py:migrations_dir` | 8 | - | unresolved | 1 |
| `backend/app/services/upgrade_service.py:migrations_dir` | 8 | - | external | 1 |
| `backend/app/services/upgrade_service.py:alembic_config` | 7 | - | external | 3 |
| `backend/app/services/upgrade_service.py:alembic_config` | 7 | - | unresolved | 2 |
| `backend/app/database_config.py:alembic_safe_url` | 16 | - | external | 2 |
| `backend/app/database_config.py:alembic_safe_url` | 16 | - | unresolved | 2 |
> Omission summary shows 8 of 32 groups; 24 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 71; effect analysis evaluated: 47, partial: 0, unavailable: 24. Counts include steps omitted from the displayed trace.

Collector observations for 47 source steps with known totals: observed: 133, emitted: 133, omitted: 0. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `readiness_check` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `readiness_snapshot` | `available` | `evaluated` | `available` | `6` | `6` | `0` |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `head_revision` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `ScriptDirectory.from_config` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `alembic_config` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `migrations_dir` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Path(…).resolve` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `Path (backend/app/services/upgr…service.py:migrations_dir)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `Config` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `str (backend/app/services/upgr…service.py:alembic_config)` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. readiness_check"]
    s2["2. readiness_snapshot"]
    s3["3. get_settings"]
    s4["4. Settings"]
    s5["5. head_revision"]
    s6["6. ScriptDirectory.from_config"]
    s7["7. alembic_config"]
    s8["8. migrations_dir"]
    s9["9. Path(…).resolve"]
    s10["10. Path (backend/app/services/upgr…service.py:migrations_dir)"]
    s11["11. Config"]
    s12["12. str (backend/app/services/upgr…service.py:alembic_config)"]
    s1 -->|"readiness_snapshot(data not statically known)"| s2
    s2 -->|"get_settings(data not statically known)"| s3
    s3 -->|"Settings(data not statically known)"| s4
    s2 -->|"head_revision(data not statically known)"| s5
    s5 -. "ScriptDirectory.from_config(alembic_config(...))" .-> s6
    s5 -->|"alembic_config(data not statically known)"| s7
    s7 -->|"migrations_dir(data not statically known)"| s8
    s8 -. "Path(…).resolve(data not statically known)" .-> s9
    s8 -. "Path (backend/app/services/upgr…service.py:migrations_dir)(__file__)" .-> s10
    s7 -. "Config(str(...))" .-> s11
    s7 -. "str (backend/app/services/upgr…service.py:alembic_config)(...)" .-> s12
    click s1 "../modules/app_main.md"
    click s2 "../modules/observability.md"
    click s3 "../modules/config.md"
    click s4 "../modules/config.md"
    click s5 "../modules/upgrade_service.md"
    click s7 "../modules/upgrade_service.md"
    click s8 "../modules/upgrade_service.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `readiness_check` | `request: Request` | - | - | `JSONResponse(...)` |
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
| `str (backend/app/services/upgr…service.py:alembic_config)` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| readiness_check | readiness_snapshot | 276 | `readiness_snapshot(data not statically known)` |
| readiness_snapshot | get_settings | 252 | `get_settings(data not statically known)` |
| get_settings | Settings | 527 | `Settings(data not statically known)` |
| readiness_snapshot | head_revision | 253 | `head_revision(data not statically known)` |
| head_revision | ScriptDirectory.from_config | 90 | `ScriptDirectory.from_config(alembic_config(...))` |
| head_revision | alembic_config | 90 | `alembic_config(data not statically known)` |
| alembic_config | migrations_dir | 70 | `migrations_dir(data not statically known)` |
| migrations_dir | Path(…).resolve | 59 | `Path(__file__).resolve(data not statically known)` |
| migrations_dir | Path (backend/app/services/upgr…service.py:migrations_dir) | 59 | `Path(__file__)` |
| alembic_config | Config | 71 | `Config(str(...))` |
| alembic_config | str (backend/app/services/upgr…service.py:alembic_config) | 71 | `str(...)` |

### Boundary effects

*No boundary-effect observations were captured in this static trace.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `head_revision` | `ScriptDirectory.from_config` | 90 |
| unresolved_call | `migrations_dir` | `Path(__file__).resolve` | 59 |
| external_call | `alembic_config` | `Config` | 71 |
| step_limit | `readiness_check` | `first 12 steps` | 0 |
| truncated_flow | `readiness_check` | `depth limit` | 0 |

## Behavior

This flow starts at `readiness_check` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
