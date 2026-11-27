"""Coherent, read-only planning observations for bounded JSON imports."""

from sqlalchemy import select
from app.authority import internal_authority
from app.commands import PlanningConflict
from app.models.iteration import Iteration
from app.services.planning_input_context import affected_iteration_ids


def import_file_sha256(data):
    """Digest of the canonical JSON form of one import file."""
    import hashlib
    import json
    return hashlib.sha256(json.dumps(data, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


async def import_scope_revisions(db, iteration_id, data):
    """Current revision of every iteration an import of this file reserves, under the caller's authority."""
    ids = await affected_iteration_ids(db, 'member', {'iteration_id': iteration_id, 'import_data': data})
    with internal_authority(db):
        return dict((await db.execute(select(Iteration.id, Iteration.revision)
            .where(Iteration.id.in_(ids)).order_by(Iteration.id))).all())


async def observe_import_planning(db, iteration_id, data):
    import json

    async def read():
        return await import_scope_revisions(db, iteration_id, data)

    before = await read()
    digest = import_file_sha256(data)
    if before != await read():
        raise PlanningConflict('planning_context_changed', 'Planning inputs changed during the import preview. Review the preview again.')
    if len(json.dumps(before, separators=(',', ':')).encode()) > 16384:
        raise PlanningConflict('planning_scope_oversized', 'The complete import revision context exceeds the supported header limit.')
    return {'expected_revisions': before, 'complete': True, 'file_sha256': digest}
