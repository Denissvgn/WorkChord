"""Build, validate, and evaluate machine-readable load result documents."""

from __future__ import annotations

from collections import Counter, defaultdict
import math
from pathlib import Path
from typing import Any, Iterable, Mapping

from jsonschema import Draft202012Validator, FormatChecker

from scripts.load.common import (
    QualificationInputError,
    RESULT_SCHEMA_PATH,
    atomic_write_json,
    capacity_contract,
    read_json_object,
    traffic_profile,
    verify_document,
)


def percentile(values: Iterable[float], quantile: float) -> float:
    ordered = sorted(float(value) for value in values)
    if not ordered:
        return 0.0
    if not 0 <= quantile <= 1:
        raise QualificationInputError("Percentile quantile must be between zero and one")
    rank = (len(ordered) - 1) * quantile
    lower = math.floor(rank)
    upper = math.ceil(rank)
    if lower == upper:
        return ordered[lower]
    fraction = rank - lower
    return ordered[lower] + ((ordered[upper] - ordered[lower]) * fraction)


def latency_summary(values: Iterable[float]) -> dict[str, float]:
    samples = list(values)
    return {
        "p50": round(percentile(samples, 0.50), 3),
        "p95": round(percentile(samples, 0.95), 3),
        "p99": round(percentile(samples, 0.99), 3),
        "max": round(max(samples, default=0.0), 3),
    }


def measurement(
    latencies: Iterable[float], statuses: Iterable[int]
) -> dict[str, Any]:
    samples = list(latencies)
    status_values = list(statuses)
    if len(samples) != len(status_values):
        raise QualificationInputError("Latency/status sample counts differ")
    return {
        "attempts": len(samples),
        "statuses": {
            str(status): count
            for status, count in sorted(Counter(status_values).items())
        },
        "latency_ms": latency_summary(samples),
    }


def validate_result(document: Mapping[str, Any], *, verify_checksum: bool = True) -> None:
    if verify_checksum:
        verify_document(document)
    schema = read_json_object(RESULT_SCHEMA_PATH)
    errors = sorted(
        Draft202012Validator(
            schema,
            format_checker=FormatChecker(),
        ).iter_errors(document),
        key=lambda error: list(error.absolute_path),
    )
    if errors:
        rendered = "; ".join(
            f"{'/'.join(map(str, error.absolute_path)) or '<root>'}: {error.message}"
            for error in errors[:10]
        )
        raise QualificationInputError(f"Load result schema validation failed: {rendered}")


def _gate(
    status: str,
    *,
    actual: Any,
    required: Any,
    reason: str,
) -> dict[str, Any]:
    return {
        "status": status,
        "actual": actual,
        "required": required,
        "reason": reason,
    }


def _maximum_gate(name: str, actual: float, maximum: float) -> tuple[str, dict[str, Any]]:
    passed = actual <= maximum
    return name, _gate(
        "passed" if passed else "failed",
        actual=actual,
        required={"maximum": maximum},
        reason=(
            f"{actual:.3f} is within the maximum {maximum:.3f}"
            if passed
            else f"{actual:.3f} exceeds the maximum {maximum:.3f}"
        ),
    )


def _minimum_gate(name: str, actual: float, minimum: float) -> tuple[str, dict[str, Any]]:
    passed = actual >= minimum
    return name, _gate(
        "passed" if passed else "failed",
        actual=actual,
        required={"minimum": minimum},
        reason=(
            f"{actual:.3f} meets the minimum {minimum:.3f}"
            if passed
            else f"{actual:.3f} is below the minimum {minimum:.3f}"
        ),
    )


def evaluate_client_gates(document: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    contract = capacity_contract()
    profile = traffic_profile(contract, str(document["traffic"]["profile_id"]))
    traffic = document["traffic"]
    operations = document["operations"]
    classes = document["classifications"]
    slos = contract["slos"]
    variance = contract["traffic"]["allowed_variance"]
    gates: dict[str, dict[str, Any]] = {}

    target_attempts = int(traffic["scheduled_attempts"])
    completed = int(traffic["completed_attempts"])
    eligible_attempts = int(traffic.get("eligible_attempts", completed))
    gates["all_attempts_completed"] = _gate(
        "passed" if completed == target_attempts else "failed",
        actual=completed,
        required=target_attempts,
        reason="Every scheduled client attempt must finish and be classified",
    )

    if eligible_attempts:
        deviations: dict[str, float] = {}
        operation_counts = traffic["operation_counts"]
        for operation in profile["operations"]:
            operation_id = operation["id"]
            actual_weight = (
                100
                * int(operation_counts.get(operation_id, 0))
                / eligible_attempts
            )
            deviations[operation_id] = round(
                actual_weight - float(operation["weight_percent"]), 4
            )
        maximum_deviation = max((abs(value) for value in deviations.values()), default=0)
        allowed = float(variance["operation_weight_percentage_points"])
        gates["operation_weight_conformance"] = _gate(
            "passed" if maximum_deviation <= allowed else "failed",
            actual={
                "maximum_absolute_percentage_point_deviation": maximum_deviation,
                "deviations": deviations,
            },
            required={"maximum_percentage_points": allowed},
            reason="Observed operation weights must match the approved manifest",
        )
    else:
        gates["operation_weight_conformance"] = _gate(
            "not_applicable",
            actual=0,
            required="at least one attempt",
            reason="Dry run has no traffic samples",
        )

    target_rps = float(traffic["target_rps"])
    actual_rps = float(traffic["actual_rps"])
    if target_rps:
        rps_deviation = abs(actual_rps - target_rps) / target_rps * 100
        allowed_rps = float(variance["aggregate_rps_percent"])
        gates["aggregate_rps_conformance"] = _gate(
            "passed" if rps_deviation <= allowed_rps else "failed",
            actual={"rps": actual_rps, "deviation_percent": round(rps_deviation, 4)},
            required={"target_rps": target_rps, "maximum_deviation_percent": allowed_rps},
            reason="Aggregate completed request rate must remain within manifest variance",
        )
    else:
        gates["aggregate_rps_conformance"] = _gate(
            "not_applicable",
            actual=actual_rps,
            required=0,
            reason="Dry run has no target request rate",
        )

    target_clients = int(traffic["target_virtual_users"])
    actual_clients = int(traffic["active_clients_peak"])
    gates["virtual_client_conformance"] = _gate(
        "passed" if actual_clients == target_clients else "failed",
        actual=actual_clients,
        required=target_clients,
        reason="Active virtual clients are distinct from connections and in-flight requests",
    )

    unexpected_statuses = 0
    unexpected_5xx = 0
    expected_conflicts = 0
    throttles = 0
    for operation in profile["operations"]:
        operation_id = operation["id"]
        observed = operations.get(operation_id, {"statuses": {}})["statuses"]
        allowed_statuses = {int(value) for value in operation["expected_statuses"]}
        for status_text, count in observed.items():
            status = int(status_text)
            if status == 409:
                expected_conflicts += int(count)
            elif status == 429:
                throttles += int(count)
            if status not in allowed_statuses:
                unexpected_statuses += int(count)
                if 500 <= status <= 599:
                    unexpected_5xx += int(count)
    denominator = max(eligible_attempts, 1)
    total_unexpected_percent = unexpected_statuses / denominator * 100
    unexpected_5xx_percent = unexpected_5xx / denominator * 100
    gates.update(
        [
            _maximum_gate(
                "unexpected_error_percent",
                total_unexpected_percent,
                float(slos["total_unexpected_error_percent_maximum"]),
            ),
            _maximum_gate(
                "unexpected_5xx_percent",
                unexpected_5xx_percent,
                float(slos["unexpected_5xx_percent_maximum"]),
            ),
        ]
    )
    gates["expected_conflicts_reported_separately"] = _gate(
        "passed",
        actual={"expected_409": expected_conflicts, "deliberate_429": throttles},
        required="separate counters",
        reason="Expected conflicts and deliberate throttles are not hidden as success",
    )

    success_coverage_failures: dict[str, Any] = {}
    for operation in profile["operations"]:
        if operation["classification"] == "external_wait":
            continue
        observed = operations.get(str(operation["id"]), {"statuses": {}})
        successful = sum(
            int(count)
            for status_text, count in observed["statuses"].items()
            if 200 <= int(status_text) < 300
        )
        if int(observed.get("attempts", 0)) > 0 and successful == 0:
            success_coverage_failures[str(operation["id"])] = dict(
                observed["statuses"]
            )
    sampling_only = traffic.get("phase") == "small"
    gates["public_contract_success_coverage"] = _gate(
        (
            "not_applicable"
            if sampling_only
            else "failed"
            if success_coverage_failures
            else "passed"
        ),
        actual=success_coverage_failures or "every sampled operation reached 2xx",
        required="Every non-provider operation exercises a successful public contract",
        reason=(
            "Small traffic samples status paths without certifying per-operation success"
            if sampling_only
            else "Validation/conflict responses cannot substitute for normal API work"
        ),
    )

    expected_classes: set[str] = set()
    for operation in profile["operations"]:
        operation_id = str(operation["id"])
        if operation_id == "rest_schedule_preview":
            expected_classes.add("schedule_preview")
        elif operation_id == "rest_schedule_apply":
            expected_classes.add("schedule_apply")
        elif operation_id in {"rest_iteration_tasks", "rest_iteration_gantt"}:
            expected_classes.add("hot_read")
        elif operation["classification"] == "read":
            expected_classes.add("core_read")
        elif operation["classification"] == "write":
            expected_classes.add("core_write")
        else:
            expected_classes.add(str(operation["classification"]))

    latency_contracts = {
        "core_read": slos["core_read_latency_ms"],
        "core_write": slos["core_write_latency_ms"],
        "hot_read": slos["hot_task_tree_gantt_latency_ms"],
        "schedule_preview": slos["schedule_preview_latency_ms"],
        "schedule_apply": slos["schedule_apply_latency_ms"],
    }
    for class_name, thresholds in latency_contracts.items():
        observed = classes.get(class_name)
        if not observed or not observed["attempts"]:
            gates[f"{class_name}_latency"] = _gate(
                (
                    "missing"
                    if target_attempts and class_name in expected_classes
                    else "not_applicable"
                ),
                actual=None,
                required=thresholds,
                reason=f"No {class_name} latency samples were recorded",
            )
            continue
        failures = {
            quantile: {
                "actual": observed["latency_ms"][quantile],
                "maximum": maximum,
            }
            for quantile, maximum in thresholds.items()
            if observed["latency_ms"][quantile] > maximum
        }
        gates[f"{class_name}_latency"] = _gate(
            "not_applicable" if sampling_only else "failed" if failures else "passed",
            actual=observed["latency_ms"],
            required=thresholds,
            reason=(
                "Small profile records latency but does not certify an SLO"
                if sampling_only
                else f"Latency thresholds exceeded: {failures}"
                if failures
                else "Recorded latency percentiles satisfy the capacity contract"
            ),
        )
    return gates


def evaluate_external_gates(
    external_metrics: Mapping[str, Any],
    integrity: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    """Evaluate every non-client SLO from explicit deployment evidence.

    Missing input is never interpreted as zero.  This lets small profiles expose
    the complete gate inventory while the pre-cutover aggregator can reject a
    candidate that omitted an application, PostgreSQL, gateway, worker, storage,
    backup, or fault measurement.
    """

    slos = capacity_contract()["slos"]
    gates: dict[str, dict[str, Any]] = {}

    def maximum(
        gate_name: str,
        metric_name: str,
        limit: float,
    ) -> None:
        value = external_metrics.get(metric_name)
        if not isinstance(value, (int, float)):
            gates[gate_name] = _gate(
                "missing",
                actual=None,
                required={"metric": metric_name, "maximum": limit},
                reason=f"External metric {metric_name} is required",
            )
            return
        gates[gate_name] = _maximum_gate(gate_name, float(value), limit)[1]

    def minimum(
        gate_name: str,
        metric_name: str,
        limit: float,
    ) -> None:
        value = external_metrics.get(metric_name)
        if not isinstance(value, (int, float)):
            gates[gate_name] = _gate(
                "missing",
                actual=None,
                required={"metric": metric_name, "minimum": limit},
                reason=f"External metric {metric_name} is required",
            )
            return
        gates[gate_name] = _minimum_gate(gate_name, float(value), limit)[1]

    maximum(
        "pool_checkout_p95",
        "pool_checkout_p95_ms",
        float(slos["pool_checkout_ms"]["p95"]),
    )
    maximum(
        "pool_checkout_p99",
        "pool_checkout_p99_ms",
        float(slos["pool_checkout_ms"]["p99"]),
    )
    maximum(
        "pool_timeouts",
        "pool_timeouts",
        float(slos["pool_checkout_ms"]["timeouts"]),
    )
    maximum(
        "steady_database_connections",
        "steady_database_connections_percent",
        float(slos["steady_database_connections_percent_maximum"]),
    )
    maximum(
        "database_cpu_steady",
        "database_cpu_steady_percent",
        float(slos["database_cpu_percent"]["steady_maximum"]),
    )
    maximum(
        "database_cpu_burst",
        "database_cpu_burst_percent",
        float(slos["database_cpu_percent"]["burst_maximum"]),
    )
    maximum(
        "ordinary_lock_wait_p99",
        "ordinary_lock_wait_p99_ms",
        float(slos["ordinary_lock_wait_ms"]["p99"]),
    )
    maximum(
        "deadlocks",
        "deadlocks",
        float(slos["ordinary_lock_wait_ms"]["deadlocks"]),
    )
    maximum(
        "web_rss",
        "web_rss_mib_per_replica_maximum",
        float(slos["web_rss_mib_per_replica_maximum"]),
    )
    maximum(
        "worker_rss",
        "worker_rss_mib_per_replica_maximum",
        float(slos["worker_rss_mib_per_replica_maximum"]),
    )
    maximum(
        "soak_memory_growth",
        "soak_memory_growth_hour_2_to_8_percent",
        float(slos["soak_memory_growth_hour_2_to_8_percent_maximum"]),
    )
    maximum(
        "delivery_oldest_ready_steady",
        "delivery_oldest_ready_steady_seconds",
        float(slos["delivery_oldest_ready_seconds"]["steady_maximum"]),
    )
    maximum(
        "delivery_oldest_ready_burst",
        "delivery_oldest_ready_burst_seconds",
        float(slos["delivery_oldest_ready_seconds"]["burst_maximum"]),
    )
    maximum(
        "delivery_ready_backlog",
        "delivery_ready_backlog_maximum",
        float(slos["delivery_ready_backlog_maximum"]),
    )
    maximum(
        "delivery_drain",
        "delivery_drain_to_steady_seconds",
        float(slos["delivery_drain_to_steady_seconds_maximum"]),
    )
    maximum(
        "database_unready_detection",
        "database_unready_detection_seconds",
        float(slos["database_unready_detection_seconds_maximum"]),
    )
    maximum(
        "database_failover",
        "database_failover_seconds",
        float(slos["database_failover_seconds_maximum"]),
    )
    maximum(
        "database_failover_attempt_failures",
        "database_failover_unexpected_attempt_failures_percent",
        float(slos["database_failover_unexpected_attempt_failures_percent_maximum"]),
    )
    maximum(
        "replica_lag_steady",
        "replica_lag_steady_seconds",
        float(slos["replica_lag_seconds"]["steady_maximum"]),
    )
    maximum(
        "replica_lag_burst",
        "replica_lag_burst_seconds",
        float(slos["replica_lag_seconds"]["burst_maximum"]),
    )
    maximum(
        "wal_archive_rpo_lag",
        "wal_archive_rpo_lag_seconds",
        float(slos["wal_archive_rpo_lag_seconds_maximum"]),
    )
    maximum(
        "storage_used_steady",
        "storage_used_steady_percent",
        float(slos["storage_used_percent"]["steady_maximum"]),
    )
    maximum(
        "storage_used_burst",
        "storage_used_burst_percent",
        float(slos["storage_used_percent"]["burst_maximum"]),
    )
    maximum(
        "storage_latency_steady",
        "storage_latency_steady_p95_ms",
        float(slos["storage_latency_ms"]["steady_p95_maximum"]),
    )
    maximum(
        "storage_latency_burst",
        "storage_latency_burst_p95_ms",
        float(slos["storage_latency_ms"]["burst_p95_maximum"]),
    )
    minimum(
        "capacity_horizon",
        "capacity_horizon_months",
        float(slos["capacity_horizon_months_minimum"]),
    )
    maximum(
        "dead_tuple_or_bloat",
        "dead_tuple_or_bloat_percent_maximum",
        float(slos["dead_tuple_or_bloat_percent_maximum"]),
    )
    maximum(
        "statistics_refresh",
        "statistics_refresh_after_bulk_load_seconds",
        float(slos["statistics_refresh_after_bulk_load_seconds_maximum"]),
    )
    maximum(
        "backup_rpo",
        "backup_rpo_seconds",
        float(slos["backup_rpo_seconds_maximum"]),
    )
    maximum(
        "restore_rto",
        "restore_rto_seconds",
        float(slos["restore_rto_seconds_maximum"]),
    )
    maximum(
        "backend_replica_reroute",
        "backend_replica_reroute_seconds",
        float(slos["backend_replica_reroute_seconds_maximum"]),
    )
    maximum(
        "backend_replica_attempt_failures",
        "backend_replica_unexpected_attempt_failures_percent",
        float(slos["total_unexpected_error_percent_maximum"]),
    )

    integrity_value = integrity.get("failures")
    if not isinstance(integrity_value, int):
        gates["domain_integrity"] = _gate(
            "missing",
            actual=None,
            required={"failures": slos["integrity_failures"]},
            reason="Invariant query bundle did not report an integer failure count",
        )
    else:
        gates["domain_integrity"] = _maximum_gate(
            "domain_integrity",
            float(integrity_value),
            float(slos["integrity_failures"]),
        )[1]
    return gates


def evaluate_workload_gates(
    document: Mapping[str, Any],
) -> dict[str, dict[str, Any]]:
    """Reject a live run that drifted from non-endpoint workload semantics."""
    contract = capacity_contract()
    evidence = document.get("workload_evidence", {})
    traffic = document["traffic"]
    profile = traffic_profile(contract, str(traffic["profile_id"]))
    allowed = float(
        contract["traffic"]["allowed_variance"][
            "operation_weight_percentage_points"
        ]
    )
    gates: dict[str, dict[str, Any]] = {}

    def distribution_gate(
        name: str,
        actual: Mapping[str, Any],
        expected: Mapping[str, Any],
        sample_count: int,
    ) -> None:
        deviations = {
            key: round(float(actual.get(key, 0)) - float(value), 4)
            for key, value in expected.items()
        }
        maximum = max((abs(value) for value in deviations.values()), default=0)
        sample_tolerance = max(allowed, 50 / max(1, sample_count))
        gates[name] = _gate(
            "passed" if maximum <= sample_tolerance else "failed",
            actual={"percent": dict(actual), "deviations": deviations},
            required={
                "percent": dict(expected),
                "maximum_percentage_points": sample_tolerance,
            },
            reason="Observed distribution must match the approved workload contract",
        )

    distribution_gate(
        "entity_distribution_conformance",
        evidence.get("entity_distribution_percent", {}),
        contract["traffic"]["entity_distribution_percent"],
        int(traffic.get("eligible_attempts", traffic["completed_attempts"])),
    )
    has_browsers = any(item["transport"] == "REST" for item in profile["operations"])
    if has_browsers:
        distribution_gate(
            "session_state_conformance",
            evidence.get("session_state_percent", {}),
            contract["traffic"]["session_state_percent"],
            sum(
                int(value)
                for value in evidence.get("session_state_counts", {}).values()
            ),
        )
    else:
        gates["session_state_conformance"] = _gate(
            "not_applicable",
            actual={},
            required="browser clients",
            reason="This profile has no browser clients",
        )

    payload_failures: dict[str, Any] = {}
    payload_distribution_failures: dict[str, Any] = {}

    def payload_summary_failures(
        label: str,
        summary: Mapping[str, Any],
        envelope: Any,
    ) -> None:
        if not isinstance(envelope, list) or len(envelope) != 3:
            payload_failures[label] = {
                "actual": dict(summary),
                "declared": envelope,
            }
            return
        observed_points = (
            float(summary["p50"]),
            float(summary["p95"]),
            float(summary["max"]),
        )
        violations = {
            name: {"actual": actual, "maximum": float(maximum)}
            for name, actual, maximum in zip(
                ("p50", "p95", "max"),
                observed_points,
                envelope,
            )
            if actual > float(maximum)
        }
        if observed_points[-1] > float(envelope[-1]):
            payload_failures[label] = {
                "actual_max": observed_points[-1],
                "declared": envelope,
            }
        if violations:
            payload_distribution_failures[label] = violations

    for name, observed in evidence.get("request_payloads", {}).items():
        declared = contract["traffic"]["payload_profiles"].get(name, {})
        envelope = declared.get(
            "request_body_bytes_p50_p95_max",
            declared.get("request_body_bytes"),
        )
        payload_summary_failures(
            f"request:{name}",
            observed["bytes"],
            envelope,
        )
    for name, observed in evidence.get("response_payloads", {}).items():
        declared = contract["traffic"]["response_profiles"].get(name, {})
        envelope = declared.get("body_bytes_p50_p95_max")
        payload_summary_failures(
            f"response:{name}",
            observed["bytes"],
            envelope,
        )
    gates["payload_envelope_conformance"] = _gate(
        "failed" if payload_failures else "passed",
        actual=payload_failures or "all observed maxima within envelope",
        required="Every payload and response stays within its declared maximum",
        reason="Oversized payloads alter the certified workload shape",
    )
    sampling_only = traffic.get("phase") == "small"
    gates["payload_distribution_conformance"] = _gate(
        (
            "not_applicable"
            if sampling_only
            else "failed"
            if payload_distribution_failures
            else "passed"
        ),
        actual=payload_distribution_failures or evidence.get(
            "request_payloads", {}
        ),
        required="Observed p50, p95, and maximum body sizes stay within the manifest",
        reason=(
            "Small profile records body distributions but only enforces hard maxima"
            if sampling_only
            else "Body-size percentiles are bounded by the approved workload manifest"
        ),
    )

    cardinality_failures: dict[str, Any] = {}
    for name, observed in evidence.get("response_cardinalities", {}).items():
        declared = contract["traffic"]["response_profiles"].get(name, {})
        envelope = declared.get("cardinality_p50_p95_max")
        if not isinstance(envelope, list) or len(envelope) != 3:
            cardinality_failures[name] = {
                "actual": observed.get("items"),
                "declared": envelope,
            }
            continue
        summary = observed["items"]
        checks = (summary["p50"], summary["p95"], summary["max"])
        violations = {
            quantile: {"actual": actual, "maximum": maximum}
            for quantile, actual, maximum in zip(
                ("p50", "p95", "max"), checks, envelope
            )
            if float(actual) > float(maximum)
            and (not sampling_only or quantile == "max")
        }
        if violations:
            cardinality_failures[name] = violations
    gates["response_cardinality_conformance"] = _gate(
        "failed" if cardinality_failures else "passed",
        actual=cardinality_failures or evidence.get(
            "response_cardinalities", {}
        ),
        required="Response cardinality p50, p95, and maximum stay within the manifest",
        reason=(
            "Small profile enforces cardinality maxima; qualification phases also "
            "enforce p50 and p95 ceilings"
        ),
    )

    think = evidence.get("think_time_seconds", {})
    think_failures: dict[str, Any] = {}
    browser = think.get("browser")
    if evidence.get("session_state_counts"):
        if not browser:
            think_failures["browser"] = "missing intervals"
        elif (
            browser["p50"] < 1
            or browser["p50"] > 15
            or browser["p95"] > 15
            or browser["max"] > 30
        ):
            think_failures["browser"] = browser
    operations = profile["operations"]
    has_agents = any(item["transport"] == "MCP" for item in operations)
    agent = think.get("agent")
    if has_agents:
        if not agent:
            think_failures["agent"] = "missing intervals"
        elif (
            agent["p50"] < 0.75
            or agent["p50"] > 6.25
            or agent["p95"] > 30
            or agent["max"] > 37.5
        ):
            think_failures["agent"] = agent
    gates["think_time_conformance"] = _gate(
        "failed" if think_failures else "passed",
        actual=think_failures or think,
        required={
            "browser": {
                "p50_minimum": 1,
                "p50_maximum": 15,
                "p95_maximum": 15,
                "maximum": 30,
            },
            "agent": {
                "p50_minimum": 0.75,
                "p50_maximum": 6.25,
                "p95_maximum": 30,
                "maximum": 37.5,
            },
        },
        reason="Per-client intervals bind active clients independently of RPS",
    )

    mechanics = evidence.get("client_mechanics", {})
    booleans_pass = all(
        mechanics.get(name) is True
        for name in ("real_cookie_tokens", "optimistic_versions", "idempotency_keys")
    )
    guidance_responses = int(mechanics.get("poll_guidance_responses", 0))
    guidance_parsed = int(mechanics.get("poll_guidance_parsed", 0))
    guidance_respected = int(mechanics.get("poll_guidance_respected", 0))
    guidance_outstanding = int(mechanics.get("poll_guidance_outstanding", 0))
    guidance_pass = not has_agents or (
        guidance_responses > 0
        and guidance_responses == guidance_parsed
        and guidance_parsed == guidance_respected + guidance_outstanding
    )
    gates["stateful_client_contracts"] = _gate(
        "passed" if booleans_pass and guidance_pass else "failed",
        actual=dict(mechanics),
        required={
            "real_cookie_tokens": True,
            "optimistic_versions": True,
            "idempotency_keys": True,
            "all_successful_poll_guidance_parsed_and_respected": True,
        },
        reason="The harness must use normal stateful client contracts",
    )

    declared_retry = profile.get("retry_policy")
    observed_retry = mechanics.get("retry_policy")
    completed = int(traffic["completed_attempts"])
    eligible = int(traffic.get("eligible_attempts", completed))
    retry_attempts = int(mechanics.get("retry_attempts", 0))
    retry_exhausted = int(mechanics.get("retry_exhausted", 0))
    attempts_peak = int(
        mechanics.get("physical_attempts_per_logical_peak", 0)
    )
    if declared_retry is not None:
        retry_pass = (
            observed_retry == declared_retry
            and eligible - completed == retry_attempts
            and attempts_peak <= int(declared_retry["maximum_attempts"])
            and 0 <= retry_exhausted <= completed
        )
        gates["bounded_retry_contracts"] = _gate(
            "passed" if retry_pass else "failed",
            actual={
                "policy": observed_retry,
                "retry_attempts": retry_attempts,
                "retry_exhausted": retry_exhausted,
                "physical_attempts_per_logical_peak": attempts_peak,
                "eligible_attempts": eligible,
                "completed_logical_attempts": completed,
            },
            required=dict(declared_retry),
            reason="Connection-surge retries must remain bounded and observable",
        )
    else:
        no_retries = (
            observed_retry is None
            and retry_attempts == 0
            and retry_exhausted == 0
            and eligible == completed
            and attempts_peak <= 1
        )
        gates["bounded_retry_contracts"] = _gate(
            "passed" if no_retries else "failed",
            actual={
                "policy": observed_retry,
                "retry_attempts": retry_attempts,
                "retry_exhausted": retry_exhausted,
                "physical_attempts_per_logical_peak": attempts_peak,
            },
            required="no implicit transport retries",
            reason="Profiles without a retry policy must issue one physical attempt",
        )

    ramp = evidence.get("connection_ramp_seconds")
    if str(profile["id"]) == "connection_surge_v1":
        ramp_pass = isinstance(ramp, (int, float)) and 114 <= float(ramp) <= 150
        gates["connection_surge_ramp"] = _gate(
            "passed" if ramp_pass else "failed",
            actual=ramp,
            required={"target_seconds": 120, "minimum": 114, "maximum": 150},
            reason="Connection-surge clients must ramp before the hold interval",
        )
    else:
        gates["connection_surge_ramp"] = _gate(
            "not_applicable",
            actual=ramp,
            required="connection_surge_v1",
            reason="This is not the connection-surge profile",
        )

    write_ids = {
        str(item["id"])
        for item in operations
        if item["classification"] == "write"
    }
    mutation_attempts = sum(
        int(document["operations"][name]["attempts"])
        for name in write_ids
    )
    conflicts = sum(
        int(document["operations"][name]["statuses"].get("409", 0))
        for name in write_ids
    )
    if mutation_attempts:
        conflict_percent = conflicts / mutation_attempts * 100
        expected_conflict = float(
            contract["traffic"]["optimistic_conflict_percent_of_mutations"]
        )
        conflict_deviation = abs(conflict_percent - expected_conflict)
        conflict_tolerance = max(
            allowed,
            150 / math.sqrt(mutation_attempts),
        )
        gates["optimistic_conflict_conformance"] = _gate(
            "passed" if conflict_deviation <= conflict_tolerance else "failed",
            actual={
                "conflicts": conflicts,
                "mutations": mutation_attempts,
                "percent": round(conflict_percent, 4),
            },
            required={
                "percent": expected_conflict,
                "maximum_percentage_point_deviation": conflict_tolerance,
            },
            reason="Expected optimistic conflicts remain a declared workload input",
        )
    else:
        gates["optimistic_conflict_conformance"] = _gate(
            "not_applicable",
            actual=0,
            required="write operations",
            reason="This profile has no mutations",
        )
    return gates


def result_status(
    gates: Mapping[str, Mapping[str, Any]], *, qualification_candidate: bool
) -> str:
    del qualification_candidate
    statuses = {str(gate.get("status")) for gate in gates.values()}
    if "failed" in statuses:
        return "failed"
    if "missing" in statuses:
        return "incomplete"
    return "passed"


def write_result(path: Path, payload: Mapping[str, Any]) -> dict[str, Any]:
    document = atomic_write_json(path, payload)
    validate_result(document)
    return document
