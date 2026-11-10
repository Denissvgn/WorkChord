# upgrade

**Entry point:** `main` (`process`)
**Source:** [upgrade](../modules/upgrade.md)
**Modules touched:** [authority](../modules/authority.md), [calendar_service](../modules/calendar_service.md), [commands](../modules/commands.md), [config](../modules/config.md), and 19 more

**Complete modules touched:**

- [authority](../modules/authority.md)
- [calendar_service](../modules/calendar_service.md)
- [commands](../modules/commands.md)
- [config](../modules/config.md)
- [database_config](../modules/database_config.md)
- [github_status_automation_service](../modules/github_status_automation_service.md)
- [identity_service](../modules/identity_service.md)
- [label_service](../modules/label_service.md)
- [maintenance](../modules/maintenance.md)
- [models_calendar](../modules/models_calendar.md)
- [models_github](../modules/models_github.md)
- [models_identity](../modules/models_identity.md)
- [models_label](../modules/models_label.md)
- [models_saved_view](../modules/models_saved_view.md)
- [models_system_settings](../modules/models_system_settings.md)
- [models_template](../modules/models_template.md)
- [project_identity](../modules/project_identity.md)
- [saved_view_service](../modules/saved_view_service.md)
- [system_settings_service](../modules/system_settings_service.md)
- [template_service](../modules/template_service.md)
- [upgrade](../modules/upgrade.md)
- [upgrade_service](../modules/upgrade_service.md)
- [url_policy](../modules/url_policy.md)

**Related modules:** [config](../modules/config.md), [upgrade_service](../modules/upgrade_service.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as _print_status
    participant p2 as get_settings
    participant p3 as run_database_repairs
    participant p4 as bootstrap_database_schema
    participant p5 as build_parser
    participant p6 as UpgradeError
    participant p7 as run_alembic_upgrade
    participant p8 as inspect_database
    participant p9 as migration_connection
    participant p10 as _validate_managed_revision
    participant p11 as run_post_migration_repairs
    participant p12 as _inspect_database_connection
    participant p13 as require_background_writes_enabled
    participant p14 as _sync_engine
    participant p15 as initialize_control_plane
    participant p16 as commit_or_flush
    participant p17 as CalendarService.get_or_create_default
    participant p18 as inspect_project_identity
    participant p19 as TemplateService.seed_default_templates
    participant p20 as LabelService.seed_default_labels
    participant p21 as SavedViewService.seed_default_views
    participant p22 as GitHubStatusAutomationService.seed_default_rules
    participant p23 as _backup_precondition
    participant p24 as _run_schema_upgrade
    participant p25 as RuntimeSettingsService.migrate_legacy_email_settings
    participant p26 as require_identity_writes
    participant p27 as backup_sqlite_database
    participant p28 as head_revision
    participant p29 as print (backend/app/cli/upgrade.py:main)
    participant p30 as build_parser().parse_args
    p0->>p1: _print_status
    p0->>p2: get_settings
    p0->>p3: run_database_repairs
    p0->>p4: bootstrap_database_schema
    p0->>p5: build_parser
    p0->>p6: UpgradeError
    p0->>p7: run_alembic_upgrade
    p1->>p8: inspect_database
    p3->>p9: migration_connection
    p3->>p10: _validate_managed_revision
    p3->>p11: run_post_migration_repairs
    p8->>p12: _inspect_database_connection
    p11->>p13: require_background_writes_enabled
    p8->>p14: _sync_engine
    p11->>p15: initialize_control_plane
    p11->>p16: commit_or_flush
    p11->>p17: CalendarService.get_or_create_default
    p7->>p18: inspect_project_identity
    p11->>p19: TemplateService.seed_default_templates
    p11->>p20: LabelService.seed_default_labels
    p11->>p21: SavedViewService.seed_default_views
    p11->>p22: GitHubStatusAutomationService.seed_default_rules
    p7->>p23: _backup_precondition
    p7->>p24: _run_schema_upgrade
    p11->>p25: RuntimeSettingsService.migrate_legacy_email_settings
    p15->>p26: require_identity_writes
    p23->>p27: backup_sqlite_database
    p12->>p28: head_revision
    p0-->>p29: print (backend/app/cli/upgrade.py:main)(...)
    p0-->>p30: build_parser().parse_args(argv)
```

> Call sequence diagram shows 30 of 486 interactions; 456 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 134 (133 omitted); unresolved 1 of 192 (191 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/cli/upgrade.py:build_parser` | 3 | - | external | 1 |
| `backend/app/cli/upgrade.py:build_parser` | 3 | - | unresolved | 8 |
| `backend/app/services/upgrade_service.py:_inspect_database_connection` | 15 | - | external | 4 |
| `backend/app/services/upgrade_service.py:_inspect_database_connection` | 15 | - | unresolved | 1 |
| `backend/app/services/upgrade_service.py:_inspect_database_connection` | 15 | [backend/app/services/upgrade_service.py](../modules/upgrade_service.md) | internal | 2 |
| `backend/app/services/upgrade_service.py:_current_revision` | 19 | - | external | 4 |
| `backend/app/services/upgrade_service.py:_current_revision` | 19 | - | unresolved | 4 |
| `backend/app/services/upgrade_service.py:head_revision` | 29 | - | external | 2 |
> Omission summary shows 8 of 132 groups; 124 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

> Trace truncated at the depth limit; deeper calls are omitted.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 161; effect analysis evaluated: 95, partial: 1, unavailable: 65. Counts include steps omitted from the displayed trace.

Collector observations for 96 source steps with known totals: observed: 373, emitted: 368, omitted: 5. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `15` | `15` | `0` |
| `build_parser().parse_args` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `build_parser` | `available` | `evaluated` | `available` | `2` | `2` | `0` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_mutually_exclusive_group` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `mode.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `mode.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `mode.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. build_parser().parse_args"]
    s3["3. build_parser"]
    s4["4. argparse.ArgumentParser"]
    s5["5. parser.add_mutually_exclusive_group"]
    s6["6. mode.add_argument"]
    s7["7. mode.add_argument"]
    s8["8. mode.add_argument"]
    s9["9. parser.add_argument"]
    s10["10. parser.add_argument"]
    s11["11. parser.add_argument"]
    s12["12. parser.add_argument"]
    s1 -. "build_parser().parse_args(argv)" .-> s2
    s1 -->|"build_parser(data not statically known)"| s3
    s3 -. "argparse.ArgumentParser(description='Upgrade WorkChord database schema safely.')" .-> s4
    s3 -. "parser.add_mutually_exclusive_group(data not statically known)" .-> s5
    s3 -. "mode.add_argument('--check', action='store_true', help='Inspect schema state and exit without changing the database.')" .-> s6
    s3 -. "mode.add_argument('--schema-only', action='store_true', help='Bootstrap an empty target to head without application rows or seed repairs.')" .-> s7
    s3 -. "mode.add_argument('--repairs-only', action='store_true', help='Run serialized post-copy seed and compatibility repairs on a current schema.')" .-> s8
    s3 -. "parser.add_argument(…)" .-> s9
    s3 -. "parser.add_argument('--backup-dir', type=Path, default=None, help='Directory for SQLite backups. Defaults to ./backups next to the DB file.')" .-> s10
    s3 -. "parser.add_argument(…)" .-> s11
    s3 -. "parser.add_argument('--no-repairs', action='store_true', help='Run migrations only; skip idempotent seed/compatibility repairs.')" .-> s12
    b0["output print"]
    s1 -. "output print" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["output print"]
    s1 -. "output print" .-> b2
    b3["output print"]
    s1 -. "output print" .-> b3
    b4["output print"]
    s1 -. "output print" .-> b4
    b5["output print"]
    s1 -. "output print" .-> b5
    b6["output print"]
    s1 -. "output print" .-> b6
    b7["output print"]
    s1 -. "output print" .-> b7
    click s1 "../modules/upgrade.md"
    click s3 "../modules/upgrade.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
    class b4 boundary
    class b5 boundary
    class b6 boundary
    class b7 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | `argv: list[str] \| None` | `UpgradeError`, `sys` | - | `0`, `0`, `0`, `2` |
| `build_parser().parse_args` | - | - | - | - |
| `build_parser` | - | `Path` | - | `parser` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_mutually_exclusive_group` | - | - | - | - |
| `mode.add_argument` | - | - | - | - |
| `mode.add_argument` | - | - | - | - |
| `mode.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | build_parser().parse_args | 80 | `build_parser().parse_args(argv)` |
| main | build_parser | 80 | `build_parser(data not statically known)` |
| build_parser | argparse.ArgumentParser | 29 | `argparse.ArgumentParser(description='Upgrade WorkChord database schema safely.')` |
| build_parser | parser.add_mutually_exclusive_group | 32 | `parser.add_mutually_exclusive_group(data not statically known)` |
| build_parser | mode.add_argument | 33 | `mode.add_argument('--check', action='store_true', help='Inspect schema state and exit without changing the database.')` |
| build_parser | mode.add_argument | 38 | `mode.add_argument('--schema-only', action='store_true', help='Bootstrap an empty target to head without application rows or seed repairs.')` |
| build_parser | mode.add_argument | 43 | `mode.add_argument('--repairs-only', action='store_true', help='Run serialized post-copy seed and compatibility repairs on a current schema.')` |
| build_parser | parser.add_argument | 48 | `parser.add_argument('--skip-backup', action='store_true', help='Do not create an automatic SQLite backup. This never bypasses the PostgreSQL external backup/PITR gate.')` |
| build_parser | parser.add_argument | 56 | `parser.add_argument('--backup-dir', type=Path, default=None, help='Directory for SQLite backups. Defaults to ./backups next to the DB file.')` |
| build_parser | parser.add_argument | 62 | `parser.add_argument('--external-backup-reference', default=None, help='Operator-provided backup/PITR recovery-point reference required before upgrading a non-empty PostgreSQL database.')` |
| build_parser | parser.add_argument | 70 | `parser.add_argument('--no-repairs', action='store_true', help='Run migrations only; skip idempotent seed/compatibility repairs.')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 94 |
| output | `print` | `main` | 98 |
| output | `print` | `main` | 125 |
| output | `print` | `main` | 130 |
| output | `print` | `main` | 132 |
| output | `print` | `main` | 134 |
| output | `print` | `main` | 135 |
| output | `print` | `main` | 143 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `main` | `build_parser().parse_args` | 80 |
| external_call | `build_parser` | `argparse.ArgumentParser` | 29 |
| unresolved_call | `build_parser` | `parser.add_mutually_exclusive_group` | 32 |
| unresolved_call | `build_parser` | `mode.add_argument` | 33 |
| unresolved_call | `build_parser` | `mode.add_argument` | 38 |
| unresolved_call | `build_parser` | `mode.add_argument` | 43 |
| unresolved_call | `build_parser` | `parser.add_argument` | 48 |
| unresolved_call | `build_parser` | `parser.add_argument` | 56 |
| unresolved_call | `build_parser` | `parser.add_argument` | 62 |
| unresolved_call | `build_parser` | `parser.add_argument` | 70 |
| step_limit | `main` | `first 12 steps` | 0 |
| truncated_flow | `main` | `depth limit` | 0 |

## Behavior

The CLI inspects the configured target without changing it when `--check` is selected. A migration-role invocation applies the initial schema only to an empty destination, or advances a known managed revision. Unknown and unversioned databases fail before DDL; they are never inferred current from table names or stamped automatically.

Schema-only initialization leaves application tables empty. Explicit repair runs under the repair process role. PostgreSQL runners share an advisory lock and nonempty upgrades require an external recovery-point reference. The command reports the resulting revision and refuses an incomplete upgrade.
