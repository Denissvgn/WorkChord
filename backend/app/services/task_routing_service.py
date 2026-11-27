"""Keep a task's structured routing consistent with its assignee and the project's review policy.

A task's routing (first rung, escalation ladder, reviewer) is part of its canonical brief. This
module fills catalog facts into a routing, checks it against the assignee's bound models and the
project's different-publisher policy, proposes a consistent replacement, and converts routing
that a brief still carries as free text.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from sqlalchemy import select

from app.commands import PlanningConflict
from app.models.agent import AgentActor, AgentModelBinding, AgentModelCatalogEntry
from app.models.project import Project
from app.models.team_member import TeamMember, TeamMemberProfile
from app.schemas.task_routing import (
    RoutingCheck, RoutingConvertResponse, RoutingIssue, RoutingReviewer, RoutingRung, TaskRouting,
)

EFFORT_RANK = {"unknown": 0, "low": 1, "medium": 2, "high": 3, "xhigh": 4, "max": 5}
_TEXT_ROUTING = re.compile(r"first rung|independent review by|^\s*reviewer:|after \w+ failed acceptance runs the task moves to",
                           re.IGNORECASE | re.MULTILINE)


class RoutingConsistencyConflict(PlanningConflict):
    """A routing change refused under the project's policy; the detail carries a consistent routing."""

    def __init__(self, check: RoutingCheck):
        self.check = check
        codes = ", ".join(issue.code for issue in check.issues if issue.severity == "conflict")
        super().__init__("routing_inconsistent",
                         f"The task's routing conflicts with its assignee or the project's review policy ({codes}). "
                         "Save the suggested routing, for example with routing_resolution apply_suggestion, or change it.")

    def detail(self):
        return {**super().detail(), "routing_check": self.check.model_dump(mode="json")}


@dataclass
class AssigneeModels:
    """The catalog entries the assignee row's agents can run."""

    assignee_id: int | None = None
    profile_id: int | None = None
    entries: list[AgentModelCatalogEntry] = field(default_factory=list)
    default_keys: set[str] = field(default_factory=set)

    @property
    def keys(self) -> set[str]:
        return {entry.key for entry in self.entries}

    @property
    def publishers(self) -> set[str]:
        return {entry.publisher_key for entry in self.entries if entry.publisher_key}


def _rank(entry) -> tuple[int, int]:
    return (entry.reasoning_tier, EFFORT_RANK.get(entry.effort, 0))


def _rung_from(entry, *, harness="", reviewer=False, **extra):
    data = {"catalog_key": entry.key, "harness": harness, "effort": entry.effort,
            "publisher_key": entry.publisher_key, "configured_model_alias": entry.configured_model_alias, **extra}
    return RoutingReviewer(**data) if reviewer else RoutingRung(**data)


async def catalog_entries(db, keys=None) -> dict[str, AgentModelCatalogEntry]:
    query = select(AgentModelCatalogEntry)
    if keys is not None:
        keys = sorted(set(keys))
        if not keys:
            return {}
        query = query.where(AgentModelCatalogEntry.key.in_(keys))
    return {entry.key: entry for entry in (await db.scalars(query.order_by(AgentModelCatalogEntry.id))).all()}


def _routing_keys(routing: TaskRouting) -> list[str]:
    rungs = ([routing.first_rung] if routing.first_rung else []) + list(routing.escalation)
    return [rung.catalog_key for rung in rungs] + ([routing.reviewer.catalog_key] if routing.reviewer else [])


async def resolve_routing(db, routing: TaskRouting) -> TaskRouting:
    """Fill each rung and the reviewer from its enabled catalog entry; refuse unknown references."""
    entries = await catalog_entries(db, _routing_keys(routing))
    data = routing.model_dump(mode="json")

    def fill(rung):
        entry = entries.get(rung["catalog_key"])
        if entry is None:
            raise ValueError(f"Routing names the unknown model catalog entry {rung['catalog_key']}")
        if not entry.enabled:
            raise ValueError(f"Routing names the disabled model catalog entry {rung['catalog_key']}")
        rung.update(effort=entry.effort, publisher_key=entry.publisher_key, configured_model_alias=entry.configured_model_alias)

    for rung in ([data["first_rung"]] if data["first_rung"] else []) + data["escalation"]:
        fill(rung)
    if data["reviewer"]:
        fill(data["reviewer"])
        profile_id = data["reviewer"].get("profile_id")
        if profile_id is not None and await db.scalar(select(TeamMemberProfile.id).where(TeamMemberProfile.id == profile_id)) is None:
            raise ValueError(f"Routing names the unknown reviewer profile {profile_id}")
    return TaskRouting.model_validate(data)


async def assignee_models(db, assignee_id) -> AssigneeModels:
    """Enabled catalog entries bound to the enabled, active agents of the assignee row's profile."""
    if assignee_id is None:
        return AssigneeModels()
    profile_id = await db.scalar(select(TeamMember.profile_id).where(TeamMember.id == assignee_id))
    if profile_id is None:
        return AssigneeModels(assignee_id=assignee_id)
    rows = (await db.execute(
        select(AgentModelBinding.is_default, AgentModelCatalogEntry)
        .join(AgentModelCatalogEntry, AgentModelCatalogEntry.id == AgentModelBinding.model_catalog_id)
        .join(AgentActor, AgentActor.id == AgentModelBinding.actor_id)
        .where(AgentActor.profile_id == profile_id, AgentActor.enabled.is_(True), AgentActor.lifecycle_state == "active",
               AgentModelBinding.enabled.is_(True), AgentModelCatalogEntry.enabled.is_(True))
        .order_by(AgentModelCatalogEntry.id)
    )).all()
    entries, seen, defaults = [], set(), set()
    for is_default, entry in rows:
        if entry.id not in seen:
            seen.add(entry.id)
            entries.append(entry)
        if is_default:
            defaults.add(entry.key)
    return AssigneeModels(assignee_id=assignee_id, profile_id=profile_id, entries=entries, default_keys=defaults)


async def _verifier_profiles(db) -> dict[str, list[int]]:
    """Catalog key -> profiles of enabled agents that hold it and whose profile verifies."""
    rows = (await db.execute(
        select(AgentModelCatalogEntry.key, TeamMemberProfile.id, TeamMemberProfile.assignment_modes)
        .join(AgentModelBinding, AgentModelBinding.model_catalog_id == AgentModelCatalogEntry.id)
        .join(AgentActor, AgentActor.id == AgentModelBinding.actor_id)
        .join(TeamMemberProfile, TeamMemberProfile.id == AgentActor.profile_id)
        .where(AgentActor.enabled.is_(True), AgentActor.lifecycle_state == "active", AgentModelBinding.enabled.is_(True),
               AgentModelCatalogEntry.enabled.is_(True), TeamMemberProfile.automation_enabled.is_(True))
    )).all()
    result: dict[str, list[int]] = {}
    for key, profile_id, modes in rows:
        if "verification" in (modes or ()) and profile_id not in result.setdefault(key, []):
            result[key].append(profile_id)
    return result


async def project_policy(db, project_id) -> tuple[bool, str]:
    if project_id is None:
        return False, "refuse"
    from app.services.review_provenance import different_publisher_required
    required = await different_publisher_required(db, project_id)
    mode = await db.scalar(select(Project.routing_conflict_mode).where(Project.id == project_id))
    return required, mode or "refuse"




@dataclass
class _Facts:
    """What a routing is checked against: the assignee, the policy and the live catalog."""

    policy: bool
    models: AssigneeModels
    catalog: dict[str, AgentModelCatalogEntry]
    verifiers: dict[str, list[int]]
    contributor_publishers: set[str] = field(default_factory=set)
    contributors_unknown: bool = False

    def verifier_profiles(self, key):
        return [profile for profile in self.verifiers.get(key, []) if profile != self.models.profile_id]

    def executing(self, first: RoutingRung | None) -> set[str]:
        """Publishers the reviewer must differ from: the assignee's, the first rung's and every recorded contributor's."""
        publishers = set(self.models.publishers) | set(self.contributor_publishers)
        if first is not None and first.publisher_key:
            publishers.add(first.publisher_key)
        return publishers


async def _contributor_publishers(db, task) -> tuple[set[str], bool]:
    """Publishers review provenance already counts as contributors of this task, as reviewer selection sees them."""
    from app.models.agent import AgentTaskAssignment
    from app.query_limits import CollectionLimitExceededError
    from app.services.agent_routing_service import AgentRoutingConflictError
    from app.services.review_provenance import review_history
    assignments = (await db.scalars(select(AgentTaskAssignment).where(AgentTaskAssignment.task_id == task.id))).all()
    try:
        history = await review_history(db, task, assignments, strict=True)
    except (AgentRoutingConflictError, CollectionLimitExceededError):
        return set(), True
    publishers = {row["publisher_key"] for row in history.contributors if row.get("publisher_key")}
    return publishers, any(not row.get("publisher_key") for row in history.contributors)


def _refreshed(routing: TaskRouting, catalog) -> TaskRouting:
    """The routing with publisher, effort and alias as the catalog states them now."""
    data = routing.model_dump(mode="json")
    for rung in ([data["first_rung"]] if data["first_rung"] else []) + data["escalation"] + ([data["reviewer"]] if data["reviewer"] else []):
        entry = catalog.get(rung["catalog_key"])
        if entry is not None:
            rung.update(effort=entry.effort, publisher_key=entry.publisher_key, configured_model_alias=entry.configured_model_alias)
    return TaskRouting.model_validate(data)


def _available(catalog, rung) -> bool:
    entry = catalog.get(rung.catalog_key) if rung is not None else None
    return entry is not None and entry.enabled


def _issues(routing: TaskRouting, facts: _Facts) -> list[RoutingIssue]:
    issues: list[RoutingIssue] = []
    models, policy, catalog = facts.models, facts.policy, facts.catalog

    def add(code, severity, field_name, message, rung=None):
        issues.append(RoutingIssue(code=code, severity=severity, field=field_name, message=message,
                                   catalog_key=getattr(rung, "catalog_key", None), publisher_key=getattr(rung, "publisher_key", None)))

    for name, rungs in (("first_rung", [routing.first_rung] if routing.first_rung else []), ("escalation", routing.escalation),
                        ("reviewer", [routing.reviewer] if routing.reviewer else [])):
        for rung in rungs:
            if not _available(catalog, rung):
                add("catalog_entry_unavailable", "warning", name, f"The catalog entry {rung.catalog_key} is missing or disabled.", rung)
    first = routing.first_rung
    if models.assignee_id is not None and not models.entries:
        add("assignee_models_unknown", "warning", "assignee",
            "The assignee has no active agent with an enabled model binding, so the first rung cannot be checked against it.")
    elif first is not None and models.entries and first.catalog_key not in models.keys:
        add("first_rung_not_assignee_model", "conflict", "first_rung",
            f"The first rung {first.catalog_key} is not a model the assignee's agent runs.", first)
    elif first is None and models.entries:
        add("first_rung_missing", "warning", "first_rung", "The routing names no first rung for the assignee.")
    executing = facts.executing(first)
    reviewer = routing.reviewer
    if reviewer is not None and reviewer.profile_id is not None and reviewer.profile_id == models.profile_id:
        add("reviewer_profile_is_assignee_profile", "conflict", "reviewer",
            "The reviewer profile is the assignee's profile; review needs a different profile.", reviewer)
    if reviewer is not None and first is not None and reviewer.catalog_key == first.catalog_key and not policy:
        add("reviewer_is_first_rung", "warning", "reviewer", "The reviewer is the model that executes the first rung.", reviewer)
    if reviewer is not None:
        holders = facts.verifier_profiles(reviewer.catalog_key)
        if not holders:
            add("reviewer_has_no_verifier", "conflict" if policy else "warning", "reviewer",
                f"No active verification profile other than the assignee's runs {reviewer.catalog_key}, so nobody can carry out this review.",
                reviewer)
        elif reviewer.profile_id is not None and reviewer.profile_id not in holders and reviewer.profile_id != models.profile_id:
            add("reviewer_profile_lacks_model", "warning", "reviewer",
                f"The reviewer profile {reviewer.profile_id} has no active verification agent running {reviewer.catalog_key}.", reviewer)
    if policy:
        if facts.contributors_unknown:
            add("contributor_publishers_unknown", "warning", "reviewer",
                "A recorded contributor of this task has no known publisher, so review independence cannot be proven yet.")
        if reviewer is None:
            add("reviewer_missing", "warning", "reviewer", "The project requires a review publisher different from every contributor; name a reviewer.")
        elif not reviewer.publisher_key:
            add("reviewer_publisher_unknown", "conflict", "reviewer",
                f"The reviewer {reviewer.catalog_key} has no known publisher, so the project's publisher policy cannot be met.", reviewer)
        elif reviewer.publisher_key in executing:
            add("reviewer_shares_assignee_publisher", "conflict", "reviewer",
                f"The reviewer {reviewer.catalog_key} has the publisher {reviewer.publisher_key} of the assignee, the first rung "
                "or a recorded contributor; the project requires a different review publisher.", reviewer)
        elif reviewer.publisher_key in {rung.publisher_key for rung in routing.escalation}:
            add("reviewer_shares_escalation_publisher", "warning", "reviewer",
                f"An escalation rung has the reviewer's publisher {reviewer.publisher_key}; after that escalation this reviewer "
                "could no longer review.", reviewer)
    return issues


def _choose_first_rung(models: AssigneeModels, current: RoutingRung | None):
    candidates = [entry for entry in models.entries if entry.key in models.default_keys] or list(models.entries)
    if not candidates:
        return None
    effort = current.effort if current is not None else None
    return next((entry for entry in candidates if effort and entry.effort == effort), candidates[0])


def suggest_routing(routing: TaskRouting, facts: _Facts) -> tuple[TaskRouting | None, list[RoutingIssue]]:
    """A routing consistent with the assignee and policy that keeps as much of the current one as it can.

    Also returns warnings about what the suggestion gives up, such as a lower first rung.
    """
    models, policy, catalog = facts.models, facts.policy, facts.catalog
    data = routing.model_copy(deep=True)
    notes: list[RoutingIssue] = []
    first = data.first_rung
    old_publisher = first.publisher_key if first is not None else None
    # Rungs the catalog no longer offers could not be saved again.
    data.escalation = [rung for rung in data.escalation if _available(catalog, rung)]
    if models.entries and (first is None or first.catalog_key not in models.keys):
        chosen = _choose_first_rung(models, first)
        data.first_rung = _rung_from(chosen)
        current = catalog.get(first.catalog_key) if first is not None else None
        if current is not None and _rank(chosen) < _rank(current):
            notes.append(RoutingIssue(code="suggested_first_rung_lower", severity="warning", field="first_rung",
                message=f"The suggested first rung {chosen.key} ranks below the current {current.key} in reasoning tier or effort.",
                catalog_key=chosen.key, publisher_key=chosen.publisher_key))
        missing = sorted(set(current.qualification_keys or []) - set(chosen.qualification_keys or [])) if current is not None else []
        if missing:
            notes.append(RoutingIssue(code="suggested_first_rung_missing_qualifications", severity="warning", field="first_rung",
                message=f"The suggested first rung {chosen.key} lacks qualification keys the current one holds: {', '.join(missing)}.",
                catalog_key=chosen.key, publisher_key=chosen.publisher_key))
        new_publisher = chosen.publisher_key
        ladder: list[RoutingRung] = []
        if old_publisher and old_publisher != new_publisher:
            # Rungs of the vendor the task moves away from become step-ups of the new first rung's vendor.
            steps = sorted((entry for entry in catalog.values()
                            if entry.enabled and entry.publisher_key == new_publisher and _rank(entry) > _rank(chosen)),
                           key=lambda entry: (_rank(entry), entry.id))
            for rung in data.escalation:
                if rung.publisher_key == old_publisher:
                    if steps:
                        ladder.append(_rung_from(steps.pop(0)))
                else:
                    ladder.append(rung)
        else:
            ladder = list(data.escalation)
        unique, seen = [], {chosen.key}
        for rung in ladder:
            if rung.catalog_key not in seen:
                seen.add(rung.catalog_key)
                unique.append(rung)
        data.escalation = unique
    elif first is not None and not _available(catalog, first):
        data.first_rung = None
    first = data.first_rung
    executing = facts.executing(first)
    reviewer = data.reviewer
    profile_clash = reviewer is not None and reviewer.profile_id is not None and reviewer.profile_id == models.profile_id
    unrunnable = reviewer is not None and (not _available(catalog, reviewer) or not facts.verifier_profiles(reviewer.catalog_key))
    needs_reviewer = (policy and (reviewer is None or not reviewer.publisher_key or reviewer.publisher_key in executing)
                      or profile_clash or unrunnable)
    if needs_reviewer:
        ladder_publishers = {rung.publisher_key for rung in data.escalation}
        old_entry = catalog.get(reviewer.catalog_key) if reviewer is not None else None
        # Only a model some verification profile runs can carry out the review.
        candidates = [entry for entry in catalog.values() if entry.enabled and facts.verifier_profiles(entry.key)
                      and (not policy or entry.publisher_key and entry.publisher_key not in executing)
                      and (policy or entry.key != (first.catalog_key if first else None))]

        def preference(entry):
            return (entry.publisher_key in ladder_publishers,
                    old_entry is None or entry.effort != old_entry.effort,
                    old_entry is None or entry.reasoning_tier != old_entry.reasoning_tier, entry.id)

        if candidates:
            chosen = min(candidates, key=preference)
            profiles = facts.verifier_profiles(chosen.key)
            data.reviewer = _rung_from(chosen, reviewer=True, profile_id=profiles[0] if len(profiles) == 1 else None,
                                       instructions=reviewer.instructions if reviewer is not None else "")
        elif profile_clash:
            data.reviewer = reviewer.model_copy(update={"profile_id": None})
    if data == routing:
        return None, notes
    return data, notes


async def check_routing(db, *, task=None, task_id=None, project_id, assignee_id, routing: dict | TaskRouting | None,
                        brief_text: str | None = None, removed_routing: bool = False) -> RoutingCheck:
    """Check one routing against one assignee under the project's policy and offer a consistent one."""
    task_id = task.id if task is not None else task_id
    if routing is None:
        check = RoutingCheck(task_id=task_id, assignee_id=assignee_id)
        check.text_routing = bool(brief_text and _TEXT_ROUTING.search(brief_text))
        if removed_routing:
            policy, mode = await project_policy(db, project_id)
            check.different_publisher_required, check.conflict_mode = policy, mode
            check.issues.append(RoutingIssue(code="routing_removed", severity="conflict" if policy else "warning", field="routing",
                message="This change removes the structured routing, so the reviewer is no longer checked against the new assignee."))
            check.consistent = not policy
        if check.text_routing:
            check.issues.append(RoutingIssue(code="routing_in_text", severity="warning", field="routing",
                message="The brief names its routing only in free text, which an assignee change does not update. Convert it to structured routing."))
        return check
    policy, mode = await project_policy(db, project_id)
    models = await assignee_models(db, assignee_id)
    stored = routing if isinstance(routing, TaskRouting) else TaskRouting.model_validate(routing)
    catalog = await catalog_entries(db)
    facts = _Facts(policy=policy, models=models, catalog=catalog, verifiers=await _verifier_profiles(db))
    if policy and task is not None:
        facts.contributor_publishers, facts.contributors_unknown = await _contributor_publishers(db, task)
    current = _refreshed(stored, catalog)
    check = RoutingCheck(task_id=task_id, assignee_id=assignee_id, assignee_profile_id=models.profile_id,
                         assignee_publishers=sorted(models.publishers), assignee_catalog_keys=sorted(models.keys),
                         different_publisher_required=policy, conflict_mode=mode, structured=True, routing=stored)
    check.issues = _issues(current, facts)
    check.consistent = not any(issue.severity == "conflict" for issue in check.issues)
    if check.issues or current != stored:
        check.suggestion, notes = suggest_routing(current, facts)
        if check.suggestion is not None:
            check.issues.extend(notes)
            if check.suggestion.reviewer != stored.reviewer:
                check.suggested_reviewer = check.suggestion.reviewer
    return check


def routing_check_for(db, task_id) -> RoutingCheck | None:
    """The routing check this command made for a task, for its response."""
    from app.commands import current_command
    command = current_command(db)
    return command.routing_checks.get(task_id) if command is not None else None


def _remember(db, task_id, check):
    from app.commands import current_command
    command = current_command(db)
    if command is not None:
        command.routing_checks[task_id] = check


async def enforce_routing(db, task, *, resolution: str = "check", changed: bool, removed_routing: bool = False) -> RoutingCheck | None:
    """Check the task's routing for its current assignee; apply the suggestion, refuse or warn.

    Runs only when the assignee or the routing changed, or when the caller asks to apply the
    suggestion. The result is kept for this command's response.
    """
    if not changed and resolution != "apply_suggestion":
        return None
    from app.schemas.task_brief import TaskBrief
    from app.services.task_brief_service import TaskBriefService
    brief = task.brief or {}
    check = await check_routing(db, task=task, project_id=task.project_id, assignee_id=task.assignee_id,
                                routing=brief.get("routing"), brief_text=task.description, removed_routing=removed_routing)
    if resolution == "apply_suggestion" and check.suggestion is not None:
        notes = [issue for issue in check.issues if issue.code.startswith("suggested_")]
        updated = TaskBrief.model_validate({**brief, "routing": check.suggestion.model_dump(mode="json")})
        await TaskBriefService(db).apply_brief(task, updated, provenance="routing_suggestion", enforce=False)
        check = await check_routing(db, task=task, project_id=task.project_id, assignee_id=task.assignee_id,
                                    routing=task.brief.get("routing"), brief_text=task.description)
        check.issues.extend(notes)
        check.applied = True
    if not check.consistent and check.conflict_mode == "refuse":
        raise RoutingConsistencyConflict(check)
    _remember(db, task.id, check)
    return check


# Free-text conversion ---------------------------------------------------------------------------

_EFFORT = r"(?P<effort>unknown|low|medium|high|xhigh|max|default)"
_FIRST_SENTENCE = re.compile(
    r"First rung:\s*(?P<name>[^\n]+?)\s+at\s+(?:thinking\s+)?" + _EFFORT + r"\s+effort"
    r"(?:\s+\((?P<key>[^)\s]+)\))?(?:\s+in\s+(?P<harness>[^.\n]+?))?\.(?=\s|$)")
_INLINE = re.compile(
    r"(?P<lead>;\s*)?first rung\s+(?P<first>\S+)\s+@\s+(?P<first_effort>\w+)"
    r"(?:;\s*escalation\s+(?P<ladder>\S+\s+@\s+\w+(?:\s*->\s*\S+\s+@\s+\w+)*))?"
    r"(?:;\s*(?P<after>(?:after the last rung|then)\s[^.\n]*))?\.(?=\s|$)", re.IGNORECASE)
_MOVES = re.compile(
    r"After (?P<runs>one|two|three|four|five|\d+) failed acceptance runs? the task moves to "
    r"(?P<name>[^.\n]+?)(?:\s+at\s+" + _EFFORT + r"\s+effort)?\.(?=\s|$)")
_REVIEWER = re.compile(
    r"Reviewer:\s*(?P<name>[^\n(]+?)\s*(?:\((?P<key>[^)\s]+)\))?\s+at\s+" + _EFFORT + r"\s+effort(?P<tail>[^.\n]*)\.(?=\s|$)")
_INDEPENDENT = re.compile(
    r"Independent review by\s+(?P<name>[^:\n]+?)(?:\s+at\s+" + _EFFORT + r"\s+effort)?(?::\s*(?P<instructions>[^\n]*?\.)|\.)(?=\s|$)")
_NUMBERS = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}


def _norm(label: str) -> str:
    return re.sub(r"\s+", " ", label.strip().lower())


class _Resolver:
    """Match a model named in prose to exactly one enabled catalog entry by exact key or alias."""

    def __init__(self, entries):
        self.entries = [entry for entry in entries if entry.enabled]

    def __call__(self, name: str | None, effort: str | None, key: str | None = None):
        # The parenthesised key is tried first; a display name only matches when it is the key or alias itself.
        for label in (key, name):
            if label and label.strip():
                wanted = _norm(label)
                matches = [entry for entry in self.entries if wanted in (entry.key, _norm(entry.configured_model_alias))]
                if matches:
                    return self._with_effort(matches, effort)
        return None

    @staticmethod
    def _with_effort(matches, effort):
        if effort == "default":
            matches = [entry for entry in matches if entry.effort == "unknown"]
        elif effort:
            matches = [entry for entry in matches if entry.effort == effort]
        return matches[0] if len(matches) == 1 else None


def _cut(text: str, start: int, end: int, replacement: str = "") -> str:
    """Remove one sentence and close the gap it leaves on its own line only."""
    line_start = text.rfind("\n", 0, start) + 1
    line_end = text.find("\n", end)
    line_end = len(text) if line_end == -1 else line_end
    original = text[line_start:line_end]
    indent = re.match(r"[ \t]*", original).group(0)
    line = text[line_start:start] + replacement + text[end:line_end]
    body = re.sub(r" {2,}", " ", line[len(indent):] if line.startswith(indent) else line.lstrip()).strip()
    return text[:line_start] + (indent + body if body else "") + text[line_end:]


def _remove_first(text: str, sentence: str) -> str:
    index = text.find(sentence)
    return text if index < 0 else _cut(text, index, index + len(sentence))


def parse_text_routing(brief: dict, entries, existing: dict | None = None) -> tuple[dict, dict, list[str], list[str]]:
    """Parse routing sentences out of a brief's context and verification.

    Returns the routing data, the brief without the sentences it resolved, the resolved sentences
    and the routing sentences it kept because no single catalog entry matched exactly. With an
    existing routing, a sentence is resolved only when it fills an empty part or repeats a
    stored one.
    """
    resolve = _Resolver(entries)
    routing: dict = dict(existing or {})
    routing.setdefault("escalation", [])
    removed: list[str] = []
    unresolved: list[str] = []
    cleaned = dict(brief)

    def key_of(slot):
        return (routing.get(slot) or {}).get("catalog_key")

    for name in ("context", "verification"):
        text = brief.get(name) or ""
        cuts: list[tuple[int, int, str]] = []

        def take(match, ok, replacement=""):
            span = match.span()
            if ok and not any(start < span[1] and span[0] < end for start, end, _ in cuts):
                removed.append(match.group(0).strip())
                cuts.append((span[0], span[1], replacement))
            else:
                unresolved.append(match.group(0).strip())

        for match in _INLINE.finditer(text):
            first = resolve(match["first"], match["first_effort"].lower())
            ladder = []
            for part in match["ladder"].split("->") if match["ladder"] else []:
                model, _, effort = part.strip().partition("@")
                ladder.append(resolve(model.strip(), effort.strip().lower()))
            resolved = first is not None and all(entry is not None for entry in ladder)
            keys = [entry.key for entry in ladder] if resolved else []
            accepted = resolved and (key_of("first_rung") in (None, first.key)) and (
                not routing["escalation"] or [rung["catalog_key"] for rung in routing["escalation"]] == keys)
            if accepted:
                if routing.get("first_rung") is None:
                    routing["first_rung"] = _rung_from(first).model_dump(mode="json")
                if not routing["escalation"]:
                    routing["escalation"] = [_rung_from(entry).model_dump(mode="json") for entry in ladder]
                if match["after"] and not routing.get("after_last_rung"):
                    after = match["after"].strip()
                    routing["after_last_rung"] = after[5:] if after.lower().startswith("then ") else after
            take(match, accepted, "." if match["lead"] else "")
        for match in _FIRST_SENTENCE.finditer(text):
            entry = resolve(match["name"], match["effort"].lower(), match["key"])
            ok = entry is not None and key_of("first_rung") in (None, entry.key)
            if ok and routing.get("first_rung") is None:
                routing["first_rung"] = _rung_from(entry, harness=(match["harness"] or "").strip()).model_dump(mode="json")
            take(match, ok)
        for match in _MOVES.finditer(text):
            entry = resolve(match["name"], (match["effort"] or "").lower() or None)
            ok = entry is not None and (not routing["escalation"] or [rung["catalog_key"] for rung in routing["escalation"]] == [entry.key])
            if ok and not routing["escalation"]:
                routing["escalation"] = [_rung_from(entry).model_dump(mode="json")]
                runs = match["runs"].lower()
                routing["escalate_after_failed_runs"] = _NUMBERS.get(runs) or int(runs)
            take(match, ok)
        for match in _REVIEWER.finditer(text):
            entry = resolve(match["name"], match["effort"].lower(), match["key"])
            ok = entry is not None and key_of("reviewer") in (None, entry.key)
            if ok and routing.get("reviewer") is None:
                routing["reviewer"] = _rung_from(entry, reviewer=True).model_dump(mode="json")
            take(match, ok)
        for match in _INDEPENDENT.finditer(text):
            entry = resolve(match["name"], (match["effort"] or "").lower() or None)
            ok = entry is not None and key_of("reviewer") in (None, entry.key)
            if ok:
                if routing.get("reviewer") is None:
                    routing["reviewer"] = _rung_from(entry, reviewer=True).model_dump(mode="json")
                if not routing["reviewer"].get("instructions"):
                    routing["reviewer"]["instructions"] = (match["instructions"] or "").strip()
            take(match, ok)
        for start, end, replacement in sorted(cuts, reverse=True):
            text = _cut(text, start, end, replacement)
        if cuts:
            cleaned[name] = text
    if routing.get("first_rung") is None:
        routing.pop("first_rung", None)
    return routing, cleaned, removed, unresolved


async def convert_text_routing(db, task, *, override: TaskRouting | None = None, apply: bool = False) -> RoutingConvertResponse:
    """Preview or apply moving a brief's free-text routing into structure, keeping every replaced sentence."""
    from app.schemas.task_brief import TaskBrief
    from app.services.task_brief_service import TaskBriefService, brief_payload, evidence_brief
    if task.brief is None:
        raise ValueError("Convert the task's description to a structured brief first")
    existing = task.brief.get("routing")
    entries = list((await catalog_entries(db)).values())
    parsed, cleaned, removed, unresolved = parse_text_routing(task.brief, entries, existing)
    if override is None and not removed:
        # Nothing to convert: the brief is left exactly as it is.
        return RoutingConvertResponse(task_id=task.id, already_structured=existing is not None,
                                      routing=TaskRouting.model_validate(existing) if existing else None,
                                      brief=task.brief, unresolved=unresolved, task_version=task.version)
    if override is not None:
        # The caller's routing settles what the parser could not; those sentences are replaced too.
        data = override.model_dump(mode="json")
        for sentence in unresolved:
            for name in ("context", "verification"):
                if sentence in (cleaned.get(name) or ""):
                    cleaned[name] = _remove_first(cleaned[name], sentence)
                    break
        removed, unresolved = removed + unresolved, []
    else:
        data = dict(parsed)
    data["source_text"] = list(dict.fromkeys(((existing or {}).get("source_text") or []) + removed))[:20]
    candidate = TaskRouting.model_validate(data)
    if candidate.first_rung is None and not candidate.escalation and candidate.reviewer is None:
        raise ValueError("The routing names no first rung, escalation or reviewer; nothing would be stored")
    routing = await resolve_routing(db, candidate)
    cleaned = {key: value for key, value in cleaned.items() if key != "routing"}
    proposed = TaskBrief.model_validate({**cleaned, "routing": routing.model_dump(mode="json")})
    check = await check_routing(db, task=task, project_id=task.project_id, assignee_id=task.assignee_id, routing=routing)
    payload = brief_payload(proposed)
    # Cutting sentences from the text is a substantive brief edit; only a routing-only change keeps progress.
    resets_progress = task.progress is not None and evidence_brief(payload) != evidence_brief(task.brief)
    response = RoutingConvertResponse(task_id=task.id, routing=routing, brief=payload, removed=removed,
                                      unresolved=unresolved, check=check, task_version=task.version, resets_progress=resets_progress)
    if apply:
        await TaskBriefService(db).apply_brief(task, proposed, provenance="routing_converted", enforce=False)
        notes = list(task.brief_migration_notes or [])
        notes += [f"Routing sentence kept as text: {sentence}" for sentence in unresolved]
        task.brief_migration_notes = list(dict.fromkeys(notes)) or None
        response.applied = True
        response.task_version = task.version
        _remember(db, task.id, check)
    return response
