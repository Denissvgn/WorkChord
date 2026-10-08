"""Local measurements retain limits and cannot become formal certification."""
import pytest
from scripts.load.local_baseline import summarize
from scripts.load.common import QualificationInputError


def declaration():
    return dict(fixture="owned",declared_before_measurement=True,concurrency=[1],
        expected_boundary_rejections=["collection_limit_exceeded"],unexpected_error_budget=0,
        latency_budget_ms=dict(read_p95=100,request_max=200))


def observation(status=200,code=None,latency=10):
    return dict(nonce="owned",fixture="synthetic-owned",real_provider_pilot=False,
        samples=[dict(concurrency=1,latency_ms=latency,response_bytes=50,response_cardinality=1,
            status=status,code=code,path="/bounded",profile="local_reads_v1",client_kind="synthetic")],
        resilience=dict(interruption_status=503,recovery_status=200))


def test_limits_are_observed_without_certification():
    result=summarize(observation(413,"collection_limit_exceeded"),declaration())
    assert result["status"]=="passed" and result["formal_certification"] is False
    assert result["synthetic_client_counts_are_not_people_capacity"] is True


def test_unexpected_failures_and_budget_misses_remain_limitations():
    assert summarize(observation(500),declaration())["status"]=="limitations"
    assert summarize(observation(latency=300),declaration())["status"]=="limitations"


@pytest.mark.parametrize("status", [200, 204, 400, 403, 404, 429, 500, 503])
def test_boundary_code_requires_its_contracted_status(status):
    result = summarize(observation(status, "collection_limit_exceeded"), declaration())
    assert result["status"] == "limitations"
    assert result["unexpected_errors"] == 1


@pytest.mark.parametrize("status,code", [(200, "other_error"), (413, None), (413, "other_error")])
def test_success_and_boundary_responses_require_consistent_codes(status, code):
    result = summarize(observation(status, code), declaration())
    assert result["status"] == "limitations" and result["unexpected_errors"] == 1


def test_ordinary_success_passes_and_undeclared_boundary_is_unexpected():
    assert summarize(observation(), declaration())["status"] == "passed"
    limits_not_allowed = declaration() | {"expected_boundary_rejections": []}
    result = summarize(observation(413, "collection_limit_exceeded"), limits_not_allowed)
    assert result["status"] == "limitations" and result["unexpected_errors"] == 1


@pytest.mark.parametrize("status", [None, True, 200.0, "200", 99, 600])
def test_malformed_http_status_is_rejected(status):
    with pytest.raises(QualificationInputError):
        summarize(observation(status), declaration())


def test_missing_or_mismatched_evidence_is_rejected():
    for raw in [observation() | {"nonce":"foreign"},observation() | {"samples":[]},observation() | {"real_provider_pilot":True}]:
        with pytest.raises(QualificationInputError):summarize(raw,declaration())


def test_nonfinite_observation_is_rejected():
    with pytest.raises(QualificationInputError):summarize(observation(latency=float("nan")),declaration())
    with pytest.raises(QualificationInputError):summarize(observation(latency=float("inf")),declaration())


def test_frozen_operation_coverage_cannot_omit_slow_or_missing_reads():
    spec = declaration() | {'operations': ['/bounded', '/summary'], 'rounds': 1}
    with pytest.raises(QualificationInputError, match='sample counts'):
        summarize(observation(), spec)
    raw = observation()
    raw['samples'].append(raw['samples'][0] | {'path': '/summary'})
    assert summarize(raw, spec)['status'] == 'passed'
    raw['samples'].append(raw['samples'][0])
    with pytest.raises(QualificationInputError, match='sample counts'):
        summarize(raw, spec)
