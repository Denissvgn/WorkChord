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
    participant p9 as HTMLResponse
    participant p10 as secrets.token_urlsafe
    participant p11 as time.time
    participant p12 as RedirectResponse
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
    p0-->>p9: HTMLResponse
    p0-->>p3: HTTPException
    p0-->>p10: secrets.token_urlsafe
    p0-->>p11: time.time
    p0-->>p12: RedirectResponse
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
    s12["12. HTMLResponse"]
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
    s1 -. "HTMLResponse(...)" .-> s12
    b0["mutation params.pop"]
    s1 -. "mutation params.pop" .-> b0
    click s1 "../modules/serve_disposable_oidc.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
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
| `HTMLResponse` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| authorize | dict | 46 | `dict(request.query_params)` |
| authorize | params.get | 47 | `params.get('redirect_uri')` |
| authorize | params.get | 47 | `params.get('client_id')` |
| authorize | params.get | 47 | `params.get('code_challenge_method')` |
| authorize | HTTPException | 48 | `HTTPException(400, 'Invalid fixture authorization request')` |
| authorize | params.pop | 49 | `params.pop('fixture_subject', None)` |
| authorize | ''.join | 51 | `''.join(...)` |
| authorize | html.escape | 51 | `html.escape(urlencode(...))` |
| authorize | urlencode | 51 | `urlencode({...})` |
| authorize | person.title | 51 | `person.title(data not statically known)` |
| authorize | HTMLResponse | 52 | `HTMLResponse(...)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `params.pop` | `authorize` | 49 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `authorize` | `params.get` | 47 |
| external_call | `authorize` | `HTTPException` | 48 |
| unresolved_call | `authorize` | `''.join` | 51 |
| external_call | `authorize` | `html.escape` | 51 |
| external_call | `authorize` | `urlencode` | 51 |
| unresolved_call | `authorize` | `person.title` | 51 |
| external_call | `authorize` | `HTMLResponse` | 52 |
| step_limit | `authorize` | `first 12 steps` | 0 |

## Behavior

This flow starts at `authorize` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
