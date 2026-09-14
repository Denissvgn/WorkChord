# check_model_aware_routing_closeout

**Entry point:** `main` (`process`)
**Source:** [check_model_aware_routing_closeout](../modules/check_model_aware_routing_closeout.md)
**Modules touched:** [agent_contract](../modules/agent_contract.md), [check_model_aware_routing_closeout](../modules/check_model_aware_routing_closeout.md)

**Related modules:** [agent_contract](../modules/agent_contract.md), [agent_team_setup](../modules/agent_team_setup.md), [app_main](../modules/app_main.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as parse_args
    participant p2 as argparse.ArgumentParser
    participant p3 as parser.add_argument
    participant p4 as parser.parse_args
    participant p5 as validate_closeout
    participant p6 as _load_json
    participant p7 as json.loads
    participant p8 as path.read_text (scripts/ci/check_model_aw…ng_closeout.py:_load_json)
    participant p9 as CloseoutContractError
    participant p10 as isinstance (scripts/ci/check_model_aw…ng_closeout.py:_load_json)
    participant p11 as inventory.get (scripts/ci/check_model_aw…eout.py:validate_closeout)
    participant p12 as _exact_ids
    participant p13 as isinstance (scripts/ci/check_model_aw…ng_closeout.py:_exact_ids)
    participant p14 as entry.get
    participant p15 as len (scripts/ci/check_model_aw…ng_closeout.py:_exact_ids)
    p0->>p1: parse_args
    p1-->>p2: argparse.ArgumentParser
    p1-->>p3: parser.add_argument
    p1-->>p3: parser.add_argument
    p1-->>p3: parser.add_argument
    p1-->>p4: parser.parse_args
    p0->>p5: validate_closeout
    p5->>p6: _load_json
    p6-->>p7: json.loads
    p6-->>p8: path.read_text (scripts/ci/check_model_aw…ng_closeout.py:_load_json)
    p6->>p9: CloseoutContractError
    p6-->>p10: isinstance (scripts/ci/check_model_aw…ng_closeout.py:_load_json)
    p6->>p9: CloseoutContractError
    p5-->>p11: inventory.get (scripts/ci/check_model_aw…eout.py:validate_closeout)
    p5->>p9: CloseoutContractError
    p5-->>p11: inventory.get (scripts/ci/check_model_aw…eout.py:validate_closeout)
    p5->>p9: CloseoutContractError
    p5->>p12: _exact_ids
    p12-->>p13: isinstance (scripts/ci/check_model_aw…ng_closeout.py:_exact_ids)
    p12->>p9: CloseoutContractError
    p12-->>p13: isinstance (scripts/ci/check_model_aw…ng_closeout.py:_exact_ids)
    p12->>p9: CloseoutContractError
    p12-->>p14: entry.get
    p12-->>p13: isinstance (scripts/ci/check_model_aw…ng_closeout.py:_exact_ids)
    p12->>p9: CloseoutContractError
    p12-->>p14: entry.get
    p12->>p9: CloseoutContractError
    p12-->>p14: entry.get
    p12-->>p13: isinstance (scripts/ci/check_model_aw…ng_closeout.py:_exact_ids)
    p12-->>p15: len (scripts/ci/check_model_aw…ng_closeout.py:_exact_ids)
```

> Call sequence diagram shows 30 of 136 interactions; 106 omitted to keep the visualization within the 30-interaction and generated-diagram limits.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. main"]
    s2["2. parse_args"]
    s3["3. argparse.ArgumentParser"]
    s4["4. parser.add_argument"]
    s5["5. parser.add_argument"]
    s6["6. parser.add_argument"]
    s7["7. parser.parse_args"]
    s8["8. validate_closeout"]
    s9["9. _load_json"]
    s10["10. json.loads"]
    s11["11. path.read_text (scripts/ci/check_model_aw…ng_closeout.py:_load_json)"]
    s12["12. CloseoutContractError"]
    s1 -->|"parse_args(data not statically known)"| s2
    s2 -. "argparse.ArgumentParser(description='Validate the model-aware routing closure inventory.')" .-> s3
    s2 -. "parser.add_argument('--inventory', type=Path, default=DEFAULT_INVENTORY)" .-> s4
    s2 -. "parser.add_argument('--output', type=Path, help='Write a bounded local closure receipt.')" .-> s5
    s2 -. "parser.add_argument('--require-tracked', action='store_true', help='Require every evidence path to be present in the Git index.')" .-> s6
    s2 -. "parser.parse_args(data not statically known)" .-> s7
    s1 -->|"validate_closeout(args.inventory.resolve(...), require_tracked=args.require_tracked)"| s8
    s8 -->|"_load_json(inventory_path)"| s9
    s9 -. "json.loads(path.read_text(...))" .-> s10
    s9 -. "path.read_text (scripts/ci/check_model_aw…ng_closeout.py:_load_json)(encoding='utf-8')" .-> s11
    s9 -->|"CloseoutContractError(...)"| s12
    b0["output print"]
    s1 -. "output print" .-> b0
    b1["output print"]
    s1 -. "output print" .-> b1
    b2["filesystem_write args.output.write_bytes"]
    s1 -. "filesystem_write args.output.write_bytes" .-> b2
    b3["output print"]
    s1 -. "output print" .-> b3
    b4["mutation evidence_paths.add"]
    s8 -. "mutation evidence_paths.add" .-> b4
    b5["filesystem_read path.read_text"]
    s9 -. "filesystem_read path.read_text" .-> b5
    click s1 "../modules/check_model_aware_routing_closeout.md"
    click s2 "../modules/check_model_aware_routing_closeout.md"
    click s8 "../modules/check_model_aware_routing_closeout.md"
    click s9 "../modules/check_model_aware_routing_closeout.md"
    click s12 "../modules/check_model_aware_routing_closeout.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
    class b3 boundary
    class b4 boundary
    class b5 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `CloseoutContractError`, `sys`, `MAX_RECEIPT_BYTES`, `sys` | - | `1`, `1`, `0` |
| `parse_args` | - | `Path`, `DEFAULT_INVENTORY`, `Path` | - | `parser.parse_args(...)` |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `validate_closeout` | `inventory_path: Path`, `require_tracked: bool` | `EXPECTED_TASK_IDS`, `EXPECTED_GATE_IDS` | - | `{...}` |
| `_load_json` | `path: Path` | `json` | - | `value` |
| `json.loads` | - | - | - | - |
| `path.read_text (scripts/ci/check_model_aw…ng_closeout.py:_load_json)` | - | - | - | - |
| `CloseoutContractError` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | parse_args | 338 | `parse_args(data not statically known)` |
| parse_args | argparse.ArgumentParser | 56 | `argparse.ArgumentParser(description='Validate the model-aware routing closure inventory.')` |
| parse_args | parser.add_argument | 59 | `parser.add_argument('--inventory', type=Path, default=DEFAULT_INVENTORY)` |
| parse_args | parser.add_argument | 64 | `parser.add_argument('--output', type=Path, help='Write a bounded local closure receipt.')` |
| parse_args | parser.add_argument | 69 | `parser.add_argument('--require-tracked', action='store_true', help='Require every evidence path to be present in the Git index.')` |
| parse_args | parser.parse_args | 74 | `parser.parse_args(data not statically known)` |
| main | validate_closeout | 340 | `validate_closeout(args.inventory.resolve(...), require_tracked=args.require_tracked)` |
| validate_closeout | _load_json | 283 | `_load_json(inventory_path)` |
| _load_json | json.loads | 79 | `json.loads(path.read_text(...))` |
| _load_json | path.read_text (scripts/ci/check_model_aw…ng_closeout.py:_load_json) | 79 | `path.read_text(encoding='utf-8')` |
| _load_json | CloseoutContractError | 81 | `CloseoutContractError(...)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| output | `print` | `main` | 345 |
| output | `print` | `main` | 351 |
| filesystem_write | `args.output.write_bytes` | `main` | 355 |
| output | `print` | `main` | 356 |
| mutation | `evidence_paths.add` | `validate_closeout` | 309 |
| filesystem_read | `path.read_text` | `_load_json` | 79 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `parse_args` | `argparse.ArgumentParser` | 56 |
| unresolved_call | `parse_args` | `parser.add_argument` | 59 |
| unresolved_call | `parse_args` | `parser.add_argument` | 64 |
| unresolved_call | `parse_args` | `parser.add_argument` | 69 |
| unresolved_call | `parse_args` | `parser.parse_args` | 74 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

This flow starts at `main` and is classified as `process`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
