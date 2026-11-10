# setup_agent_team

**Entry point:** `main` (`process`)
**Source:** [setup_agent_team](../modules/setup_agent_team.md)
**Modules touched:** [setup_agent_team](../modules/setup_agent_team.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as parse_args
    participant p2 as json.dump
    participant p3 as args.handler
    participant p4 as sys.stdout.write
    participant p5 as argparse.ArgumentParser
    participant p6 as parser.add_argument
    participant p7 as os.getenv
    participant p8 as parser.add_subparsers
    participant p9 as commands.add_parser
    participant p10 as validate.add_argument
    participant p11 as validate.set_defaults
    participant p12 as plan.add_argument
    participant p13 as plan.set_defaults
    participant p14 as apply.add_argument
    participant p15 as secrets.token_hex
    p0->>p1: parse_args
    p0-->>p2: json.dump(value, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    p0-->>p3: args.handler(args)
    p0-->>p4: sys.stdout.write('\n')
    p1-->>p5: argparse.ArgumentParser(description='Operate the digest-bound agent-team setup API without handling runtime credentials.')
    p1-->>p6: parser.add_argument('--base-url', default=os.getenv(...))
    p1-->>p7: os.getenv('WORKCHORD_BASE_URL', 'http://localhost:8001')
    p1-->>p6: parser.add_argument('--api-prefix', default=os.getenv(...))
    p1-->>p7: os.getenv('WORKCHORD_API_PREFIX', '/api')
    p1-->>p6: parser.add_argument('--admin-key', default=os.getenv(...), help='Defaults to WORKCHORD_ADMIN_API_KEY and is never printed.')
    p1-->>p7: os.getenv('WORKCHORD_ADMIN_API_KEY', '')
    p1-->>p6: parser.add_argument('--timeout', type=float, default=15.0)
    p1-->>p8: parser.add_subparsers(dest='command', required=True)
    p1-->>p9: commands.add_parser('validate')
    p1-->>p10: validate.add_argument('manifest', type=Path)
    p1-->>p11: validate.set_defaults(handler=run_validate)
    p1-->>p9: commands.add_parser('plan')
    p1-->>p12: plan.add_argument('manifest', type=Path)
    p1-->>p12: plan.add_argument('--expected-revision', type=int, required=True)
    p1-->>p13: plan.set_defaults(handler=run_plan)
    p1-->>p9: commands.add_parser('apply')
    p1-->>p14: apply.add_argument('manifest', type=Path)
    p1-->>p14: apply.add_argument('--plan', type=Path, required=True)
    p1-->>p14: apply.add_argument('--approve', action='append', default=[...])
    p1-->>p14: apply.add_argument('--confirm', action='append', default=[...])
    p1-->>p14: apply.add_argument('--idempotency-key', default=...)
    p1-->>p15: secrets.token_hex(12)
    p1-->>p14: apply.add_argument('--rationale', default='Apply approved agent-team reconciliation actions')
    p1-->>p14: apply.add_argument('--correlation-id', default=...)
    p1-->>p15: secrets.token_hex(8)
```

> Call sequence diagram shows 30 of 38 interactions; 8 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 8 of 8 (0 omitted); unresolved 21 of 29 (8 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `scripts/api_keys/setup_agent_team.py:parse_args` | 2 | - | unresolved | 8 |
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis partially available.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 2; effect analysis evaluated: 1, partial: 1, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 2 source steps with known totals: observed: 16, emitted: 15, omitted: 1. Unavailable totals are excluded.

- Effect collector omitted observations before flow assembly; displayed effects are partial.

| Step | Callable record | Effect analysis | Collector totals | Observed | Emitted | Omitted |
|---|---|---|---|---:|---:|---:|
| `main` | `available` | `evaluated` | `available` | `3` | `3` | `0` |
| `parse_args` | `available` | `partial` | `available` | `13` | `12` | `1` |
| `argparse.ArgumentParser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `os.getenv` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `os.getenv` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `os.getenv` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_argument` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `parser.add_subparsers` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |
| `commands.add_parser` | `not_applicable` | `not_applicable` | `not_applicable` | — | — | — |

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. parse_args"]
    s3["3. argparse.ArgumentParser"]
    s4["4. parser.add_argument"]
    s5["5. os.getenv"]
    s6["6. parser.add_argument"]
    s7["7. os.getenv"]
    s8["8. parser.add_argument"]
    s9["9. os.getenv"]
    s10["10. parser.add_argument"]
    s11["11. parser.add_subparsers"]
    s12["12. commands.add_parser"]
    s1 -->|"parse_args(data not statically known)"| s2
    s2 -. "argparse.ArgumentParser(description='Operate the digest-bound agent-team setup API without handling runtime credentials.')" .-> s3
    s2 -. "parser.add_argument('--base-url', default=os.getenv(...))" .-> s4
    s2 -. "os.getenv('WORKCHORD_BASE_URL', 'http://localhost:8001')" .-> s5
    s2 -. "parser.add_argument('--api-prefix', default=os.getenv(...))" .-> s6
    s2 -. "os.getenv('WORKCHORD_API_PREFIX', '/api')" .-> s7
    s2 -. "parser.add_argument('--admin-key', default=os.getenv(...), help='Defaults to WORKCHORD_ADMIN_API_KEY and is never printed.')" .-> s8
    s2 -. "os.getenv('WORKCHORD_ADMIN_API_KEY', '')" .-> s9
    s2 -. "parser.add_argument('--timeout', type=float, default=15.0)" .-> s10
    s2 -. "parser.add_subparsers(dest='command', required=True)" .-> s11
    s2 -. "commands.add_parser('validate')" .-> s12
    b0["output sys.stdout.write"]
    s1 -. "output sys.stdout.write" .-> b0
    b1["environment_read os.getenv"]
    s2 -. "environment_read os.getenv" .-> b1
    b2["environment_read os.getenv"]
    s2 -. "environment_read os.getenv" .-> b2
    b3["environment_read os.getenv"]
    s2 -. "environment_read os.getenv" .-> b3
    click s1 "../modules/setup_agent_team.md"
    click s2 "../modules/setup_agent_team.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `sys` | - | `0` |
| `parse_args` | - | `Path`, `run_validate`, `Path`, `run_plan`, `Path`, `Path`, `run_apply`, `run_status` | - | `parser.parse_args(...)` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `os.getenv` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `os.getenv` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `os.getenv` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_subparsers` | - | - | - | - |
| `commands.add_parser` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | parse_args | 264 | `parse_args(data not statically known)` |
| parse_args | argparse.ArgumentParser | 200 | `argparse.ArgumentParser(description='Operate the digest-bound agent-team setup API without handling runtime credentials.')` |
| parse_args | parser.add_argument | 206 | `parser.add_argument('--base-url', default=os.getenv(...))` |
| parse_args | os.getenv | 208 | `os.getenv('WORKCHORD_BASE_URL', 'http://localhost:8001')` |
| parse_args | parser.add_argument | 210 | `parser.add_argument('--api-prefix', default=os.getenv(...))` |
| parse_args | os.getenv | 212 | `os.getenv('WORKCHORD_API_PREFIX', '/api')` |
| parse_args | parser.add_argument | 214 | `parser.add_argument('--admin-key', default=os.getenv(...), help='Defaults to WORKCHORD_ADMIN_API_KEY and is never printed.')` |
| parse_args | os.getenv | 216 | `os.getenv('WORKCHORD_ADMIN_API_KEY', '')` |
| parse_args | parser.add_argument | 219 | `parser.add_argument('--timeout', type=float, default=15.0)` |
| parse_args | parser.add_subparsers | 220 | `parser.add_subparsers(dest='command', required=True)` |
| parse_args | commands.add_parser | 222 | `commands.add_parser('validate')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `sys.stdout.write` | `main` | 267 |
| environment_read | `os.getenv` | `parse_args` | 208 |
| environment_read | `os.getenv` | `parse_args` | 212 |
| environment_read | `os.getenv` | `parse_args` | 216 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `parse_args` | `argparse.ArgumentParser` | 200 |
| unresolved_call | `parse_args` | `parser.add_argument` | 206 |
| unresolved_call | `parse_args` | `parser.add_argument` | 210 |
| unresolved_call | `parse_args` | `parser.add_argument` | 214 |
| unresolved_call | `parse_args` | `parser.add_argument` | 219 |
| unresolved_call | `parse_args` | `parser.add_subparsers` | 220 |
| unresolved_call | `parse_args` | `commands.add_parser` | 222 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
