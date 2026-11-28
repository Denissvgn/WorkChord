# worker

**Entry point:** `main` (`process`)
**Source:** [worker](../modules/worker.md)
**Modules touched:** [app_database](../modules/app_database.md), [app_maintenance](../modules/app_maintenance.md), [authority](../modules/authority.md), [commands](../modules/commands.md), and 8 more

**Complete modules touched:**

- [app_database](../modules/app_database.md)
- [app_maintenance](../modules/app_maintenance.md)
- [authority](../modules/authority.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [database_runtime](../modules/database_runtime.md)
- [discussion_service](../modules/discussion_service.md)
- [outbound_webhook_service](../modules/outbound_webhook_service.md)
- [task_reactivation_service](../modules/task_reactivation_service.md)
- [time](../modules/time.md)
- [upgrade_service](../modules/upgrade_service.md)
- [worker](../modules/worker.md)

**Related modules:** [app_database](../modules/app_database.md), [config](../modules/config.md), [outbound_webhook_service](../modules/outbound_webhook_service.md), [task_reactivation_service](../modules/task_reactivation_service.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as _run
    participant p2 as build_parser
    participant p3 as get_settings
    participant p4 as init_db
    participant p5 as run_due_outbound_delivery_jobs
    participant p6 as outbound_delivery_worker_loop
    participant p7 as postponement_check_loop
    participant p8 as assert_database_current
    participant p9 as require_background_writes_enabled
    participant p10 as run_due_postponement_checks
    participant p11 as OutboundWebhookService.run_due_jobs
    participant p12 as inspect_database
    participant p13 as OutboundWebhookService.claim_due_deliveries
    participant p14 as OutboundWebhookService.process_claimed_delivery
    participant p15 as ReactivationService.run_date_check
    participant p16 as _inspect_database_connection
    participant p17 as _sync_engine
    participant p18 as OutboundWebhookService._claim_due_postgresql
    participant p19 as ReactivationService._due
    participant p20 as commit_or_flush
    participant p21 as OutboundWebhookService._attempt_delivery
    participant p22 as ReactivationService.evaluate_one
    participant p23 as OutboundWebhookService._claim_delivery_id
    participant p24 as close_database
    participant p25 as Settings
    participant p26 as OutboundWebhookService
    participant p27 as UpgradeError
    participant p28 as MaintenanceModeError
    participant p29 as asyncio.run
    participant p30 as build_parser().parse_args
    p0->>p1: _run
    p0->>p2: build_parser
    p1->>p3: get_settings
    p1->>p4: init_db
    p1->>p5: run_due_outbound_delivery_jobs
    p1->>p6: outbound_delivery_worker_loop
    p1->>p7: postponement_check_loop
    p4->>p8: assert_database_current
    p5->>p9: require_background_writes_enabled
    p7->>p10: run_due_postponement_checks
    p5->>p11: OutboundWebhookService.run_due_jobs
    p8->>p12: inspect_database
    p11->>p13: OutboundWebhookService.claim_due_deliveries
    p11->>p14: OutboundWebhookService.process_claimed_delivery
    p10->>p15: ReactivationService.run_date_check
    p12->>p16: _inspect_database_connection
    p12->>p17: _sync_engine
    p13->>p18: OutboundWebhookService._claim_due_postgresql
    p15->>p19: ReactivationService._due
    p14->>p20: commit_or_flush
    p14->>p21: OutboundWebhookService._attempt_delivery
    p15->>p22: ReactivationService.evaluate_one
    p13->>p23: OutboundWebhookService._claim_delivery_id
    p1->>p24: close_database
    p3->>p25: Settings
    p5->>p26: OutboundWebhookService
    p8->>p27: UpgradeError
    p9->>p28: MaintenanceModeError
    p0-->>p29: asyncio.run(_run(...))
    p0-->>p30: build_parser().parse_args(argv)
```

> Call sequence diagram shows 30 of 178 interactions; 148 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 39 (38 omitted); unresolved 1 of 76 (75 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/cli/worker.py:build_parser` | 3 | - | external | 1 |
| `backend/app/cli/worker.py:build_parser` | 3 | - | unresolved | 1 |
| `backend/app/cli/worker.py:_run` | 7 | - | external | 7 |
| `backend/app/services/upgrade_service.py:_inspect_database_connection` | 16 | - | external | 4 |
| `backend/app/services/upgrade_service.py:_inspect_database_connection` | 16 | - | unresolved | 1 |
| `backend/app/services/upgrade_service.py:_inspect_database_connection` | 16 | [backend/app/services/upgrade_service.py](../modules/upgrade_service.md) | internal | 3 |
| `backend/app/services/upgrade_service.py:_sync_engine` | 25 | [backend/app/services/upgrade_service.py](../modules/upgrade_service.md) | internal | 1 |
| `backend/app/services/upgrade_service.py:_sync_engine` | 25 | - | external | 2 |
> Omission summary shows 8 of 60 groups; 52 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 64; effect analysis evaluated: 55, partial: 1, unavailable: 8. Counts include steps omitted from the displayed trace.

Collector observations for 56 source steps with known totals: observed: 236, emitted: 224, omitted: 12. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `build_parser().parse_args` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `build_parser` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `asyncio.run` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `_run` | `available` | `evaluated` | `available` | `14` | `14` | `0` |
| `get_settings` | `available` | `evaluated` | `available` | `1` | `1` | `0` |
| `Settings` | `unavailable` | `unavailable` | `unavailable` | — | — | — |
| `print` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `print` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `print` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. build_parser().parse_args"]
    s3["3. build_parser"]
    s4["4. argparse.ArgumentParser"]
    s5["5. parser.add_argument"]
    s6["6. asyncio.run"]
    s7["7. _run"]
    s8["8. get_settings"]
    s9["9. Settings"]
    s10["10. print"]
    s11["11. print"]
    s12["12. print"]
    s1 -. "build_parser().parse_args(argv)" .-> s2
    s1 -->|"build_parser(data not statically known)"| s3
    s3 -. "argparse.ArgumentParser(description='Run the WorkChord durable delivery worker.')" .-> s4
    s3 -. "parser.add_argument('--once', action='store_true', help='Process one bounded batch and exit.')" .-> s5
    s1 -. "asyncio.run(_run(...))" .-> s6
    s1 -->|"_run(once=args.once)"| s7
    s7 -->|"get_settings(data not statically known)"| s8
    s8 -->|"Settings(data not statically known)"| s9
    s7 -. "print('DATABASE_PROCESS_ROLE=delivery_worker is required', file=sys.stderr)" .-> s10
    s7 -. "print('Outbound delivery worker is disabled', file=sys.stderr)" .-> s11
    s7 -. "print(..., file=sys.stderr)" .-> s12
    b0["output print"]
    s7 -. "output print" .-> b0
    b1["output print"]
    s7 -. "output print" .-> b1
    b2["output print"]
    s7 -. "output print" .-> b2
    b3["output print"]
    s7 -. "output print" .-> b3
    click s1 "../modules/worker.md"
    click s3 "../modules/worker.md"
    click s7 "../modules/worker.md"
    click s8 "../modules/config.md"
    click s9 "../modules/config.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | `argv: Optional[list[str]]` | - | - | `asyncio.run(...)` |
| `build_parser().parse_args` | - | - | - | - |
| `build_parser` | - | - | - | `parser` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `asyncio.run` | - | - | - | - |
| `_run` | `once: bool` | `sys`, `sys`, `sys`, `signal` | - | `2`, `2`, `0`, `0`, `0` |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `print` | - | - | - | - |
| `print` | - | - | - | - |
| `print` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | build_parser().parse_args | 81 | `build_parser().parse_args(argv)` |
| main | build_parser | 81 | `build_parser(data not statically known)` |
| build_parser | argparse.ArgumentParser | 21 | `argparse.ArgumentParser(description='Run the WorkChord durable delivery worker.')` |
| build_parser | parser.add_argument | 24 | `parser.add_argument('--once', action='store_true', help='Process one bounded batch and exit.')` |
| main | asyncio.run | 82 | `asyncio.run(_run(...))` |
| main | _run | 82 | `_run(once=args.once)` |
| _run | get_settings | 33 | `get_settings(data not statically known)` |
| get_settings | Settings | 528 | `Settings(data not statically known)` |
| _run | print | 35 | `print('DATABASE_PROCESS_ROLE=delivery_worker is required', file=sys.stderr)` |
| _run | print | 41 | `print('Outbound delivery worker is disabled', file=sys.stderr)` |
| _run | print | 44 | `print(..., file=sys.stderr)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `_run` | 35 |
| output | `print` | `_run` | 41 |
| output | `print` | `_run` | 44 |
| output | `print` | `_run` | 56 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `main` | `build_parser().parse_args` | 81 |
| external_call | `build_parser` | `argparse.ArgumentParser` | 21 |
| unresolved_call | `build_parser` | `parser.add_argument` | 24 |
| external_call | `main` | `asyncio.run` | 82 |
| step_limit | `main` | `first 12 steps` | 0 |
| truncated_flow | `main` | `depth limit` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
