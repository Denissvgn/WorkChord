#!/usr/bin/env python3
"""Synthetic OIDC issuer confined to the disposable browser network and database."""

import base64
import hashlib
import html
import json
import os
import secrets
import time
from urllib.parse import parse_qs, urlencode

from cryptography.hazmat.primitives.asymmetric import rsa
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import jwt
from sqlalchemy import create_engine, text
import uvicorn

from tests.support.database import assert_safe_test_database_url

url = assert_safe_test_database_url(os.environ["DATABASE_URL"])
if url.get_backend_name() != "sqlite" or os.environ.get("DEPLOYMENT_ENVIRONMENT") != "test":
    raise RuntimeError("The synthetic issuer requires an isolated test database")
issuer = os.environ.get("WORKCHORD_FIXTURE_ISSUER", "http://oidc:8002")
if issuer not in {"http://localhost:8002", "http://oidc:8002"}:
    raise RuntimeError("Only an isolated fixture issuer is allowed")
redirect_uri = "http://localhost:4173/api/auth/callback"
key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
jwk = json.loads(jwt.algorithms.RSAAlgorithm.to_jwk(key.public_key()))
jwk["kid"] = "disposable-key"
grants = {}
app = FastAPI()


@app.get("/.well-known/openid-configuration")
def configuration():
    return {"issuer": issuer, "authorization_endpoint": issuer + "/authorize", "token_endpoint": issuer + "/token", "jwks_uri": issuer + "/keys"}


@app.get("/keys")
def keys():
    return {"keys": [jwk]}


@app.get("/authorize")
def authorize(request: Request):
    params = dict(request.query_params)
    if params.get("redirect_uri") != redirect_uri or params.get("client_id") != "browser-client" or params.get("code_challenge_method") != "S256":
        raise HTTPException(400, "Invalid fixture authorization request")
    subject = params.pop("fixture_subject", None)
    if subject is None:
        links = ''.join(f'<a href="/authorize?{html.escape(urlencode({**params, "fixture_subject": person}))}">Continue as {person.title()}</a><br>' for person in ["alice", "bob", "charlie"])
        return HTMLResponse('<html lang="en"><title>Disposable identity provider</title><h1>Choose a fixture account</h1>' + links + '</html>')
    if subject not in {"alice", "bob", "charlie"}:
        raise HTTPException(400)
    code = secrets.token_urlsafe(24)
    grants[code] = {**params, "subject": subject, "expires": time.time() + 120}
    return RedirectResponse(redirect_uri + "?" + urlencode({"code": code, "state": params["state"]}), status_code=303)


@app.post("/token")
async def token(request: Request):
    params = {name: values[0] for name, values in parse_qs((await request.body()).decode()).items()}
    grant = grants.pop(params.get("code"), None)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(params.get("code_verifier", "").encode()).digest()).rstrip(b"=").decode()
    if not grant or grant["expires"] < time.time() or challenge != grant["code_challenge"] or params.get("redirect_uri") != redirect_uri or params.get("client_secret") != "disposable-browser-secret":
        raise HTTPException(400, "Invalid fixture code exchange")
    claims = {"iss": issuer, "sub": grant["subject"], "name": grant["subject"].title(), "aud": "browser-client", "iat": int(time.time()), "exp": int(time.time()) + 120, "nonce": grant["nonce"]}
    return {"id_token": jwt.encode(claims, key, algorithm="RS256", headers={"kid": jwk["kid"]})}


@app.post("/control/expire")
async def expire(request: Request):
    """Expire a fixture session without waiting eight hours during browser checks."""
    if request.headers.get("X-Fixture-Key") != "disposable-browser-control":
        raise HTTPException(403)
    body = await request.json()
    digest = hashlib.sha256(body["token"].encode()).hexdigest()
    engine = create_engine(url.set(drivername="sqlite"))
    try:
        with engine.begin() as connection:
            result = connection.execute(text("UPDATE user_sessions SET expires_at = '2000-01-01 00:00:00' WHERE session_token_hash = :digest AND principal_id IS NOT NULL"), {"digest": digest})
        return {"expired": result.rowcount}
    finally:
        engine.dispose()


if __name__ == "__main__":
    uvicorn.run(app, host=os.environ.get("WORKCHORD_FIXTURE_BIND", "127.0.0.1"), port=8002, access_log=False)
