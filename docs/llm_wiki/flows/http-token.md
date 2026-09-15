# token

**Entry point:** `token` (`http`)
**Source:** [serve_disposable_oidc](../modules/serve_disposable_oidc.md)
**Modules touched:** [serve_disposable_oidc](../modules/serve_disposable_oidc.md)

## Call sequence

<!-- Auto-generated from static call edges. Dashed arrows are external or unresolved calls. Reviewed runtime conditions and side effects belong in Behavior. -->
```mermaid
sequenceDiagram
    participant p0 as token
    participant p1 as parse_qs(…).items
    participant p2 as parse_qs
    participant p3 as (…).decode
    participant p4 as request.body
    participant p5 as grants.pop
    participant p6 as params.get
    participant p7 as base64.urlsafe_b64encode(…).rstrip(…).decode
    participant p8 as base64.urlsafe_b64encode(…).rstrip
    participant p9 as base64.urlsafe_b64encode
    participant p10 as hashlib.sha256(…).digest
    participant p11 as hashlib.sha256
    participant p12 as params.get(…).encode
    participant p13 as time.time
    participant p14 as HTTPException
    participant p15 as grant[…].title
    participant p16 as int
    participant p17 as jwt.encode
    p0-->>p1: parse_qs(…).items
    p0-->>p2: parse_qs
    p0-->>p3: (…).decode
    p0-->>p4: request.body
    p0-->>p5: grants.pop
    p0-->>p6: params.get
    p0-->>p7: base64.urlsafe_b64encode(…).rstrip(…).decode
    p0-->>p8: base64.urlsafe_b64encode(…).rstrip
    p0-->>p9: base64.urlsafe_b64encode
    p0-->>p10: hashlib.sha256(…).digest
    p0-->>p11: hashlib.sha256
    p0-->>p12: params.get(…).encode
    p0-->>p6: params.get
    p0-->>p13: time.time
    p0-->>p6: params.get
    p0-->>p6: params.get
    p0-->>p14: HTTPException
    p0-->>p15: grant[…].title
    p0-->>p16: int
    p0-->>p13: time.time
    p0-->>p16: int
    p0-->>p13: time.time
    p0-->>p17: jwt.encode
```

## Data flow

<!-- Auto-generated static analysis. Treat values and boundaries as best-effort hints, not runtime proof. -->
```mermaid
flowchart LR
    s1["1. token"]
    s2["2. parse_qs(…).items"]
    s3["3. parse_qs"]
    s4["4. (…).decode"]
    s5["5. request.body"]
    s6["6. grants.pop"]
    s7["7. params.get"]
    s8["8. base64.urlsafe_b64encode(…).rstrip(…).decode"]
    s9["9. base64.urlsafe_b64encode(…).rstrip"]
    s10["10. base64.urlsafe_b64encode"]
    s11["11. hashlib.sha256(…).digest"]
    s12["12. hashlib.sha256"]
    s1 -. "parse_qs(…).items(data not statically known)" .-> s2
    s1 -. "parse_qs(...)" .-> s3
    s1 -. "(…).decode(data not statically known)" .-> s4
    s1 -. "request.body(data not statically known)" .-> s5
    s1 -. "grants.pop(params.get(...), None)" .-> s6
    s1 -. "params.get('code')" .-> s7
    s1 -. "base64.urlsafe_b64encode(…).rstrip(…).decode(data not statically known)" .-> s8
    s1 -. "base64.urlsafe_b64encode(…).rstrip(b'=')" .-> s9
    s1 -. "base64.urlsafe_b64encode(...)" .-> s10
    s1 -. "hashlib.sha256(…).digest(data not statically known)" .-> s11
    s1 -. "hashlib.sha256(...)" .-> s12
    b0["mutation grants.pop"]
    s1 -. "mutation grants.pop" .-> b0
    click s1 "../modules/serve_disposable_oidc.md"
    classDef boundary stroke:#b45309,stroke-dasharray: 4 2
    class b0 boundary
```

### Step data

| Step | Inputs | Reads | Writes | Returns |
|---|---|---|---|---|
| `token` | `request: Request` | `redirect_uri`, `issuer`, `key`, `jwk` | - | `{...}` |
| `parse_qs(…).items` | - | - | - | - |
| `parse_qs` | - | - | - | - |
| `(…).decode` | - | - | - | - |
| `request.body` | - | - | - | - |
| `grants.pop` | - | - | - | - |
| `params.get` | - | - | - | - |
| `base64.urlsafe_b64encode(…).rstrip(…).decode` | - | - | - | - |
| `base64.urlsafe_b64encode(…).rstrip` | - | - | - | - |
| `base64.urlsafe_b64encode` | - | - | - | - |
| `hashlib.sha256(…).digest` | - | - | - | - |
| `hashlib.sha256` | - | - | - | - |

### Call data

| From | To | Line | Call |
|---|---|---:|---|
| token | parse_qs(…).items | 62 | `parse_qs((await request.body()).decode()).items(data not statically known)` |
| token | parse_qs | 62 | `parse_qs(...)` |
| token | (…).decode | 62 | `(await request.body()).decode(data not statically known)` |
| token | request.body | 62 | `request.body(data not statically known)` |
| token | grants.pop | 63 | `grants.pop(params.get(...), None)` |
| token | params.get | 63 | `params.get('code')` |
| token | base64.urlsafe_b64encode(…).rstrip(…).decode | 64 | `base64.urlsafe_b64encode(hashlib.sha256(params.get('code_verifier', '').encode()).digest()).rstrip(b'=').decode(data not statically known)` |
| token | base64.urlsafe_b64encode(…).rstrip | 64 | `base64.urlsafe_b64encode(hashlib.sha256(params.get('code_verifier', '').encode()).digest()).rstrip(b'=')` |
| token | base64.urlsafe_b64encode | 64 | `base64.urlsafe_b64encode(...)` |
| token | hashlib.sha256(…).digest | 64 | `hashlib.sha256(params.get('code_verifier', '').encode()).digest(data not statically known)` |
| token | hashlib.sha256 | 64 | `hashlib.sha256(...)` |

### Boundary effects

| Kind | Target | Step | Line |
|---|---|---|---:|
| mutation | `grants.pop` | `token` | 63 |

### Static analysis gaps

| Kind | Step | Target | Line |
|---|---|---|---:|
| unresolved_call | `token` | `parse_qs((await request.body()).decode()).items` | 62 |
| external_call | `token` | `parse_qs` | 62 |
| unresolved_call | `token` | `(await request.body()).decode` | 62 |
| unresolved_call | `token` | `request.body` | 62 |
| unresolved_call | `token` | `base64.urlsafe_b64encode(hashlib.sha256(params.get('code_verifier', '').encode()).digest()).rstrip(b'=').decode` | 64 |
| unresolved_call | `token` | `base64.urlsafe_b64encode(hashlib.sha256(params.get('code_verifier', '').encode()).digest()).rstrip` | 64 |
| external_call | `token` | `base64.urlsafe_b64encode` | 64 |
| unresolved_call | `token` | `hashlib.sha256(params.get('code_verifier', '').encode()).digest` | 64 |
| external_call | `token` | `hashlib.sha256` | 64 |
| step_limit | `token` | `first 12 steps` | 0 |

## Behavior

This flow starts at `token` and is classified as `http`. The generated call and data-flow sections are bounded static projections; runtime conditions and side effects require source-level confirmation.
