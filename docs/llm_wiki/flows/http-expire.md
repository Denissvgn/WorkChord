# expire

**Entry point:** `expire` (`http`)
**Source:** [serve_disposable_oidc](../modules/serve_disposable_oidc.md)
**Modules touched:** [serve_disposable_oidc](../modules/serve_disposable_oidc.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as expire
    participant p1 as request.headers.get
    participant p2 as HTTPException
    participant p3 as request.json
    participant p4 as hashlib.sha256(…).hexdigest
    participant p5 as hashlib.sha256
    participant p6 as body[…].encode
    participant p7 as create_engine
    participant p8 as url.set
    participant p9 as engine.begin
    participant p10 as connection.execute
    participant p11 as text
    participant p12 as engine.dispose
    p0-->>p1: request.headers.get
    p0-->>p2: HTTPException
    p0-->>p3: request.json
    p0-->>p4: hashlib.sha256(…).hexdigest
    p0-->>p5: hashlib.sha256
    p0-->>p6: body[…].encode
    p0-->>p7: create_engine
    p0-->>p8: url.set
    p0-->>p9: engine.begin
    p0-->>p10: connection.execute
    p0-->>p11: text
    p0-->>p12: engine.dispose
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. expire"]
    s2["2. request.headers.get"]
    s3["3. HTTPException"]
    s4["4. request.json"]
    s5["5. hashlib.sha256(…).hexdigest"]
    s6["6. hashlib.sha256"]
    s7["7. body[…].encode"]
    s8["8. create_engine"]
    s9["9. url.set"]
    s10["10. engine.begin"]
    s11["11. connection.execute"]
    s12["12. text"]
    s1 -. "request.headers.get('X-Fixture-Key')" .-> s2
    s1 -. "HTTPException(403)" .-> s3
    s1 -. "request.json(data not statically known)" .-> s4
    s1 -. "hashlib.sha256(…).hexdigest(data not statically known)" .-> s5
    s1 -. "hashlib.sha256(...)" .-> s6
    s1 -. "body[…].encode(data not statically known)" .-> s7
    s1 -. "create_engine(url.set(...))" .-> s8
    s1 -. "url.set(drivername='sqlite')" .-> s9
    s1 -. "engine.begin(data not statically known)" .-> s10
    s1 -. "connection.execute(text(...), {...})" .-> s11
    s1 -. "text(#34;UPDATE user_sessions SET expires_at = '2000-01-01 00:00:00' WHERE session_token_hash = :digest AND principal_id IS NOT NULL#34;)" .-> s12
    click s1 "../modules/serve_disposable_oidc.md"
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `expire` | `request: Request` | - | - | `{...}` |
| `request.headers.get` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `request.json` | - | - | - | - |
| `hashlib.sha256(…).hexdigest` | - | - | - | - |
| `hashlib.sha256` | - | - | - | - |
| `body[…].encode` | - | - | - | - |
| `create_engine` | - | - | - | - |
| `url.set` | - | - | - | - |
| `engine.begin` | - | - | - | - |
| `connection.execute` | - | - | - | - |
| `text` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| expire | request.headers.get | 77 | `request.headers.get('X-Fixture-Key')` |
| expire | HTTPException | 78 | `HTTPException(403)` |
| expire | request.json | 79 | `request.json(data not statically known)` |
| expire | hashlib.sha256(…).hexdigest | 80 | `hashlib.sha256(body['token'].encode()).hexdigest(data not statically known)` |
| expire | hashlib.sha256 | 80 | `hashlib.sha256(...)` |
| expire | body[…].encode | 80 | `body['token'].encode(data not statically known)` |
| expire | create_engine | 81 | `create_engine(url.set(...))` |
| expire | url.set | 81 | `url.set(drivername='sqlite')` |
| expire | engine.begin | 83 | `engine.begin(data not statically known)` |
| expire | connection.execute | 84 | `connection.execute(text(...), {...})` |
| expire | text | 84 | `text("UPDATE user_sessions SET expires_at = '2000-01-01 00:00:00' WHERE session_token_hash = :digest AND principal_id IS NOT NULL")` |

### Boundary effects

*No boundary effects detected.*

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `expire` | `request.headers.get` | 77 |
| external_call | `expire` | `HTTPException` | 78 |
| unresolved_call | `expire` | `request.json` | 79 |
| unresolved_call | `expire` | `hashlib.sha256(body['token'].encode()).hexdigest` | 80 |
| external_call | `expire` | `hashlib.sha256` | 80 |
| unresolved_call | `expire` | `body['token'].encode` | 80 |
| external_call | `expire` | `create_engine` | 81 |
| unresolved_call | `expire` | `engine.begin` | 83 |
| unresolved_call | `expire` | `connection.execute` | 84 |
| external_call | `expire` | `text` | 84 |
| step_limit | `expire` | `first 12 steps` | 0 |

## Behavior

This flow starts at `expire` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
