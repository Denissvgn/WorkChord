# generate_client_contract

**Entry point:** `main` (`process`)
**Source:** [generate_client_contract](../modules/generate_client_contract.md)
**Modules touched:** [generate_client_contract](../modules/generate_client_contract.md)

**Related modules:** [app_main](../modules/app_main.md)

## Call sequence

> Static overview in presentation order, not runtime execution order. Arrows retain captured callers; representative internal continuations and boundary examples precede repeated helper detail.

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as main
    participant p1 as argparse.ArgumentParser
    participant p2 as parser.add_argument
    participant p3 as parser.parse_args
    participant p4 as serialized_contract
    participant p5 as args.output.exists
    participant p6 as args.output.read_text
    participant p7 as parser.exit
    participant p8 as args.output.parent.mkdir
    participant p9 as args.output.write_text
    participant p10 as json.dumps
    participant p11 as build_contract
    participant p12 as app.openapi
    participant p13 as set
    participant p14 as schema[…].keys
    participant p15 as ValueError
    participant p16 as sorted
    participant p17 as collect
    participant p18 as components[…].get
    p0-->>p1: argparse.ArgumentParser(description=__doc__)
    p0-->>p2: parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    p0-->>p2: parser.add_argument('--check', action='store_true')
    p0-->>p3: parser.parse_args
    p0->>p4: serialized_contract
    p0-->>p5: args.output.exists
    p0-->>p6: args.output.read_text
    p0-->>p7: parser.exit(1, 'Client contract differs regenerate and review consumer compatibility.\n')
    p0-->>p8: args.output.parent.mkdir(parents=True, exist_ok=True)
    p0-->>p9: args.output.write_text(expected)
    p4-->>p10: json.dumps(build_contract(...), ensure_ascii=False, indent=2, sort_keys=True)
    p4->>p11: build_contract
    p11-->>p12: app.openapi
    p11-->>p13: set(CLIENT_PATHS)
    p11-->>p14: schema[…].keys
    p11-->>p15: ValueError(...)
    p11-->>p16: sorted(missing)
    p11-->>p17: collect(paths)
    p11-->>p18: components[…].get('required', [...])
```

> Call sequence diagram shows 19 of 19 interactions; 0 omitted to keep the visualization within the 30-interaction and generated-diagram limits, with uncertain identities omitted rather than inferred.

> Captured boundary calls: external 5 of 5 (0 omitted); unresolved 12 of 12 (0 omitted). These counts cover the captured static trace.
> Detailed flow queries retain their own coverage and limits; omitted paths may execute at runtime.

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->

### Analysis coverage

**Effect analysis evaluated.** Flow assembly and source effect analysis are separate; empty observations do not prove an empty handler body.

Source steps: 3; effect analysis evaluated: 3, partial: 0, unavailable: 0. Counts include steps omitted from the displayed trace.

Collector observations for 3 source steps with known totals: observed: 9, emitted: 9, omitted: 0. Unavailable totals are excluded.

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
| main | argparse.ArgumentParser | 83 | `argparse.ArgumentParser(description=__doc__)` |
| main | parser.add_argument | 84 | `parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)` |
| main | parser.add_argument | 85 | `parser.add_argument('--check', action='store_true')` |
| main | parser.parse_args | 86 | `parser.parse_args(data not statically known)` |
| main | serialized_contract | 87 | `serialized_contract(data not statically known)` |
| serialized_contract | json.dumps | 79 | `json.dumps(build_contract(...), ensure_ascii=False, indent=2, sort_keys=True)` |
| serialized_contract | build_contract | 79 | `build_contract(data not statically known)` |
| build_contract | app.openapi | 37 | `app.openapi(data not statically known)` |
| build_contract | set | 38 | `set(CLIENT_PATHS)` |
| build_contract | schema[…].keys | 38 | `schema['paths'].keys(data not statically known)` |
| build_contract | ValueError | 40 | `ValueError(...)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| filesystem_read | `args.output.read_text` | `main` | 89 |
| filesystem_write | `args.output.write_text` | `main` | 93 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| external_call | `main` | `argparse.ArgumentParser` | 83 |
| unresolved_call | `main` | `parser.add_argument` | 84 |
| unresolved_call | `main` | `parser.add_argument` | 85 |
| unresolved_call | `main` | `parser.parse_args` | 86 |
| external_call | `serialized_contract` | `json.dumps` | 79 |
| unresolved_call | `build_contract` | `app.openapi` | 37 |
| unresolved_call | `build_contract` | `schema['paths'].keys` | 38 |
| external_call | `build_contract` | `ValueError` | 40 |
| step_limit | `main` | `first 12 steps` | 0 |

## Behavior

The exporter reads registered schema metadata without starting the HTTP lifespan. It follows referenced component schemas, serializes deterministically, and either writes the requested artifact or compares exact bytes under --check. Route removal fails explicitly. It provides a shared contract baseline without introducing a public feature-capability endpoint.
