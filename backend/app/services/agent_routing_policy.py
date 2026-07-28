"""Pure, provider-neutral policy for model-aware agent routing.

The module freezes the vocabulary and decision rules shared by persistence,
REST, MCP, and future candidate ranking.  It does not grant actor authority,
infer precise skills from prose, or select a provider/model by name.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import IntEnum, StrEnum
import json
import math
from types import MappingProxyType
from typing import Any, Iterable, Mapping


ROUTING_POLICY_VERSION = "model-aware-routing-v1"
MAX_ROUTING_PACKET_BYTES = 32_768
MAX_ROUTING_SNAPSHOT_BYTES = MAX_ROUTING_PACKET_BYTES
MIN_ROUTING_ASSESSMENT_CONFIDENCE = 0.60
ROUTING_PREVIEW_TTL_SECONDS = 300
MAX_ROUTING_ELIGIBLE_CANDIDATES = 25
MAX_ROUTING_EXCLUSIONS = 50
# Keep the shorter name as the shared service/schema boundary.
MAX_ROUTING_CANDIDATES = MAX_ROUTING_ELIGIBLE_CANDIDATES
MODEL_FAILURE_CATEGORIES = frozenset(
    {
        "reasoning_insufficiency",
        "context_insufficiency",
        "modality_insufficiency",
        "tool_insufficiency",
    }
)
NON_MODEL_FAILURE_CATEGORY = "non_model_or_unclassified"
ROUTING_DECISION_AUTHORITY = "agent-routing-service-v1"
ROUTING_LINEAGE_AUTHORITY = "agent-work-service-v1"
SERVER_OWNED_ROUTING_SNAPSHOT_SCHEMAS = frozenset(
    {
        "routing-decision-snapshot-v1",
        "routing-lineage-snapshot-v1",
    }
)
ROUTING_DECISION_LINEAGE_FIELDS = (
    "schema_version",
    "authority",
    "policy_version",
    "task_id",
    "task_version",
    "assessment_id",
    "assessment_task_version",
    "assessment_band",
    "assessment_confidence",
    "assessment_reason_codes",
    "purpose",
    "actor_id",
    "actor_revision",
    "actor_queue_revision",
    "profile_id",
    "profile_revision",
    "capacity_owner_id",
    "capacity_owner_profile_id",
    "model_binding_id",
    "model_binding_revision",
    "model_catalog_id",
    "model_catalog_key",
    "model_catalog_revision",
    "configured_model_alias",
    "selected_reasoning_tier",
    "selected_context_tier",
    "review_mode",
    "reviewer_profile_id",
    "routing_preview_id",
    "routing_preview_digest",
    "input_digest",
    "preview_generated_at",
    "preview_expires_at",
    "selected_rank",
    "adequacy_class",
    "selection_reason_codes",
    "eligible_candidate_summaries",
    "exclusion_summaries",
    "eligible_candidates_omitted",
    "exclusions_omitted",
    "confidence",
    "trust_lineage",
    "source_assignment_id",
    "snapshot_sha256",
)


def normalize_model_failure_category(value: Any) -> str:
    """Project untrusted failure evidence into the closed escalation taxonomy."""

    normalized = str(value or "").strip().lower().replace("-", "_")
    if normalized in MODEL_FAILURE_CATEGORIES:
        return normalized
    return NON_MODEL_FAILURE_CATEGORY


class ReasoningTier(IntEnum):
    """Closed provider-neutral reasoning capability tiers."""

    ROUTINE = 1
    STANDARD = 2
    ADVANCED = 3


class ContextTier(StrEnum):
    """Closed context-capacity tiers ordered by increasing capacity."""

    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


class CostTier(StrEnum):
    """Closed relative cost tiers; exact prices are deliberately excluded."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class LatencyTier(StrEnum):
    """Closed relative latency tiers."""

    FAST = "fast"
    BALANCED = "balanced"
    SLOW = "slow"


class DifficultyAxis(StrEnum):
    """The five governed task-difficulty axes."""

    REASONING = "reasoning"
    AMBIGUITY = "ambiguity"
    CONTEXT_BREADTH = "context_breadth"
    RISK = "risk"
    VERIFICATION_BURDEN = "verification_burden"


class DifficultyBand(StrEnum):
    """Derived task-difficulty bands."""

    ROUTINE = "routine"
    STANDARD = "standard"
    ADVANCED = "advanced"


class ReviewMode(StrEnum):
    """Closed review modes ordered by increasing independence requirements."""

    NONE = "none"
    STANDARD = "standard"
    INDEPENDENT = "independent"
    SPECIALIST_INDEPENDENT = "specialist-independent"


class AssessmentReasonCode(StrEnum):
    """Governed reasons that may raise the derived band or review floor."""

    NOVEL_ARCHITECTURE = "novel-architecture"
    MATERIAL_AMBIGUITY = "material-ambiguity"
    BROAD_CONTEXT = "broad-context"
    SECURITY = "security"
    AUTHORIZATION = "authorization"
    MIGRATION = "migration"
    DATA_INTEGRITY = "data-integrity"
    CONCURRENCY = "concurrency"
    PRODUCTION = "production"
    IRREVERSIBLE_CHANGE = "irreversible-change"
    INDEPENDENT_VERIFICATION = "independent-verification"
    SPECIALIST_VERIFICATION = "specialist-verification"


class AssignmentIntent(StrEnum):
    """Normalized assignment intents derived from purpose and queue class."""

    EXECUTION = "execution"
    VERIFICATION = "verification"
    REWORK = "rework"
    RECOVERY = "recovery"


class RoutingBlockerCode(StrEnum):
    """Stable hard blockers shared by preview and assignment enforcement."""

    ASSIGNMENT_PURPOSE_QUEUE_CLASS_INCOMPATIBLE = (
        "assignment_purpose_queue_class_incompatible"
    )
    ASSESSMENT_MISSING = "assessment_missing"
    ASSESSMENT_STALE = "assessment_stale"
    ASSESSMENT_POLICY_MISMATCH = "assessment_policy_mismatch"
    ASSESSMENT_LOW_CONFIDENCE = "assessment_low_confidence"
    TASK_DEFINITION_NOT_READY = "task_definition_not_ready"
    TASK_STATUS_INCOMPATIBLE = "task_status_incompatible"
    TASK_DEFERRED = "task_deferred"
    TASK_COMPOSITE = "task_composite"
    TASK_DEPENDENCY_UNRESOLVED = "task_dependency_unresolved"
    ACTOR_DISABLED = "actor_disabled"
    ACTOR_ROLE_INCOMPATIBLE = "actor_role_incompatible"
    ACTOR_SCOPE_MISSING = "actor_scope_missing"
    ACTOR_POLICY_INCOMPATIBLE = "actor_policy_incompatible"
    ACTOR_TOPOLOGY_INCOMPATIBLE = "actor_topology_incompatible"
    ACTOR_PROFILE_MISSING = "actor_profile_missing"
    CAPACITY_OWNER_MISSING = "capacity_owner_missing"
    CAPACITY_OWNER_PROFILE_MISSING = "capacity_owner_profile_missing"
    ACTOR_CAPACITY_PROFILE_MISMATCH = "actor_capacity_profile_mismatch"
    PROFILE_KIND_HUMAN = "profile_kind_human"
    PROFILE_KIND_UNSUPPORTED = "profile_kind_unsupported"
    PROFILE_AUTOMATION_DISABLED = "profile_automation_disabled"
    PROFILE_ASSIGNMENT_MODE_MISSING = "profile_assignment_mode_missing"
    REQUIRED_SKILL_MISSING = "required_skill_missing"
    REQUIRED_SKILL_LEVEL_INSUFFICIENT = "required_skill_level_insufficient"
    REQUIRED_SKILL_BLOCKING_WEAKNESS = "required_skill_blocking_weakness"
    MODEL_BINDING_MISSING = "model_binding_missing"
    MODEL_BINDING_DISABLED = "model_binding_disabled"
    MODEL_BINDING_STALE = "model_binding_stale"
    MODEL_CATALOG_MISSING = "model_catalog_missing"
    MODEL_CATALOG_DISABLED = "model_catalog_disabled"
    MODEL_REASONING_TIER_INSUFFICIENT = "model_reasoning_tier_insufficient"
    MODEL_CONTEXT_TIER_INSUFFICIENT = "model_context_tier_insufficient"
    MODEL_MODALITY_MISSING = "model_modality_missing"
    MODEL_TOOL_MISSING = "model_tool_missing"
    MODEL_DATA_POLICY_MISSING = "model_data_policy_missing"
    CAPACITY_UNAVAILABLE = "capacity_unavailable"
    WORKLOAD_LIMIT_EXCEEDED = "workload_limit_exceeded"
    VACATION_CONFLICT = "vacation_conflict"
    SCHEDULE_MISSING = "schedule_missing"
    SCHEDULE_CONFLICT = "schedule_conflict"
    QUEUE_LIMIT_EXCEEDED = "queue_limit_exceeded"
    CURRENT_WORK_CONFLICT = "current_work_conflict"
    REVIEWER_PROFILE_MISSING = "reviewer_profile_missing"
    REVIEWER_PROFILE_MISMATCH = "reviewer_profile_mismatch"
    VERIFICATION_ACTOR_NOT_INDEPENDENT = "verification_actor_not_independent"
    VERIFICATION_PROFILE_NOT_INDEPENDENT = "verification_profile_not_independent"
    VERIFICATION_INDEPENDENCE_UNVERIFIABLE = (
        "verification_independence_unverifiable"
    )
    VERIFICATION_SPECIALIST_SKILL_MISSING = (
        "verification_specialist_skill_missing"
    )
    PREVIEW_NOT_FOUND = "preview_not_found"
    PREVIEW_STALE = "preview_stale"
    PREVIEW_EXPIRED = "preview_expired"
    PREVIEW_DIGEST_MISMATCH = "preview_digest_mismatch"
    NO_ELIGIBLE_CANDIDATE = "no_eligible_candidate"


CONTEXT_TIER_ORDER = MappingProxyType(
    {
        ContextTier.SMALL.value: 1,
        ContextTier.MEDIUM.value: 2,
        ContextTier.LARGE.value: 3,
    }
)
COST_TIER_ORDER = MappingProxyType(
    {
        CostTier.LOW.value: 1,
        CostTier.MEDIUM.value: 2,
        CostTier.HIGH.value: 3,
    }
)
LATENCY_TIER_ORDER = MappingProxyType(
    {
        LatencyTier.FAST.value: 1,
        LatencyTier.BALANCED.value: 2,
        LatencyTier.SLOW.value: 3,
    }
)
DIFFICULTY_BAND_ORDER = MappingProxyType(
    {
        DifficultyBand.ROUTINE.value: 1,
        DifficultyBand.STANDARD.value: 2,
        DifficultyBand.ADVANCED.value: 3,
    }
)
REVIEW_MODE_ORDER = MappingProxyType(
    {
        ReviewMode.NONE.value: 0,
        ReviewMode.STANDARD.value: 1,
        ReviewMode.INDEPENDENT.value: 2,
        ReviewMode.SPECIALIST_INDEPENDENT.value: 3,
    }
)


ROUTING_SKILL_DEFINITIONS: tuple[dict[str, Any], ...] = (
    {
        "skill_key": "pm-control",
        "skill_name": "PM Control",
        "category": "pm",
        "keywords": ["commitment", "priority", "scope", "decision"],
    },
    {
        "skill_key": "planning-intake",
        "skill_name": "Planning And Intake",
        "category": "planning",
        "keywords": ["triage", "decompose", "acceptance", "backlog"],
    },
    {
        "skill_key": "iteration-capacity",
        "skill_name": "Iteration Capacity",
        "category": "pm",
        "keywords": ["capacity", "workload", "vacation", "utilization"],
    },
    {
        "skill_key": "schedule-control",
        "skill_name": "Schedule Control",
        "category": "pm",
        "keywords": ["schedule", "gantt", "dependency", "deadline"],
    },
    {
        "skill_key": "delivery-forecast",
        "skill_name": "Delivery Forecast",
        "category": "pm",
        "keywords": ["forecast", "overdue", "risk", "target date"],
    },
    {
        "skill_key": "risk-control",
        "skill_name": "Risk Control",
        "category": "pm",
        "keywords": ["risk", "mitigation", "blocker", "escalation"],
    },
    {
        "skill_key": "status-reporting",
        "skill_name": "Status Reporting",
        "category": "reporting",
        "keywords": ["health", "progress", "decision", "next steps"],
    },
    {
        "skill_key": "agent-routing",
        "skill_name": "Agent Routing",
        "category": "agent",
        "keywords": ["route", "assignment", "capability", "reviewer"],
    },
    {
        "skill_key": "backend-python",
        "skill_name": "Python Backend",
        "category": "engineering",
        "keywords": ["python", "fastapi", "sqlalchemy", "alembic"],
    },
    {
        "skill_key": "backend-go",
        "skill_name": "Go Backend",
        "category": "engineering",
        "keywords": ["go", "service", "concurrency", "api"],
    },
    {
        "skill_key": "backend-rust",
        "skill_name": "Rust Backend",
        "category": "engineering",
        "keywords": ["rust", "systems", "safety", "api"],
    },
    {
        "skill_key": "frontend-react",
        "skill_name": "React Frontend",
        "category": "engineering",
        "keywords": ["react", "typescript", "ui", "state"],
    },
    {
        "skill_key": "quality-verification",
        "skill_name": "Quality Verification",
        "category": "quality",
        "keywords": ["test", "verify", "regression", "evidence"],
    },
    {
        "skill_key": "documentation",
        "skill_name": "Documentation",
        "category": "documentation",
        "keywords": ["docs", "wiki", "guide", "runbook"],
    },
    {
        "skill_key": "operations",
        "skill_name": "Release And Operations",
        "category": "operations",
        "keywords": ["release", "runtime", "deploy", "rollback"],
    },
    {
        "skill_key": "design",
        "skill_name": "UX And UI Design",
        "category": "design",
        "keywords": ["ux", "ui", "prototype", "handoff"],
    },
    {
        "skill_key": "security-review",
        "skill_name": "Security Review",
        "category": "security",
        "keywords": ["security", "permission", "secret", "threat"],
    },
    {
        "skill_key": "data-integrity-review",
        "skill_name": "Data Integrity Review",
        "category": "quality",
        "keywords": ["migration", "transaction", "consistency", "concurrency"],
    },
    {
        "skill_key": "agent-discovery-triage",
        "skill_name": "Agent Discovery Triage",
        "category": "planning",
        "keywords": ["discovery", "out of scope", "follow-up", "triage"],
    },
    {
        "skill_key": "mcp-agent-api",
        "skill_name": "MCP Agent API",
        "category": "agent",
        "keywords": ["mcp", "rest", "claim", "run"],
    },
    {
        "skill_key": "human-decision-authority",
        "skill_name": "Human Decision Authority",
        "category": "governance",
        "keywords": ["stakeholder", "approval", "commitment", "production access"],
    },
)
ROUTING_SKILL_KEYS = frozenset(
    str(definition["skill_key"]) for definition in ROUTING_SKILL_DEFINITIONS
)

# These mappings narrow a coarse readiness label to explicit skill choices.
# They never select a skill automatically and never prove that a profile has it.
CAPABILITY_LABEL_SKILL_KEYS = MappingProxyType(
    {
        "cap:code": frozenset(
            {
                "backend-python",
                "backend-go",
                "backend-rust",
                "frontend-react",
                "mcp-agent-api",
            }
        ),
        "cap:test": frozenset(
            {
                "quality-verification",
                "data-integrity-review",
                "security-review",
            }
        ),
        "cap:docs": frozenset({"documentation", "status-reporting"}),
        "cap:research": frozenset(
            {"planning-intake", "agent-discovery-triage"}
        ),
    }
)
if not all(
    skill_keys <= ROUTING_SKILL_KEYS
    for skill_keys in CAPABILITY_LABEL_SKILL_KEYS.values()
):
    raise RuntimeError("Capability labels reference unknown routing skill keys")


@dataclass(frozen=True)
class ReasonCodeRule:
    """Minimum band/review requirements attached to one governed reason."""

    minimum_band: str
    minimum_review_mode: str


REASON_CODE_RULES = MappingProxyType(
    {
        AssessmentReasonCode.NOVEL_ARCHITECTURE.value: ReasonCodeRule(
            DifficultyBand.ADVANCED.value,
            ReviewMode.STANDARD.value,
        ),
        AssessmentReasonCode.MATERIAL_AMBIGUITY.value: ReasonCodeRule(
            DifficultyBand.ADVANCED.value,
            ReviewMode.STANDARD.value,
        ),
        AssessmentReasonCode.BROAD_CONTEXT.value: ReasonCodeRule(
            DifficultyBand.ADVANCED.value,
            ReviewMode.STANDARD.value,
        ),
        AssessmentReasonCode.SECURITY.value: ReasonCodeRule(
            DifficultyBand.ADVANCED.value,
            ReviewMode.INDEPENDENT.value,
        ),
        AssessmentReasonCode.AUTHORIZATION.value: ReasonCodeRule(
            DifficultyBand.ADVANCED.value,
            ReviewMode.INDEPENDENT.value,
        ),
        AssessmentReasonCode.MIGRATION.value: ReasonCodeRule(
            DifficultyBand.ADVANCED.value,
            ReviewMode.INDEPENDENT.value,
        ),
        AssessmentReasonCode.DATA_INTEGRITY.value: ReasonCodeRule(
            DifficultyBand.ADVANCED.value,
            ReviewMode.INDEPENDENT.value,
        ),
        AssessmentReasonCode.CONCURRENCY.value: ReasonCodeRule(
            DifficultyBand.ADVANCED.value,
            ReviewMode.INDEPENDENT.value,
        ),
        AssessmentReasonCode.PRODUCTION.value: ReasonCodeRule(
            DifficultyBand.ADVANCED.value,
            ReviewMode.INDEPENDENT.value,
        ),
        AssessmentReasonCode.IRREVERSIBLE_CHANGE.value: ReasonCodeRule(
            DifficultyBand.ADVANCED.value,
            ReviewMode.INDEPENDENT.value,
        ),
        AssessmentReasonCode.INDEPENDENT_VERIFICATION.value: ReasonCodeRule(
            DifficultyBand.ADVANCED.value,
            ReviewMode.INDEPENDENT.value,
        ),
        AssessmentReasonCode.SPECIALIST_VERIFICATION.value: ReasonCodeRule(
            DifficultyBand.ADVANCED.value,
            ReviewMode.SPECIALIST_INDEPENDENT.value,
        ),
    }
)
ASSESSMENT_REASON_CODES = frozenset(REASON_CODE_RULES)


VALID_ASSIGNMENT_INTENTS = MappingProxyType(
    {
        ("execution", "normal"): AssignmentIntent.EXECUTION.value,
        ("execution", "rework"): AssignmentIntent.REWORK.value,
        ("execution", "recovery"): AssignmentIntent.RECOVERY.value,
        ("verification", "normal"): AssignmentIntent.VERIFICATION.value,
    }
)


@dataclass(frozen=True)
class RoutingProfileEvidence:
    """Secret-free profile evidence used by compatibility decisions."""

    profile_id: int
    profile_kind: str
    automation_enabled: bool
    assignment_modes: frozenset[str] = field(default_factory=frozenset)
    skill_levels: Mapping[str, int] = field(default_factory=dict)
    weakness_keys: frozenset[str] = field(default_factory=frozenset)


@dataclass(frozen=True)
class RoutingEligibilityDecision:
    """Separated authority/compatibility evidence for one candidate."""

    authority_evaluated: bool = False
    compatibility_evaluated: bool = False
    authority_blocker_codes: tuple[str, ...] = ()
    compatibility_blocker_codes: tuple[str, ...] = ()
    missing_specialist_skills: tuple[str, ...] = ()

    @property
    def hard_blocker_codes(self) -> tuple[str, ...]:
        """Return the deterministic de-duplicated union of both blocker sets."""

        return tuple(
            dict.fromkeys(
                (
                    *self.authority_blocker_codes,
                    *self.compatibility_blocker_codes,
                )
            )
        )

    @property
    def authorized(self) -> bool:
        return self.authority_evaluated and not self.authority_blocker_codes

    @property
    def compatible(self) -> bool:
        return self.compatibility_evaluated and not self.compatibility_blocker_codes

    @property
    def eligible(self) -> bool:
        return self.authorized and self.compatible

    def merged_with(
        self,
        other: "RoutingEligibilityDecision",
    ) -> "RoutingEligibilityDecision":
        """Combine separately evaluated authority and compatibility evidence."""

        return RoutingEligibilityDecision(
            authority_evaluated=(
                self.authority_evaluated or other.authority_evaluated
            ),
            compatibility_evaluated=(
                self.compatibility_evaluated or other.compatibility_evaluated
            ),
            authority_blocker_codes=tuple(
                dict.fromkeys(
                    (
                        *self.authority_blocker_codes,
                        *other.authority_blocker_codes,
                    )
                )
            ),
            compatibility_blocker_codes=tuple(
                dict.fromkeys(
                    (
                        *self.compatibility_blocker_codes,
                        *other.compatibility_blocker_codes,
                    )
                )
            ),
            missing_specialist_skills=tuple(
                sorted(
                    set(self.missing_specialist_skills)
                    | set(other.missing_specialist_skills)
                )
            ),
        )


@dataclass(frozen=True)
class RoutingSkillDecision:
    """Deterministic required-skill evidence for one profile."""

    hard_blocker_codes: tuple[str, ...] = ()
    matched_skill_levels: tuple[tuple[str, int], ...] = ()
    missing_skill_keys: tuple[str, ...] = ()
    insufficient_skill_keys: tuple[str, ...] = ()
    blocking_weakness_keys: tuple[str, ...] = ()

    @property
    def eligible(self) -> bool:
        return not self.hard_blocker_codes


@dataclass(frozen=True)
class RoutingModelEnvelopeDecision:
    """Deterministic binding/catalog capability evidence for one candidate."""

    hard_blocker_codes: tuple[str, ...] = ()
    adequacy_class: int | None = None
    missing_modality_tags: tuple[str, ...] = ()
    missing_tool_tags: tuple[str, ...] = ()
    missing_data_policy_tags: tuple[str, ...] = ()

    @property
    def eligible(self) -> bool:
        return not self.hard_blocker_codes


def _axis_values(axes: Mapping[str, Any] | Any) -> dict[str, int]:
    expected = tuple(axis.value for axis in DifficultyAxis)
    if isinstance(axes, Mapping):
        unknown = set(axes).difference(expected)
        missing = set(expected).difference(axes)
        if unknown or missing:
            raise ValueError("Difficulty axes must contain the five governed keys")
        raw_values = {key: axes[key] for key in expected}
    else:
        try:
            raw_values = {key: getattr(axes, key) for key in expected}
        except AttributeError as exc:
            raise ValueError(
                "Difficulty axes must contain the five governed keys"
            ) from exc
    for key, value in raw_values.items():
        if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 3:
            raise ValueError(f"Difficulty axis {key} must be an integer from 1 to 3")
    return raw_values


def _reason_values(reason_codes: Iterable[str]) -> tuple[str, ...]:
    normalized = tuple(sorted(str(code).strip().lower() for code in reason_codes))
    if len(normalized) != len(set(normalized)):
        raise ValueError("Assessment reason codes must be unique")
    unknown = set(normalized).difference(ASSESSMENT_REASON_CODES)
    if unknown:
        raise ValueError(
            "Unknown assessment reason codes: " + ", ".join(sorted(unknown))
        )
    return normalized


def derive_difficulty_band(
    axes: Mapping[str, Any] | Any,
    reason_codes: Iterable[str] = (),
) -> str:
    """Derive the only valid band without averaging decisive axes."""

    values = _axis_values(axes)
    if any(value == 3 for value in values.values()):
        derived = DifficultyBand.ADVANCED.value
    elif all(value == 1 for value in values.values()):
        derived = DifficultyBand.ROUTINE.value
    else:
        derived = DifficultyBand.STANDARD.value
    for reason_code in _reason_values(reason_codes):
        rule = REASON_CODE_RULES[reason_code]
        if DIFFICULTY_BAND_ORDER[rule.minimum_band] > DIFFICULTY_BAND_ORDER[derived]:
            derived = rule.minimum_band
    return derived


def minimum_review_mode(
    axes: Mapping[str, Any] | Any,
    reason_codes: Iterable[str] = (),
) -> str:
    """Return the minimum review mode required by axes and governed reasons."""

    values = _axis_values(axes)
    minimum = ReviewMode.NONE.value
    if (
        values[DifficultyAxis.RISK.value] == 3
        or values[DifficultyAxis.VERIFICATION_BURDEN.value] == 3
    ):
        minimum = ReviewMode.INDEPENDENT.value
    for reason_code in _reason_values(reason_codes):
        required = REASON_CODE_RULES[reason_code].minimum_review_mode
        if REVIEW_MODE_ORDER[required] > REVIEW_MODE_ORDER[minimum]:
            minimum = required
    return minimum


def review_mode_meets(actual: str, minimum: str) -> bool:
    """Return whether one closed review mode meets the required floor."""

    try:
        return REVIEW_MODE_ORDER[str(actual)] >= REVIEW_MODE_ORDER[str(minimum)]
    except KeyError as exc:
        raise ValueError("Unknown review mode") from exc


def assessment_confidence_meets_minimum(confidence: float) -> bool:
    """Return whether an authoritative assessment meets the frozen v1 floor."""

    if (
        isinstance(confidence, bool)
        or not isinstance(confidence, (int, float))
        or not math.isfinite(confidence)
        or not 0.0 <= confidence <= 1.0
    ):
        raise ValueError("confidence must be a finite number from 0 to 1")
    return confidence >= MIN_ROUTING_ASSESSMENT_CONFIDENCE


def context_tier_meets(actual: str, minimum: str) -> bool:
    """Return whether an actual context tier meets a required tier."""

    try:
        return CONTEXT_TIER_ORDER[str(actual)] >= CONTEXT_TIER_ORDER[str(minimum)]
    except KeyError as exc:
        raise ValueError("Unknown context tier") from exc


def routing_skills_for_capability_labels(labels: Iterable[str]) -> tuple[str, ...]:
    """Return explicit skill choices for known coarse readiness labels.

    The returned union is a vocabulary boundary, not an inference that every
    listed skill is required or that any candidate possesses it.
    """

    skills: set[str] = set()
    for raw_label in labels:
        label = str(raw_label).strip().lower()
        skills.update(CAPABILITY_LABEL_SKILL_KEYS.get(label, ()))
    return tuple(sorted(skills))


def _normalized_skill_levels(
    levels: Mapping[str, int],
    *,
    label: str,
    governed_keys_only: bool,
) -> dict[str, int]:
    if not isinstance(levels, Mapping):
        raise ValueError(f"{label} must be a mapping")
    normalized: dict[str, int] = {}
    for raw_key, raw_level in levels.items():
        if not isinstance(raw_key, str):
            raise ValueError(f"{label} keys must be strings")
        key = raw_key.strip().lower()
        if not key:
            raise ValueError(f"{label} keys must not be blank")
        if key in normalized:
            raise ValueError(f"{label} keys must be unique after normalization")
        if governed_keys_only and key not in ROUTING_SKILL_KEYS:
            raise ValueError(f"Unknown routing skill key: {key}")
        if (
            isinstance(raw_level, bool)
            or not isinstance(raw_level, int)
            or not 1 <= raw_level <= 5
        ):
            raise ValueError(f"{label} levels must be integers from 1 to 5")
        normalized[key] = raw_level
    return normalized


def evaluate_required_skills(
    *,
    required_skill_levels: Mapping[str, int],
    actual_skill_levels: Mapping[str, int],
    weakness_keys: Iterable[str] = (),
) -> RoutingSkillDecision:
    """Evaluate precise governed skill requirements without prose inference."""

    required = _normalized_skill_levels(
        required_skill_levels,
        label="Required skill",
        governed_keys_only=True,
    )
    actual = _normalized_skill_levels(
        actual_skill_levels,
        label="Actual skill",
        governed_keys_only=False,
    )
    weaknesses = {
        str(raw_key).strip().lower()
        for raw_key in weakness_keys
        if str(raw_key).strip()
    }

    missing = tuple(sorted(set(required).difference(actual)))
    insufficient = tuple(
        sorted(
            key
            for key, minimum_level in required.items()
            if key in actual and actual[key] < minimum_level
        )
    )
    blocking_weaknesses = tuple(sorted(set(required).intersection(weaknesses)))
    disqualified = set(missing) | set(insufficient) | set(blocking_weaknesses)
    matched = tuple(
        sorted(
            (key, actual[key])
            for key in required
            if key not in disqualified
        )
    )

    blockers: list[str] = []
    if missing:
        blockers.append(RoutingBlockerCode.REQUIRED_SKILL_MISSING.value)
    if insufficient:
        blockers.append(
            RoutingBlockerCode.REQUIRED_SKILL_LEVEL_INSUFFICIENT.value
        )
    if blocking_weaknesses:
        blockers.append(
            RoutingBlockerCode.REQUIRED_SKILL_BLOCKING_WEAKNESS.value
        )
    return RoutingSkillDecision(
        hard_blocker_codes=tuple(blockers),
        matched_skill_levels=matched,
        missing_skill_keys=missing,
        insufficient_skill_keys=insufficient,
        blocking_weakness_keys=blocking_weaknesses,
    )


def _envelope_value(envelope: Mapping[str, Any] | Any, key: str) -> Any:
    if isinstance(envelope, Mapping):
        if key not in envelope:
            raise ValueError(f"Required model envelope is missing {key}")
        return envelope[key]
    try:
        return getattr(envelope, key)
    except AttributeError as exc:
        raise ValueError(
            f"Required model envelope is missing {key}"
        ) from exc


def _normalized_tag_set(values: Iterable[str], *, label: str) -> frozenset[str]:
    normalized: set[str] = set()
    for raw_value in values:
        if not isinstance(raw_value, str):
            raise ValueError(f"{label} entries must be strings")
        value = raw_value.strip().lower()
        if not value:
            raise ValueError(f"{label} entries must not be blank")
        normalized.add(value)
    return frozenset(normalized)


def model_adequacy_class(
    *,
    minimum_reasoning_tier: int,
    actual_reasoning_tier: int,
    minimum_context_tier: str,
    actual_context_tier: str,
) -> int:
    """Return deterministic excess capability steps for an adequate model."""

    for label, value in (
        ("minimum_reasoning_tier", minimum_reasoning_tier),
        ("actual_reasoning_tier", actual_reasoning_tier),
    ):
        if (
            isinstance(value, bool)
            or not isinstance(value, int)
            or value not in {tier.value for tier in ReasoningTier}
        ):
            raise ValueError(f"{label} must be a governed reasoning tier")
    try:
        minimum_context_order = CONTEXT_TIER_ORDER[str(minimum_context_tier)]
        actual_context_order = CONTEXT_TIER_ORDER[str(actual_context_tier)]
    except KeyError as exc:
        raise ValueError("Unknown context tier") from exc
    if actual_reasoning_tier < minimum_reasoning_tier:
        raise ValueError("Actual reasoning tier is below the required minimum")
    if actual_context_order < minimum_context_order:
        raise ValueError("Actual context tier is below the required minimum")
    return (
        actual_reasoning_tier
        - minimum_reasoning_tier
        + actual_context_order
        - minimum_context_order
    )


def evaluate_model_envelope(
    required_model: Mapping[str, Any] | Any,
    *,
    binding_present: bool = True,
    binding_enabled: bool = True,
    binding_revision_current: bool = True,
    catalog_present: bool = True,
    catalog_enabled: bool = True,
    actual_reasoning_tier: int | None,
    actual_context_tier: str | None,
    actual_modality_tags: Iterable[str] = (),
    actual_tool_tags: Iterable[str] = (),
    actual_data_policy_tags: Iterable[str] = (),
) -> RoutingModelEnvelopeDecision:
    """Evaluate one binding/catalog pair against a required model envelope."""

    minimum_reasoning_tier = _envelope_value(
        required_model,
        "minimum_reasoning_tier",
    )
    minimum_context_tier = str(
        _envelope_value(required_model, "minimum_context_tier")
    )
    required_modalities = _normalized_tag_set(
        _envelope_value(required_model, "modality_tags"),
        label="Required modality",
    )
    required_tools = _normalized_tag_set(
        _envelope_value(required_model, "tool_tags"),
        label="Required tool",
    )
    required_data_policies = _normalized_tag_set(
        _envelope_value(required_model, "data_policy_tags"),
        label="Required data policy",
    )
    actual_modalities = _normalized_tag_set(
        actual_modality_tags,
        label="Actual modality",
    )
    actual_tools = _normalized_tag_set(actual_tool_tags, label="Actual tool")
    actual_data_policies = _normalized_tag_set(
        actual_data_policy_tags,
        label="Actual data policy",
    )

    blockers: list[str] = []
    if not binding_present:
        blockers.append(RoutingBlockerCode.MODEL_BINDING_MISSING.value)
    elif not binding_enabled:
        blockers.append(RoutingBlockerCode.MODEL_BINDING_DISABLED.value)
    if binding_present and not binding_revision_current:
        blockers.append(RoutingBlockerCode.MODEL_BINDING_STALE.value)
    if not catalog_present:
        blockers.append(RoutingBlockerCode.MODEL_CATALOG_MISSING.value)
    elif not catalog_enabled:
        blockers.append(RoutingBlockerCode.MODEL_CATALOG_DISABLED.value)

    reasoning_adequate = (
        actual_reasoning_tier is not None
        and not isinstance(actual_reasoning_tier, bool)
        and isinstance(actual_reasoning_tier, int)
        and actual_reasoning_tier >= minimum_reasoning_tier
    )
    if not reasoning_adequate:
        blockers.append(
            RoutingBlockerCode.MODEL_REASONING_TIER_INSUFFICIENT.value
        )
    context_adequate = (
        actual_context_tier is not None
        and context_tier_meets(actual_context_tier, minimum_context_tier)
    )
    if not context_adequate:
        blockers.append(
            RoutingBlockerCode.MODEL_CONTEXT_TIER_INSUFFICIENT.value
        )

    missing_modalities = tuple(sorted(required_modalities - actual_modalities))
    missing_tools = tuple(sorted(required_tools - actual_tools))
    missing_data_policies = tuple(
        sorted(required_data_policies - actual_data_policies)
    )
    if missing_modalities:
        blockers.append(RoutingBlockerCode.MODEL_MODALITY_MISSING.value)
    if missing_tools:
        blockers.append(RoutingBlockerCode.MODEL_TOOL_MISSING.value)
    if missing_data_policies:
        blockers.append(RoutingBlockerCode.MODEL_DATA_POLICY_MISSING.value)

    adequacy_class: int | None = None
    if reasoning_adequate and context_adequate:
        adequacy_class = model_adequacy_class(
            minimum_reasoning_tier=minimum_reasoning_tier,
            actual_reasoning_tier=actual_reasoning_tier,
            minimum_context_tier=minimum_context_tier,
            actual_context_tier=actual_context_tier,
        )
    return RoutingModelEnvelopeDecision(
        hard_blocker_codes=tuple(dict.fromkeys(blockers)),
        adequacy_class=adequacy_class,
        missing_modality_tags=missing_modalities,
        missing_tool_tags=missing_tools,
        missing_data_policy_tags=missing_data_policies,
    )


def routing_candidate_rank_key(
    *,
    adequacy_class: int,
    cost_tier: str,
    queue_depth: int,
    schedule_delay_days: float,
    latency_tier: str,
    actor_id: int,
    binding_id: int,
) -> tuple[int, int, int, float, int, int, int]:
    """Freeze v1 ranking after all hard eligibility gates have passed."""

    integer_values = {
        "adequacy_class": adequacy_class,
        "queue_depth": queue_depth,
        "actor_id": actor_id,
        "binding_id": binding_id,
    }
    for label, value in integer_values.items():
        minimum = 1 if label in {"actor_id", "binding_id"} else 0
        if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
            raise ValueError(f"{label} must be an integer of at least {minimum}")
    if (
        isinstance(schedule_delay_days, bool)
        or not isinstance(schedule_delay_days, (int, float))
        or not math.isfinite(schedule_delay_days)
        or schedule_delay_days < 0
    ):
        raise ValueError("schedule_delay_days must be a finite non-negative number")
    try:
        cost_order = COST_TIER_ORDER[str(cost_tier)]
    except KeyError as exc:
        raise ValueError("Unknown cost tier") from exc
    try:
        latency_order = LATENCY_TIER_ORDER[str(latency_tier)]
    except KeyError as exc:
        raise ValueError("Unknown latency tier") from exc
    return (
        adequacy_class,
        cost_order,
        queue_depth,
        float(schedule_delay_days),
        latency_order,
        actor_id,
        binding_id,
    )


def _validate_json_native(
    value: Any,
    *,
    ancestors: set[int] | None = None,
    depth: int = 0,
) -> None:
    """Reject values whose JSON representation would be lossy or unstable."""

    if depth > 64:
        raise ValueError("Routing evidence exceeds the maximum JSON nesting depth")
    if value is None or isinstance(value, (str, bool, int)):
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError("Routing evidence numbers must be finite")
        return
    if not isinstance(value, (list, dict)):
        raise ValueError("Routing evidence must contain only JSON-native values")

    active_ancestors = ancestors if ancestors is not None else set()
    identity = id(value)
    if identity in active_ancestors:
        raise ValueError("Routing evidence must not contain reference cycles")
    active_ancestors.add(identity)
    try:
        if isinstance(value, list):
            for item in value:
                _validate_json_native(
                    item,
                    ancestors=active_ancestors,
                    depth=depth + 1,
                )
            return
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("Routing evidence object keys must be strings")
            _validate_json_native(
                item,
                ancestors=active_ancestors,
                depth=depth + 1,
            )
    finally:
        active_ancestors.remove(identity)


def canonical_routing_json_bytes(value: Any) -> bytes:
    """Serialize JSON-native normalized routing evidence as stable UTF-8."""

    if hasattr(value, "model_dump"):
        value = value.model_dump(mode="json")
    _validate_json_native(value)
    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        ).encode("utf-8")
    except (TypeError, ValueError, UnicodeError) as exc:
        raise ValueError(
            "Routing evidence must have a valid UTF-8 JSON representation"
        ) from exc


def validate_routing_packet_size(
    value: Any,
    *,
    label: str = "Routing packet",
    maximum_bytes: int = MAX_ROUTING_PACKET_BYTES,
) -> Any:
    """Reject a canonical routing packet that exceeds its storage boundary."""

    if len(canonical_routing_json_bytes(value)) > maximum_bytes:
        raise ValueError(f"{label} must not exceed {maximum_bytes} bytes")
    return value


def assignment_intent(purpose: str, queue_class: str) -> str:
    """Normalize a valid assignment purpose/queue tuple to one intent."""

    try:
        return VALID_ASSIGNMENT_INTENTS[(str(purpose), str(queue_class))]
    except KeyError as exc:
        raise ValueError(
            RoutingBlockerCode.ASSIGNMENT_PURPOSE_QUEUE_CLASS_INCOMPATIBLE.value
        ) from exc


def evaluate_actor_authorization(
    *,
    intent: str,
    enabled: bool,
    role: str,
    scopes: Iterable[str],
) -> RoutingEligibilityDecision:
    """Evaluate authority only; capability evidence cannot clear these blockers."""

    try:
        normalized_intent = AssignmentIntent(str(intent))
    except ValueError as exc:
        raise ValueError("Unknown assignment intent") from exc
    blockers: list[str] = []
    if not enabled:
        blockers.append(RoutingBlockerCode.ACTOR_DISABLED.value)
    scope_set = {str(scope) for scope in scopes}
    if normalized_intent == AssignmentIntent.VERIFICATION:
        if role not in {"verifier", "pm"}:
            blockers.append(RoutingBlockerCode.ACTOR_ROLE_INCOMPATIBLE.value)
        if "admin" not in scope_set and "verification:write" not in scope_set:
            blockers.append(RoutingBlockerCode.ACTOR_SCOPE_MISSING.value)
    else:
        if role not in {"worker", "pm"}:
            blockers.append(RoutingBlockerCode.ACTOR_ROLE_INCOMPATIBLE.value)
        if "admin" not in scope_set and "work:execute" not in scope_set:
            blockers.append(RoutingBlockerCode.ACTOR_SCOPE_MISSING.value)
    return RoutingEligibilityDecision(
        authority_evaluated=True,
        authority_blocker_codes=tuple(blockers),
    )


def evaluate_assignment_compatibility(
    *,
    intent: str,
    actor_id: int,
    actor_profile: RoutingProfileEvidence | None,
    capacity_owner_id: int | None = None,
    capacity_owner_profile_id: int | None = None,
    reviewer_profile_id: int | None = None,
    execution_actor_ids: Iterable[int | None] = (),
    execution_profile_ids: Iterable[int | None] = (),
    review_mode: str = ReviewMode.NONE.value,
    required_specialist_skill_levels: Mapping[str, int] | None = None,
) -> RoutingEligibilityDecision:
    """Evaluate unattended profile/capacity/verifier compatibility.

    Authorization is intentionally absent.  Callers must evaluate authority
    separately and merge the decisions before treating a candidate as eligible.
    """

    try:
        normalized_intent = AssignmentIntent(str(intent))
    except ValueError as exc:
        raise ValueError("Unknown assignment intent") from exc
    if str(review_mode) not in REVIEW_MODE_ORDER:
        raise ValueError("Unknown review mode")

    blockers: list[str] = []
    missing_specialist_skills: tuple[str, ...] = ()
    if actor_profile is None:
        blockers.append(RoutingBlockerCode.ACTOR_PROFILE_MISSING.value)
        return RoutingEligibilityDecision(
            compatibility_evaluated=True,
            compatibility_blocker_codes=tuple(blockers)
        )

    if actor_profile.profile_kind == "human":
        blockers.append(RoutingBlockerCode.PROFILE_KIND_HUMAN.value)
    elif actor_profile.profile_kind not in {"agent", "hybrid"}:
        blockers.append(RoutingBlockerCode.PROFILE_KIND_UNSUPPORTED.value)
    if not actor_profile.automation_enabled:
        blockers.append(RoutingBlockerCode.PROFILE_AUTOMATION_DISABLED.value)

    required_mode = (
        "verification"
        if normalized_intent == AssignmentIntent.VERIFICATION
        else "execution"
    )
    if required_mode not in actor_profile.assignment_modes:
        blockers.append(RoutingBlockerCode.PROFILE_ASSIGNMENT_MODE_MISSING.value)

    if normalized_intent != AssignmentIntent.VERIFICATION:
        if capacity_owner_id is None:
            blockers.append(RoutingBlockerCode.CAPACITY_OWNER_MISSING.value)
        elif capacity_owner_profile_id is None:
            blockers.append(
                RoutingBlockerCode.CAPACITY_OWNER_PROFILE_MISSING.value
            )
        elif actor_profile.profile_id != capacity_owner_profile_id:
            blockers.append(
                RoutingBlockerCode.ACTOR_CAPACITY_PROFILE_MISMATCH.value
            )
    else:
        if reviewer_profile_id is None:
            blockers.append(RoutingBlockerCode.REVIEWER_PROFILE_MISSING.value)
        elif reviewer_profile_id != actor_profile.profile_id:
            blockers.append(RoutingBlockerCode.REVIEWER_PROFILE_MISMATCH.value)

        implementation_actor_values = tuple(execution_actor_ids)
        implementation_profile_values = tuple(execution_profile_ids)
        known_implementation_actors = {
            int(value)
            for value in implementation_actor_values
            if value is not None
        }
        known_implementation_profiles = {
            int(value)
            for value in implementation_profile_values
            if value is not None
        }
        if (
            not implementation_actor_values
            or len(implementation_actor_values)
            != len(implementation_profile_values)
            or any(value is None for value in implementation_actor_values)
            or any(value is None for value in implementation_profile_values)
        ):
            blockers.append(
                RoutingBlockerCode.VERIFICATION_INDEPENDENCE_UNVERIFIABLE.value
            )
        if actor_id in known_implementation_actors:
            blockers.append(
                RoutingBlockerCode.VERIFICATION_ACTOR_NOT_INDEPENDENT.value
            )
        if actor_profile.profile_id in known_implementation_profiles:
            blockers.append(
                RoutingBlockerCode.VERIFICATION_PROFILE_NOT_INDEPENDENT.value
            )

        if str(review_mode) == ReviewMode.SPECIALIST_INDEPENDENT.value:
            required_levels: dict[str, int] = {}
            for raw_skill_key, minimum_level in (
                required_specialist_skill_levels or {}
            ).items():
                skill_key = str(raw_skill_key).strip().lower()
                if skill_key in required_levels:
                    raise ValueError(
                        "Specialist skill keys must be unique after normalization"
                    )
                if skill_key not in ROUTING_SKILL_KEYS:
                    raise ValueError(
                        f"Unknown routing skill key: {skill_key}"
                    )
                if (
                    isinstance(minimum_level, bool)
                    or not isinstance(minimum_level, int)
                    or not 1 <= minimum_level <= 5
                ):
                    raise ValueError(
                        "Specialist skill levels must be between 1 and 5"
                    )
                required_levels[skill_key] = minimum_level
            missing_specialist_skills = tuple(
                sorted(
                    skill_key
                    for skill_key, minimum_level in required_levels.items()
                    if skill_key in actor_profile.weakness_keys
                    or actor_profile.skill_levels.get(skill_key, 0)
                    < minimum_level
                )
            )
            if not required_levels or missing_specialist_skills:
                blockers.append(
                    RoutingBlockerCode.VERIFICATION_SPECIALIST_SKILL_MISSING.value
                )

    return RoutingEligibilityDecision(
        compatibility_evaluated=True,
        compatibility_blocker_codes=tuple(dict.fromkeys(blockers)),
        missing_specialist_skills=missing_specialist_skills,
    )
