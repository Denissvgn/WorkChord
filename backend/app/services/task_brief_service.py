"""Canonical brief rendering, conservative legacy conversion and evidence commands."""

import re
from uuid import NAMESPACE_URL, uuid5

from sqlalchemy import func, select

from app.authority import AuthorityError, require_project
from app.commands import atomic_command
from app.models.task import Task
from app.models.task_brief import TaskBriefRevision, TaskProgressRecord, TaskReviewRecord
from app.schemas.task_brief import TaskBrief, ProgressWrite, TaskReviewWrite


HEADINGS = {
    "context and sources": "context", "контекст и источники": "context",
    "goal": "goal", "цель": "goal", "context": "context", "контекст": "context",
    "scope": "scope", "объем работ": "scope", "объём работ": "scope",
    "out of scope": "exclusions", "exclusions": "exclusions", "вне рамок": "exclusions",
    "acceptance criteria": "acceptance_criteria", "acceptance": "acceptance_criteria",
    "критерии приемки": "acceptance_criteria", "критерии приёмки": "acceptance_criteria",
    "verification": "verification", "проверка": "verification",
    "artifacts": "artifact_expectations", "expected artifacts": "artifact_expectations",
    "артефакты": "artifact_expectations",
}
LABELS = {
    "goal": "Goal", "context": "Context", "scope": "Scope", "exclusions": "Out of scope",
    "verification": "Verification", "artifact_expectations": "Expected artifacts",
}


def render_brief(brief: TaskBrief | dict) -> str:
    """Derive Markdown from canonical fields without projecting progress as acceptance."""
    data = brief.model_dump() if isinstance(brief, TaskBrief) else brief
    sections = []
    for field in ("goal", "context", "scope", "exclusions", "acceptance_criteria", "verification", "artifact_expectations"):
        if field == "acceptance_criteria":
            criteria = data.get(field, [])
            if criteria:
                lines = [f"- [ ] {item['text']}" + (f"\n  Verification: {item['verification']}" if item.get("verification") else "") for item in criteria]
                sections.append("## Acceptance criteria\n" + "\n".join(lines))
        elif data.get(field):
            sections.append(f"## {LABELS[field]}\n{data[field]}")
    return "\n\n".join(sections)


def brief_definition_blockers(brief: dict) -> list[str]:
    """Shared structured definition requirements for every agent projection."""
    blockers = [f"brief_{field}" for field in ("goal", "scope") if not brief.get(field, "").strip()]
    if not brief.get("acceptance_criteria"):
        blockers.append("brief_acceptance_criteria")
    if not brief.get("verification", "").strip() and not all(item.get("verification", "").strip() for item in brief.get("acceptance_criteria", [])):
        blockers.append("brief_verification")
    return blockers


def import_legacy_brief(task_id: int, description: str | None) -> tuple[TaskBrief, list[str]]:
    """Conservatively parse supported headings and preserve every unparsed line."""
    original = description or ""
    if len(original) > 100_000:
        raise ValueError("Legacy description exceeds the 100000 character conversion limit")
    fields: dict = {"acceptance_criteria": []}
    blocks: dict[str, list[str]] = {}
    notes: list[str] = []
    section = "context"
    occurrence: dict[str, int] = {}
    fence = None
    for line in original.splitlines():
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})", line)
        if marker or fence is not None:
            blocks.setdefault("context", []).append(line)
            if marker:
                if fence is None:
                    fence = marker[1][0]
                    notes.append("Code blocks were retained as context; review their examples separately.")
                elif marker[1][0] == fence:
                    fence = None
            continue
        heading = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if heading:
            label = heading[1].strip().rstrip(":").casefold()
            if label in HEADINGS:
                section = HEADINGS[label]
                continue
            notes.append(f"Unrecognized heading retained: {heading[1]}")
            section = "context"
        checkbox = re.match(r"^([-*])\s+\[([ xX])\]\s+(.+)$", line)
        bullet = re.match(r"^[-*]\s+(.+)$", line) if section == "acceptance_criteria" else None
        if checkbox or bullet:
            if section != "acceptance_criteria":
                notes.append("Checklist items outside acceptance sections are proposed criteria and need review.")
            text = checkbox[3] if checkbox else bullet[1]
            occurrence[text] = occurrence.get(text, 0) + 1
            fields["acceptance_criteria"].append({
                "id": uuid5(NAMESPACE_URL, f"workchord:task:{task_id}:criterion:{text}:{occurrence[text]}").hex,
                "text": text, "revision": 1,
            })
            if checkbox and checkbox[2].lower() == "x":
                notes.append("Legacy checkmarks were retained in the original text; they do not establish acceptance.")
        else:
            if re.match(r"^\s+[-*]\s", line):
                notes.append("Nested list content needs review and was retained in context.")
            if section == "acceptance_criteria" and line.strip():
                notes.append("Unparsed acceptance text was retained in context and needs review.")
            target = "context" if section == "acceptance_criteria" else section
            blocks.setdefault(target, []).append(line)
    fields.update({key: "\n".join(lines).strip() for key, lines in blocks.items()})
    return TaskBrief.model_validate(fields), list(dict.fromkeys(notes))


def clear_acceptance(task: Task) -> None:
    """Invalidate the current projection while immutable verdict history remains."""
    task.accepted_at = task.accepted_by_principal_id = task.accepted_version = None


def clear_execution_evidence(task: Task) -> None:
    """A changed execution context needs fresh progress; history remains immutable."""
    task.progress = None
    clear_acceptance(task)


def brief_from_draft(draft, *, title=None, context=None) -> TaskBrief:
    """Project old draft/template fields into the canonical input contract."""
    from app.schemas.task_brief import BriefCriterion
    def value(key, default=None):
        return draft.get(key, default) if isinstance(draft, dict) else getattr(draft, key, default)
    def lines(key):
        items = value(key, []) or []
        return "\n".join(f"- {item}" for item in items) if isinstance(items, list) else str(items)
    context_parts = [context if context is not None else value("description", "") or ""]
    for key, label in (("suggested_checklist", "Implementation checklist"), ("risks", "Risks"),
                       ("implementation_notes", "Implementation notes"), ("open_questions", "Open questions")):
        if lines(key):
            context_parts.append(f"## {label}\n{lines(key)}")
    return TaskBrief(goal=title or value("title", "") or "", context="\n\n".join(part for part in context_parts if part),
        scope=lines("scope"), exclusions=lines("out_of_scope"), verification=lines("verification"), artifact_expectations=lines("expected_artifacts"),
        acceptance_criteria=[BriefCriterion(text=item) for item in value("acceptance_criteria", []) or []])


class TaskBriefService:
    def __init__(self, db):
        self.db = db

    @property
    def tasks(self):
        from app.services.task_service import TaskService
        return TaskService(self.db)

    async def apply_brief(self, task: Task, brief: TaskBrief, *, provenance="structured") -> bool:
        """Apply one canonical representation under the task command's existing fence."""
        require_project(self.db, task.project_id, "edit")
        previous = task.brief or {}
        old = {item["id"]: item for item in previous.get("acceptance_criteria", [])}
        payload = brief.model_dump(mode="json")
        for criterion in payload["acceptance_criteria"]:
            prior = old.get(criterion["id"])
            if prior:
                material = any(prior.get(key, "") != criterion[key] for key in ("text", "verification"))
                if criterion["revision"] != prior["revision"]:
                    raise ValueError("Use the current criterion revision; the server increments it when its content changes")
                criterion["revision"] = prior["revision"] + int(material)
            elif criterion["revision"] != 1:
                raise ValueError("A new criterion starts at revision 1")
        if payload == task.brief:
            return False
        if task.brief is None:
            task.legacy_description = task.description
            if task.description:
                try:
                    _, task.brief_migration_notes = import_legacy_brief(task.id, task.description)
                except ValueError:
                    task.brief_migration_notes = ["Original text retained; automatic conversion was not available."]
        await self.tasks.reserve_task_version(task, task.version)
        task.brief = payload
        task.brief_revision = max(task.brief_revision or 0, await self.db.scalar(select(func.max(TaskBriefRevision.revision)).where(TaskBriefRevision.original_task_id == task.id)) or 0) + 1
        task.brief_provenance = provenance
        task.description = render_brief(payload)
        task.progress = None
        clear_acceptance(task)
        self.db.add(TaskBriefRevision(task_id=task.id, original_task_id=task.id, revision=task.brief_revision, task_version=task.version,
            principal_id=getattr(self.db.info.get("authority"), "principal_id", None), payload=payload, provenance=provenance))
        await self.tasks.record_task_event(task.id, "brief_changed", {"brief_revision": task.brief_revision, "version": task.version, "provenance": provenance})
        return True

    async def restore_brief(self, task, snapshot):
        """Keep restored legacy images inside an already adopted canonical boundary."""
        import copy
        payload = copy.deepcopy(snapshot.get("brief"))
        if payload is None:
            if task.brief is None:
                return
            imported, notes = import_legacy_brief(task.id, snapshot.get("description"))
            payload = imported.model_dump(mode="json")
            task.brief_migration_notes = notes
        current_criteria = {criterion["id"]: criterion["revision"] for criterion in (task.brief or {}).get("acceptance_criteria", [])}
        for criterion in payload.get("acceptance_criteria", []):
            criterion["revision"] = current_criteria.get(criterion["id"], 1)
        await self.apply_brief(task, TaskBrief.model_validate(payload), provenance="restored")
        task.description = render_brief(task.brief)
        if "legacy_description" in snapshot:
            task.legacy_description = snapshot["legacy_description"]

    @atomic_command
    async def write(self, task_id, data):
        task = await self._locked(task_id, data.expected_version)
        await self.apply_brief(task, data.brief)
        await self.db.flush()
        return await self.tasks.get_by_id(task_id)

    async def conversion(self, task_id, data):
        task = await self.tasks.get_by_id(task_id)
        if task is None:
            raise ValueError("Task not found or inaccessible")
        self.tasks.ensure_expected_version(task, data.expected_version)
        if task.brief is not None:
            return {"brief": task.brief, "notes": task.brief_migration_notes or [], "already_converted": True}
        brief, notes = import_legacy_brief(task.id, task.description)
        if data.apply:
            from app.commands import command_transaction
            async with command_transaction(self.db):
                task = await self._locked(task_id, data.expected_version)
                brief, notes = import_legacy_brief(task.id, task.description)
                await self.apply_brief(task, brief, provenance="legacy_converted")
                task.brief_migration_notes = notes
        return {"brief": brief.model_dump(mode="json"), "notes": notes, "already_converted": False}

    async def _locked(self, task_id, version):
        await self.tasks._lock_task_scope(task_id)
        task = await self.tasks.get_by_id(task_id)
        if task is None:
            raise ValueError("Task not found or inaccessible")
        self.tasks.ensure_expected_version(task, version)
        from app.services.snapshot_service import SnapshotService
        await SnapshotService(self.db).create_snapshot(task.iteration_id, "before_brief_command")
        return task

    @atomic_command
    async def write_progress(self, task_id: int, data: ProgressWrite, *, fenced_submission=False):
        task = await self._locked(task_id, data.expected_version)
        require_project(self.db, task.project_id, "execute")
        authority = self.db.info.get("authority")
        if authority and authority.kind == "agent" and not fenced_submission:
            raise AuthorityError("agent_protocol_required", "Submit criterion evidence through assigned work with its current claim fence.")
        if task.canceled_at or task.status == "closed" or task.is_summary:
            raise ValueError("Progress requires open leaf work")
        criteria = {item["id"]: item for item in (task.brief or {}).get("acceptance_criteria", [])}
        for item in data.criteria:
            if item.criterion_id not in criteria or criteria[item.criterion_id]["revision"] != item.criterion_revision:
                raise ValueError("Progress references a missing or stale criterion")
            if item.state == "completed" and not item.evidence.strip():
                raise ValueError("Completed criteria require evidence")
        await self.tasks.reserve_task_version(task, data.expected_version)
        task.artifact_revision = max(task.artifact_revision or 0, await self.db.scalar(select(func.max(TaskProgressRecord.artifact_revision)).where(TaskProgressRecord.original_task_id == task.id)) or 0) + 1
        task.progress = {"criteria": [item.model_dump() for item in data.criteria], "artifacts": data.artifacts,
                         "brief_revision": task.brief_revision, "artifact_revision": task.artifact_revision}
        clear_acceptance(task)
        self.db.add(TaskProgressRecord(task_id=task.id, original_task_id=task.id, task_version=task.version, brief_revision=task.brief_revision,
            artifact_revision=task.artifact_revision, principal_id=getattr(self.db.info.get("authority"), "principal_id", None), payload=task.progress))
        await self.tasks.record_task_event(task.id, "criterion_progress_recorded", {"artifact_revision": task.artifact_revision, "version": task.version})
        await self.db.flush()
        return task

    async def require_review(self, task: Task, *, accepting: bool):
        """One independence and evidence boundary for human and assigned-agent review."""
        require_project(self.db, task.project_id, "review")
        authority = self.db.info.get("authority")
        principal = getattr(authority, "principal_id", None)
        override = bool(authority and authority.operator and authority.review_override and authority.reason)
        if authority and authority.kind == "agent" and authority.actor_role != "verifier":
            raise AuthorityError("independent_review_required", "Execution cannot accept its own work.")
        progress_author = await self.db.scalar(select(TaskProgressRecord.principal_id).where(TaskProgressRecord.original_task_id == task.id,
            TaskProgressRecord.artifact_revision == task.artifact_revision)) if task.artifact_revision else None
        if principal is not None and principal in {task.executed_by_principal_id, progress_author} and not override:
            raise AuthorityError("independent_review_required", "Another reviewer must review this work.")
        if task.canceled_at or task.is_summary or task.status != "resolved":
            raise ValueError("Review requires resolved, uncanceled leaf work")
        if not accepting:
            return
        from app.models.autonomy import AgentWorkPackage
        package = await self.db.scalar(select(AgentWorkPackage).where(AgentWorkPackage.execution_task_id == task.id)
            .order_by(AgentWorkPackage.id.desc()).limit(1))
        if package is not None and package.state != "passed":
            raise AuthorityError("package_verification_required", "The authoritative work package must pass its verification protocol.")
        if task.brief and package is not None:
            from app.autonomy.canonical import sha256_hex
            if (package.task_context_version, package.task_brief_revision, package.task_artifact_revision, package.task_brief_digest) != (task.version, task.brief_revision, task.artifact_revision, sha256_hex(task.brief)):
                raise AuthorityError("package_context_stale", "Work-package verification is bound to another task, brief or artifact revision.")
        if task.brief and not override:
            progress = task.progress or {}
            if progress.get("brief_revision") != task.brief_revision:
                raise ValueError("Current brief evidence is required before acceptance")
            reported = {item["criterion_id"]: item for item in progress.get("criteria", [])}
            for criterion in task.brief.get("acceptance_criteria", []):
                item = reported.get(criterion["id"], {})
                if item.get("criterion_revision") != criterion["revision"] or item.get("state") != "completed" or not item.get("evidence", "").strip():
                    raise ValueError("Every current criterion requires completed progress and evidence")

    async def record_review(self, task, *, verdict, reason, evidence=""):
        record = TaskReviewRecord(task_id=task.id, original_task_id=task.id, task_version=task.version, brief_revision=task.brief_revision,
            artifact_revision=task.artifact_revision, principal_id=getattr(self.db.info.get("authority"), "principal_id", None),
            verdict=verdict, reason=reason, evidence=evidence)
        self.db.add(record)
        return record

    @atomic_command
    async def review(self, task_id: int, data: TaskReviewWrite):
        task = await self._locked(task_id, data.expected_version)
        authority = self.db.info.get("authority")
        if authority and authority.kind == "agent":
            raise AuthorityError("agent_protocol_required", "Use the assigned verification command.")
        if (task.brief_revision, task.artifact_revision) != (data.brief_revision, data.artifact_revision):
            raise ValueError("Brief or artifact revision is stale")
        await self.require_review(task, accepting=data.verdict == "accept")
        task, _, _ = await self.tasks.change_status(task.id, "closed" if data.verdict == "accept" else "active",
            reason=data.reason, expected_version=task.version, review_evidence=data.evidence, review_rework=data.verdict == "reject", commit=False)
        if data.verdict == "reject":
            await self.record_review(task, verdict="reject", reason=data.reason, evidence=data.evidence)
        return task
