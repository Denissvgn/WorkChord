# authorize

**Entry point:** `authorize` (`http`)
**Source:** [serve_disposable_oidc](../modules/serve_disposable_oidc.md)
**Modules touched:** [serve_disposable_oidc](../modules/serve_disposable_oidc.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as authorize
    participant p1 as dict
    participant p2 as params.get
    participant p3 as HTTPException
    participant p4 as params.pop
    participant p5 as ''.join
    participant p6 as html.escape
    participant p7 as urlencode
    participant p8 as person.title
    participant p9 as os.environ.get
    participant p10 as HTMLResponse
    participant p11 as set
    participant p12 as secrets.token_urlsafe
    participant p13 as time.time
    participant p14 as RedirectResponse
    p0-->>p1: dict
    p0-->>p2: params.get
    p0-->>p2: params.get
    p0-->>p2: params.get
    p0-->>p3: HTTPException
    p0-->>p4: params.pop
    p0-->>p5: ''.join
    p0-->>p6: html.escape
    p0-->>p7: urlencode
    p0-->>p8: person.title
    p0-->>p9: os.environ.get
    p0-->>p10: HTMLResponse
    p0-->>p9: os.environ.get
    p0-->>p11: set
    p0-->>p3: HTTPException
    p0-->>p12: secrets.token_urlsafe
    p0-->>p13: time.time
    p0-->>p14: RedirectResponse
    p0-->>p7: urlencode
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. authorize"]
    s2["2. dict"]
    s3["3. params.get"]
    s4["4. params.get"]
    s5["5. params.get"]
    s6["6. HTTPException"]
    s7["7. params.pop"]
    s8["8. ''.join"]
    s9["9. html.escape"]
    s10["10. urlencode"]
    s11["11. person.title"]
    s12["12. os.environ.get"]
    s1 -. "dict(request.query_params)" .-> s2
    s1 -. "params.get('redirect_uri')" .-> s3
    s1 -. "params.get('client_id')" .-> s4
    s1 -. "params.get('code_challenge_method')" .-> s5
    s1 -. "HTTPException(400, 'Invalid fixture authorization request')" .-> s6
    s1 -. "params.pop('fixture_subject', None)" .-> s7
    s1 -. "''.join(...)" .-> s8
    s1 -. "html.escape(urlencode(...))" .-> s9
    s1 -. "urlencode({...})" .-> s10
    s1 -. "person.title(data not statically known)" .-> s11
    s1 -. "os.environ.get('WORKCHORD_FIXTURE_PLANNING')" .-> s12
    b0["mutation params.pop"]
    s1 -. "mutation params.pop" .-> b0
    b1["environment_read os.environ.get"]
    s1 -. "environment_read os.environ.get" .-> b1
    b2["environment_read os.environ.get"]
    s1 -. "environment_read os.environ.get" .-> b2
    click s1 "../modules/serve_disposable_oidc.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
    class b1 boundary
    class b2 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `authorize` | `request: Request` | `redirect_uri`, `redirect_uri` | `grants[...]` | `HTMLResponse(...)`, `RedirectResponse(...)` |
| `dict` | - | - | - | - |
| `params.get` | - | - | - | - |
| `params.get` | - | - | - | - |
| `params.get` | - | - | - | - |
| `HTTPException` | - | - | - | - |
| `params.pop` | - | - | - | - |
| `''.join` | - | - | - | - |
| `html.escape` | - | - | - | - |
| `urlencode` | - | - | - | - |
| `person.title` | - | - | - | - |
| `os.environ.get` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| authorize | dict | 48 | `dict(request.query_params)` |
| authorize | params.get | 49 | `params.get('redirect_uri')` |
| authorize | params.get | 49 | `params.get('client_id')` |
| authorize | params.get | 49 | `params.get('code_challenge_method')` |
| authorize | HTTPException | 50 | `HTTPException(400, 'Invalid fixture authorization request')` |
| authorize | params.pop | 51 | `params.pop('fixture_subject', None)` |
| authorize | ''.join | 53 | `''.join(...)` |
| authorize | html.escape | 53 | `html.escape(urlencode(...))` |
| authorize | urlencode | 53 | `urlencode({...})` |
| authorize | person.title | 53 | `person.title(data not statically known)` |
| authorize | os.environ.get | 53 | `os.environ.get('WORKCHORD_FIXTURE_PLANNING')` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `params.pop` | `authorize` | 51 |
| environment_read | `os.environ.get` | `authorize` | 53 |
| environment_read | `os.environ.get` | `authorize` | 55 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `authorize` | `params.get` | 49 |
| external_call | `authorize` | `HTTPException` | 50 |
| step_limit | `authorize` | `first 12 steps` | 0 |

## Behavior

This flow starts at `authorize` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
