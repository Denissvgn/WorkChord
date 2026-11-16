"""Accept agdash session links as an external link provider."""

from alembic import op


revision = "20261116_0015"
down_revision = "20261115_0014"
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table("external_links") as batch:
        batch.drop_constraint("ck_external_links_provider", type_="check")
        batch.create_check_constraint(
            "ck_external_links_provider",
            "provider IN ('github', 'gitlab', 'figma', 'sentry', 'custom', 'agdash')",
        )


def downgrade():
    raise RuntimeError("The agdash link provider cannot be downgraded; restore the matching verified backup")
