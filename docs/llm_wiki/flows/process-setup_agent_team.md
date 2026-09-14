# setup_agent_team

**Entry point:** `main` (`process`)
**Source:** [setup_agent_team](../modules/setup_agent_team.md)
**Modules touched:** [setup_agent_team](../modules/setup_agent_team.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as parse_args
    participant p2 as argparse.ArgumentParser
    participant p3 as parser.add_argument
    participant p4 as os.getenv
    participant p5 as parser.add_subparsers
    participant p6 as commands.add_parser
    participant p7 as validate.add_argument
    participant p8 as validate.set_defaults
    participant p9 as plan.add_argument
    participant p10 as plan.set_defaults
    participant p11 as apply.add_argument
    participant p12 as secrets.token_hex
    participant p13 as apply.set_defaults
    participant p14 as status.add_argument
    p0->>p1: parse_args
    p1-->>p2: argparse.ArgumentParser
    p1-->>p3: parser.add_argument
    p1-->>p4: os.getenv
    p1-->>p3: parser.add_argument
    p1-->>p4: os.getenv
    p1-->>p3: parser.add_argument
    p1-->>p4: os.getenv
    p1-->>p3: parser.add_argument
    p1-->>p5: parser.add_subparsers
    p1-->>p6: commands.add_parser
    p1-->>p7: validate.add_argument
    p1-->>p8: validate.set_defaults
    p1-->>p6: commands.add_parser
    p1-->>p9: plan.add_argument
    p1-->>p9: plan.add_argument
    p1-->>p10: plan.set_defaults
    p1-->>p6: commands.add_parser
    p1-->>p11: apply.add_argument
    p1-->>p11: apply.add_argument
    p1-->>p11: apply.add_argument
    p1-->>p11: apply.add_argument
    p1-->>p11: apply.add_argument
    p1-->>p12: secrets.token_hex
    p1-->>p11: apply.add_argument
    p1-->>p11: apply.add_argument
    p1-->>p12: secrets.token_hex
    p1-->>p13: apply.set_defaults
    p1-->>p6: commands.add_parser
    p1-->>p14: status.add_argument
```

> Call sequence diagram shows 30 of 38 interactions; 8 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
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
