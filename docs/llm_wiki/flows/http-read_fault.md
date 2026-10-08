# read_fault

**Entry point:** `read_fault` (`http`)
**Source:** [serve_disposable_api](../modules/serve_disposable_api.md)
**Modules touched:** [serve_disposable_api](../modules/serve_disposable_api.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as read_fault
    participant p1 as request.headers.get
    participant p2 as HTTPException
    participant p3 as request.json
    participant p4 as isinstance
    participant p5 as body.get
    participant p6 as type
    participant p7 as faults.clear
    participant p8 as time.monotonic
    p0-->>p1: request.headers.get
    p0-->>p2: HTTPException
    p0-->>p3: request.json
    p0-->>p4: isinstance
    p0-->>p2: HTTPException
    p0-->>p5: body.get
    p0-->>p5: body.get
    p0-->>p2: HTTPException
    p0-->>p6: type
    p0-->>p2: HTTPException
    p0-->>p7: faults.clear
    p0-->>p8: time.monotonic
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. read_fault"]
    s2["2. request.headers.get"]
    s3["3. HTTPException"]
    s4["4. request.json"]
    s5["5. isinstance"]
    s6["6. HTTPException"]
    s7["7. body.get"]
    s8["8. body.get"]
    s9["9. HTTPException"]
    s10["10. type"]
    s11["11. HTTPException"]
    s12["12. faults.clear"]
    s1 -. "request.headers.get('X-Fixture-Key')" .-> s2
    s1 -. "HTTPException(403)" .-> s3
    s1 -. "request.json(data not statically known)" .-> s4
    s1 -. "isinstance(body, dict)" .-> s5
    s1 -. "HTTPException(422)" .-> s6
    s1 -. "body.get('status')" .-> s7
    s1 -. "body.get('task_id')" .-> s8
    s1 -. "HTTPException(422)" .-> s9
    s1 -. "type(task_id)" .-> s10
    s1 -. "HTTPException(422)" .-> s11
    s1 -. "faults.clear(data not statically known)" .-> s12
    b0["mutation faults.clear"]
    s1 -. "mutation faults.clear" .-> b0
    click s1 "../modules/serve_disposable_api.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `read_fault` | `request: Request`, `task_id: int` | - | `faults[...]` | `{...}` |
| `request.headers.get` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `request.json` | - | - | - | - |
| `isinstance` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `body.get` | - | - | - | - |
| `body.get` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `type` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `faults.clear` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| read_fault | request.headers.get | 84 | `request.headers.get('X-Fixture-Key')` |
| read_fault | HTTPException | 85 | `HTTPException(403)` |
| read_fault | request.json | 86 | `request.json(data not statically known)` |
| read_fault | isinstance | 87 | `isinstance(body, dict)` |
| read_fault | HTTPException | 88 | `HTTPException(422)` |
| read_fault | body.get | 89 | `body.get('status')` |
| read_fault | body.get | 90 | `body.get('task_id')` |
| read_fault | HTTPException | 91 | `HTTPException(422)` |
| read_fault | type | 92 | `type(task_id)` |
| read_fault | HTTPException | 93 | `HTTPException(422)` |
| read_fault | faults.clear | 94 | `faults.clear(data not statically known)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `faults.clear` | `read_fault` | 94 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `read_fault` | `request.headers.get` | 84 |
| unresolved_call | `read_fault` | `HTTPException` | 85 |
| unresolved_call | `read_fault` | `request.json` | 86 |
| external_call | `read_fault` | `isinstance` | 87 |
| unresolved_call | `read_fault` | `HTTPException` | 88 |
| unresolved_call | `read_fault` | `body.get` | 89 |
| unresolved_call | `read_fault` | `body.get` | 90 |
| unresolved_call | `read_fault` | `HTTPException` | 91 |
| external_call | `read_fault` | `type` | 92 |
| unresolved_call | `read_fault` | `HTTPException` | 93 |
| step_limit | `read_fault` | `first 12 steps` | 0 |

## Behavior

The route is registered only by the safety-fenced temporary SQLite application when an invocation nonce is configured. It retains ordinary task-edit authority, checks the matching nonce header and path/body task ID, accepts a positive bounded task ID and a limited failure status, replaces the single in-memory override and expires it after thirty seconds. Status zero removes the effect. Middleware applies the override only to task GET reads; it does not change stored tasks or authorize ordinary mutations. Static boundary detection misses these dynamic registration and middleware effects.
