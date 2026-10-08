"""Summarize declared local observations without issuing capacity certification."""
from __future__ import annotations

import argparse
import asyncio
import os
import platform
import time
from urllib.parse import urlsplit
import httpx
from collections import Counter, defaultdict
import json
import math
from pathlib import Path
import subprocess

from scripts.load.common import QualificationInputError, atomic_write_json, sha256_file, utc_now_text, authorized_base_url
from scripts.load.result import latency_summary
from scripts.load.run import Attempt, Recorder
from scripts.load.source_binding import source_binding, verify_binding


def summarize(raw, declaration):
    if raw.get("fixture") != "synthetic-owned" or raw.get("real_provider_pilot") is not False:
        raise QualificationInputError("Only synthetic local observations are supported")
    if raw.get("nonce") != declaration.get("fixture") or declaration.get("declared_before_measurement") is not True:
        raise QualificationInputError("A matching predeclared workload is required")
    groups = defaultdict(list)
    recorder = Recorder()
    for sample in raw.get("samples", []):
        if not isinstance(sample, dict) or sample.get("concurrency") not in declaration["concurrency"]:
            raise QualificationInputError("Observation does not match declared concurrency")
        values = [sample.get(k) for k in ("latency_ms", "response_bytes", "response_cardinality")]
        if any(not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v) or v < 0 for v in values):
            raise QualificationInputError("Malformed measurement")
        status = sample.get("status")
        if type(status) is not int or not 100 <= status <= 599:
            raise QualificationInputError("Malformed HTTP status")
        code = sample.get("code")
        boundary = (status == 413 and code == "collection_limit_exceeded"
            and code in declaration["expected_boundary_rejections"])
        expected = boundary or (200 <= status < 300 and code is None)
        attempt = Attempt(sample["path"], "expected_boundary" if boundary else "read", sample["status"],
            sample["latency_ms"], 0, sample["response_bytes"], sample["response_cardinality"],
            "local_workset", sample["profile"], "bounded_projection", sample["client_kind"])
        recorder.begin();recorder.finish(attempt)
        groups[(sample["profile"], sample["concurrency"], sample["path"])].append((sample, expected))
    if not recorder.attempts:
        raise QualificationInputError("An empty run is not evidence")
    required = declaration.get('operations')
    if required is not None:
        expected_counts = {(c, path): c * declaration['rounds'] for c in declaration['concurrency'] for path in required}
        actual_counts = Counter((s['concurrency'], s['path']) for s in raw['samples'])
        if actual_counts != expected_counts:
            raise QualificationInputError('Observed operations/sample counts differ from frozen workload')
    distributions=[]
    failures=0
    for (profile, concurrency, path), rows in sorted(groups.items()):
        latency=latency_summary(row["latency_ms"] for row,_ in rows)
        errors=sum(not ok for _,ok in rows);failures+=errors
        distributions.append(dict(profile=profile, concurrency=concurrency, operation=path, samples=len(rows),
            status_counts=dict(Counter(str(row["status"]) for row,_ in rows)), unexpected_errors=errors,
            latency_ms=latency, response_bytes_max=max(row["response_bytes"] for row,_ in rows),
            latency_budget_met=latency["p95"]<=declaration["latency_budget_ms"]["read_p95"]
                and latency["max"]<=declaration["latency_budget_ms"]["request_max"]))
    recovery=raw.get("resilience", {})
    recovered=(recovery.get("interruption_status")==503 and recovery.get("recovery_status")==200) or recovery.get("transaction_rollback_verified") is True
    passed=failures<=declaration["unexpected_error_budget"] and recovered and all(row["latency_budget_met"] for row in distributions)
    return dict(schema_version="local-workset-measurement-v1", measured_at=utc_now_text(), status="passed" if passed else "limitations",
        samples=len(recorder.attempts), distributions=distributions, unexpected_errors=failures,
        resilience=raw.get("resilience"), recovery_verified=recovered, formal_certification=False,
        synthetic_client_counts_are_not_people_capacity=True, real_provider_pilot=False,
        tooling_basis=["scripts.load.run.Recorder", "scripts.load.run.Attempt", "scripts.load.result.latency_summary"],
        environment=raw.get("environment", {}), datasets=declaration.get("datasets", {}), declaration=declaration)


async def measure(args, declaration):
    base = authorized_base_url(args.base_url, authorize_host=urlsplit(args.base_url).netloc,
        environment="test", production_authorization=None, change_id=None)
    if urlsplit(base).hostname not in {"localhost", "127.0.0.1", "::1"}:
        raise QualificationInputError("Local measurements require a loopback fixture")
    cookies=json.loads(args.session_state.read_text()).get("cookies", [])
    human_cookies={item["name"]:item["value"] for item in cookies}
    agent_key=os.environ.get(args.agent_key_env, "")
    if not agent_key:raise QualificationInputError("Set the explicitly selected synthetic agent-key environment variable")
    profiles=[("human_reads_v1","synthetic_authenticated_human",[
        "/api/tasks/lookup?iteration_id=1&limit=100", "/api/tasks/9/detail?children_after_id=2560",
        "/api/projects/portfolio-summaries/page?limit=100", "/api/tasks/delivery-metrics?iteration_id=3", "/api/iterations/3/tasks", "/api/team-member-profiles/1/capacity?start=2026-01-01&end=2026-02-01"]),
        ("agent_poll_v1","synthetic_agent",["/api/agent/me/work","/api/agent/me/claims","/api/agent/capabilities"]),
        ("bounded_read_limits_v1","synthetic_browser",["/api/tasks/delivery-metrics?project_id=1","/api/iterations/1/tasks"])]
    samples=[]
    async with httpx.AsyncClient(base_url=base,cookies=human_cookies,timeout=30) as human, httpx.AsyncClient(base_url=base,
            headers={"X-Agent-API-Key":agent_key},timeout=30) as agent:
        proof=await human.get("/api/auth/me")
        if proof.headers.get("X-WorkChord-Fixture") != args.nonce:raise QualificationInputError("Fixture nonce mismatch")
        identity=proof.json()
        if identity.get("authenticated") is not True:raise QualificationInputError("An authenticated synthetic human session is required")
        for concurrency in declaration["concurrency"]:
            for profile,kind,paths in profiles:
                async def client(index):
                    transport=agent if kind=="synthetic_agent" else human
                    for _ in range(declaration["rounds"]):
                        for path in paths:
                            before=time.perf_counter();response=await transport.get(path)
                            if response.headers.get("X-WorkChord-Fixture")!=args.nonce:raise QualificationInputError("Fixture changed during measurement")
                            data=response.json();detail=data.get("detail") if isinstance(data,dict) else None
                            samples.append(dict(profile=profile,client_kind=kind,concurrency=concurrency,client=index,path=path,
                                status=response.status_code,latency_ms=(time.perf_counter()-before)*1000,
                                response_bytes=len(response.content),response_cardinality=len(data.get("items", [])) if isinstance(data,dict) and "items" in data else len(data) if isinstance(data,list) else 1,
                                code=detail.get("code") if isinstance(detail,dict) else None,state=data.get("state") if isinstance(data,dict) else None))
                            await asyncio.sleep(.1)
                await asyncio.gather(*(client(i) for i in range(concurrency)))
        headers={"X-Fixture-Key":args.nonce,"X-CSRF-Token":identity.get("csrf_token", ""),"Origin":"http://localhost:4173"}
        response=await human.post("/api/tasks/9/_fixture/read-fault",headers=headers,json={"task_id":9,"status":503})
        if response.status_code!=200:raise QualificationInputError("Controlled interruption was not authorized")
        try:interrupted=(await human.get("/api/tasks/9/detail")).status_code
        finally:
            response=await human.post("/api/tasks/9/_fixture/read-fault",headers=headers,json={"task_id":9,"status":0})
            if response.status_code!=200:raise QualificationInputError("Controlled interruption cleanup failed")
        recovered=(await human.get("/api/tasks/9/detail")).status_code
    return dict(nonce=args.nonce,fixture="synthetic-owned",real_provider_pilot=False,samples=samples,
        resilience=dict(interruption_status=interrupted,recovery_status=recovered),
        environment=dict(client_platform=platform.platform(),client_architecture=platform.machine(),python=platform.python_version(),
            httpx=httpx.__version__,base_url=base,identity_basis="synthetic_OIDC_human_and_cookie_free_agent"))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--observations",type=Path)
    parser.add_argument("--base-url")
    parser.add_argument("--nonce")
    parser.add_argument("--session-state",type=Path)
    parser.add_argument("--agent-key-env",default="WORKCHORD_BENCHMARK_AGENT_KEY")
    parser.add_argument("--declaration",type=Path,required=True)
    parser.add_argument("--source-revision")
    parser.add_argument("--source-sha256")
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():parser.error("Use a new output path; historical observations are immutable")
    try:
        binding = source_binding()
        declaration=json.loads(args.declaration.read_text())
        if args.observations:
            raw=json.loads(args.observations.read_text())
        else:
            if not args.base_url or not args.nonce or not args.session_state:parser.error("Measurement requires base URL, nonce and private session state")
            raw=asyncio.run(measure(args,declaration))
        result=summarize(raw,declaration)
        result['raw_observations'] = raw
        result['source_binding'] = {'before': binding, 'after': verify_binding(binding)}
        result["source_revision"]=args.source_revision or subprocess.check_output(["git","rev-parse","HEAD"],text=True).strip()
        result["source_sha256"]=args.source_sha256
        result["source_dirty_measurement_basis"]=bool(args.source_revision and args.source_sha256)
        result["observations_sha256"]=sha256_file(args.observations) if args.observations else None
        result["declaration_sha256"]=sha256_file(args.declaration)
        atomic_write_json(args.output,result)
    except (QualificationInputError,ValueError,KeyError,TypeError) as exc:parser.error(str(exc))
    print(result["status"])
    return 0 if result["status"]=="passed" else 1


if __name__=="__main__":raise SystemExit(main())
