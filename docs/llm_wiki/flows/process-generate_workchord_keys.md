# generate_workchord_keys

**Entry point:** `main` (`process`)
**Source:** [generate_workchord_keys](../modules/generate_workchord_keys.md)
**Modules touched:** [generate_workchord_keys](../modules/generate_workchord_keys.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as parse_args
    participant p2 as selected_keys
    participant p3 as build_payload
    participant p4 as render_shell
    participant p5 as render_env
    participant p6 as print
    participant p7 as raw_key.upper
    participant p8 as json.dumps
    participant p9 as argparse.ArgumentParser
    participant p10 as datetime.now(…).isoformat
    participant p11 as isinstance (scripts/api_keys/generate…chord_keys.py:render_shell)
    participant p12 as isinstance (scripts/api_keys/generate…rkchord_keys.py:render_env)
    participant p13 as parser.add_argument
    participant p14 as ', '.join
    participant p15 as datetime.now
    participant p16 as lines.append (scripts/api_keys/generate…chord_keys.py:render_shell)
    participant p17 as lines.extend
    participant p18 as SystemExit
    participant p19 as <dynamic>
    participant p20 as values.items (scripts/api_keys/generate…chord_keys.py:render_shell)
    participant p21 as values.items (scripts/api_keys/generate…rkchord_keys.py:render_env)
    participant p22 as keys.append
    participant p23 as lines.append (scripts/api_keys/generate…rkchord_keys.py:render_env)
    p0->>p1: parse_args
    p0->>p2: selected_keys
    p0->>p3: build_payload
    p0->>p4: render_shell
    p0->>p5: render_env
    p0-->>p6: print(json.dumps(...))
    p2-->>p7: raw_key.upper
    p0-->>p8: json.dumps(payload, indent=2, sort_keys=True)
    p0-->>p6: print(render_shell(...))
    p0-->>p6: print(render_env(...))
    p1-->>p9: argparse.ArgumentParser(description='Generate local WorkChord API keys and shared secrets.')
    p3-->>p10: datetime.now(…).isoformat(timespec='seconds')
    p4-->>p11: isinstance (scripts/api_keys/generate…chord_keys.py:render_shell)(values, dict)
    p5-->>p12: isinstance (scripts/api_keys/generate…rkchord_keys.py:render_env)(values, dict)
    p1-->>p13: parser.add_argument('--format', choices=[...], default='env', help='Output format. Defaults to dotenv env lines.')
    p2-->>p14: ', '.join(KEY_GENERATORS)
    p3-->>p15: datetime.now(UTC)
    p4-->>p16: lines.append (scripts/api_keys/generate…chord_keys.py:render_shell)(' Source this file only in trusted shells.')
    p5-->>p17: lines.extend([...])
    p1-->>p13: parser.add_argument('--only', action='append', metavar='KEY', help='Generate only this key. Repeat for multiple keys.')
    p2-->>p18: SystemExit(...)
    p3-->>p19: <dynamic>
    p4-->>p20: values.items (scripts/api_keys/generate…chord_keys.py:render_shell)
    p5-->>p21: values.items (scripts/api_keys/generate…rkchord_keys.py:render_env)
    p1-->>p13: parser.add_argument('--include-outbound-webhook', action='store_true', help='Also generate an outbound webhook target signing secret.')
    p2-->>p22: keys.append(key)
    p4-->>p16: lines.append (scripts/api_keys/generate…chord_keys.py:render_shell)(...)
    p5-->>p23: lines.append (scripts/api_keys/generate…rkchord_keys.py:render_env)(...)
    p1-->>p13: parser.add_argument('--no-comments', action='store_true', help='Suppress explanatory comments in env and shell output.')
    p2-->>p22: keys.append('OUTBOUND_WEBHOOK_SIGNING_SECRET')
```

> Call sequence diagram shows 30 of 38 interactions; 8 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 9 of 11 (2 omitted); unresolved 16 of 22 (6 omitted). These counts cover the captured static trace.

Omitted captured detail, grouped by actual caller occurrence and target module:

| Caller | Parent step | Target module | Kind | Omitted interactions |
| --- | --- | --- | --- | --- |
| `scripts/api_keys/generate_workchord_keys.py:parse_args` | 2 | - | unresolved | 1 |
| `scripts/api_keys/generate_workchord_keys.py:render_shell` | 22 | - | external | 2 |
| `scripts/api_keys/generate_workchord_keys.py:render_shell` | 22 | - | unresolved | 1 |
| `scripts/api_keys/generate_workchord_keys.py:render_env` | 31 | - | unresolved | 4 |
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 6; effect analysis evaluated: 6, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 6 source steps with known totals: observed: 30, emitted: 30, omitted: 0. Unavailable totals are excluded.

```mermaid
flowchart LR
    s1["1. main"]
    s2["2. parse_args"]
    s3["3. argparse.ArgumentParser"]
    s4["4. parser.add_argument"]
    s5["5. parser.add_argument"]
    s6["6. parser.add_argument"]
    s7["7. parser.add_argument"]
    s8["8. parser.parse_args"]
    s9["9. selected_keys"]
    s10["10. raw_key.upper"]
    s11["11. ', '.join"]
    s12["12. SystemExit"]
    s1 -->|"parse_args(data not statically known)"| s2
    s2 -. "argparse.ArgumentParser(description='Generate local WorkChord API keys and shared secrets.')" .-> s3
    s2 -. "parser.add_argument('--format', choices=[...], default='env', help='Output format. Defaults to dotenv env lines.')" .-> s4
    s2 -. "parser.add_argument('--only', action='append', metavar='KEY', help='Generate only this key. Repeat for multiple keys.')" .-> s5
    s2 -. "parser.add_argument('--include-outbound-webhook', action='store_true', help='Also generate an outbound webhook target signing secret.')" .-> s6
    s2 -. "parser.add_argument('--no-comments', action='store_true', help='Suppress explanatory comments in env and shell output.')" .-> s7
    s2 -. "parser.parse_args(data not statically known)" .-> s8
    s1 -->|"selected_keys(args.only, args.include_outbound_webhook)"| s9
    s9 -. "raw_key.upper(data not statically known)" .-> s10
    s9 -. "', '.join(KEY_GENERATORS)" .-> s11
    s9 -. "SystemExit(...)" .-> s12
    b0["output print"]
    s1 -. "output print" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["output print"]
    s1 -. "output print" .-> b2
    b3["mutation keys.append"]
    s9 -. "mutation keys.append" .-> b3
    b4["mutation keys.append"]
    s9 -. "mutation keys.append" .-> b4
    click s1 "../modules/generate_workchord_keys.md"
    click s2 "../modules/generate_workchord_keys.md"
    click s9 "../modules/generate_workchord_keys.md"
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
| `main` | - | - | - | - |
| `parse_args` | - | - | - | `parser.parse_args(...)` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `selected_keys` | `raw_keys: list[str] \| None`, `include_outbound: bool` | `KEY_GENERATORS`, `KEY_GENERATORS` | - | `keys`, `keys` |
| `raw_key.upper` | - | - | - | - |
| `', '.join` | - | - | - | - |
| `SystemExit` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | parse_args | 169 | `parse_args(data not statically known)` |
| parse_args | argparse.ArgumentParser | 140 | `argparse.ArgumentParser(description='Generate local WorkChord API keys and shared secrets.')` |
| parse_args | parser.add_argument | 143 | `parser.add_argument('--format', choices=[...], default='env', help='Output format. Defaults to dotenv env lines.')` |
| parse_args | parser.add_argument | 149 | `parser.add_argument('--only', action='append', metavar='KEY', help='Generate only this key. Repeat for multiple keys.')` |
| parse_args | parser.add_argument | 155 | `parser.add_argument('--include-outbound-webhook', action='store_true', help='Also generate an outbound webhook target signing secret.')` |
| parse_args | parser.add_argument | 160 | `parser.add_argument('--no-comments', action='store_true', help='Suppress explanatory comments in env and shell output.')` |
| parse_args | parser.parse_args | 165 | `parser.parse_args(data not statically known)` |
| main | selected_keys | 170 | `selected_keys(args.only, args.include_outbound_webhook)` |
| selected_keys | raw_key.upper | 63 | `raw_key.upper(data not statically known)` |
| selected_keys | ', '.join | 65 | `', '.join(KEY_GENERATORS)` |
| selected_keys | SystemExit | 66 | `SystemExit(...)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 175 |
| output | `print` | `main` | 177 |
| output | `print` | `main` | 179 |
| mutation | `keys.append` | `selected_keys` | 68 |
| mutation | `keys.append` | `selected_keys` | 79 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `parse_args` | `argparse.ArgumentParser` | 140 |
| unresolved_call | `parse_args` | `parser.add_argument` | 143 |
| unresolved_call | `parse_args` | `parser.add_argument` | 149 |
| unresolved_call | `parse_args` | `parser.add_argument` | 155 |
| unresolved_call | `parse_args` | `parser.add_argument` | 160 |
| unresolved_call | `parse_args` | `parser.parse_args` | 165 |
| unresolved_call | `selected_keys` | `raw_key.upper` | 63 |
| unresolved_call | `selected_keys` | `', '.join` | 65 |
| external_call | `selected_keys` | `SystemExit` | 66 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
