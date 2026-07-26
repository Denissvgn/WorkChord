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
    """Stable authority and compatibility blockers for exact-actor routing."""

    ASSIGNMENT_PURPOSE_QUEUE_CLASS_INCOMPATIBLE = (
        "assignment_purpose_queue_class_incompatible"
    )
    ACTOR_DISABLED = "actor_disabled"
    ACTOR_ROLE_INCOMPATIBLE = "actor_role_incompatible"
    ACTOR_SCOPE_MISSING = "actor_scope_missing"
    ACTOR_PROFILE_MISSING = "actor_profile_missing"
    CAPACITY_OWNER_MISSING = "capacity_owner_missing"
    CAPACITY_OWNER_PROFILE_MISSING = "capacity_owner_profile_missing"
    ACTOR_CAPACITY_PROFILE_MISMATCH = "actor_capacity_profile_mismatch"
    PROFILE_KIND_HUMAN = "profile_kind_human"
    PROFILE_KIND_UNSUPPORTED = "profile_kind_unsupported"
    PROFILE_AUTOMATION_DISABLED = "profile_automation_disabled"
    PROFILE_ASSIGNMENT_MODE_MISSING = "profile_assignment_mode_missing"
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
