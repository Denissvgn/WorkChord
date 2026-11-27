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


def _issues(routing: TaskRouting, models: AssigneeModels, entries, policy: bool) -> list[RoutingIssue]:
    issues: list[RoutingIssue] = []

    def add(code, severity, field_name, message, rung=None):
        issues.append(RoutingIssue(code=code, severity=severity, field=field_name, message=message,
                                   catalog_key=getattr(rung, "catalog_key", None), publisher_key=getattr(rung, "publisher_key", None)))

    for name, rungs in (("first_rung", [routing.first_rung] if routing.first_rung else []), ("escalation", routing.escalation),
                        ("reviewer", [routing.reviewer] if routing.reviewer else [])):
        for rung in rungs:
            entry = entries.get(rung.catalog_key)
            if entry is None or not entry.enabled:
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
    executing = set(models.publishers) | ({first.publisher_key} if first is not None and first.publisher_key else set())
    reviewer = routing.reviewer
    if reviewer is not None and reviewer.profile_id is not None and reviewer.profile_id == models.profile_id:
        add("reviewer_profile_is_assignee_profile", "conflict", "reviewer",
            "The reviewer profile is the assignee's profile; review needs a different profile.", reviewer)
    if reviewer is not None and first is not None and reviewer.catalog_key == first.catalog_key and not policy:
        add("reviewer_is_first_rung", "warning", "reviewer", "The reviewer is the model that executes the first rung.", reviewer)
    if policy:
        if reviewer is None:
            add("reviewer_missing", "warning", "reviewer", "The project requires a review publisher different from every contributor; name a reviewer.")
        elif not reviewer.publisher_key:
            add("reviewer_publisher_unknown", "conflict", "reviewer",
                f"The reviewer {reviewer.catalog_key} has no known publisher, so the project's publisher policy cannot be met.", reviewer)
        elif reviewer.publisher_key in executing:
            add("reviewer_shares_assignee_publisher", "conflict", "reviewer",
                f"The reviewer {reviewer.catalog_key} has the publisher {reviewer.publisher_key} of the assignee; "
                "the project requires a different review publisher.", reviewer)
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


async def suggest_routing(db, routing: TaskRouting, models: AssigneeModels, policy: bool, entries) -> TaskRouting | None:
    """A routing consistent with the assignee and policy that keeps as much of the current one as it can."""
    data = routing.model_copy(deep=True)
    first = data.first_rung
    old_publisher = first.publisher_key if first is not None else None
    if models.entries and (first is None or first.catalog_key not in models.keys):
        chosen = _choose_first_rung(models, first)
        data.first_rung = _rung_from(chosen)
        new_publisher = chosen.publisher_key
        ladder: list[RoutingRung] = []
        if old_publisher and old_publisher != new_publisher:
            # Rungs of the vendor the task moves away from become step-ups of the new first rung's vendor.
            catalog = await catalog_entries(db)
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
    first = data.first_rung
    executing = set(models.publishers) | ({first.publisher_key} if first is not None and first.publisher_key else set())
    reviewer = data.reviewer
    profile_clash = reviewer is not None and reviewer.profile_id is not None and reviewer.profile_id == models.profile_id
    if policy and (reviewer is None or not reviewer.publisher_key or reviewer.publisher_key in executing) or profile_clash:
        catalog = await catalog_entries(db)
        verifiers = await _verifier_profiles(db)
        ladder_publishers = {rung.publisher_key for rung in data.escalation}
        old_entry = catalog.get(reviewer.catalog_key) if reviewer is not None else None
        candidates = [entry for entry in catalog.values() if entry.enabled
                      and (not policy or entry.publisher_key and entry.publisher_key not in executing)
                      and (policy or reviewer is None or entry.key != (first.catalog_key if first else None))]

        def preference(entry):
            profiles = [profile for profile in verifiers.get(entry.key, []) if profile != models.profile_id]
            return (not profiles, entry.publisher_key in ladder_publishers, entry.publisher_key != old_publisher,
                    old_entry is None or entry.effort != old_entry.effort,
                    old_entry is None or entry.reasoning_tier != old_entry.reasoning_tier, entry.id)

        if candidates:
            chosen = min(candidates, key=preference)
            profiles = [profile for profile in verifiers.get(chosen.key, []) if profile != models.profile_id]
            data.reviewer = _rung_from(chosen, reviewer=True, profile_id=profiles[0] if len(profiles) == 1 else None,
                                       instructions=reviewer.instructions if reviewer is not None else "")
        elif profile_clash:
            data.reviewer = reviewer.model_copy(update={"profile_id": None})
    if data == routing:
        return None
    return data


async def check_routing(db, *, task_id=None, project_id, assignee_id, routing: dict | TaskRouting | None,
                        brief_text: str | None = None) -> RoutingCheck:
    """Check one routing against one assignee under the project's policy and offer a consistent one."""
    policy, mode = await project_policy(db, project_id)
    models = await assignee_models(db, assignee_id)
    check = RoutingCheck(task_id=task_id, assignee_id=assignee_id, assignee_profile_id=models.profile_id,
                         assignee_publishers=sorted(models.publishers), assignee_catalog_keys=sorted(models.keys),
                         different_publisher_required=policy, conflict_mode=mode)
    if routing is None:
        check.text_routing = bool(brief_text and _TEXT_ROUTING.search(brief_text))
        if check.text_routing:
            check.issues.append(RoutingIssue(code="routing_in_text", severity="warning", field="routing",
                message="The brief names its routing only in free text, which an assignee change does not update. Convert it to structured routing."))
        return check
    routing = routing if isinstance(routing, TaskRouting) else TaskRouting.model_validate(routing)
    entries = await catalog_entries(db, _routing_keys(routing))
    check.structured = True
    check.routing = routing
    check.issues = _issues(routing, models, entries, policy)
    check.consistent = not any(issue.severity == "conflict" for issue in check.issues)
    if check.issues:
        check.suggestion = await suggest_routing(db, routing, models, policy, entries)
        if check.suggestion is not None and check.suggestion.reviewer != routing.reviewer:
            check.suggested_reviewer = check.suggestion.reviewer
    return check


async def enforce_routing(db, task, *, resolution: str = "check", changed: bool) -> RoutingCheck | None:
    """Check the task's routing for its current assignee; apply the suggestion, refuse or warn.

    Runs only when the assignee or the routing changed, or when the caller asks to apply the
    suggestion. The result is kept on the task for its response.
    """
    if not changed and resolution != "apply_suggestion":
        return None
    from app.schemas.task_brief import TaskBrief
    from app.services.task_brief_service import TaskBriefService
    brief = task.brief or {}
    check = await check_routing(db, task_id=task.id, project_id=task.project_id, assignee_id=task.assignee_id,
                                routing=brief.get("routing"), brief_text=task.description)
    if resolution == "apply_suggestion" and check.suggestion is not None:
        updated = TaskBrief.model_validate({**brief, "routing": check.suggestion.model_dump(mode="json")})
        await TaskBriefService(db).apply_brief(task, updated, provenance="routing_suggestion", enforce=False)
        check = await check_routing(db, task_id=task.id, project_id=task.project_id, assignee_id=task.assignee_id,
                                    routing=task.brief.get("routing"), brief_text=task.description)
        check.applied = True
    if not check.consistent and check.conflict_mode == "refuse":
        raise RoutingConsistencyConflict(check)
    task.__dict__["_routing_check"] = check
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


def _tokens(value: str) -> list[str]:
    return [token for token in re.split(r"[^a-z0-9]+", value.lower()) if token]


def _subsequence(needle: list[str], haystack: list[str]) -> bool:
    iterator = iter(haystack)
    return all(token in iterator for token in needle)


class _Resolver:
    """Match a model named in prose to exactly one enabled catalog entry."""

    def __init__(self, entries):
        self.entries = [entry for entry in entries if entry.enabled]

    def __call__(self, name: str | None, effort: str | None, key: str | None = None):
        for label in (key, name):
            if label and label.strip():
                match = self._match(label.strip(), effort)
                if match is not None:
                    return match
        return None

    def _match(self, label: str, effort: str | None):
        lowered = label.lower()
        matches = [entry for entry in self.entries if lowered in (entry.key, entry.configured_model_alias.lower())]
        if not matches:
            words = _tokens(label)
            scored = []
            for entry in self.entries:
                best = max((len(_tokens(text)) for text in (entry.configured_model_alias, entry.key)
                            if _tokens(text) and _subsequence(_tokens(text), words)), default=0)
                if best:
                    scored.append((best, entry))
            if scored:
                top = max(score for score, _ in scored)
                matches = [entry for score, entry in scored if score == top]
        if len(matches) > 1 and effort and effort != "default":
            matches = [entry for entry in matches if entry.effort == effort]
        elif len(matches) > 1 and effort == "default":
            matches = [entry for entry in matches if entry.effort == "unknown"] or matches
        elif len(matches) == 1 and effort and effort not in ("default", matches[0].effort) and matches[0].effort != "unknown":
            matches = []
        return matches[0] if len(matches) == 1 else None


def _tidy(text: str) -> str:
    """Close the gaps a removed sentence leaves without touching the remaining lines."""
    return "\n".join(re.sub(r"  +", " ", line).rstrip() for line in text.split("\n")).strip()


def parse_text_routing(brief: dict, entries) -> tuple[dict, dict, list[str], list[str]]:
    """Parse routing sentences out of a brief's context and verification.

    Returns the routing data, the brief without the sentences it resolved, the resolved sentences
    and the routing sentences it kept because no single catalog entry matched.
    """
    resolve = _Resolver(entries)
    routing: dict = {"escalation": []}
    removed: list[str] = []
    unresolved: list[str] = []
    texts = {name: brief.get(name) or "" for name in ("context", "verification")}

    def take(name, match, ok, replacement=""):
        if ok:
            removed.append(match.group(0).strip())
            texts[name] = texts[name].replace(match.group(0), replacement, 1)
        else:
            unresolved.append(match.group(0).strip())

    for name in texts:
        for match in list(_INLINE.finditer(texts[name])):
            first = resolve(match["first"], match["first_effort"].lower())
            ladder = []
            for part in match["ladder"].split("->") if match["ladder"] else []:
                model, _, effort = part.strip().partition("@")
                ladder.append(resolve(model.strip(), effort.strip().lower()))
            accepted = first is not None and all(entry is not None for entry in ladder) and "first_rung" not in routing
            if accepted:
                routing["first_rung"] = _rung_from(first).model_dump(mode="json")
                routing["escalation"] = [_rung_from(entry).model_dump(mode="json") for entry in ladder]
                if match["after"]:
                    after = match["after"].strip()
                    routing["after_last_rung"] = after[5:] if after.lower().startswith("then ") else after
            take(name, match, accepted, "." if match["lead"] else "")
        for match in list(_FIRST_SENTENCE.finditer(texts[name])):
            entry = resolve(match["name"], match["effort"].lower(), match["key"])
            ok = entry is not None and "first_rung" not in routing
            if ok:
                routing["first_rung"] = _rung_from(entry, harness=(match["harness"] or "").strip()).model_dump(mode="json")
            take(name, match, ok)
        for match in list(_MOVES.finditer(texts[name])):
            entry = resolve(match["name"], (match["effort"] or "").lower() or None)
            ok = entry is not None and not routing["escalation"]
            if ok:
                routing["escalation"] = [_rung_from(entry).model_dump(mode="json")]
                runs = match["runs"].lower()
                routing["escalate_after_failed_runs"] = _NUMBERS.get(runs) or int(runs)
            take(name, match, ok)
        for match in list(_REVIEWER.finditer(texts[name])):
            entry = resolve(match["name"], match["effort"].lower(), match["key"])
            ok = entry is not None and "reviewer" not in routing
            if ok:
                routing["reviewer"] = _rung_from(entry, reviewer=True).model_dump(mode="json")
            take(name, match, ok)
        for match in list(_INDEPENDENT.finditer(texts[name])):
            entry = resolve(match["name"], (match["effort"] or "").lower() or None)
            current = routing.get("reviewer")
            ok = entry is not None and (current is None or current["catalog_key"] == entry.key)
            if ok:
                if current is None:
                    routing["reviewer"] = current = _rung_from(entry, reviewer=True).model_dump(mode="json")
                current["instructions"] = (match["instructions"] or "").strip().rstrip(".")
            take(name, match, ok)
    if routing.get("first_rung") is None:
        routing.pop("first_rung", None)
    cleaned = dict(brief)
    for name, text in texts.items():
        cleaned[name] = _tidy(text) if text != (brief.get(name) or "") else text
    return routing, cleaned, removed, unresolved


async def convert_text_routing(db, task, *, override: TaskRouting | None = None, apply: bool = False) -> RoutingConvertResponse:
    """Preview or apply moving a brief's free-text routing into structure, keeping every replaced sentence."""
    from app.schemas.task_brief import TaskBrief
    from app.services.task_brief_service import TaskBriefService
    if task.brief is None:
        raise ValueError("Convert the task's description to a structured brief first")
    if task.brief.get("routing") is not None and override is None:
        return RoutingConvertResponse(task_id=task.id, already_structured=True, routing=TaskRouting.model_validate(task.brief["routing"]),
                                      brief=task.brief, task_version=task.version)
    entries = list((await catalog_entries(db)).values())
    parsed, cleaned, removed, unresolved = parse_text_routing(task.brief, entries)
    if override is not None:
        # The caller's routing settles what the parser could not; those sentences are replaced too.
        data = override.model_dump(mode="json")
        for sentence in unresolved:
            for name in ("context", "verification"):
                if sentence in (cleaned.get(name) or ""):
                    cleaned[name] = _tidy(cleaned[name].replace(sentence, "", 1))
                    break
        removed, unresolved = removed + unresolved, []
    else:
        data = dict(parsed)
    data["source_text"] = list(dict.fromkeys(((task.brief.get("routing") or {}).get("source_text") or []) + removed))[:20]
    routing = await resolve_routing(db, TaskRouting.model_validate(data))
    cleaned = {key: value for key, value in cleaned.items() if key != "routing"}
    proposed = TaskBrief.model_validate({**cleaned, "routing": routing.model_dump(mode="json")})
    from app.services.task_brief_service import brief_payload
    check = await check_routing(db, task_id=task.id, project_id=task.project_id, assignee_id=task.assignee_id, routing=routing)
    response = RoutingConvertResponse(task_id=task.id, routing=routing, brief=brief_payload(proposed), removed=removed,
                                      unresolved=unresolved, check=check, task_version=task.version)
    if apply:
        await TaskBriefService(db).apply_brief(task, proposed, provenance="routing_converted", enforce=False)
        notes = list(task.brief_migration_notes or [])
        notes += [f"Routing sentence kept as text: {sentence}" for sentence in unresolved]
        task.brief_migration_notes = list(dict.fromkeys(notes)) or None
        response.applied = True
        response.task_version = task.version
        task.__dict__["_routing_check"] = check
    return response
