"""Create the complete initial WorkChord schema.

This revision is a frozen schema definition. Future changes belong in new
revisions; importing application model metadata here would change history.
Schema creation does not seed identities, settings, or other application rows.
"""

from alembic import op
import sqlalchemy as sa

revision = "20260928_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create tables and indexes without data backfills.
    op.create_table('agent_model_catalog_entries',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('key', sa.String(length=120), nullable=False),
    sa.Column('provider', sa.String(length=120), nullable=False),
    sa.Column('configured_model_alias', sa.String(length=255), nullable=False),
    sa.Column('reasoning_tier', sa.Integer(), nullable=False),
    sa.Column('context_tier', sa.String(length=20), nullable=False),
    sa.Column('modality_tags', sa.JSON(), server_default=sa.text('\'["text"]\''), nullable=False),
    sa.Column('cost_tier', sa.String(length=20), nullable=False),
    sa.Column('latency_tier', sa.String(length=20), nullable=False),
    sa.Column('enabled', sa.Boolean(), server_default=sa.true(), nullable=False),
    sa.Column('revision', sa.Integer(), server_default=sa.text("'1'"), nullable=False),
    sa.Column('last_verified_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.CheckConstraint("context_tier IN ('small', 'medium', 'large')", name='ck_agent_model_catalog_context_tier'),
    sa.CheckConstraint("cost_tier IN ('low', 'medium', 'high')", name='ck_agent_model_catalog_cost_tier'),
    sa.CheckConstraint("latency_tier IN ('fast', 'balanced', 'slow')", name='ck_agent_model_catalog_latency_tier'),
    sa.CheckConstraint('key = lower(trim(key))', name='ck_agent_model_catalog_key_canonical'),
    sa.CheckConstraint('length(trim(configured_model_alias)) > 0', name='ck_agent_model_catalog_alias_not_blank'),
    sa.CheckConstraint('length(trim(key)) > 0', name='ck_agent_model_catalog_key_not_blank'),
    sa.CheckConstraint('length(trim(provider)) > 0', name='ck_agent_model_catalog_provider_not_blank'),
    sa.CheckConstraint('reasoning_tier >= 1 AND reasoning_tier <= 3', name='ck_agent_model_catalog_reasoning_tier'),
    sa.CheckConstraint('revision >= 1', name='ck_agent_model_catalog_revision'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key', name='uq_agent_model_catalog_key')
    )
    op.create_index('ix_agent_model_catalog_enabled', 'agent_model_catalog_entries', ['enabled'], unique=False)
    op.create_table('calendars',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('year', sa.Integer(), nullable=False),
    sa.Column('holidays', sa.JSON(), nullable=False),
    sa.Column('weekend_days', sa.JSON(), nullable=False),
    sa.Column('short_days', sa.JSON(), nullable=False),
    sa.Column('timezone', sa.String(length=64), server_default=sa.text("'UTC'"), nullable=False),
    sa.Column('nominal_day_hours', sa.Float(), server_default=sa.text("'8'"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('database_migration_gates',
    sa.Column('run_id', sa.String(length=64), nullable=False),
    sa.Column('source_manifest_sha256', sa.String(length=64), nullable=False),
    sa.Column('source_snapshot_sha256', sa.String(length=64), nullable=False),
    sa.Column('target_identity_sha256', sa.String(length=64), nullable=False),
    sa.Column('status', sa.String(length=30), nullable=False),
    sa.Column('completed_tables', sa.JSON(), nullable=False),
    sa.Column('failure_code', sa.String(length=120), nullable=True),
    sa.Column('raw_report_sha256', sa.String(length=64), nullable=True),
    sa.Column('reconciliation_report_sha256', sa.String(length=64), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("status IN ('loading', 'loaded', 'reconciling', 'raw_reconciled', 'reconciled', 'failed')", name='ck_database_migration_gates_status'),
    sa.PrimaryKeyConstraint('run_id')
    )
    op.create_index('ix_database_migration_gates_status', 'database_migration_gates', ['status'], unique=False)
    op.create_table('external_links',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('entity_type', sa.String(length=50), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=False),
    sa.Column('provider', sa.String(length=50), nullable=False),
    sa.Column('external_key', sa.String(length=255), nullable=True),
    sa.Column('url', sa.String(length=1000), nullable=True),
    sa.Column('title', sa.String(length=500), nullable=True),
    sa.Column('status', sa.String(length=100), nullable=True),
    sa.Column('metadata_json', sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.CheckConstraint("entity_type IN ('task', 'project', 'release')", name='ck_external_links_entity_type'),
    sa.CheckConstraint("provider IN ('github', 'gitlab', 'figma', 'sentry', 'custom')", name='ck_external_links_provider'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_external_links_entity', 'external_links', ['entity_type', 'entity_id'], unique=False)
    op.create_index('ix_external_links_provider_key', 'external_links', ['provider', 'external_key'], unique=False)
    op.create_index('ix_external_links_updated_at', 'external_links', ['updated_at'], unique=False)
    op.create_index('ix_external_links_url', 'external_links', ['url'], unique=False)
    op.create_table('github_status_automation_rules',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('enabled', sa.Boolean(), server_default=sa.false(), nullable=False),
    sa.Column('github_event_type', sa.String(length=100), nullable=False),
    sa.Column('from_status', sa.String(length=50), nullable=True),
    sa.Column('target_status', sa.String(length=50), nullable=False),
    sa.Column('reason_template', sa.Text(), nullable=True),
    sa.Column('sort_order', sa.Integer(), server_default=sa.text('0'), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.CheckConstraint("from_status IS NULL OR from_status IN ('planned', 'active', 'resolved', 'closed')", name='ck_github_status_rules_from_status'),
    sa.CheckConstraint("github_event_type IN ('github_pr_opened', 'github_pr_reopened', 'github_pr_ready_for_review', 'github_pr_synchronize', 'github_pr_closed', 'github_pr_merged')", name='ck_github_status_rules_event_type'),
    sa.CheckConstraint("target_status IN ('active', 'resolved', 'closed')", name='ck_github_status_rules_target_status'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_github_status_rules_event_enabled', 'github_status_automation_rules', ['github_event_type', 'enabled'], unique=False)
    op.create_index('ix_github_status_rules_sort', 'github_status_automation_rules', ['sort_order', 'id'], unique=False)
    op.create_table('initiatives',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('health', sa.String(length=50), server_default=sa.text("'unknown'"), nullable=False),
    sa.Column('target_date', sa.Date(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('owner_profile_id', sa.Integer(), nullable=True),
    sa.CheckConstraint("health IN ('unknown', 'on_track', 'at_risk', 'off_track')", name='ck_initiatives_health'),
    sa.ForeignKeyConstraint(['owner_id'], ['team_members.id'], name='fk_initiatives_owner_id', ondelete='SET NULL', use_alter=True),
    sa.ForeignKeyConstraint(['owner_profile_id'], ['team_member_profiles.id'], name='fk_initiatives_owner_profile_id_team_member_profiles', ondelete='SET NULL', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_initiatives_health', 'initiatives', ['health'], unique=False)
    op.create_index('ix_initiatives_owner_id', 'initiatives', ['owner_id'], unique=False)
    op.create_index('ix_initiatives_owner_profile_id', 'initiatives', ['owner_profile_id'], unique=False)
    op.create_index('ix_initiatives_target_date', 'initiatives', ['target_date'], unique=False)
    op.create_index('ix_initiatives_target_name', 'initiatives', ['target_date', 'name', 'id'], unique=False)
    op.create_table('iterations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('manager_email', sa.String(length=255), nullable=True),
    sa.Column('calendar_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('revision', sa.Integer(), server_default=sa.text("'1'"), nullable=False),
    sa.ForeignKeyConstraint(['calendar_id'], ['calendars.id'], name='fk_iterations_calendar_id', use_alter=True),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], name='fk_iterations_project_id_projects', ondelete='SET NULL', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_iterations_project_id', 'iterations', ['project_id'], unique=False)
    op.create_table('label_groups',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('key', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('color', sa.String(length=7), server_default=sa.text("'#64748b'"), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default=sa.true(), nullable=False),
    sa.Column('sort_order', sa.Integer(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('seed_key', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key', name='uq_label_groups_key')
    )
    op.create_index('ix_label_groups_active_order', 'label_groups', ['is_active', 'sort_order'], unique=False)
    op.create_index('ix_label_groups_created_at', 'label_groups', ['created_at'], unique=False)
    op.create_index('ix_label_groups_is_active', 'label_groups', ['is_active'], unique=False)
    op.create_index('ix_label_groups_key', 'label_groups', ['key'], unique=False)
    op.create_index('ix_label_groups_seed_key', 'label_groups', ['seed_key'], unique=1)
    op.create_index('ix_label_groups_sort_order', 'label_groups', ['sort_order'], unique=False)
    op.create_index('ix_label_groups_updated_at', 'label_groups', ['updated_at'], unique=False)
    op.create_table('oidc_login_attempts',
    sa.Column('state_hash', sa.String(length=64), nullable=False),
    sa.Column('browser_hash', sa.String(length=64), nullable=False),
    sa.Column('nonce', sa.String(length=128), nullable=False),
    sa.Column('verifier', sa.String(length=128), nullable=False),
    sa.Column('return_path', sa.String(length=512), nullable=False),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('consumed_at', sa.DateTime(timezone=True), nullable=True),
    sa.PrimaryKeyConstraint('state_hash')
    )
    op.create_index('ix_oidc_login_attempts_expires_at', 'oidc_login_attempts', ['expires_at'], unique=False)
    op.create_table('outbound_webhook_events',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('event_id', sa.String(length=64), nullable=False),
    sa.Column('event_type', sa.String(length=120), nullable=False),
    sa.Column('entity_type', sa.String(length=80), nullable=False),
    sa.Column('entity_id', sa.Integer(), nullable=True),
    sa.Column('payload_json', sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('occurred_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('event_id', name='uq_outbound_webhook_events_event_id')
    )
    op.create_index('ix_outbound_webhook_events_entity', 'outbound_webhook_events', ['entity_type', 'entity_id'], unique=False)
    op.create_index('ix_outbound_webhook_events_entity_id', 'outbound_webhook_events', ['entity_id'], unique=False)
    op.create_index('ix_outbound_webhook_events_entity_type', 'outbound_webhook_events', ['entity_type'], unique=False)
    op.create_index('ix_outbound_webhook_events_event_id', 'outbound_webhook_events', ['event_id'], unique=False)
    op.create_index('ix_outbound_webhook_events_event_type', 'outbound_webhook_events', ['event_type'], unique=False)
    op.create_index('ix_outbound_webhook_events_occurred_at', 'outbound_webhook_events', ['occurred_at'], unique=False)
    op.create_index('ix_outbound_webhook_events_type_time', 'outbound_webhook_events', ['event_type', 'occurred_at'], unique=False)
    op.create_table('outbound_webhook_targets',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('url', sa.String(length=1000), nullable=False),
    sa.Column('enabled', sa.Boolean(), server_default=sa.true(), nullable=False),
    sa.Column('subscribed_events_json', sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
    sa.Column('secret', sa.String(length=500), nullable=True),
    sa.Column('headers_json', sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_outbound_webhook_targets_created_at', 'outbound_webhook_targets', ['created_at'], unique=False)
    op.create_index('ix_outbound_webhook_targets_enabled', 'outbound_webhook_targets', ['enabled'], unique=False)
    op.create_index('ix_outbound_webhook_targets_updated_at', 'outbound_webhook_targets', ['updated_at'], unique=False)
    op.create_table('projects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=50), server_default=sa.text("'planned'"), nullable=False),
    sa.Column('health', sa.String(length=50), server_default=sa.text("'unknown'"), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('target_date', sa.Date(), nullable=True),
    sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('sort_order', sa.Integer(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=True),
    sa.Column('initiative_id', sa.Integer(), nullable=True),
    sa.Column('owner_profile_id', sa.Integer(), nullable=True),
    sa.Column('timezone', sa.String(length=64), server_default=sa.text("'UTC'"), nullable=False),
    sa.ForeignKeyConstraint(['initiative_id'], ['initiatives.id'], name='fk_projects_initiative_id_initiatives', ondelete='SET NULL', use_alter=True),
    sa.ForeignKeyConstraint(['owner_id'], ['team_members.id'], name='fk_projects_owner_id', ondelete='SET NULL', use_alter=True),
    sa.ForeignKeyConstraint(['owner_profile_id'], ['team_member_profiles.id'], name='fk_projects_owner_profile_id_team_member_profiles', ondelete='SET NULL', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_projects_health', 'projects', ['health'], unique=False)
    op.create_index('ix_projects_initiative_id', 'projects', ['initiative_id'], unique=False)
    op.create_index('ix_projects_owner_id', 'projects', ['owner_id'], unique=False)
    op.create_index('ix_projects_owner_profile_id', 'projects', ['owner_profile_id'], unique=False)
    op.create_index('ix_projects_status', 'projects', ['status'], unique=False)
    op.create_index('ix_projects_target_date', 'projects', ['target_date'], unique=False)
    op.create_table('request_sources',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=500), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('source_type', sa.String(length=50), nullable=False),
    sa.Column('source_name', sa.String(length=255), nullable=True),
    sa.Column('source_url', sa.String(length=1000), nullable=True),
    sa.Column('external_key', sa.String(length=255), nullable=True),
    sa.Column('priority_hint', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.CheckConstraint("source_type IN ('customer', 'internal', 'support', 'email', 'web', 'import')", name='ck_request_sources_source_type'),
    sa.CheckConstraint('priority_hint IS NULL OR (priority_hint >= 1 AND priority_hint <= 10)', name='ck_request_sources_priority_hint_range'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_request_sources_created_at', 'request_sources', ['created_at'], unique=False)
    op.create_index('ix_request_sources_external_key', 'request_sources', ['external_key'], unique=False)
    op.create_index('ix_request_sources_source_type', 'request_sources', ['source_type'], unique=False)
    op.create_index('ix_request_sources_source_url', 'request_sources', ['source_url'], unique=False)
    op.create_table('system_settings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('key', sa.String(length=120), nullable=False),
    sa.Column('category', sa.String(length=80), nullable=False),
    sa.Column('value_json', sa.JSON(), nullable=True),
    sa.Column('secret_ciphertext', sa.Text(), nullable=True),
    sa.Column('is_secret', sa.Boolean(), server_default=sa.false(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('key', name='uq_system_settings_key')
    )
    op.create_index('ix_system_settings_category', 'system_settings', ['category'], unique=False)
    op.create_index('ix_system_settings_category_key', 'system_settings', ['category', 'key'], unique=False)
    op.create_index('ix_system_settings_key', 'system_settings', ['key'], unique=False)
    op.create_table('task_deletion_fences',
    sa.Column('original_task_id', sa.Integer(), autoincrement=False, nullable=False),
    sa.Column('last_version', sa.Integer(), nullable=False),
    sa.CheckConstraint('last_version >= 1', name='ck_task_deletion_fence_version'),
    sa.PrimaryKeyConstraint('original_task_id')
    )
    op.create_table('team_member_profiles',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('display_name', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('headline', sa.String(length=255), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('automation_enabled', sa.Boolean(), server_default=sa.true(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('seed_key', sa.String(length=120), nullable=True),
    sa.Column('profile_kind', sa.String(length=30), server_default=sa.text("'human'"), nullable=False),
    sa.Column('assignment_modes', sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_team_member_profiles_automation_enabled', 'team_member_profiles', ['automation_enabled'], unique=False)
    op.create_index('ix_team_member_profiles_display_name', 'team_member_profiles', ['display_name'], unique=False)
    op.create_index('ix_team_member_profiles_email', 'team_member_profiles', ['email'], unique=False)
    op.create_index('ix_team_member_profiles_seed_key', 'team_member_profiles', ['seed_key'], unique=1)
    op.create_table('team_members',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('position', sa.String(length=255), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('availability_percent', sa.Float(), nullable=False),
    sa.Column('professionalism_coefficient', sa.Float(), nullable=False),
    sa.Column('operational_utilization', sa.Float(), nullable=False),
    sa.Column('iteration_id', sa.Integer(), nullable=True),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['iteration_id'], ['iterations.id'], name='fk_team_members_iteration_id', ondelete='SET NULL', use_alter=True),
    sa.ForeignKeyConstraint(['profile_id'], ['team_member_profiles.id'], name='fk_team_members_profile_id_team_member_profiles', ondelete='SET NULL', use_alter=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_team_members_profile_id', 'team_members', ['profile_id'], unique=False)
    op.create_table('work_templates',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('template_type', sa.String(length=50), nullable=False),
    sa.Column('default_title', sa.String(length=500), nullable=True),
    sa.Column('default_description', sa.Text(), nullable=True),
    sa.Column('default_priority', sa.Integer(), nullable=True),
    sa.Column('default_effort_days', sa.Float(), nullable=True),
    sa.Column('default_labels', sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
    sa.Column('default_checklist', sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
    sa.Column('default_payload', sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default=sa.true(), nullable=False),
    sa.Column('sort_order', sa.Integer(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('seed_key', sa.String(length=100), nullable=True),
    sa.CheckConstraint("template_type IN ('task', 'project', 'triage')", name='ck_work_templates_template_type'),
    sa.CheckConstraint('default_effort_days IS NULL OR default_effort_days >= 0.1', name='ck_work_templates_default_effort_days_min'),
    sa.CheckConstraint('default_priority IS NULL OR (default_priority >= 1 AND default_priority <= 10)', name='ck_work_templates_default_priority_range'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_work_templates_created_at', 'work_templates', ['created_at'], unique=False)
    op.create_index('ix_work_templates_is_active', 'work_templates', ['is_active'], unique=False)
    op.create_index('ix_work_templates_seed_key', 'work_templates', ['seed_key'], unique=1)
    op.create_index('ix_work_templates_sort_order', 'work_templates', ['sort_order'], unique=False)
    op.create_index('ix_work_templates_template_type', 'work_templates', ['template_type'], unique=False)
    op.create_index('ix_work_templates_type_active_order', 'work_templates', ['template_type', 'is_active', 'sort_order'], unique=False)
    op.create_index('ix_work_templates_updated_at', 'work_templates', ['updated_at'], unique=False)
    op.create_table('agent_actors',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('display_name', sa.String(length=255), nullable=False),
    sa.Column('api_key_hash', sa.String(length=128), nullable=False),
    sa.Column('scopes', sa.Text(), server_default=sa.text("'[]'"), nullable=False),
    sa.Column('enabled', sa.Boolean(), server_default=sa.true(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('last_seen_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('role', sa.String(length=30), server_default=sa.text("'worker'"), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=True),
    sa.Column('work_policy', sa.String(length=40), server_default=sa.text("'assigned_only'"), nullable=False),
    sa.Column('max_parallel_work', sa.Integer(), server_default=sa.text("'1'"), nullable=False),
    sa.Column('queue_revision', sa.Integer(), server_default=sa.text("'1'"), nullable=False),
    sa.Column('lifecycle_state', sa.String(length=30), server_default=sa.text("'active'"), nullable=False),
    sa.CheckConstraint("lifecycle_state IN ('active', 'onboarding', 'disabled')", name='ck_agent_actors_lifecycle_state'),
    sa.CheckConstraint("work_policy = 'assigned_only'", name='ck_agent_actors_supported_work_policy'),
    sa.CheckConstraint('max_parallel_work = 1', name='ck_agent_actors_supported_parallel_work'),
    sa.ForeignKeyConstraint(['profile_id'], ['team_member_profiles.id'], name='fk_agent_actors_profile_id', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('api_key_hash'),
    sa.UniqueConstraint('name')
    )
    op.create_index('ix_agent_actors_profile_id', 'agent_actors', ['profile_id'], unique=False)
    op.create_table('labels',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('slug', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('group_id', sa.Integer(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('color', sa.String(length=7), server_default=sa.text("'#64748b'"), nullable=False),
    sa.Column('is_active', sa.Boolean(), server_default=sa.true(), nullable=False),
    sa.Column('sort_order', sa.Integer(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('seed_key', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['group_id'], ['label_groups.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('slug', name='uq_labels_slug')
    )
    op.create_index('ix_labels_created_at', 'labels', ['created_at'], unique=False)
    op.create_index('ix_labels_group_active_order', 'labels', ['group_id', 'is_active', 'sort_order'], unique=False)
    op.create_index('ix_labels_group_id', 'labels', ['group_id'], unique=False)
    op.create_index('ix_labels_is_active', 'labels', ['is_active'], unique=False)
    op.create_index('ix_labels_seed_key', 'labels', ['seed_key'], unique=1)
    op.create_index('ix_labels_slug', 'labels', ['slug'], unique=False)
    op.create_index('ix_labels_sort_order', 'labels', ['sort_order'], unique=False)
    op.create_index('ix_labels_updated_at', 'labels', ['updated_at'], unique=False)
    op.create_table('legacy_snapshot_imports',
    sa.Column('checksum', sa.String(length=64), nullable=False),
    sa.Column('iteration_id', sa.Integer(), nullable=False),
    sa.Column('source_name', sa.String(length=255), nullable=False),
    sa.Column('disposition', sa.String(length=32), nullable=False),
    sa.Column('reason', sa.Text(), nullable=False),
    sa.Column('imported_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['iteration_id'], ['iterations.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('checksum')
    )
    op.create_index('ix_legacy_snapshot_imports_iteration_id', 'legacy_snapshot_imports', ['iteration_id'], unique=False)
    op.create_table('outbound_webhook_deliveries',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('target_id', sa.Integer(), nullable=True),
    sa.Column('event_id', sa.Integer(), nullable=False),
    sa.Column('target_name', sa.String(length=255), nullable=False),
    sa.Column('target_url', sa.String(length=1000), nullable=False),
    sa.Column('status', sa.String(length=50), server_default=sa.text("'pending'"), nullable=False),
    sa.Column('attempt_count', sa.Integer(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('last_http_status', sa.Integer(), nullable=True),
    sa.Column('last_error', sa.Text(), nullable=True),
    sa.Column('last_response_body', sa.Text(), nullable=True),
    sa.Column('last_attempt_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('next_retry_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('delivered_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('channel', sa.String(length=30), server_default=sa.text("'webhook'"), nullable=False),
    sa.Column('payload_json', sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('max_attempts', sa.Integer(), server_default=sa.text("'5'"), nullable=False),
    sa.Column('lease_token', sa.String(length=64), nullable=True),
    sa.Column('lease_expires_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('terminal_at', sa.DateTime(timezone=True), nullable=True),
    sa.CheckConstraint("channel IN ('webhook', 'email')", name='ck_outbound_webhook_deliveries_channel'),
    sa.CheckConstraint("status IN ('pending', 'delivered', 'failed')", name='ck_outbound_webhook_deliveries_status'),
    sa.ForeignKeyConstraint(['event_id'], ['outbound_webhook_events.id'], name='fk_outbound_webhook_deliveries_event_id', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['target_id'], ['outbound_webhook_targets.id'], name='fk_outbound_webhook_deliveries_target_id', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_outbound_webhook_deliveries_channel', 'outbound_webhook_deliveries', ['channel'], unique=False)
    op.create_index('ix_outbound_webhook_deliveries_created_at', 'outbound_webhook_deliveries', ['created_at'], unique=False)
    op.create_index('ix_outbound_webhook_deliveries_due', 'outbound_webhook_deliveries', ['status', 'next_retry_at', 'lease_expires_at'], unique=False)
    op.create_index('ix_outbound_webhook_deliveries_event_id', 'outbound_webhook_deliveries', ['event_id'], unique=False)
    op.create_index('ix_outbound_webhook_deliveries_lease_token', 'outbound_webhook_deliveries', ['lease_token'], unique=False)
    op.create_index('ix_outbound_webhook_deliveries_status', 'outbound_webhook_deliveries', ['status'], unique=False)
    op.create_index('ix_outbound_webhook_deliveries_target_id', 'outbound_webhook_deliveries', ['target_id'], unique=False)
    op.create_index('ix_outbound_webhook_deliveries_target_status', 'outbound_webhook_deliveries', ['target_id', 'status'], unique=False)
    op.create_table('project_milestones',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('target_date', sa.Date(), nullable=True),
    sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('sort_order', sa.Integer(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('status', sa.String(length=50), server_default=sa.text("'planned'"), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.CheckConstraint("status IN ('planned', 'active', 'completed', 'canceled')", name='ck_project_milestones_status'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_project_milestones_project_id', 'project_milestones', ['project_id'], unique=False)
    op.create_index('ix_project_milestones_project_order', 'project_milestones', ['project_id', 'sort_order', 'target_date', 'id'], unique=False)
    op.create_index('ix_project_milestones_status', 'project_milestones', ['status'], unique=False)
    op.create_index('ix_project_milestones_target_date', 'project_milestones', ['target_date'], unique=False)
    op.create_table('releases',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), server_default=sa.text("'planned'"), nullable=False),
    sa.Column('target_date', sa.Date(), nullable=True),
    sa.Column('shipped_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('version', sa.String(length=100), nullable=True),
    sa.Column('environment', sa.String(length=100), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.CheckConstraint("status IN ('planned', 'building', 'shipped', 'canceled')", name='ck_releases_status'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_releases_project_id', 'releases', ['project_id'], unique=False)
    op.create_index('ix_releases_project_status_date', 'releases', ['project_id', 'status', 'target_date', 'id'], unique=False)
    op.create_index('ix_releases_status', 'releases', ['status'], unique=False)
    op.create_index('ix_releases_target_date', 'releases', ['target_date'], unique=False)
    op.create_table('team_member_profile_skills',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=False),
    sa.Column('skill_key', sa.String(length=120), nullable=False),
    sa.Column('skill_name', sa.String(length=255), nullable=False),
    sa.Column('category', sa.String(length=120), nullable=True),
    sa.Column('level', sa.Integer(), server_default=sa.text("'3'"), nullable=False),
    sa.Column('interest', sa.Integer(), server_default=sa.text("'3'"), nullable=False),
    sa.Column('is_weakness', sa.Boolean(), server_default=sa.false(), nullable=False),
    sa.Column('keywords_json', sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint('interest >= 1 AND interest <= 5', name='ck_team_member_profile_skills_interest'),
    sa.CheckConstraint('level >= 1 AND level <= 5', name='ck_team_member_profile_skills_level'),
    sa.ForeignKeyConstraint(['profile_id'], ['team_member_profiles.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_team_member_profile_skills_category', 'team_member_profile_skills', ['category'], unique=False)
    op.create_index('ix_team_member_profile_skills_is_weakness', 'team_member_profile_skills', ['is_weakness'], unique=False)
    op.create_index('ix_team_member_profile_skills_profile_id', 'team_member_profile_skills', ['profile_id'], unique=False)
    op.create_index('ix_team_member_profile_skills_skill_key', 'team_member_profile_skills', ['skill_key'], unique=False)
    op.create_index('uq_team_member_profile_skills_profile_skill_key', 'team_member_profile_skills', ['profile_id', 'skill_key'], unique=1)
    op.create_table('vacations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('start_date', sa.Date(), nullable=False),
    sa.Column('end_date', sa.Date(), nullable=False),
    sa.Column('team_member_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['team_member_id'], ['team_members.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('agent_autonomy_topologies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('topology_key', sa.String(length=100), nullable=False),
    sa.Column('revision', sa.Integer(), nullable=False),
    sa.Column('manifest_digest', sa.String(length=64), nullable=False),
    sa.Column('charter_digest', sa.String(length=64), nullable=False),
    sa.Column('primary_actor_id', sa.Integer(), nullable=True),
    sa.Column('state', sa.String(length=30), nullable=False),
    sa.Column('external_journal_revision', sa.Integer(), nullable=False),
    sa.Column('external_journal_head_digest', sa.String(length=64), nullable=False),
    sa.Column('applied_receipt_digest', sa.String(length=64), nullable=True),
    sa.Column('blocker_codes', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("state IN ('planned', 'applying', 'active', 'blocked', 'disabled')", name='ck_agent_autonomy_topologies_state'),
    sa.CheckConstraint('external_journal_revision >= 0', name='ck_agent_autonomy_topologies_journal_revision'),
    sa.CheckConstraint('revision >= 1', name='ck_agent_autonomy_topologies_revision'),
    sa.ForeignKeyConstraint(['primary_actor_id'], ['agent_actors.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('primary_actor_id'),
    sa.UniqueConstraint('topology_key')
    )
    op.create_table('agent_idempotency_records',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('actor_id', sa.Integer(), nullable=False),
    sa.Column('operation', sa.String(length=100), nullable=False),
    sa.Column('target_type', sa.String(length=50), nullable=False),
    sa.Column('target_id', sa.Integer(), nullable=False),
    sa.Column('idempotency_key', sa.String(length=255), nullable=False),
    sa.Column('request_hash', sa.String(length=64), nullable=False),
    sa.Column('response_payload', sa.Text(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['actor_id'], ['agent_actors.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('actor_id', 'operation', 'target_type', 'target_id', 'idempotency_key', name='uq_agent_idempotency_operation')
    )
    op.create_index('ix_agent_idempotency_records_actor_id', 'agent_idempotency_records', ['actor_id'], unique=False)
    op.create_index('ix_agent_idempotency_records_created_at', 'agent_idempotency_records', ['created_at'], unique=False)
    op.create_table('agent_model_bindings',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('actor_id', sa.Integer(), nullable=False),
    sa.Column('model_catalog_id', sa.Integer(), nullable=False),
    sa.Column('is_default', sa.Boolean(), server_default=sa.false(), nullable=False),
    sa.Column('enabled', sa.Boolean(), server_default=sa.true(), nullable=False),
    sa.Column('tool_tags', sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
    sa.Column('data_policy_tags', sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
    sa.Column('revision', sa.Integer(), server_default=sa.text("'1'"), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.CheckConstraint('(NOT is_default) OR enabled', name='ck_agent_model_bindings_default_enabled'),
    sa.CheckConstraint('revision >= 1', name='ck_agent_model_bindings_revision'),
    sa.ForeignKeyConstraint(['actor_id'], ['agent_actors.id'], name='fk_agent_model_bindings_actor_id', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['model_catalog_id'], ['agent_model_catalog_entries.id'], name='fk_agent_model_bindings_model_catalog_id', ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('actor_id', 'model_catalog_id', name='uq_agent_model_bindings_actor_catalog')
    )
    op.create_index('ix_agent_model_bindings_actor_enabled', 'agent_model_bindings', ['actor_id', 'enabled'], unique=False)
    op.create_index('ix_agent_model_bindings_catalog_enabled', 'agent_model_bindings', ['model_catalog_id', 'enabled'], unique=False)
    op.create_index('uq_agent_model_bindings_default_enabled', 'agent_model_bindings', ['actor_id'], unique=1, sqlite_where=sa.text('is_default AND enabled'), postgresql_where=sa.text('is_default AND enabled'))
    op.create_table('agent_team_topologies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('topology_key', sa.String(length=100), nullable=False),
    sa.Column('revision', sa.Integer(), nullable=False),
    sa.Column('manifest_digest', sa.String(length=64), nullable=False),
    sa.Column('manifest_payload', sa.Text(), nullable=False),
    sa.Column('primary_actor_id', sa.Integer(), nullable=True),
    sa.Column('state', sa.String(length=30), nullable=False),
    sa.Column('blocker_codes', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("state IN ('configured', 'onboarding', 'runtime_ready', 'blocked', 'disabled')", name='ck_agent_team_topologies_state'),
    sa.CheckConstraint('revision >= 1', name='ck_agent_team_topologies_revision'),
    sa.ForeignKeyConstraint(['primary_actor_id'], ['agent_actors.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('primary_actor_id'),
    sa.UniqueConstraint('topology_key')
    )
    op.create_index('ix_agent_team_topologies_state', 'agent_team_topologies', ['state'], unique=False)
    op.create_table('principals',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('kind', sa.String(length=16), nullable=False),
    sa.Column('display_name', sa.String(length=255), nullable=False),
    sa.Column('enabled', sa.Boolean(), nullable=False),
    sa.Column('agent_actor_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("kind IN ('human', 'agent', 'system')", name='ck_principals_kind'),
    sa.ForeignKeyConstraint(['agent_actor_id'], ['agent_actors.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('agent_actor_id')
    )
    op.create_table('agent_autonomy_topology_members',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('topology_id', sa.Integer(), nullable=False),
    sa.Column('logical_key', sa.String(length=100), nullable=False),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.Column('object_revision', sa.Integer(), nullable=False),
    sa.Column('lifecycle_state', sa.String(length=40), nullable=False),
    sa.Column('desired_member_digest', sa.String(length=64), nullable=False),
    sa.Column('independence_group', sa.String(length=100), nullable=False),
    sa.Column('role_package_checksum', sa.String(length=64), nullable=False),
    sa.Column('external_identity_binding_digest', sa.String(length=64), nullable=False),
    sa.Column('runtime_attestation_digest', sa.String(length=64), nullable=True),
    sa.Column('credential_delivery_receipt_digest', sa.String(length=64), nullable=True),
    sa.Column('runtime_acknowledgement_digest', sa.String(length=64), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("lifecycle_state IN ('desired', 'configured', 'credential_delivered', 'onboarding', 'connected', 'runtime_ready', 'disabled')", name='ck_agent_autonomy_members_lifecycle'),
    sa.CheckConstraint('object_revision >= 1', name='ck_agent_autonomy_members_revision'),
    sa.ForeignKeyConstraint(['actor_id'], ['agent_actors.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['topology_id'], ['agent_autonomy_topologies.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('actor_id', name='uq_agent_autonomy_members_actor'),
    sa.UniqueConstraint('topology_id', 'logical_key', name='uq_agent_autonomy_members_logical_key')
    )
    op.create_index('ix_agent_autonomy_members_topology_state', 'agent_autonomy_topology_members', ['topology_id', 'lifecycle_state'], unique=False)
    op.create_table('agent_team_apply_runs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('apply_id', sa.String(length=32), nullable=False),
    sa.Column('topology_id', sa.Integer(), nullable=True),
    sa.Column('topology_key', sa.String(length=100), nullable=False),
    sa.Column('principal_key', sa.String(length=160), nullable=False),
    sa.Column('principal_actor_id', sa.Integer(), nullable=True),
    sa.Column('idempotency_key', sa.String(length=255), nullable=False),
    sa.Column('request_digest', sa.String(length=64), nullable=False),
    sa.Column('manifest_digest', sa.String(length=64), nullable=False),
    sa.Column('plan_digest', sa.String(length=64), nullable=False),
    sa.Column('expected_topology_revision', sa.Integer(), nullable=False),
    sa.Column('resulting_topology_revision', sa.Integer(), nullable=False),
    sa.Column('approved_action_ids', sa.Text(), nullable=False),
    sa.Column('confirmed_action_ids', sa.Text(), nullable=False),
    sa.Column('plan_payload', sa.Text(), nullable=False),
    sa.Column('rationale', sa.String(length=2000), nullable=False),
    sa.Column('correlation_id', sa.String(length=255), nullable=False),
    sa.Column('status', sa.String(length=30), nullable=False),
    sa.Column('blocker_codes', sa.Text(), nullable=False),
    sa.Column('response_payload', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("status IN ('running', 'completed', 'partial', 'blocked')", name='ck_agent_team_apply_runs_status'),
    sa.CheckConstraint('expected_topology_revision >= 0', name='ck_agent_team_apply_runs_expected_revision'),
    sa.CheckConstraint('resulting_topology_revision >= 0', name='ck_agent_team_apply_runs_resulting_revision'),
    sa.ForeignKeyConstraint(['principal_actor_id'], ['agent_actors.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['topology_id'], ['agent_team_topologies.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('apply_id'),
    sa.UniqueConstraint('principal_key', 'idempotency_key', name='uq_agent_team_apply_runs_idempotency')
    )
    op.create_index('ix_agent_team_apply_runs_topology_created', 'agent_team_apply_runs', ['topology_key', 'created_at'], unique=False)
    op.create_table('agent_team_managed_objects',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('topology_id', sa.Integer(), nullable=False),
    sa.Column('object_type', sa.String(length=30), nullable=False),
    sa.Column('logical_key', sa.String(length=160), nullable=False),
    sa.Column('object_id', sa.Integer(), nullable=False),
    sa.Column('object_revision', sa.Integer(), nullable=False),
    sa.Column('desired_digest', sa.String(length=64), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("object_type IN ('profile', 'model_catalog', 'model_binding')", name='ck_agent_team_managed_objects_type'),
    sa.CheckConstraint('object_revision >= 1', name='ck_agent_team_managed_objects_revision'),
    sa.ForeignKeyConstraint(['topology_id'], ['agent_team_topologies.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('topology_id', 'object_type', 'logical_key', name='uq_agent_team_managed_objects_logical'),
    sa.UniqueConstraint('topology_id', 'object_type', 'object_id', name='uq_agent_team_managed_objects_reference')
    )
    op.create_table('agent_team_topology_members',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('topology_id', sa.Integer(), nullable=False),
    sa.Column('actor_key', sa.String(length=100), nullable=False),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.Column('actor_name', sa.String(length=100), nullable=False),
    sa.Column('role', sa.String(length=30), nullable=False),
    sa.Column('object_revision', sa.Integer(), nullable=False),
    sa.Column('lifecycle_state', sa.String(length=40), nullable=False),
    sa.Column('desired_member_digest', sa.String(length=64), nullable=False),
    sa.Column('desired_member_payload', sa.Text(), nullable=False),
    sa.Column('scope_preset', sa.String(length=40), nullable=False),
    sa.Column('profile_key', sa.String(length=120), nullable=False),
    sa.Column('skill_package_name', sa.String(length=120), nullable=False),
    sa.Column('skill_package_version', sa.String(length=40), nullable=False),
    sa.Column('skill_package_checksum', sa.String(length=64), nullable=False),
    sa.Column('model_binding_keys', sa.Text(), nullable=False),
    sa.Column('default_model_binding_key', sa.String(length=120), nullable=False),
    sa.Column('assignment_modes', sa.Text(), nullable=False),
    sa.Column('runtime_ref', sa.String(length=1024), nullable=False),
    sa.Column('credential_ref', sa.String(length=1024), nullable=False),
    sa.Column('credential_delivery_state', sa.String(length=30), nullable=False),
    sa.Column('credential_delivery_receipt_digest', sa.String(length=64), nullable=True),
    sa.Column('handoff_digest', sa.String(length=64), nullable=True),
    sa.Column('runtime_acknowledgement_digest', sa.String(length=64), nullable=True),
    sa.Column('runtime_acknowledgement_payload', sa.Text(), nullable=True),
    sa.Column('runtime_acknowledged_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('ack_attempt_count', sa.Integer(), nullable=False),
    sa.Column('ack_window_started_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("credential_delivery_state IN ('pending', 'delivered', 'uncertain', 'not_required')", name='ck_agent_team_members_credential_state'),
    sa.CheckConstraint("lifecycle_state IN ('desired', 'configured', 'credential_delivered', 'onboarding', 'connected', 'runtime_ready', 'disabled')", name='ck_agent_team_members_lifecycle'),
    sa.CheckConstraint("role IN ('pm', 'worker', 'verifier')", name='ck_agent_team_members_role'),
    sa.CheckConstraint('ack_attempt_count >= 0', name='ck_agent_team_members_ack_attempts'),
    sa.CheckConstraint('object_revision >= 1', name='ck_agent_team_members_object_revision'),
    sa.ForeignKeyConstraint(['actor_id'], ['agent_actors.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['topology_id'], ['agent_team_topologies.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('actor_id', name='uq_agent_team_members_actor'),
    sa.UniqueConstraint('credential_ref', name='uq_agent_team_members_credential_ref'),
    sa.UniqueConstraint('runtime_ref', name='uq_agent_team_members_runtime_ref'),
    sa.UniqueConstraint('topology_id', 'actor_key', name='uq_agent_team_members_actor_key')
    )
    op.create_index('ix_agent_team_members_topology_lifecycle', 'agent_team_topology_members', ['topology_id', 'lifecycle_state'], unique=False)
    op.create_table('application_snapshots',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('iteration_id', sa.Integer(), nullable=True),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('schema_version', sa.Integer(), nullable=False),
    sa.Column('input_revision', sa.Integer(), nullable=False),
    sa.Column('payload', sa.JSON(), nullable=False),
    sa.Column('checksum', sa.String(length=64), nullable=False),
    sa.Column('provenance', sa.String(length=32), nullable=False),
    sa.Column('created_by_principal_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.CheckConstraint('iteration_id IS NOT NULL OR project_id IS NOT NULL', name='ck_application_snapshot_scope'),
    sa.ForeignKeyConstraint(['created_by_principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['iteration_id'], ['iterations.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], name='fk_application_snapshots_project_id_projects', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('iteration_id', 'filename', name='uq_application_snapshot_filename'),
    sa.UniqueConstraint('project_id', 'filename', name='uq_application_snapshot_project_filename')
    )
    op.create_index('ix_application_snapshots_created_at', 'application_snapshots', ['created_at'], unique=False)
    op.create_index('ix_application_snapshots_iteration_id', 'application_snapshots', ['iteration_id'], unique=False)
    op.create_index('ix_application_snapshots_project_id', 'application_snapshots', ['project_id'], unique=False)
    op.create_table('command_audit',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('principal_id', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('action', sa.String(length=128), nullable=False),
    sa.Column('source', sa.String(length=32), nullable=False),
    sa.Column('correlation_id', sa.String(length=128), nullable=False),
    sa.Column('reason', sa.Text(), nullable=True),
    sa.Column('details', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_command_audit_created_at', 'command_audit', ['created_at'], unique=False)
    op.create_index('ix_command_audit_principal_id', 'command_audit', ['principal_id'], unique=False)
    op.create_index('ix_command_audit_project_id', 'command_audit', ['project_id'], unique=False)
    op.create_table('identity_subjects',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('principal_id', sa.Integer(), nullable=False),
    sa.Column('issuer', sa.String(length=512), nullable=False),
    sa.Column('subject', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['principal_id'], ['principals.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('issuer', 'subject', name='uq_identity_subject')
    )
    op.create_index('ix_identity_subjects_principal_id', 'identity_subjects', ['principal_id'], unique=False)
    op.create_table('principal_profile_links',
    sa.Column('principal_id', sa.Integer(), nullable=False),
    sa.Column('profile_id', sa.Integer(), nullable=False),
    sa.Column('linked_by_principal_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['linked_by_principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['principal_id'], ['principals.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['profile_id'], ['team_member_profiles.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('principal_id'),
    sa.UniqueConstraint('profile_id')
    )
    op.create_table('project_memberships',
    sa.Column('principal_id', sa.Integer(), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=16), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("role IN ('viewer', 'editor', 'executor', 'reviewer', 'manager')", name='ck_project_memberships_role'),
    sa.ForeignKeyConstraint(['principal_id'], ['principals.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('principal_id', 'project_id')
    )
    op.create_table('tasks',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=500), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('priority', sa.Integer(), nullable=False),
    sa.Column('effort_days', sa.Float(), nullable=True),
    sa.Column('effort_hours', sa.Float(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('actual_start_date', sa.Date(), nullable=True),
    sa.Column('actual_end_date', sa.Date(), nullable=True),
    sa.Column('calculated_effort_days', sa.Float(), nullable=True),
    sa.Column('min_start_date', sa.Date(), nullable=True),
    sa.Column('max_end_date', sa.Date(), nullable=True),
    sa.Column('is_optional', sa.Boolean(), nullable=False),
    sa.Column('is_deferred', sa.Boolean(), nullable=False),
    sa.Column('tags', sa.String(length=1000), nullable=True),
    sa.Column('sort_order', sa.Integer(), nullable=False),
    sa.Column('iteration_id', sa.Integer(), nullable=True),
    sa.Column('parent_id', sa.Integer(), nullable=True),
    sa.Column('assignee_id', sa.Integer(), nullable=True),
    sa.Column('external_key', sa.String(length=255), nullable=True),
    sa.Column('source', sa.String(length=100), nullable=True),
    sa.Column('source_url', sa.String(length=1000), nullable=True),
    sa.Column('version', sa.Integer(), server_default=sa.text("'1'"), nullable=False),
    sa.Column('claimed_by', sa.Integer(), nullable=True),
    sa.Column('claim_expires_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('milestone_id', sa.Integer(), nullable=True),
    sa.Column('claim_id', sa.String(length=64), nullable=True),
    sa.Column('claim_generation', sa.Integer(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('executed_by_principal_id', sa.Integer(), nullable=True),
    sa.Column('accepted_by_principal_id', sa.Integer(), nullable=True),
    sa.Column('is_summary', sa.Boolean(), server_default=sa.false(), nullable=False),
    sa.Column('baseline_start_date', sa.Date(), nullable=True),
    sa.Column('baseline_end_date', sa.Date(), nullable=True),
    sa.Column('baseline_revision', sa.Integer(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('baseline_provenance', sa.String(length=32), server_default=sa.text("'legacy_unknown'"), nullable=False),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('resolved_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('accepted_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('accepted_version', sa.Integer(), nullable=True),
    sa.Column('owner_profile_id', sa.Integer(), nullable=True),
    sa.Column('ownership_provenance', sa.String(length=32), server_default=sa.text("'unassigned'"), nullable=False),
    sa.Column('nominal_day_hours', sa.Float(), server_default=sa.text("'8'"), nullable=False),
    sa.Column('estimate_provenance', sa.String(length=32), server_default=sa.text("'unknown'"), nullable=False),
    sa.Column('legacy_estimate', sa.JSON(), nullable=True),
    sa.Column('blocked_reason', sa.Text(), nullable=True),
    sa.Column('canceled_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('canceled_reason', sa.Text(), nullable=True),
    sa.Column('canceled_by_principal_id', sa.Integer(), nullable=True),
    sa.Column('execution_mode', sa.String(length=16), server_default=sa.text("'scheduled'"), nullable=False),
    sa.Column('brief', sa.JSON(), nullable=True),
    sa.Column('brief_revision', sa.Integer(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('brief_provenance', sa.String(length=32), server_default=sa.text("'legacy_text'"), nullable=False),
    sa.Column('legacy_description', sa.Text(), nullable=True),
    sa.Column('brief_migration_notes', sa.JSON(), nullable=True),
    sa.Column('artifact_revision', sa.Integer(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('progress', sa.JSON(), nullable=True),
    sa.Column('domain_backfill_version', sa.Integer(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('domain_migration_notes', sa.JSON(), nullable=True),
    sa.CheckConstraint('effort_hours IS NULL OR effort_hours >= 0', name='ck_tasks_effort_hours'),
    sa.CheckConstraint('iteration_id IS NOT NULL OR project_id IS NOT NULL', name='ck_tasks_work_scope'),
    sa.CheckConstraint('nominal_day_hours > 0 AND nominal_day_hours <= 24', name='ck_tasks_nominal_day_hours'),
    sa.ForeignKeyConstraint(['accepted_by_principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['assignee_id'], ['team_members.id'], ),
    sa.ForeignKeyConstraint(['canceled_by_principal_id'], ['principals.id'], name='fk_tasks_canceled_by_principal_id_principals', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['claimed_by'], ['agent_actors.id'], name='fk_tasks_claimed_by_agent_actors'),
    sa.ForeignKeyConstraint(['executed_by_principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['iteration_id'], ['iterations.id'], ),
    sa.ForeignKeyConstraint(['milestone_id'], ['project_milestones.id'], name='fk_tasks_milestone_id_project_milestones', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['owner_profile_id'], ['team_member_profiles.id'], name='fk_tasks_owner_profile_id_team_member_profiles', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['parent_id'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], name='fk_tasks_project_id_projects', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sqlite_autoincrement=True
    )
    op.create_index('ix_tasks_assignee_id', 'tasks', ['assignee_id'], unique=False)
    op.create_index('ix_tasks_claim_id', 'tasks', ['claim_id'], unique=False)
    op.create_index('ix_tasks_external_key', 'tasks', ['external_key'], unique=False)
    op.create_index('ix_tasks_iteration_id', 'tasks', ['iteration_id'], unique=False)
    op.create_index('ix_tasks_milestone_id', 'tasks', ['milestone_id'], unique=False)
    op.create_index('ix_tasks_owner_profile_id', 'tasks', ['owner_profile_id'], unique=False)
    op.create_index('ix_tasks_parent_id', 'tasks', ['parent_id'], unique=False)
    op.create_index('ix_tasks_project_id', 'tasks', ['project_id'], unique=False)
    op.create_table('user_sessions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('ip_address', sa.String(), nullable=False),
    sa.Column('user_agent', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('last_seen_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('public_id', sa.String(length=24), nullable=False),
    sa.Column('session_token_hash', sa.String(length=64), nullable=True),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('principal_id', sa.Integer(), nullable=True),
    sa.Column('csrf_token', sa.String(length=128), nullable=True),
    sa.Column('authenticated_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_user_sessions_ip_address', 'user_sessions', ['ip_address'], unique=False)
    op.create_index('ix_user_sessions_principal_id', 'user_sessions', ['principal_id'], unique=False)
    op.create_index('ix_user_sessions_public_id', 'user_sessions', ['public_id'], unique=1)
    op.create_index('ix_user_sessions_session_token_hash', 'user_sessions', ['session_token_hash'], unique=1)
    op.create_table('workspace_authority_state',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('bootstrap_principal_id', sa.Integer(), nullable=True),
    sa.Column('operator_principal_id', sa.Integer(), nullable=True),
    sa.CheckConstraint('id = 1', name='ck_workspace_authority_singleton'),
    sa.ForeignKeyConstraint(['bootstrap_principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['operator_principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('workspace_memberships',
    sa.Column('principal_id', sa.Integer(), nullable=False),
    sa.Column('role', sa.String(length=16), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("role IN ('owner', 'operator', 'member')", name='ck_workspace_memberships_role'),
    sa.ForeignKeyConstraint(['principal_id'], ['principals.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('principal_id')
    )
    op.create_table('agent_task_assignments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('actor_id', sa.Integer(), nullable=False),
    sa.Column('team_member_id', sa.Integer(), nullable=True),
    sa.Column('purpose', sa.String(length=30), server_default=sa.text("'execution'"), nullable=False),
    sa.Column('queue_class', sa.String(length=30), server_default=sa.text("'normal'"), nullable=False),
    sa.Column('state', sa.String(length=30), server_default=sa.text("'queued'"), nullable=False),
    sa.Column('queue_rank', sa.Integer(), server_default=sa.text("'1000'"), nullable=False),
    sa.Column('not_before', sa.DateTime(timezone=True), nullable=True),
    sa.Column('assigned_by_actor_id', sa.Integer(), nullable=True),
    sa.Column('reviewer_profile_id', sa.Integer(), nullable=True),
    sa.Column('task_version', sa.Integer(), nullable=False),
    sa.Column('routing_snapshot', sa.Text(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('reason', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('model_binding_id', sa.Integer(), nullable=True),
    sa.Column('model_binding_revision', sa.Integer(), nullable=True),
    sa.CheckConstraint("purpose IN ('execution', 'verification')", name='ck_agent_task_assignments_purpose'),
    sa.CheckConstraint("queue_class IN ('normal', 'rework', 'recovery')", name='ck_agent_task_assignments_queue_class'),
    sa.CheckConstraint("state IN ('queued', 'accepted', 'fulfilled', 'cancelled')", name='ck_agent_task_assignments_state'),
    sa.CheckConstraint('(model_binding_id IS NULL AND model_binding_revision IS NULL) OR (model_binding_id IS NOT NULL AND model_binding_revision IS NOT NULL AND model_binding_revision >= 1)', name='ck_agent_task_assignments_model_binding_pair'),
    sa.ForeignKeyConstraint(['actor_id'], ['agent_actors.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['assigned_by_actor_id'], ['agent_actors.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['model_binding_id'], ['agent_model_bindings.id'], name='fk_agent_task_assignments_model_binding_id', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['reviewer_profile_id'], ['team_member_profiles.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['team_member_id'], ['team_members.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_agent_task_assignments_actor_id', 'agent_task_assignments', ['actor_id'], unique=False)
    op.create_index('ix_agent_task_assignments_actor_queue', 'agent_task_assignments', ['actor_id', 'purpose', 'state', 'queue_rank'], unique=False)
    op.create_index('ix_agent_task_assignments_created_at', 'agent_task_assignments', ['created_at'], unique=False)
    op.create_index('ix_agent_task_assignments_model_binding_id', 'agent_task_assignments', ['model_binding_id'], unique=False)
    op.create_index('ix_agent_task_assignments_task_id', 'agent_task_assignments', ['task_id'], unique=False)
    op.create_index('ix_agent_task_assignments_task_state', 'agent_task_assignments', ['task_id', 'purpose', 'state'], unique=False)
    op.create_index('uq_agent_task_assignments_live_purpose', 'agent_task_assignments', ['task_id', 'purpose'], unique=1, sqlite_where=sa.text("state IN ('queued', 'accepted')"), postgresql_where=sa.text("state IN ('queued', 'accepted')"))
    op.create_table('agent_team_action_receipts',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('apply_run_id', sa.Integer(), nullable=False),
    sa.Column('action_id', sa.String(length=128), nullable=False),
    sa.Column('action_digest', sa.String(length=64), nullable=False),
    sa.Column('reconciliation_class', sa.String(length=40), nullable=False),
    sa.Column('operation', sa.String(length=80), nullable=False),
    sa.Column('actor_key', sa.String(length=100), nullable=False),
    sa.Column('status', sa.String(length=30), nullable=False),
    sa.Column('target_actor_id', sa.Integer(), nullable=True),
    sa.Column('before_revision', sa.Integer(), nullable=True),
    sa.Column('after_revision', sa.Integer(), nullable=True),
    sa.Column('blocker_code', sa.String(length=128), nullable=True),
    sa.Column('next_action', sa.String(length=255), nullable=True),
    sa.Column('result_payload', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("status IN ('pending', 'applied', 'no_change', 'blocked')", name='ck_agent_team_action_receipts_status'),
    sa.CheckConstraint('(before_revision IS NULL OR before_revision >= 1) AND (after_revision IS NULL OR after_revision >= 1)', name='ck_agent_team_action_receipts_revisions'),
    sa.ForeignKeyConstraint(['apply_run_id'], ['agent_team_apply_runs.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('apply_run_id', 'action_id', name='uq_agent_team_action_receipts_action')
    )
    op.create_table('agent_work_packages',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('package_key', sa.String(length=255), nullable=False),
    sa.Column('package_version', sa.Integer(), nullable=False),
    sa.Column('execution_task_id', sa.Integer(), nullable=True),
    sa.Column('predecessor_package_id', sa.Integer(), nullable=True),
    sa.Column('state', sa.String(length=30), nullable=False),
    sa.Column('artifact_set_digest', sa.String(length=64), nullable=False),
    sa.Column('contract_manifest_digest', sa.String(length=64), nullable=False),
    sa.Column('source_contract_digest', sa.String(length=64), nullable=False),
    sa.Column('creation_request_digest', sa.String(length=64), nullable=False),
    sa.Column('external_journal_revision', sa.Integer(), nullable=False),
    sa.Column('external_journal_head_digest', sa.String(length=64), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('task_context_version', sa.Integer(), nullable=True),
    sa.Column('task_brief_revision', sa.Integer(), nullable=True),
    sa.Column('task_artifact_revision', sa.Integer(), nullable=True),
    sa.Column('task_brief_digest', sa.String(length=64), nullable=True),
    sa.CheckConstraint("state IN ('planned', 'evaluating', 'passed', 'rework_required')", name='ck_agent_work_packages_state'),
    sa.CheckConstraint('external_journal_revision >= 1', name='ck_agent_work_packages_journal_revision'),
    sa.CheckConstraint('package_version >= 1', name='ck_agent_work_packages_version'),
    sa.ForeignKeyConstraint(['execution_task_id'], ['tasks.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['predecessor_package_id'], ['agent_work_packages.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('package_key', 'package_version', name='uq_agent_work_packages_key_version')
    )
    op.create_index('ix_agent_work_packages_execution_task_id', 'agent_work_packages', ['execution_task_id'], unique=False)
    op.create_index('ix_agent_work_packages_state', 'agent_work_packages', ['state'], unique=False)
    op.create_table('ownership_transfers',
    sa.Column('guest_session_id', sa.Integer(), nullable=False),
    sa.Column('principal_id', sa.Integer(), nullable=False),
    sa.Column('authorized_by_principal_id', sa.Integer(), nullable=False),
    sa.Column('reason', sa.Text(), nullable=False),
    sa.Column('transferred_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['authorized_by_principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['guest_session_id'], ['user_sessions.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('guest_session_id')
    )
    op.create_table('plan_shares',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('public_id', sa.String(length=48), nullable=False),
    sa.Column('iteration_id', sa.Integer(), nullable=False),
    sa.Column('created_by_session_id', sa.Integer(), nullable=False),
    sa.Column('snapshot_data', sa.JSON(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('revoked_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('owner_principal_id', sa.Integer(), nullable=True),
    sa.Column('expires_at', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['created_by_session_id'], ['user_sessions.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['iteration_id'], ['iterations.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['owner_principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_plan_shares_created_at', 'plan_shares', ['created_at'], unique=False)
    op.create_index('ix_plan_shares_created_by_session_id', 'plan_shares', ['created_by_session_id'], unique=False)
    op.create_index('ix_plan_shares_expires_at', 'plan_shares', ['expires_at'], unique=False)
    op.create_index('ix_plan_shares_iteration_id', 'plan_shares', ['iteration_id'], unique=False)
    op.create_index('ix_plan_shares_iteration_owner_created', 'plan_shares', ['iteration_id', 'created_by_session_id', 'created_at'], unique=False)
    op.create_index('ix_plan_shares_owner_principal_id', 'plan_shares', ['owner_principal_id'], unique=False)
    op.create_index('ix_plan_shares_public_id', 'plan_shares', ['public_id'], unique=1)
    op.create_index('ix_plan_shares_revoked_at', 'plan_shares', ['revoked_at'], unique=False)
    op.create_table('project_updates',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('project_id', sa.Integer(), nullable=False),
    sa.Column('health', sa.String(length=50), nullable=False),
    sa.Column('summary', sa.Text(), nullable=False),
    sa.Column('progress_text', sa.Text(), nullable=True),
    sa.Column('risks_text', sa.Text(), nullable=True),
    sa.Column('decisions_text', sa.Text(), nullable=True),
    sa.Column('next_steps_text', sa.Text(), nullable=True),
    sa.Column('created_by_session_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('created_by_actor_id', sa.Integer(), nullable=True),
    sa.Column('evidence_json', sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('correlation_id', sa.String(length=255), nullable=True),
    sa.Column('idempotency_key', sa.String(length=255), nullable=True),
    sa.CheckConstraint("health IN ('unknown', 'on_track', 'at_risk', 'off_track')", name='ck_project_updates_health'),
    sa.ForeignKeyConstraint(['created_by_actor_id'], ['agent_actors.id'], name='fk_project_updates_created_by_actor_id', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['created_by_session_id'], ['user_sessions.id'], name='fk_project_updates_created_by_session_id_user_sessions', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_project_updates_correlation_id', 'project_updates', ['correlation_id'], unique=False)
    op.create_index('ix_project_updates_created_at', 'project_updates', ['created_at'], unique=False)
    op.create_index('ix_project_updates_created_by_actor_id', 'project_updates', ['created_by_actor_id'], unique=False)
    op.create_index('ix_project_updates_created_by_session_id', 'project_updates', ['created_by_session_id'], unique=False)
    op.create_index('ix_project_updates_health', 'project_updates', ['health'], unique=False)
    op.create_index('ix_project_updates_idempotency_key', 'project_updates', ['idempotency_key'], unique=False)
    op.create_index('ix_project_updates_project_created', 'project_updates', ['project_id', 'created_at', 'id'], unique=False)
    op.create_index('ix_project_updates_project_id', 'project_updates', ['project_id'], unique=False)
    op.create_table('release_tasks',
    sa.Column('release_id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.ForeignKeyConstraint(['release_id'], ['releases.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('release_id', 'task_id', name='pk_release_tasks')
    )
    op.create_index('ix_release_tasks_task_id', 'release_tasks', ['task_id'], unique=False)
    op.create_table('saved_views',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('view_type', sa.String(length=50), nullable=False),
    sa.Column('scope', sa.String(length=50), nullable=False),
    sa.Column('filters_json', sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('sort_json', sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('columns_json', sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('created_by_session_id', sa.Integer(), nullable=True),
    sa.Column('schema_version', sa.Integer(), server_default=sa.text("'1'"), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('seed_key', sa.String(length=100), nullable=True),
    sa.Column('owner_principal_id', sa.Integer(), nullable=True),
    sa.Column('metric_migration_note', sa.String(length=64), nullable=True),
    sa.CheckConstraint("scope IN ('personal', 'shared', 'system')", name='ck_saved_views_scope'),
    sa.CheckConstraint("view_type IN ('tasks', 'projects', 'triage')", name='ck_saved_views_view_type'),
    sa.CheckConstraint('schema_version >= 1', name='ck_saved_views_schema_version_min'),
    sa.ForeignKeyConstraint(['created_by_session_id'], ['user_sessions.id'], name='fk_saved_views_created_by_session_id_user_sessions', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['owner_principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_saved_views_created_at', 'saved_views', ['created_at'], unique=False)
    op.create_index('ix_saved_views_created_by_session_id', 'saved_views', ['created_by_session_id'], unique=False)
    op.create_index('ix_saved_views_owner_principal_id', 'saved_views', ['owner_principal_id'], unique=False)
    op.create_index('ix_saved_views_scope', 'saved_views', ['scope'], unique=False)
    op.create_index('ix_saved_views_seed_key', 'saved_views', ['seed_key'], unique=1)
    op.create_index('ix_saved_views_type_creator', 'saved_views', ['view_type', 'created_by_session_id'], unique=False)
    op.create_index('ix_saved_views_type_scope', 'saved_views', ['view_type', 'scope'], unique=False)
    op.create_index('ix_saved_views_updated_at', 'saved_views', ['updated_at'], unique=False)
    op.create_index('ix_saved_views_view_type', 'saved_views', ['view_type'], unique=False)
    op.create_table('task_brief_revisions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('original_task_id', sa.Integer(), nullable=False),
    sa.Column('task_version', sa.Integer(), nullable=False),
    sa.Column('principal_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('revision', sa.Integer(), nullable=False),
    sa.Column('payload', sa.JSON(), nullable=False),
    sa.Column('provenance', sa.String(length=32), nullable=False),
    sa.ForeignKeyConstraint(['principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('original_task_id', 'revision', name='uq_task_brief_revision')
    )
    op.create_index('ix_task_brief_revisions_original_task_id', 'task_brief_revisions', ['original_task_id'], unique=False)
    op.create_index('ix_task_brief_revisions_task_id', 'task_brief_revisions', ['task_id'], unique=False)
    op.create_table('task_dependencies',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('depends_on_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['depends_on_id'], ['tasks.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_task_dependencies_depends_on_id', 'task_dependencies', ['depends_on_id'], unique=False)
    op.create_index('ix_task_dependencies_task_id', 'task_dependencies', ['task_id'], unique=False)
    op.create_table('task_events',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('actor_type', sa.String(length=50), server_default=sa.text("'user'"), nullable=False),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.Column('event_type', sa.String(length=100), nullable=False),
    sa.Column('payload', sa.Text(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('trace_id', sa.String(length=255), nullable=True),
    sa.Column('span_id', sa.String(length=255), nullable=True),
    sa.Column('correlation_id', sa.String(length=255), nullable=True),
    sa.Column('idempotency_key', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['actor_id'], ['agent_actors.id'], ),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_task_events_actor_id', 'task_events', ['actor_id'], unique=False)
    op.create_index('ix_task_events_correlation_id', 'task_events', ['correlation_id'], unique=False)
    op.create_index('ix_task_events_created_at', 'task_events', ['created_at'], unique=False)
    op.create_index('ix_task_events_event_type', 'task_events', ['event_type'], unique=False)
    op.create_index('ix_task_events_idempotency_key', 'task_events', ['idempotency_key'], unique=False)
    op.create_index('ix_task_events_task_id', 'task_events', ['task_id'], unique=False)
    op.create_index('ix_task_events_trace_id', 'task_events', ['trace_id'], unique=False)
    op.create_index('uq_task_events_agent_idempotency_key', 'task_events', ['task_id', 'actor_id', 'event_type', 'idempotency_key'], unique=1, sqlite_where=sa.text('idempotency_key IS NOT NULL AND actor_id IS NOT NULL AND task_id IS NOT NULL'), postgresql_where=sa.text('idempotency_key IS NOT NULL AND actor_id IS NOT NULL AND task_id IS NOT NULL'))
    op.create_table('task_progress_records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('original_task_id', sa.Integer(), nullable=False),
    sa.Column('task_version', sa.Integer(), nullable=False),
    sa.Column('principal_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('brief_revision', sa.Integer(), nullable=False),
    sa.Column('artifact_revision', sa.Integer(), nullable=False),
    sa.Column('payload', sa.JSON(), nullable=False),
    sa.ForeignKeyConstraint(['principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('original_task_id', 'artifact_revision', name='uq_task_progress_revision')
    )
    op.create_index('ix_task_progress_records_original_task_id', 'task_progress_records', ['original_task_id'], unique=False)
    op.create_index('ix_task_progress_records_task_id', 'task_progress_records', ['task_id'], unique=False)
    op.create_table('task_review_records',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('original_task_id', sa.Integer(), nullable=False),
    sa.Column('task_version', sa.Integer(), nullable=False),
    sa.Column('principal_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('brief_revision', sa.Integer(), nullable=False),
    sa.Column('artifact_revision', sa.Integer(), nullable=False),
    sa.Column('verdict', sa.String(length=16), nullable=False),
    sa.Column('reason', sa.Text(), nullable=False),
    sa.Column('evidence', sa.Text(), nullable=False),
    sa.ForeignKeyConstraint(['principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_task_review_records_original_task_id', 'task_review_records', ['original_task_id'], unique=False)
    op.create_index('ix_task_review_records_task_id', 'task_review_records', ['task_id'], unique=False)
    op.create_table('task_routing_assessments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('task_version', sa.Integer(), nullable=False),
    sa.Column('policy_version', sa.String(length=80), server_default=sa.text("'model-aware-routing-v1'"), nullable=False),
    sa.Column('band', sa.String(length=20), nullable=False),
    sa.Column('reasoning_axis', sa.Integer(), nullable=False),
    sa.Column('ambiguity_axis', sa.Integer(), nullable=False),
    sa.Column('context_breadth_axis', sa.Integer(), nullable=False),
    sa.Column('risk_axis', sa.Integer(), nullable=False),
    sa.Column('verification_burden_axis', sa.Integer(), nullable=False),
    sa.Column('required_skill_levels', sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('required_model', sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('review_mode', sa.String(length=40), nullable=False),
    sa.Column('confidence', sa.Float(), nullable=False),
    sa.Column('reason_codes', sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
    sa.Column('rationale', sa.Text(), nullable=False),
    sa.Column('assessor', sa.String(length=255), nullable=False),
    sa.Column('assessor_actor_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.CheckConstraint("band <> 'routine' OR (reasoning_axis = 1 AND ambiguity_axis = 1 AND context_breadth_axis = 1 AND risk_axis = 1 AND verification_burden_axis = 1)", name='ck_task_routing_assessments_routine_band'),
    sa.CheckConstraint("band <> 'standard' OR (reasoning_axis < 3 AND ambiguity_axis < 3 AND context_breadth_axis < 3 AND risk_axis < 3 AND verification_burden_axis < 3)", name='ck_task_routing_assessments_standard_band'),
    sa.CheckConstraint("band IN ('routine', 'standard', 'advanced')", name='ck_task_routing_assessments_band'),
    sa.CheckConstraint("policy_version = 'model-aware-routing-v1'", name='ck_task_routing_assessments_policy_version'),
    sa.CheckConstraint("review_mode IN ('none', 'standard', 'independent', 'specialist-independent')", name='ck_task_routing_assessments_review_mode'),
    sa.CheckConstraint("risk_axis < 3 OR review_mode IN ('independent', 'specialist-independent')", name='ck_task_routing_assessments_risk_review'),
    sa.CheckConstraint('confidence >= 0.0 AND confidence <= 1.0', name='ck_task_routing_assessments_confidence'),
    sa.CheckConstraint('reasoning_axis BETWEEN 1 AND 3 AND ambiguity_axis BETWEEN 1 AND 3 AND context_breadth_axis BETWEEN 1 AND 3 AND risk_axis BETWEEN 1 AND 3 AND verification_burden_axis BETWEEN 1 AND 3', name='ck_task_routing_assessments_axes'),
    sa.CheckConstraint('task_version >= 1', name='ck_task_routing_assessments_task_version'),
    sa.ForeignKeyConstraint(['assessor_actor_id'], ['agent_actors.id'], name='fk_task_routing_assessments_assessor_actor_id', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='fk_task_routing_assessments_task_id', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('task_id', 'task_version', 'policy_version', name='uq_task_routing_assessments_task_version_policy')
    )
    op.create_index('ix_task_routing_assessments_policy_band', 'task_routing_assessments', ['policy_version', 'band'], unique=False)
    op.create_index('ix_task_routing_assessments_task_version', 'task_routing_assessments', ['task_id', 'task_version'], unique=False)
    op.create_table('task_schedule_baselines',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('revision', sa.Integer(), nullable=False),
    sa.Column('start_date', sa.Date(), nullable=True),
    sa.Column('end_date', sa.Date(), nullable=True),
    sa.Column('timezone', sa.String(length=64), nullable=False),
    sa.Column('reason', sa.Text(), nullable=False),
    sa.Column('principal_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['principal_id'], ['principals.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('task_id', 'revision', name='uq_task_schedule_baseline_revision')
    )
    op.create_index('ix_task_schedule_baselines_task_id', 'task_schedule_baselines', ['task_id'], unique=False)
    op.create_table('task_status_logs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=False),
    sa.Column('from_status', sa.String(length=50), nullable=False),
    sa.Column('to_status', sa.String(length=50), nullable=False),
    sa.Column('changed_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('reason', sa.Text(), nullable=True),
    sa.Column('triggered_by', sa.String(length=50), nullable=False),
    sa.Column('affected_task_ids', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_task_status_logs_changed_at', 'task_status_logs', ['changed_at'], unique=False)
    op.create_index('ix_task_status_logs_task_id', 'task_status_logs', ['task_id'], unique=False)
    op.create_table('triage_items',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=500), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('source', sa.String(length=100), nullable=True),
    sa.Column('source_url', sa.String(length=1000), nullable=True),
    sa.Column('external_key', sa.String(length=255), nullable=True),
    sa.Column('status', sa.String(length=50), server_default=sa.text("'new'"), nullable=False),
    sa.Column('priority_hint', sa.Integer(), nullable=True),
    sa.Column('assignee_hint', sa.String(length=255), nullable=True),
    sa.Column('labels', sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
    sa.Column('snoozed_until', sa.DateTime(timezone=True), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.Column('project_hint_id', sa.Integer(), nullable=True),
    sa.Column('iteration_hint_id', sa.Integer(), nullable=True),
    sa.Column('duplicate_of_id', sa.Integer(), nullable=True),
    sa.Column('duplicate_task_id', sa.Integer(), nullable=True),
    sa.Column('converted_task_id', sa.Integer(), nullable=True),
    sa.Column('metadata_json', sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
    sa.CheckConstraint('duplicate_of_id IS NULL OR duplicate_task_id IS NULL', name='ck_triage_items_one_duplicate_target'),
    sa.CheckConstraint('priority_hint IS NULL OR (priority_hint >= 1 AND priority_hint <= 10)', name='ck_triage_items_priority_hint_range'),
    sa.ForeignKeyConstraint(['converted_task_id'], ['tasks.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['duplicate_of_id'], ['triage_items.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['duplicate_task_id'], ['tasks.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['iteration_hint_id'], ['iterations.id'], ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['project_hint_id'], ['projects.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_triage_items_converted_task_id', 'triage_items', ['converted_task_id'], unique=False)
    op.create_index('ix_triage_items_created_at', 'triage_items', ['created_at'], unique=False)
    op.create_index('ix_triage_items_duplicate_of_id', 'triage_items', ['duplicate_of_id'], unique=False)
    op.create_index('ix_triage_items_duplicate_task_id', 'triage_items', ['duplicate_task_id'], unique=False)
    op.create_index('ix_triage_items_external_key', 'triage_items', ['external_key'], unique=False)
    op.create_index('ix_triage_items_iteration_hint_id', 'triage_items', ['iteration_hint_id'], unique=False)
    op.create_index('ix_triage_items_project_hint_id', 'triage_items', ['project_hint_id'], unique=False)
    op.create_index('ix_triage_items_snoozed_until', 'triage_items', ['snoozed_until'], unique=False)
    op.create_index('ix_triage_items_status', 'triage_items', ['status'], unique=False)
    op.create_index('ix_triage_items_updated_at', 'triage_items', ['updated_at'], unique=False)
    op.create_table('agent_observation_jobs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('job_key', sa.String(length=255), nullable=False),
    sa.Column('job_version', sa.Integer(), nullable=False),
    sa.Column('package_id', sa.Integer(), nullable=True),
    sa.Column('observation_kind', sa.String(length=100), nullable=False),
    sa.Column('state', sa.String(length=30), nullable=False),
    sa.Column('policy_digest', sa.String(length=64), nullable=False),
    sa.Column('trusted_clock_ref_digest', sa.String(length=64), nullable=False),
    sa.Column('minimum_elapsed_seconds', sa.Integer(), nullable=False),
    sa.Column('starts_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('due_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('valid_until', sa.DateTime(timezone=True), nullable=False),
    sa.Column('checkpoint_digest', sa.String(length=64), nullable=True),
    sa.Column('credential_lineage_digest', sa.String(length=64), nullable=False),
    sa.Column('result_evidence_digest', sa.String(length=64), nullable=True),
    sa.Column('external_journal_revision', sa.Integer(), nullable=False),
    sa.Column('external_journal_head_digest', sa.String(length=64), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("state IN ('planned', 'scheduled', 'running', 'met', 'missed', 'failed', 'blocked_external')", name='ck_agent_observation_jobs_state'),
    sa.CheckConstraint('external_journal_revision >= 0', name='ck_agent_observation_jobs_journal_revision'),
    sa.CheckConstraint('job_version >= 1', name='ck_agent_observation_jobs_version'),
    sa.CheckConstraint('minimum_elapsed_seconds >= 1', name='ck_agent_observation_jobs_minimum_elapsed'),
    sa.CheckConstraint('starts_at < due_at AND due_at < valid_until', name='ck_agent_observation_jobs_time_order'),
    sa.ForeignKeyConstraint(['package_id'], ['agent_work_packages.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('job_key', 'job_version', name='uq_agent_observation_jobs_key_version')
    )
    op.create_index('ix_agent_observation_jobs_due_state', 'agent_observation_jobs', ['due_at', 'state'], unique=False)
    op.create_table('agent_runs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('actor_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), server_default=sa.text("'running'"), nullable=False),
    sa.Column('trace_id', sa.String(length=255), nullable=True),
    sa.Column('model', sa.String(length=255), nullable=True),
    sa.Column('tool_name', sa.String(length=255), nullable=True),
    sa.Column('run_metadata', sa.Text(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('artifact_links', sa.Text(), server_default=sa.text("'[]'"), nullable=False),
    sa.Column('commit_url', sa.String(length=1000), nullable=True),
    sa.Column('pr_url', sa.String(length=1000), nullable=True),
    sa.Column('summary', sa.Text(), nullable=True),
    sa.Column('error', sa.Text(), nullable=True),
    sa.Column('idempotency_key', sa.String(length=255), nullable=True),
    sa.Column('started_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('assignment_id', sa.Integer(), nullable=True),
    sa.Column('claim_generation', sa.Integer(), nullable=True),
    sa.Column('heartbeat_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('model_binding_id', sa.Integer(), nullable=True),
    sa.Column('model_binding_revision', sa.Integer(), nullable=True),
    sa.Column('configured_model_alias', sa.String(length=255), nullable=True),
    sa.Column('resolved_model_id', sa.String(length=255), nullable=True),
    sa.Column('model_trust_state', sa.String(length=30), server_default=sa.text("'unreported'"), nullable=False),
    sa.Column('model_match_basis', sa.String(length=40), nullable=True),
    sa.CheckConstraint("(model_trust_state = 'matched' AND model_match_basis IS NOT NULL AND model_match_basis IN ('configured_alias', 'catalog_key')) OR (model_trust_state <> 'matched' AND model_match_basis IS NULL)", name='ck_agent_runs_model_match_basis'),
    sa.CheckConstraint("model_trust_state IN ('matched', 'mismatch', 'unreported', 'unverifiable')", name='ck_agent_runs_model_trust_state'),
    sa.CheckConstraint('(model_binding_id IS NULL AND model_binding_revision IS NULL) OR (model_binding_id IS NOT NULL AND model_binding_revision IS NOT NULL AND model_binding_revision >= 1)', name='ck_agent_runs_model_binding_pair'),
    sa.ForeignKeyConstraint(['actor_id'], ['agent_actors.id'], ),
    sa.ForeignKeyConstraint(['assignment_id'], ['agent_task_assignments.id'], name='fk_agent_runs_assignment_id', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['model_binding_id'], ['agent_model_bindings.id'], name='fk_agent_runs_model_binding_id', ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_agent_runs_actor_id', 'agent_runs', ['actor_id'], unique=False)
    op.create_index('ix_agent_runs_assignment_id', 'agent_runs', ['assignment_id'], unique=False)
    op.create_index('ix_agent_runs_idempotency_key', 'agent_runs', ['idempotency_key'], unique=False)
    op.create_index('ix_agent_runs_model_binding_id', 'agent_runs', ['model_binding_id'], unique=False)
    op.create_index('ix_agent_runs_started_at', 'agent_runs', ['started_at'], unique=False)
    op.create_index('ix_agent_runs_status', 'agent_runs', ['status'], unique=False)
    op.create_index('ix_agent_runs_task_id', 'agent_runs', ['task_id'], unique=False)
    op.create_index('ix_agent_runs_trace_id', 'agent_runs', ['trace_id'], unique=False)
    op.create_index('uq_agent_runs_running_assignment', 'agent_runs', ['assignment_id'], unique=1, sqlite_where=sa.text("assignment_id IS NOT NULL AND status = 'running'"), postgresql_where=sa.text("assignment_id IS NOT NULL AND status = 'running'"))
    op.create_table('agent_verification_requirements',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('package_id', sa.Integer(), nullable=False),
    sa.Column('slot_key', sa.String(length=255), nullable=False),
    sa.Column('verifier_logical_key', sa.String(length=100), nullable=False),
    sa.Column('state', sa.String(length=30), nullable=False),
    sa.Column('assigned_verifier_actor_id', sa.Integer(), nullable=True),
    sa.Column('assignment_id', sa.Integer(), nullable=True),
    sa.Column('criterion_schema', sa.String(length=255), nullable=False),
    sa.Column('artifact_set_digest', sa.String(length=64), nullable=False),
    sa.Column('evaluator_version', sa.String(length=255), nullable=False),
    sa.Column('executor_independence_group', sa.String(length=100), nullable=False),
    sa.Column('verifier_independence_group', sa.String(length=100), nullable=False),
    sa.Column('lease_generation', sa.Integer(), nullable=False),
    sa.Column('lease_digest', sa.String(length=64), nullable=True),
    sa.Column('attempt_start_digest', sa.String(length=64), nullable=True),
    sa.Column('lease_expires_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('heartbeat_at', sa.DateTime(timezone=True), nullable=True),
    sa.Column('evidence_digest', sa.String(length=64), nullable=True),
    sa.Column('verdict_digest', sa.String(length=64), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint("state IN ('planned', 'ready', 'claimed', 'running', 'passed', 'rejected', 'expired')", name='ck_agent_verification_requirements_state'),
    sa.CheckConstraint("state NOT IN ('claimed', 'running', 'passed', 'rejected') OR (assigned_verifier_actor_id IS NOT NULL AND lease_generation >= 1 AND lease_digest IS NOT NULL AND attempt_start_digest IS NOT NULL AND lease_expires_at IS NOT NULL)", name='ck_agent_verification_requirements_live_fence'),
    sa.CheckConstraint('executor_independence_group <> verifier_independence_group', name='ck_agent_verification_requirements_independence'),
    sa.CheckConstraint('lease_generation >= 0', name='ck_agent_verification_requirements_lease_generation'),
    sa.ForeignKeyConstraint(['assigned_verifier_actor_id'], ['agent_actors.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['assignment_id'], ['agent_task_assignments.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['package_id'], ['agent_work_packages.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('assignment_id', name='uq_agent_verification_requirements_assignment'),
    sa.UniqueConstraint('package_id', 'slot_key', name='uq_agent_verification_requirements_slot')
    )
    op.create_index('ix_agent_verification_requirements_actor_state', 'agent_verification_requirements', ['assigned_verifier_actor_id', 'state'], unique=False)
    op.create_index('ix_agent_verification_requirements_assigned_verifier_actor_id', 'agent_verification_requirements', ['assigned_verifier_actor_id'], unique=False)
    op.create_table('request_source_links',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('request_source_id', sa.Integer(), nullable=False),
    sa.Column('triage_item_id', sa.Integer(), nullable=True),
    sa.Column('task_id', sa.Integer(), nullable=True),
    sa.Column('project_id', sa.Integer(), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.CheckConstraint('(CASE WHEN triage_item_id IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN task_id IS NOT NULL THEN 1 ELSE 0 END + CASE WHEN project_id IS NOT NULL THEN 1 ELSE 0 END) = 1', name='ck_request_source_links_exactly_one_target'),
    sa.ForeignKeyConstraint(['project_id'], ['projects.id'], name='fk_request_source_links_project_id', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['request_source_id'], ['request_sources.id'], name='fk_request_source_links_request_source_id', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], name='fk_request_source_links_task_id', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['triage_item_id'], ['triage_items.id'], name='fk_request_source_links_triage_item_id', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('request_source_id', 'project_id', name='uq_request_source_links_source_project'),
    sa.UniqueConstraint('request_source_id', 'task_id', name='uq_request_source_links_source_task'),
    sa.UniqueConstraint('request_source_id', 'triage_item_id', name='uq_request_source_links_source_triage_item')
    )
    op.create_index('ix_request_source_links_project_id', 'request_source_links', ['project_id'], unique=False)
    op.create_index('ix_request_source_links_request_source_id', 'request_source_links', ['request_source_id'], unique=False)
    op.create_index('ix_request_source_links_task_id', 'request_source_links', ['task_id'], unique=False)
    op.create_index('ix_request_source_links_triage_item_id', 'request_source_links', ['triage_item_id'], unique=False)
    op.create_table('triage_classification_suggestions',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('triage_item_id', sa.Integer(), nullable=False),
    sa.Column('suggested_type_label_slug', sa.String(length=100), nullable=True),
    sa.Column('suggested_area_label_slug', sa.String(length=100), nullable=True),
    sa.Column('suggested_priority', sa.Integer(), nullable=True),
    sa.Column('suggested_label_slugs', sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
    sa.Column('unmatched_label_text', sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
    sa.Column('suggested_assignee_id', sa.Integer(), nullable=True),
    sa.Column('suggested_assignee_hint', sa.String(length=255), nullable=True),
    sa.Column('suggested_project_id', sa.Integer(), nullable=True),
    sa.Column('duplicate_candidates', sa.JSON(), server_default=sa.text("'[]'"), nullable=False),
    sa.Column('confidence', sa.Float(), server_default=sa.text("'0'"), nullable=False),
    sa.Column('rationale', sa.Text(), nullable=True),
    sa.Column('provider', sa.String(length=100), nullable=True),
    sa.Column('model', sa.String(length=255), nullable=True),
    sa.Column('is_fallback', sa.Boolean(), server_default=sa.false(), nullable=False),
    sa.Column('raw_response_json', sa.JSON(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
    sa.CheckConstraint('confidence >= 0 AND confidence <= 1', name='ck_triage_classification_suggestions_confidence_range'),
    sa.CheckConstraint('suggested_priority IS NULL OR (suggested_priority >= 1 AND suggested_priority <= 10)', name='ck_triage_classification_suggestions_priority_range'),
    sa.ForeignKeyConstraint(['suggested_assignee_id'], ['team_members.id'], name='fk_triage_classification_suggestions_assignee_id', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['suggested_project_id'], ['projects.id'], name='fk_triage_classification_suggestions_project_id', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['triage_item_id'], ['triage_items.id'], name='fk_triage_classification_suggestions_triage_item_id', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_triage_classification_suggestions_created_at', 'triage_classification_suggestions', ['created_at'], unique=False)
    op.create_index('ix_triage_classification_suggestions_is_fallback', 'triage_classification_suggestions', ['is_fallback'], unique=False)
    op.create_index('ix_triage_classification_suggestions_suggested_assignee_id', 'triage_classification_suggestions', ['suggested_assignee_id'], unique=False)
    op.create_index('ix_triage_classification_suggestions_suggested_project_id', 'triage_classification_suggestions', ['suggested_project_id'], unique=False)
    op.create_index('ix_triage_classification_suggestions_triage_item_id', 'triage_classification_suggestions', ['triage_item_id'], unique=False)
    op.create_table('agent_run_events',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('run_id', sa.Integer(), nullable=False),
    sa.Column('event_type', sa.String(length=100), nullable=False),
    sa.Column('message', sa.Text(), nullable=True),
    sa.Column('payload', sa.Text(), server_default=sa.text("'{}'"), nullable=False),
    sa.Column('trace_id', sa.String(length=255), nullable=True),
    sa.Column('span_id', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.Column('correlation_id', sa.String(length=255), nullable=True),
    sa.Column('idempotency_key', sa.String(length=255), nullable=True),
    sa.ForeignKeyConstraint(['run_id'], ['agent_runs.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_agent_run_events_correlation_id', 'agent_run_events', ['correlation_id'], unique=False)
    op.create_index('ix_agent_run_events_created_at', 'agent_run_events', ['created_at'], unique=False)
    op.create_index('ix_agent_run_events_event_type', 'agent_run_events', ['event_type'], unique=False)
    op.create_index('ix_agent_run_events_run_id', 'agent_run_events', ['run_id'], unique=False)
    op.create_index('ix_agent_run_events_trace_id', 'agent_run_events', ['trace_id'], unique=False)
    op.create_index('uq_agent_run_events_run_id_idempotency_key', 'agent_run_events', ['run_id', 'idempotency_key'], unique=1, sqlite_where=sa.text('idempotency_key IS NOT NULL'), postgresql_where=sa.text('idempotency_key IS NOT NULL'))
    op.create_table('agent_verification_events',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('requirement_id', sa.Integer(), nullable=False),
    sa.Column('sequence', sa.Integer(), nullable=False),
    sa.Column('event_type', sa.String(length=100), nullable=False),
    sa.Column('actor_id', sa.Integer(), nullable=True),
    sa.Column('lease_generation', sa.Integer(), nullable=False),
    sa.Column('payload_digest', sa.String(length=64), nullable=False),
    sa.Column('previous_hash', sa.String(length=64), nullable=False),
    sa.Column('event_digest', sa.String(length=64), nullable=False),
    sa.Column('idempotency_key', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
    sa.CheckConstraint('sequence >= 1', name='ck_agent_verification_events_sequence'),
    sa.ForeignKeyConstraint(['actor_id'], ['agent_actors.id'], ondelete='RESTRICT'),
    sa.ForeignKeyConstraint(['requirement_id'], ['agent_verification_requirements.id'], ondelete='RESTRICT'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('requirement_id', 'idempotency_key', name='uq_agent_verification_events_idempotency'),
    sa.UniqueConstraint('requirement_id', 'sequence', name='uq_agent_verification_events_sequence')
    )

    # PostgreSQL requires both tables before installing cyclic references.
    if op.get_bind().dialect.name == "postgresql":
        op.create_foreign_key('fk_initiatives_owner_id', 'initiatives', 'team_members', ['owner_id'], ['id'], ondelete='SET NULL')
        op.create_foreign_key('fk_initiatives_owner_profile_id_team_member_profiles', 'initiatives', 'team_member_profiles', ['owner_profile_id'], ['id'], ondelete='SET NULL')
        op.create_foreign_key('fk_iterations_calendar_id', 'iterations', 'calendars', ['calendar_id'], ['id'], ondelete=None)
        op.create_foreign_key('fk_iterations_project_id_projects', 'iterations', 'projects', ['project_id'], ['id'], ondelete='SET NULL')
        op.create_foreign_key('fk_projects_initiative_id_initiatives', 'projects', 'initiatives', ['initiative_id'], ['id'], ondelete='SET NULL')
        op.create_foreign_key('fk_projects_owner_id', 'projects', 'team_members', ['owner_id'], ['id'], ondelete='SET NULL')
        op.create_foreign_key('fk_projects_owner_profile_id_team_member_profiles', 'projects', 'team_member_profiles', ['owner_profile_id'], ['id'], ondelete='SET NULL')
        op.create_foreign_key('fk_team_members_iteration_id', 'team_members', 'iterations', ['iteration_id'], ['id'], ondelete='SET NULL')
        op.create_foreign_key('fk_team_members_profile_id_team_member_profiles', 'team_members', 'team_member_profiles', ['profile_id'], ['id'], ondelete='SET NULL')


def downgrade():
    raise RuntimeError(
        "The initial schema cannot be downgraded safely. Restore a complete "
        "backup with its matching application image, or explicitly recreate "
        "a disposable development database."
    )
