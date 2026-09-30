# liveness_check

**Entry point:** `liveness_check` (`http`)
**Source:** [app_main](../modules/app_main.md)
**Modules touched:** [app_main](../modules/app_main.md), [config](../modules/config.md), [maintenance](../modules/maintenance.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as liveness_check
    participant p1 as maintenance_state
    participant p2 as get_settings
    participant p3 as Settings
    participant p4 as socket.gethostname
    participant p5 as maintenance_configuration_fingerprint
    participant p6 as json.dumps(…).encode
    participant p7 as json.dumps
    participant p8 as hashlib.sha256(…).hexdigest
    participant p9 as hashlib.sha256
    participant p10 as list
    p0->>p1: maintenance_state
    p1->>p2: get_settings
    p2->>p3: Settings
    p1-->>p4: socket.gethostname
    p1->>p5: maintenance_configuration_fingerprint
    p5->>p2: get_settings
    p5-->>p6: json.dumps(…).encode
    p5-->>p7: json.dumps
    p5-->>p8: hashlib.sha256(…).hexdigest
    p5-->>p9: hashlib.sha256
    p1-->>p10: list
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. liveness_check"]
    s2["2. maintenance_state"]
    s3["3. get_settings"]
    s4["4. Settings"]
    s5["5. socket.gethostname"]
    s6["6. maintenance_configuration_fingerprint"]
    s7["7. get_settings"]
    s8["8. json.dumps(…).encode"]
    s9["9. json.dumps"]
    s10["10. hashlib.sha256(…).hexdigest"]
    s11["11. hashlib.sha256"]
    s12["12. list"]
    s1 -->|"maintenance_state(data not statically known)"| s2
    s2 -->|"get_settings(data not statically known)"| s3
    s3 -->|"Settings(data not statically known)"| s4
    s2 -. "socket.gethostname(data not statically known)" .-> s5
    s2 -->|"maintenance_configuration_fingerprint(data not statically known)"| s6
    s6 -->|"get_settings(data not statically known)"| s7
    s6 -. "json.dumps(…).encode(data not statically known)" .-> s8
    s6 -. "json.dumps(payload, sort_keys=True, separators=(...))" .-> s9
    s6 -. "hashlib.sha256(…).hexdigest(data not statically known)" .-> s10
    s6 -. "hashlib.sha256(encoded)" .-> s11
    s2 -. "list(settings.maintenance_validation_allowlist)" .-> s12
    b0["network socket.gethostname"]
    s2 -. "network socket.gethostname" .-> b0
    click s1 "../modules/app_main.md"
    click s2 "../modules/maintenance.md"
    click s3 "../modules/config.md"
    click s4 "../modules/config.md"
    click s6 "../modules/maintenance.md"
    click s7 "../modules/config.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `liveness_check` | - | - | - | `{...}` |
| `maintenance_state` | - | - | - | `{...}` |
| `get_settings` | - | - | - | `Settings(...)` |
| `Settings` | - | - | - | - |
| `socket.gethostname` | - | - | - | - |
| `maintenance_configuration_fingerprint` | - | - | - | `...` |
| `get_settings` | - | - | - | `Settings(...)` |
| `json.dumps(…).encode` | - | - | - | - |
| `json.dumps` | - | - | - | - |
| `hashlib.sha256(…).hexdigest` | - | - | - | - |
| `hashlib.sha256` | - | - | - | - |
| `list` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| liveness_check | maintenance_state | 242 | `maintenance_state(data not statically known)` |
| maintenance_state | get_settings | 57 | `get_settings(data not statically known)` |
| get_settings | Settings | 479 | `Settings(data not statically known)` |
| maintenance_state | socket.gethostname | 59 | `socket.gethostname(data not statically known)` |
| maintenance_state | maintenance_configuration_fingerprint | 68 | `maintenance_configuration_fingerprint(data not statically known)` |
| maintenance_configuration_fingerprint | get_settings | 46 | `get_settings(data not statically known)` |
| maintenance_configuration_fingerprint | json.dumps(…).encode | 52 | `json.dumps(payload, sort_keys=True, separators=(',', ':')).encode(data not statically known)` |
| maintenance_configuration_fingerprint | json.dumps | 52 | `json.dumps(payload, sort_keys=True, separators=(...))` |
| maintenance_configuration_fingerprint | hashlib.sha256(…).hexdigest | 53 | `hashlib.sha256(encoded).hexdigest(data not statically known)` |
| maintenance_configuration_fingerprint | hashlib.sha256 | 53 | `hashlib.sha256(encoded)` |
| maintenance_state | list | 69 | `list(settings.maintenance_validation_allowlist)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| network | `socket.gethostname` | `maintenance_state` | 59 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `maintenance_configuration_fingerprint` | `json.dumps(payload, sort_keys=True, separators=(',', ':')).encode` | 52 |
| external_call | `maintenance_configuration_fingerprint` | `json.dumps` | 52 |
| unresolved_call | `maintenance_configuration_fingerprint` | `hashlib.sha256(encoded).hexdigest` | 53 |
| external_call | `maintenance_configuration_fingerprint` | `hashlib.sha256` | 53 |

## Behavior

This flow starts at `liveness_check` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
