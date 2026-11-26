"""The stock frontend proxy must forward MCP requests with the client's Host port.

The MCP host guard matches the default allowlist (localhost:*, 127.0.0.1:*,
[::1]:*) on the port. nginx's $host drops the port, so the MCP location must
forward $http_host. The round-trip test runs the real frontend/nginx.conf in
nginx, with a stub backend that echoes the Host it receives, and feeds that
forwarded value through the real MCPHostValidationMiddleware.
"""

from __future__ import annotations

import asyncio
import re
import shutil
import subprocess
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path

import pytest

from app.mcp_server import MCPHostValidationMiddleware


REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
NGINX_CONF = REPOSITORY_ROOT / "frontend/nginx.conf"
FRONTEND_DOCKERFILE = REPOSITORY_ROOT / "Dockerfile.frontend"
NON_DEFAULT_PORT = 8480


def _nginx_image() -> str:
    match = re.search(r"^ARG NGINX_IMAGE=(\S+)$", FRONTEND_DOCKERFILE.read_text(), re.M)
    assert match, "Dockerfile.frontend must pin NGINX_IMAGE"
    return match.group(1)


def _location_block(config: str, header: str) -> str:
    start = config.index(header)
    return config[start : config.index("\n    }", start)]


def test_mcp_location_forwards_host_with_port_and_precedes_api_prefix() -> None:
    config = NGINX_CONF.read_text()
    block = _location_block(config, "location ~ ^/api/mcp(/|$) {")

    assert "proxy_set_header Host $http_host;" in block
    assert "proxy_pass http://backend:8001;" in block
    assert "proxy_set_header Host $host;" not in block
    # Regex locations outrank the plain /api prefix, so MCP requests reach this block.
    assert config.index("location ~ ^/api/mcp(/|$) {") < config.index("location /api {")


def _guard_status(host: str) -> int:
    statuses: list[int] = []

    async def inner_app(scope, receive, send) -> None:  # pragma: no cover - accept path
        await send({"type": "http.response.start", "status": 200, "headers": []})
        await send({"type": "http.response.body", "body": b""})

    async def send(message) -> None:
        if message["type"] == "http.response.start":
            statuses.append(message["status"])

    async def receive() -> dict:
        return {"type": "http.request", "body": b"", "more_body": False}

    scope = {"type": "http", "headers": [(b"host", host.encode("latin1"))]}
    asyncio.run(MCPHostValidationMiddleware(inner_app)(scope, receive, send))
    return statuses[0]


def test_host_guard_accepts_default_loopback_hosts_on_non_default_port() -> None:
    for host in (
        f"localhost:{NON_DEFAULT_PORT}",
        f"127.0.0.1:{NON_DEFAULT_PORT}",
        f"[::1]:{NON_DEFAULT_PORT}",
    ):
        assert _guard_status(host) == 200, host


def test_host_guard_rejects_host_outside_allowlist() -> None:
    assert _guard_status(f"evil.example:{NON_DEFAULT_PORT}") == 421


def _docker_available() -> bool:
    if shutil.which("docker") is None:
        return False
    try:
        return (
            subprocess.run(["docker", "info"], capture_output=True, timeout=10).returncode
            == 0
        )
    except subprocess.TimeoutExpired:
        return False


needs_docker = pytest.mark.skipif(
    not _docker_available(), reason="Docker daemon is required to run nginx"
)


def _docker(*args: str) -> str:
    result = subprocess.run(
        ["docker", *args], capture_output=True, text=True, timeout=300, check=False
    )
    assert result.returncode == 0, f"docker {' '.join(args)}: {result.stderr}"
    return result.stdout.strip()


STUB_BACKEND_CONF = """
server {
    listen 8001;
    location / {
        return 200 "host=$http_host\\n";
    }
}
"""


@pytest.fixture()
def proxy_url():
    suffix = uuid.uuid4().hex[:10]
    network = f"mcp-proxy-{suffix}"
    backend = f"mcp-stub-{suffix}"
    proxy = f"mcp-proxy-front-{suffix}"
    image = _nginx_image()
    _docker("network", "create", network)
    try:
        # The stub takes the name "backend" on the network, the proxy's upstream.
        _docker(
            "run", "-d", "--name", backend, "--network", network, "--network-alias", "backend",
            "-e", f"STUB_CONF={STUB_BACKEND_CONF}", image,
            "sh", "-c",
            'printf "%s" "$STUB_CONF" > /etc/nginx/conf.d/default.conf && exec nginx -g "daemon off;"',
        )
        _docker(
            "run", "-d", "--name", proxy, "--network", network,
            "-p", "127.0.0.1::80",
            "-v", f"{NGINX_CONF}:/etc/nginx/conf.d/default.conf:ro",
            image,
        )
        # Validate the mounted configuration exactly as the frontend image loads it.
        _docker("exec", proxy, "nginx", "-t")
        port = _docker("port", proxy, "80/tcp").rsplit(":", 1)[-1]
        url = f"http://127.0.0.1:{port}"
        _wait_until_serving(url)
        yield url
    finally:
        subprocess.run(["docker", "rm", "-f", proxy, backend], capture_output=True)
        subprocess.run(["docker", "network", "rm", network], capture_output=True)


def _wait_until_serving(url: str, timeout: float = 60.0) -> None:
    deadline = time.monotonic() + timeout
    while True:
        try:
            with urllib.request.urlopen(f"{url}/api/mcp-other", timeout=5):
                return
        except (urllib.error.URLError, ConnectionError):
            # 502 while the stub backend starts, or a refused connection: retry.
            if time.monotonic() > deadline:
                raise
            time.sleep(0.5)


def _forwarded_host(url: str, path: str, host_header: str) -> str:
    request = urllib.request.Request(f"{url}{path}", headers={"Host": host_header})
    with urllib.request.urlopen(request, timeout=10) as response:
        body = response.read().decode().strip()
    assert body.startswith("host="), body
    return body.removeprefix("host=")


@needs_docker
@pytest.mark.allow_network
@pytest.mark.parametrize("mcp_path", ["/api/mcp", "/api/mcp/"])
def test_proxy_forwards_mcp_host_with_port_and_guard_accepts_it(proxy_url: str, mcp_path: str) -> None:
    for client_host in (
        f"localhost:{NON_DEFAULT_PORT}",
        f"127.0.0.1:{NON_DEFAULT_PORT}",
        f"[::1]:{NON_DEFAULT_PORT}",
    ):
        forwarded = _forwarded_host(proxy_url, mcp_path, client_host)
        assert forwarded == client_host
        assert _guard_status(forwarded) == 200


@needs_docker
@pytest.mark.allow_network
def test_proxy_keeps_disallowed_host_visible_to_guard_as_421(proxy_url: str) -> None:
    forwarded = _forwarded_host(proxy_url, "/api/mcp", f"evil.example:{NON_DEFAULT_PORT}")
    assert forwarded == f"evil.example:{NON_DEFAULT_PORT}"
    assert _guard_status(forwarded) == 421


@needs_docker
@pytest.mark.allow_network
def test_proxy_leaves_other_api_paths_on_bare_host(proxy_url: str) -> None:
    # /api/mcp-other is not the MCP mount, so it keeps the $host forwarding.
    assert _forwarded_host(proxy_url, "/api/mcp-other", f"localhost:{NON_DEFAULT_PORT}") == "localhost"
