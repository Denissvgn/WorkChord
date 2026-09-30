# generate_agent_team_report_contract

**Entry point:** `main` (`process`)
**Source:** [generate_agent_team_report_contract](../modules/generate_agent_team_report_contract.md)
**Modules touched:** [generate_agent_team_report_contract](../modules/generate_agent_team_report_contract.md)

**Related modules:** [agent_team_setup](../modules/agent_team_setup.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as parse_args
    participant p2 as argparse.ArgumentParser
    participant p3 as parser.add_argument
    participant p4 as DEFAULT_OUTPUT.relative_to
    participant p5 as parser.parse_args
    participant p6 as args.output.resolve
    participant p7 as rendered_schema
    participant p8 as sys.path.insert
    participant p9 as str
    participant p10 as AgentTeamSetupReport.model_json_schema
    participant p11 as (…).encode
    participant p12 as json.dumps
    participant p13 as output.read_bytes
    participant p14 as output.parent.mkdir
    participant p15 as output.write_bytes
    p0->>p1: parse_args
    p1-->>p2: argparse.ArgumentParser
    p1-->>p3: parser.add_argument
    p1-->>p4: DEFAULT_OUTPUT.relative_to
    p1-->>p3: parser.add_argument
    p1-->>p5: parser.parse_args
    p0-->>p6: args.output.resolve
    p0->>p7: rendered_schema
    p7-->>p8: sys.path.insert
    p7-->>p9: str
    p7-->>p10: AgentTeamSetupReport.model_json_schema
    p7-->>p11: (…).encode
    p7-->>p12: json.dumps
    p0-->>p13: output.read_bytes
    p0-->>p14: output.parent.mkdir
    p0-->>p15: output.write_bytes
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. main"]
    s2["2. parse_args"]
    s3["3. argparse.ArgumentParser"]
    s4["4. parser.add_argument"]
    s5["5. DEFAULT_OUTPUT.relative_to"]
    s6["6. parser.add_argument"]
    s7["7. parser.parse_args"]
    s8["8. args.output.resolve"]
    s9["9. rendered_schema"]
    s10["10. sys.path.insert"]
    s11["11. str"]
    s12["12. AgentTeamSetupReport.model_json_schema"]
    s1 -->|"parse_args(data not statically known)"| s2
    s2 -. "argparse.ArgumentParser(description='Generate the agent-team-setup-report-v1 JSON Schema.')" .-> s3
    s2 -. "parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT, help=...)" .-> s4
    s2 -. "DEFAULT_OUTPUT.relative_to(REPOSITORY_ROOT)" .-> s5
    s2 -. "parser.add_argument('--check', action='store_true', help='Exit nonzero when the existing output differs.')" .-> s6
    s2 -. "parser.parse_args(data not statically known)" .-> s7
    s1 -. "args.output.resolve(data not statically known)" .-> s8
    s1 -->|"rendered_schema(data not statically known)"| s9
    s9 -. "sys.path.insert(0, str(...))" .-> s10
    s9 -. "str(BACKEND_ROOT)" .-> s11
    s9 -. "AgentTeamSetupReport.model_json_schema(ref_template='#35;/$defs/{model}', mode='validation')" .-> s12
    b0["filesystem_read output.read_bytes"]
    s1 -. "filesystem_read output.read_bytes" .-> b0
    b1["filesystem_write output.write_bytes"]
    s1 -. "filesystem_write output.write_bytes" .-> b1
    b2["mutation sys.path.insert"]
    s9 -. "mutation sys.path.insert" .-> b2
    click s1 "../modules/generate_agent_team_report_contract.md"
    click s2 "../modules/generate_agent_team_report_contract.md"
    click s9 "../modules/generate_agent_team_report_contract.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | - | - | `1`, `...`, `0` |
| `parse_args` | - | `Path`, `DEFAULT_OUTPUT`, `REPOSITORY_ROOT` | - | `parser.parse_args(...)` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `DEFAULT_OUTPUT.relative_to` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `args.output.resolve` | - | - | - | - |
| `rendered_schema` | - | `BACKEND_ROOT` | `schema[...]`, `schema[...]` | `...` |
| `sys.path.insert` | - | - | - | - |
| `str` | - | - | - | - |
| `AgentTeamSetupReport.model_json_schema` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | parse_args | 63 | `parse_args(data not statically known)` |
| parse_args | argparse.ArgumentParser | 23 | `argparse.ArgumentParser(description='Generate the agent-team-setup-report-v1 JSON Schema.')` |
| parse_args | parser.add_argument | 26 | `parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT, help=...)` |
| parse_args | DEFAULT_OUTPUT.relative_to | 32 | `DEFAULT_OUTPUT.relative_to(REPOSITORY_ROOT)` |
| parse_args | parser.add_argument | 35 | `parser.add_argument('--check', action='store_true', help='Exit nonzero when the existing output differs.')` |
| parse_args | parser.parse_args | 40 | `parser.parse_args(data not statically known)` |
| main | args.output.resolve | 64 | `args.output.resolve(data not statically known)` |
| main | rendered_schema | 65 | `rendered_schema(data not statically known)` |
| rendered_schema | sys.path.insert | 44 | `sys.path.insert(0, str(...))` |
| rendered_schema | str | 44 | `str(BACKEND_ROOT)` |
| rendered_schema | AgentTeamSetupReport.model_json_schema | 47 | `AgentTeamSetupReport.model_json_schema(ref_template='#/$defs/{model}', mode='validation')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| filesystem_read | `output.read_bytes` | `main` | 68 |
| filesystem_write | `output.write_bytes` | `main` | 73 |
| mutation | `sys.path.insert` | `rendered_schema` | 44 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `parse_args` | `argparse.ArgumentParser` | 23 |
| unresolved_call | `parse_args` | `parser.add_argument` | 26 |
| unresolved_call | `parse_args` | `DEFAULT_OUTPUT.relative_to` | 32 |
| unresolved_call | `parse_args` | `parser.add_argument` | 35 |
| unresolved_call | `parse_args` | `parser.parse_args` | 40 |
| unresolved_call | `main` | `args.output.resolve` | 64 |
| unresolved_call | `rendered_schema` | `AgentTeamSetupReport.model_json_schema` | 47 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
