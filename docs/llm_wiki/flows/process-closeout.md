# closeout

**Entry point:** `main` (`process`)
**Source:** [cli_closeout](../modules/cli_closeout.md)
**Modules touched:** [cli_closeout](../modules/cli_closeout.md), [database_migration_closeout](../modules/database_migration_closeout.md), [database_migration_cutover](../modules/database_migration_cutover.md), and 2 more

**Complete modules touched:**

- [cli_closeout](../modules/cli_closeout.md)
- [database_migration_closeout](../modules/database_migration_closeout.md)
- [database_migration_cutover](../modules/database_migration_cutover.md)
- [database_migration_manifest](../modules/database_migration_manifest.md)
- [execution_mode](../modules/execution_mode.md)

**Related modules:** [database_migration_closeout](../modules/database_migration_closeout.md), [database_migration_cutover](../modules/database_migration_cutover.md), [database_migration_manifest](../modules/database_migration_manifest.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as build_parser
    participant p2 as publish_postcutover_release
    participant p3 as render_release_notes
    participant p4 as finalize_closeout
    participant p5 as verify_closeout_report
    participant p6 as read_document
    participant p7 as _dependency_summary
    participant p8 as _release_identity
    participant p9 as _evaluate_closeout_input
    participant p10 as _validate_qualification
    participant p11 as _write_public_text
    participant p12 as _validate_closure_decision
    participant p13 as _validate_production_report
    participant p14 as _read_json_object
    participant p15 as _safe_identifier
    participant p16 as _installed_application_version
    participant p17 as _artifact_references
    participant p18 as _publication_exceptions
    participant p19 as _repository_document_set
    participant p20 as _release_notes_markdown
    participant p21 as _validate_publication
    participant p22 as _sign_document
    participant p23 as verify_signed_document
    participant p24 as _require_new_output
    participant p25 as _validate_dependency_summary
    participant p26 as _private_key
    participant p27 as _text
    participant p28 as verify_document
    participant p29 as print
    participant p30 as build_parser().parse_args
    p0->>p1: build_parser
    p0->>p2: publish_postcutover_release
    p0->>p3: render_release_notes
    p0->>p4: finalize_closeout
    p0->>p5: verify_closeout_report
    p2->>p6: read_document
    p4->>p7: _dependency_summary
    p2->>p8: _release_identity
    p4->>p9: _evaluate_closeout_input
    p2->>p10: _validate_qualification
    p3->>p11: _write_public_text
    p5->>p12: _validate_closure_decision
    p2->>p13: _validate_production_report
    p2->>p14: _read_json_object
    p2->>p15: _safe_identifier
    p2->>p16: _installed_application_version
    p2->>p17: _artifact_references
    p2->>p18: _publication_exceptions
    p2->>p19: _repository_document_set
    p2->>p20: _release_notes_markdown
    p2->>p21: _validate_publication
    p2->>p22: _sign_document
    p10->>p23: verify_signed_document
    p22->>p24: _require_new_output
    p9->>p25: _validate_dependency_summary
    p22->>p26: _private_key
    p8->>p27: _text
    p6->>p28: verify_document
    p0-->>p29: print(...)
    p0-->>p30: build_parser().parse_args(argv)
```

> Call sequence diagram shows 30 of 1386 interactions; 1356 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 1 of 266 (265 omitted); unresolved 1 of 532 (531 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `backend/app/cli/closeout.py:build_parser` | 3 | - | external | 1 |
| `backend/app/cli/closeout.py:build_parser` | 3 | - | unresolved | 18 |
| `backend/app/cli/closeout.py:build_parser` | 3 | [backend/app/cli/closeout.py](../modules/cli_closeout.md) | internal | 3 |
| `backend/app/cli/closeout.py:_signing_arguments` | 14 | - | unresolved | 3 |
| `backend/app/cli/closeout.py:_optional_closeout_dependencies` | 24 | - | unresolved | 8 |
| `backend/app/database_migration/manifest.py:read_document` | 38 | - | external | 2 |
| `backend/app/database_migration/manifest.py:read_document` | 38 | - | unresolved | 1 |
| `backend/app/database_migration/manifest.py:read_document` | 38 | [backend/app/database_migration/manifest.py](../modules/database_migration_manifest.md) | internal | 2 |
> Omission summary shows 8 of 186 groups; 178 further groups are not expanded here. Counts above include all omitted interactions.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 589; effect analysis evaluated: 294, partial: 13, unavailable: 282. Counts include steps omitted from the displayed trace.

Collector observations for 307 source steps with known totals: observed: 1454, emitted: 1392, omitted: 62. Unavailable totals are excluded.

- Callable record unavailable for one or more source steps; those steps have no represented callable body.
- Effect collector omitted observations before flow assembly; displayed effects are partial.
- Effect collector totals unavailable; observed counts cover captured records only.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `13` | `13` | `0` |
| `build_parser().parse_args` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `build_parser` | `available` | `partial` | `available` | `14` | `9` | `5` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_subparsers` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `commands.add_parser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `publication.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `publication.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `publication.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `publication.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `publication.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `publication.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. build_parser().parse_args"]
    s3["3. build_parser"]
    s4["4. argparse.ArgumentParser"]
    s5["5. parser.add_subparsers"]
    s6["6. commands.add_parser"]
    s7["7. publication.add_argument"]
    s8["8. publication.add_argument"]
    s9["9. publication.add_argument"]
    s10["10. publication.add_argument"]
    s11["11. publication.add_argument"]
    s12["12. publication.add_argument"]
    s1 -. "build_parser().parse_args(argv)" .-> s2
    s1 -->|"build_parser(data not statically known)"| s3
    s3 -. "argparse.ArgumentParser(…)" .-> s4
    s3 -. "parser.add_subparsers(dest='command', required=True)" .-> s5
    s3 -. "commands.add_parser('publish-release', help='Sign post-cutover release facts after verifying the production chain.')" .-> s6
    s3 -. "publication.add_argument('--input', type=Path, required=True)" .-> s7
    s3 -. "publication.add_argument('--repository-root', type=Path, required=True)" .-> s8
    s3 -. "publication.add_argument('--release-manifest', type=Path, required=True)" .-> s9
    s3 -. "publication.add_argument('--qualification-report', type=Path, required=True)" .-> s10
    s3 -. "publication.add_argument('--qualification-public-key', type=Path, required=True)" .-> s11
    s3 -. "publication.add_argument('--production-cutover', type=Path, required=True)" .-> s12
    b0["output print"]
    s1 -. "output print" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["output print"]
    s1 -. "output print" .-> b2
    b3["output print"]
    s1 -. "output print" .-> b3
    click s1 "../modules/cli_closeout.md"
    click s3 "../modules/cli_closeout.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | `argv: list[str] \| None` | `CutoverEvidenceError`, `ManifestError`, `sys` | - | `0`, `0`, `2`, `0`, `2` |
| `build_parser().parse_args` | - | - | - | - |
| `build_parser` | - | `Path`, `Path`, `Path`, `Path`, `Path`, `Path`, `Path`, `Path` | - | `parser` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_subparsers` | - | - | - | - |
| `commands.add_parser` | - | - | - | - |
| `publication.add_argument` | - | - | - | - |
| `publication.add_argument` | - | - | - | - |
| `publication.add_argument` | - | - | - | - |
| `publication.add_argument` | - | - | - | - |
| `publication.add_argument` | - | - | - | - |
| `publication.add_argument` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | build_parser().parse_args | 88 | `build_parser().parse_args(argv)` |
| main | build_parser | 88 | `build_parser(data not statically known)` |
| build_parser | argparse.ArgumentParser | 37 | `argparse.ArgumentParser(description='Fail-closed DBM-DOC-002 and DBM-CLOSE-001 evidence. This command does not mutate a database, deployment, or existing release document.')` |
| build_parser | parser.add_subparsers | 43 | `parser.add_subparsers(dest='command', required=True)` |
| build_parser | commands.add_parser | 45 | `commands.add_parser('publish-release', help='Sign post-cutover release facts after verifying the production chain.')` |
| build_parser | publication.add_argument | 49 | `publication.add_argument('--input', type=Path, required=True)` |
| build_parser | publication.add_argument | 50 | `publication.add_argument('--repository-root', type=Path, required=True)` |
| build_parser | publication.add_argument | 51 | `publication.add_argument('--release-manifest', type=Path, required=True)` |
| build_parser | publication.add_argument | 52 | `publication.add_argument('--qualification-report', type=Path, required=True)` |
| build_parser | publication.add_argument | 53 | `publication.add_argument('--qualification-public-key', type=Path, required=True)` |
| build_parser | publication.add_argument | 54 | `publication.add_argument('--production-cutover', type=Path, required=True)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 109 |
| output | `print` | `main` | 131 |
| output | `print` | `main` | 135 |
| output | `print` | `main` | 147 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `main` | `build_parser().parse_args` | 88 |
| external_call | `build_parser` | `argparse.ArgumentParser` | 37 |
| unresolved_call | `build_parser` | `parser.add_subparsers` | 43 |
| unresolved_call | `build_parser` | `commands.add_parser` | 45 |
| unresolved_call | `build_parser` | `publication.add_argument` | 49 |
| unresolved_call | `build_parser` | `publication.add_argument` | 50 |
| unresolved_call | `build_parser` | `publication.add_argument` | 51 |
| unresolved_call | `build_parser` | `publication.add_argument` | 52 |
| unresolved_call | `build_parser` | `publication.add_argument` | 53 |
| unresolved_call | `build_parser` | `publication.add_argument` | 54 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
