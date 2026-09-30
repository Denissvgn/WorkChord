# generate_client_contract

**Entry point:** `main` (`process`)
**Source:** [generate_client_contract](../modules/generate_client_contract.md)
**Modules touched:** [generate_client_contract](../modules/generate_client_contract.md)

**Related modules:** [app_main](../modules/app_main.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as argparse.ArgumentParser
    participant p2 as parser.add_argument
    participant p3 as parser.parse_args
    participant p4 as serialized_contract
    participant p5 as json.dumps
    participant p6 as build_contract
    participant p7 as app.openapi
    participant p8 as set
    participant p9 as schema[…].keys
    participant p10 as ValueError
    participant p11 as sorted
    participant p12 as collect
    participant p13 as components[…].get
    participant p14 as args.output.exists
    participant p15 as args.output.read_text
    participant p16 as parser.exit
    participant p17 as args.output.parent.mkdir
    participant p18 as args.output.write_text
    p0-->>p1: argparse.ArgumentParser
    p0-->>p2: parser.add_argument
    p0-->>p2: parser.add_argument
    p0-->>p3: parser.parse_args
    p0->>p4: serialized_contract
    p4-->>p5: json.dumps
    p4->>p6: build_contract
    p6-->>p7: app.openapi
    p6-->>p8: set
    p6-->>p9: schema[…].keys
    p6-->>p10: ValueError
    p6-->>p11: sorted
    p6-->>p12: collect
    p6-->>p13: components[…].get
    p0-->>p14: args.output.exists
    p0-->>p15: args.output.read_text
    p0-->>p16: parser.exit
    p0-->>p17: args.output.parent.mkdir
    p0-->>p18: args.output.write_text
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. main"]
    s2["2. argparse.ArgumentParser"]
    s3["3. parser.add_argument"]
    s4["4. parser.add_argument"]
    s5["5. parser.parse_args"]
    s6["6. serialized_contract"]
    s7["7. json.dumps"]
    s8["8. build_contract"]
    s9["9. app.openapi"]
    s10["10. set"]
    s11["11. schema[…].keys"]
    s12["12. ValueError"]
    s1 -. "argparse.ArgumentParser(description=__doc__)" .-> s2
    s1 -. "parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)" .-> s3
    s1 -. "parser.add_argument('--check', action='store_true')" .-> s4
    s1 -. "parser.parse_args(data not statically known)" .-> s5
    s1 -->|"serialized_contract(data not statically known)"| s6
    s6 -. "json.dumps(build_contract(...), ensure_ascii=False, indent=2, sort_keys=True)" .-> s7
    s6 -->|"build_contract(data not statically known)"| s8
    s8 -. "app.openapi(data not statically known)" .-> s9
    s8 -. "set(CLIENT_PATHS)" .-> s10
    s8 -. "schema[…].keys(data not statically known)" .-> s11
    s8 -. "ValueError(...)" .-> s12
    b0["filesystem_read args.output.read_text"]
    s1 -. "filesystem_read args.output.read_text" .-> b0
    b1["filesystem_write args.output.write_text"]
    s1 -. "filesystem_write args.output.write_text" .-> b1
    click s1 "../modules/generate_client_contract.md"
    click s6 "../modules/generate_client_contract.md"
    click s8 "../modules/generate_client_contract.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `main` | - | `Path`, `DEFAULT_OUTPUT` | - | - |
| `argparse.ArgumentParser` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.add_argument` | - | - | - | - |
| `parser.parse_args` | - | - | - | - |
| `serialized_contract` | - | - | - | `...` |
| `json.dumps` | - | - | - | - |
| `build_contract` | - | `CLIENT_PATHS`, `CLIENT_PATHS`, `app` | - | `{...}` |
| `app.openapi` | - | - | - | - |
| `set` | - | - | - | - |
| `schema[…].keys` | - | - | - | - |
| `ValueError` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| main | argparse.ArgumentParser | 69 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.add_argument | 70 | `parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)` |
| main | parser.add_argument | 71 | `parser.add_argument('--check', action='store_true')` |
| main | parser.parse_args | 72 | `parser.parse_args(data not statically known)` |
| main | serialized_contract | 73 | `serialized_contract(data not statically known)` |
| serialized_contract | json.dumps | 65 | `json.dumps(build_contract(...), ensure_ascii=False, indent=2, sort_keys=True)` |
| serialized_contract | build_contract | 65 | `build_contract(data not statically known)` |
| build_contract | app.openapi | 24 | `app.openapi(data not statically known)` |
| build_contract | set | 25 | `set(CLIENT_PATHS)` |
| build_contract | schema[…].keys | 25 | `schema['paths'].keys(data not statically known)` |
| build_contract | ValueError | 27 | `ValueError(...)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| filesystem_read | `args.output.read_text` | `main` | 75 |
| filesystem_write | `args.output.write_text` | `main` | 79 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 69 |
| unresolved_call | `main` | `parser.add_argument` | 70 |
| unresolved_call | `main` | `parser.add_argument` | 71 |
| unresolved_call | `main` | `parser.parse_args` | 72 |
| external_call | `serialized_contract` | `json.dumps` | 65 |
| unresolved_call | `build_contract` | `app.openapi` | 24 |
| unresolved_call | `build_contract` | `schema['paths'].keys` | 25 |
| external_call | `build_contract` | `ValueError` | 27 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

The exporter reads registered schema metadata without starting the HTTP lifespan. It follows referenced component schemas, serializes deterministically, and either writes the requested artifact or compares exact bytes under --check. Route removal fails explicitly. It provides a shared contract baseline without introducing a public feature-capability endpoint.
