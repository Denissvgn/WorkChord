# generate_agent_team_contract

**Entry point:** `main` (`process`)
**Source:** [generate_agent_team_contract](../modules/generate_agent_team_contract.md)
**Modules touched:** [generate_agent_team_contract](../modules/generate_agent_team_contract.md)

**Related modules:** [agent_team_setup](../modules/agent_team_setup.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as parse_args
    participant p2 as args.output.resolve
    participant p3 as rendered_schema
    participant p4 as output.read_bytes
    participant p5 as output.parent.mkdir
    participant p6 as output.write_bytes
    participant p7 as argparse.ArgumentParser
    participant p8 as sys.path.insert
    participant p9 as parser.add_argument
    participant p10 as str
    participant p11 as DEFAULT_OUTPUT.relative_to
    participant p12 as AgentTeamMaster.model_json_schema
    participant p13 as (…).encode
    participant p14 as parser.parse_args
    participant p15 as json.dumps
    p0->>p1: parse_args
    p0-->>p2: args.output.resolve
    p0->>p3: rendered_schema
    p0-->>p4: output.read_bytes
    p0-->>p5: output.parent.mkdir(parents=True, exist_ok=True)
    p0-->>p6: output.write_bytes(expected)
    p1-->>p7: argparse.ArgumentParser(description='Generate the agent-team-master-v1 JSON Schema.')
    p3-->>p8: sys.path.insert(0, str(...))
    p1-->>p9: parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT, help=...)
    p3-->>p10: str(BACKEND_ROOT)
    p1-->>p11: DEFAULT_OUTPUT.relative_to(REPOSITORY_ROOT)
    p3-->>p12: AgentTeamMaster.model_json_schema(ref_template=' /$defs/{model}', mode='validation')
    p1-->>p9: parser.add_argument('--check', action='store_true', help='Exit nonzero when the existing output differs.')
    p3-->>p13: (…).encode('utf-8')
    p1-->>p14: parser.parse_args
    p3-->>p15: json.dumps(schema, ensure_ascii=False, indent=2, sort_keys=True)
```

> Call sequence diagram shows 16 of 16 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 4 of 4 (0 omitted); unresolved 10 of 10 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 3; effect analysis evaluated: 3, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 3 source steps with known totals: observed: 14, emitted: 14, omitted: 0. Unavailable totals are excluded.

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
    s12["12. AgentTeamMaster.model_json_schema"]
    s1 -->|"parse_args(data not statically known)"| s2
    s2 -. "argparse.ArgumentParser(description='Generate the agent-team-master-v1 JSON Schema.')" .-> s3
    s2 -. "parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT, help=...)" .-> s4
    s2 -. "DEFAULT_OUTPUT.relative_to(REPOSITORY_ROOT)" .-> s5
    s2 -. "parser.add_argument('--check', action='store_true', help='Exit nonzero when the existing output differs.')" .-> s6
    s2 -. "parser.parse_args(data not statically known)" .-> s7
    s1 -. "args.output.resolve(data not statically known)" .-> s8
    s1 -->|"rendered_schema(data not statically known)"| s9
    s9 -. "sys.path.insert(0, str(...))" .-> s10
    s9 -. "str(BACKEND_ROOT)" .-> s11
    s9 -. "AgentTeamMaster.model_json_schema(ref_template='#35;/$defs/{model}', mode='validation')" .-> s12
    b0["filesystem_read output.read_bytes"]
    s1 -. "filesystem_read output.read_bytes" .-> b0
    b1["filesystem_write output.write_bytes"]
    s1 -. "filesystem_write output.write_bytes" .-> b1
    b2["mutation sys.path.insert"]
    s9 -. "mutation sys.path.insert" .-> b2
    click s1 "../modules/generate_agent_team_contract.md"
    click s2 "../modules/generate_agent_team_contract.md"
    click s9 "../modules/generate_agent_team_contract.md"
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
| `AgentTeamMaster.model_json_schema` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | parse_args | 55 | `parse_args(data not statically known)` |
| parse_args | argparse.ArgumentParser | 18 | `argparse.ArgumentParser(description='Generate the agent-team-master-v1 JSON Schema.')` |
| parse_args | parser.add_argument | 21 | `parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT, help=...)` |
| parse_args | DEFAULT_OUTPUT.relative_to | 27 | `DEFAULT_OUTPUT.relative_to(REPOSITORY_ROOT)` |
| parse_args | parser.add_argument | 30 | `parser.add_argument('--check', action='store_true', help='Exit nonzero when the existing output differs.')` |
| parse_args | parser.parse_args | 35 | `parser.parse_args(data not statically known)` |
| main | args.output.resolve | 56 | `args.output.resolve(data not statically known)` |
| main | rendered_schema | 57 | `rendered_schema(data not statically known)` |
| rendered_schema | sys.path.insert | 39 | `sys.path.insert(0, str(...))` |
| rendered_schema | str | 39 | `str(BACKEND_ROOT)` |
| rendered_schema | AgentTeamMaster.model_json_schema | 42 | `AgentTeamMaster.model_json_schema(ref_template='#/$defs/{model}', mode='validation')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| filesystem_read | `output.read_bytes` | `main` | 60 |
| filesystem_write | `output.write_bytes` | `main` | 65 |
| mutation | `sys.path.insert` | `rendered_schema` | 39 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `parse_args` | `argparse.ArgumentParser` | 18 |
| unresolved_call | `parse_args` | `parser.add_argument` | 21 |
| unresolved_call | `parse_args` | `DEFAULT_OUTPUT.relative_to` | 27 |
| unresolved_call | `parse_args` | `parser.add_argument` | 30 |
| unresolved_call | `parse_args` | `parser.parse_args` | 35 |
| unresolved_call | `main` | `args.output.resolve` | 56 |
| unresolved_call | `rendered_schema` | `AgentTeamMaster.model_json_schema` | 42 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
