"""Add durable profile availability without changing the frozen initial schema."""

from alembic import op
import sqlalchemy as sa

revision = "20260930_0002"
down_revision = "20260928_0001"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("planning_state",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("revision", sa.Integer(), nullable=False),
        sa.CheckConstraint("id = 1 AND revision >= 0", name="ck_planning_state_singleton"))
    op.create_table("profile_availability",
        sa.Column("profile_id", sa.Integer(), sa.ForeignKey("team_member_profiles.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("calendar_id", sa.Integer(), sa.ForeignKey("calendars.id", ondelete="RESTRICT")),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("provenance", sa.String(40), nullable=False),
        sa.Column("calendar_conflicts", sa.JSON(), nullable=False),
        sa.CheckConstraint("version >= 1", name="ck_profile_availability_version"))
    op.create_table("profile_absences",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("profile_id", sa.Integer(), sa.ForeignKey("team_member_profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("end_date", sa.Date(), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("deleted", sa.Boolean(), nullable=False),
        sa.Column("provenance", sa.JSON(), nullable=False),
        sa.CheckConstraint("end_date >= start_date", name="ck_profile_absence_dates"),
        sa.CheckConstraint("version >= 1", name="ck_profile_absence_version"))
    op.create_index("ix_profile_absences_profile_id", "profile_absences", ["profile_id"])
    with op.batch_alter_table("vacations") as batch:
        batch.add_column(sa.Column("profile_absence_id", sa.Integer(), nullable=True))
        batch.create_foreign_key("fk_vacations_profile_absence", "profile_absences", ["profile_absence_id"], ["id"], ondelete="RESTRICT")
        batch.create_index("ix_vacations_profile_absence_id", ["profile_absence_id"])

    connection = op.get_bind()
    metadata = sa.MetaData()
    profiles, members, iterations, vacations, availability, absences, calendars = (
        sa.Table(name, metadata, autoload_with=connection) for name in (
            "team_member_profiles", "team_members", "iterations", "vacations",
            "profile_availability", "profile_absences", "calendars"))
    for profile_id in connection.scalars(sa.select(profiles.c.id)):
        rows = connection.execute(sa.select(calendars).join(iterations, iterations.c.calendar_id == calendars.c.id)
            .join(members, members.c.iteration_id == iterations.c.id).where(members.c.profile_id == profile_id)).mappings().all()
        # Calendar labels/IDs can differ while their actual working rules agree.
        signatures = {(row["year"], row["timezone"], row["nominal_day_hours"],
                       tuple(sorted(row["holidays"])), tuple(sorted(row["weekend_days"])),
                       tuple(sorted(row["short_days"]))) for row in rows}
        calendar_ids = sorted({row["id"] for row in rows})
        connection.execute(availability.insert().values(profile_id=profile_id,
            calendar_id=calendar_ids[0] if len(signatures) == 1 else None, version=1,
            provenance="legacy_allocations", calendar_conflicts=calendar_ids if len(signatures) > 1 else []))
        grouped = {}
        for row in connection.execute(sa.select(vacations).join(members, vacations.c.team_member_id == members.c.id)
                                      .where(members.c.profile_id == profile_id).order_by(vacations.c.id)).mappings():
            grouped.setdefault((row["start_date"], row["end_date"]), []).append(row["id"])
        for (start, end), ids in grouped.items():
            result = connection.execute(absences.insert().values(profile_id=profile_id, start_date=start,
                end_date=end, version=1, deleted=False, provenance=[{"legacy_vacation_ids": ids}]))
            connection.execute(vacations.update().where(vacations.c.id.in_(ids))
                               .values(profile_absence_id=result.inserted_primary_key[0]))


def downgrade():
    raise RuntimeError("Profile availability cannot be downgraded; restore a verified database backup.")
