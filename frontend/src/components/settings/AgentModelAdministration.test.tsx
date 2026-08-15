import { screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type {
    AgentActor,
    AgentActorRosterItem,
    AgentCapabilities,
    AgentModelBinding,
    AgentModelCatalogEntry,
} from '../../types/agent';
import { renderWithProviders } from '../../test/renderWithProviders';
import { AgentModelAdministration } from './AgentModelAdministration';

const agentAccessMock = vi.hoisted(() => ({
    useAgentAccess: vi.fn(),
}));

const agentServiceMock = vi.hoisted(() => ({
    getCapabilities: vi.fn(),
    getActorRoster: vi.fn(),
    getModelCatalog: vi.fn(),
    getModelBindings: vi.fn(),
    createModelCatalogEntry: vi.fn(),
    updateModelCatalogEntry: vi.fn(),
    disableModelCatalogEntry: vi.fn(),
    createModelBinding: vi.fn(),
    updateModelBinding: vi.fn(),
    disableModelBinding: vi.fn(),
}));

vi.mock('../../hooks/useAgentAccess', () => agentAccessMock);
vi.mock('../../services/agentService', () => ({
    agentService: agentServiceMock,
}));

const actorFixture = (overrides: Partial<AgentActor> = {}): AgentActor => ({
    id: 1,
    name: 'planning-pm',
    display_name: 'Planning PM',
    scopes: ['planning:read'],
    enabled: true,
    role: 'pm',
    profile_id: 10,
    work_policy: 'assigned_only',
    max_parallel_work: 1,
    queue_revision: 2,
    created_at: '2026-07-28T10:00:00Z',
    last_seen_at: '2026-07-28T10:30:00Z',
    ...overrides,
});

const catalogFixture = (
    overrides: Partial<AgentModelCatalogEntry> = {},
): AgentModelCatalogEntry => ({
    id: 11,
    key: 'balanced-code',
    provider: 'configured-provider',
    configured_model_alias: 'Balanced Code',
    reasoning_tier: 2,
    context_tier: 'medium',
    modality_tags: ['text'],
    cost_tier: 'medium',
    latency_tier: 'balanced',
    enabled: true,
    revision: 3,
    last_verified_at: '2026-07-28T09:00:00Z',
    created_at: '2026-07-28T08:00:00Z',
    updated_at: '2026-07-28T09:00:00Z',
    ...overrides,
});

const bindingFixture = (
    overrides: Partial<AgentModelBinding> = {},
): AgentModelBinding => ({
    id: 21,
    actor_id: 2,
    model_catalog_id: 11,
    is_default: true,
    enabled: true,
    tool_tags: ['code-edit'],
    data_policy_tags: ['private-code'],
    revision: 4,
    model_catalog_key: 'balanced-code',
    selectable: true,
    model_catalog: catalogFixture(),
    live_assignment_count: 1,
    historical_assignment_count: 2,
    run_reference_count: 3,
    created_at: '2026-07-28T08:15:00Z',
    updated_at: '2026-07-28T09:15:00Z',
    ...overrides,
});

const rosterFixture = (
    overrides: Partial<AgentActorRosterItem> = {},
): AgentActorRosterItem => ({
    ...actorFixture({
        id: 2,
        name: 'worker-alpha',
        display_name: 'Worker Alpha',
        scopes: ['tasks:read'],
        role: 'worker',
        profile_id: 20,
        queue_revision: 7,
    }),
    actor_revision: 4,
    profile_revision: 'p20-rev4',
    profile: {
        id: 20,
        revision: 'p20-rev4',
        display_name: 'Frontend Worker',
        automation_enabled: true,
        profile_kind: 'agent',
        assignment_modes: ['execution'],
        skills: [],
        updated_at: '2026-07-28T09:10:00Z',
    },
    eligible_model_bindings: [bindingFixture()],
    queued_assignments: 2,
    accepted_assignments: 1,
    running_runs: 1,
    ...overrides,
});

const capabilitiesFixture = (scopes: string[]): AgentCapabilities => ({
    server_version: '1.6.2',
    api_contract: 'workchord-agent/v1',
    actor: actorFixture({ scopes }),
    scopes,
    lease_limits: {
        minimum_seconds: 60,
        default_seconds: 3600,
        maximum_seconds: 86400,
    },
    features: ['actor-roster-v1', 'model-aware-routing-v1'],
    model_aware_routing: {
        configured_mode: 'enforced',
        effective_mode: 'enforced',
        feature_advertised: true,
        blocker_codes: [],
        topology_readiness: {
            schema_version: 'model-aware-routing-topology-readiness-v1',
            status: 'ready',
            source: 'agent-team-master-v1',
            topology_id: 'routing-topology-1',
            topology_revision: 1,
            blocker_codes: [],
        },
    },
    recommended_skills: {},
    lifecycle_actions: [],
    skill_catalog_version: null,
    skill_catalog_url: null,
    skill_discovery_url: null,
});

describe('AgentModelAdministration', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        agentAccessMock.useAgentAccess.mockReturnValue({ hasAgentKey: true });
        agentServiceMock.getCapabilities.mockResolvedValue(
            capabilitiesFixture(['planning:read']),
        );
        agentServiceMock.getActorRoster.mockResolvedValue([rosterFixture()]);
        agentServiceMock.getModelCatalog.mockResolvedValue([catalogFixture()]);
        agentServiceMock.getModelBindings.mockResolvedValue([bindingFixture()]);
        agentServiceMock.updateModelCatalogEntry.mockResolvedValue({});
        agentServiceMock.updateModelBinding.mockResolvedValue({});
    });

    it('shows planning readers complete evidence without mutation controls', async () => {
        renderWithProviders(<AgentModelAdministration />);

        expect(await screen.findByRole('heading', {
            level: 2,
            name: 'Model and actor evidence',
        })).toBeInTheDocument();
        expect(screen.getByText('Actor scope: planning:read · read only')).toBeInTheDocument();
        expect(screen.getByText('Configured routing mode')).toBeInTheDocument();
        expect(screen.getByText('Effective routing mode')).toBeInTheDocument();
        expect(screen.getAllByText('Enforced')).toHaveLength(2);
        expect(screen.getByText('Routing topology eligibility')).toBeInTheDocument();
        expect(screen.getByText('Eligible')).toBeInTheDocument();

        expect(screen.getByRole('heading', { name: 'Exact actor roster' })).toBeInTheDocument();
        expect(screen.getAllByRole('heading', { name: 'Worker Alpha' })).toHaveLength(2);
        expect(screen.getByRole('heading', { name: 'Model catalog' })).toBeInTheDocument();
        expect(screen.getByRole('heading', { name: 'Balanced Code' })).toBeInTheDocument();
        expect(screen.getByRole('heading', { name: 'Actor model bindings' })).toBeInTheDocument();
        expect(screen.getByText('Tools: code-edit')).toBeInTheDocument();
        expect(screen.getByText('Selectable binding evidence')).toBeInTheDocument();

        expect(screen.queryByRole('heading', { name: 'Audited change controls' })).not.toBeInTheDocument();
        expect(screen.queryByRole('heading', { name: 'Create catalog entry' })).not.toBeInTheDocument();
        expect(screen.queryByRole('heading', { name: 'Create model binding' })).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Edit' })).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Disable' })).not.toBeInTheDocument();
    });

    it('shows audited mutation controls to stored admin actors', async () => {
        agentServiceMock.getCapabilities.mockResolvedValue(
            capabilitiesFixture(['admin']),
        );

        renderWithProviders(<AgentModelAdministration />);

        expect(await screen.findByText('Actor scope: admin · changes enabled')).toBeInTheDocument();
        expect(screen.getByRole('heading', { name: 'Audited change controls' })).toBeInTheDocument();
        expect(screen.getByRole('textbox', { name: 'Change rationale' })).toBeRequired();
        expect(screen.getByRole('heading', { name: 'Create catalog entry' })).toBeInTheDocument();
        expect(screen.getByRole('heading', { name: 'Create model binding' })).toBeInTheDocument();
        expect(screen.getAllByRole('button', { name: 'Create' })).toHaveLength(2);
        expect(screen.getAllByRole('button', { name: /^Edit / })).toHaveLength(2);
        expect(screen.getAllByRole('button', { name: /^Disable / })).toHaveLength(2);
    });

    it('labels disabled and unselectable bindings without claiming task eligibility', async () => {
        agentServiceMock.getActorRoster.mockResolvedValue([
            rosterFixture({ eligible_model_bindings: [] }),
        ]);
        agentServiceMock.getModelBindings.mockResolvedValue([
            bindingFixture({
                id: 22,
                revision: 5,
                enabled: true,
                selectable: false,
            }),
            bindingFixture({
                id: 23,
                revision: 6,
                enabled: false,
                selectable: false,
            }),
        ]);

        renderWithProviders(<AgentModelAdministration />);

        expect(await screen.findByRole('heading', {
            name: 'Actor model bindings',
        })).toBeInTheDocument();
        await waitFor(() => {
            expect(screen.getByText('Stale or unselectable')).toBeInTheDocument();
            expect(screen.getByText('Disabled')).toBeInTheDocument();
        });
        expect(screen.queryByText('Selectable')).not.toBeInTheDocument();
        expect(screen.getByText('No selectable binding evidence')).toBeInTheDocument();
    });

    it('does not present a selectable binding as healthy when its actor is disabled', async () => {
        agentServiceMock.getActorRoster.mockResolvedValue([
            rosterFixture({
                enabled: false,
                eligible_model_bindings: [],
            }),
        ]);
        agentServiceMock.getModelBindings.mockResolvedValue([
            bindingFixture({
                enabled: true,
                selectable: true,
            }),
        ]);

        renderWithProviders(<AgentModelAdministration />);

        expect(await screen.findByRole('heading', {
            name: 'Actor model bindings',
        })).toBeInTheDocument();
        expect(screen.getByText('Stale or unselectable')).toBeInTheDocument();
        expect(screen.queryByText('Selectable')).not.toBeInTheDocument();
    });

    it('enables disabled catalog entries and bindings with audited revisions', async () => {
        const disabledCatalog = catalogFixture({
            configured_model_alias: 'Dormant Code',
            enabled: false,
            revision: 8,
        });
        const disabledBinding = bindingFixture({
            enabled: false,
            revision: 9,
            selectable: false,
            model_catalog: disabledCatalog,
        });
        agentServiceMock.getCapabilities.mockResolvedValue(
            capabilitiesFixture(['admin']),
        );
        agentServiceMock.getActorRoster.mockResolvedValue([
            rosterFixture({ eligible_model_bindings: [] }),
        ]);
        agentServiceMock.getModelCatalog.mockResolvedValue([disabledCatalog]);
        agentServiceMock.getModelBindings.mockResolvedValue([disabledBinding]);

        const { user } = renderWithProviders(<AgentModelAdministration />);

        expect(await screen.findByText('Actor scope: admin · changes enabled')).toBeInTheDocument();
        const enableCatalog = screen.getByRole('button', {
            name: 'Enable model catalog entry Dormant Code',
        });
        const enableBinding = screen.getByRole('button', {
            name: 'Enable binding for Worker Alpha using Dormant Code',
        });
        expect(enableCatalog).toBeDisabled();
        expect(enableBinding).toBeDisabled();

        await user.type(
            screen.getByRole('textbox', { name: 'Change rationale' }),
            'Restore approved routing evidence.',
        );
        const reconcile = screen.getByRole('checkbox', {
            name: 'Explicitly reconcile affected live assignments',
        });
        await user.click(reconcile);
        await user.click(enableCatalog);
        const catalogDialog = await screen.findByRole('dialog', {
            name: 'Enable model catalog entry',
        });
        await user.click(within(catalogDialog).getByRole('button', { name: 'Enable' }));

        await waitFor(() => {
            expect(agentServiceMock.updateModelCatalogEntry).toHaveBeenCalledWith(
                disabledCatalog.id,
                {
                    expected_revision: 8,
                    enabled: true,
                    reconcile_live_assignments: true,
                },
                expect.objectContaining({
                    rationale: 'Restore approved routing evidence.',
                }),
            );
        });

        await waitFor(() => expect(reconcile).not.toBeChecked());
        await user.click(reconcile);
        await user.click(screen.getByRole('button', {
            name: 'Enable binding for Worker Alpha using Dormant Code',
        }));
        const bindingDialog = await screen.findByRole('dialog', {
            name: 'Enable model binding',
        });
        await user.click(within(bindingDialog).getByRole('button', { name: 'Enable' }));
        await waitFor(() => {
            expect(agentServiceMock.updateModelBinding).toHaveBeenCalledWith(
                disabledBinding.id,
                {
                    expected_revision: 9,
                    enabled: true,
                    reconcile_live_assignments: true,
                },
                expect.objectContaining({
                    rationale: 'Restore approved routing evidence.',
                }),
            );
        });
    });

    it('preserves a stale catalog draft until overwrite is explicitly prepared', async () => {
        agentServiceMock.getCapabilities.mockResolvedValue(
            capabilitiesFixture(['admin']),
        );
        agentServiceMock.updateModelCatalogEntry.mockRejectedValueOnce({
            response: {
                status: 409,
                data: {
                    detail: {
                        code: 'agent_model_revision_conflict',
                        message: 'model_catalog revision is stale',
                        current_revision: 4,
                    },
                },
            },
        });

        const { user } = renderWithProviders(<AgentModelAdministration />);

        await screen.findByText('Actor scope: admin · changes enabled');
        await user.type(
            screen.getByRole('textbox', { name: 'Change rationale' }),
            'Update the configured alias.',
        );
        await user.click(screen.getByRole('button', {
            name: 'Edit model catalog entry Balanced Code',
        }));
        expect(screen.getByRole('heading', { name: 'Edit catalog entry' })).toBeInTheDocument();
        const alias = screen.getByRole('textbox', { name: 'Configured model alias' });
        await user.clear(alias);
        await user.type(alias, 'Balanced Code v2');

        await user.click(screen.getByRole('button', { name: 'Save' }));

        expect(await screen.findByRole('alert')).toHaveTextContent(
            'model_catalog revision is stale',
        );
        expect(screen.getByRole('heading', { name: 'Edit catalog entry' })).toBeInTheDocument();
        expect(screen.getByRole('textbox', { name: 'Stable catalog key' })).toHaveValue('balanced-code');
        expect(alias).toHaveValue('Balanced Code v2');
        expect(agentServiceMock.updateModelCatalogEntry).toHaveBeenLastCalledWith(
            11,
            expect.objectContaining({ expected_revision: 3 }),
            expect.any(Object),
        );

        await user.click(screen.getByRole('button', { name: 'Prepare overwrite' }));
        const overwriteDialog = await screen.findByRole('dialog', {
            name: 'Prepare this draft to overwrite the latest state?',
        });
        await user.click(within(overwriteDialog).getByRole('button', { name: 'Prepare overwrite' }));
        await user.click(screen.getByRole('button', { name: 'Save' }));
        await waitFor(() => {
            expect(agentServiceMock.updateModelCatalogEntry).toHaveBeenLastCalledWith(
                11,
                expect.objectContaining({
                    expected_revision: 4,
                    configured_model_alias: 'Balanced Code v2',
                }),
                expect.any(Object),
            );
        });
    });

    it('preserves a stale binding draft until overwrite is explicitly prepared', async () => {
        agentServiceMock.getCapabilities.mockResolvedValue(
            capabilitiesFixture(['admin']),
        );
        agentServiceMock.updateModelBinding.mockRejectedValueOnce({
            response: {
                status: 409,
                data: {
                    detail: {
                        code: 'agent_model_revision_conflict',
                        message: 'model_binding revision is stale',
                        current_revision: 5,
                    },
                },
            },
        });

        const { user } = renderWithProviders(<AgentModelAdministration />);

        await screen.findByText('Actor scope: admin · changes enabled');
        await user.type(
            screen.getByRole('textbox', { name: 'Change rationale' }),
            'Update the binding policy.',
        );
        await user.click(screen.getByRole('button', {
            name: 'Edit binding for Worker Alpha using Balanced Code',
        }));
        expect(screen.getByRole('heading', { name: 'Edit model binding' })).toBeInTheDocument();
        const tools = screen.getByRole('textbox', { name: 'Tools' });
        await user.clear(tools);
        await user.type(tools, 'code-edit, shell');

        await user.click(screen.getByRole('button', { name: 'Save' }));

        expect(await screen.findByRole('alert')).toHaveTextContent(
            'model_binding revision is stale',
        );
        expect(screen.getByRole('heading', { name: 'Edit model binding' })).toBeInTheDocument();
        expect(screen.getByRole('combobox', { name: 'Actor' })).toHaveValue('2');
        expect(tools).toHaveValue('code-edit, shell');
        expect(agentServiceMock.updateModelBinding).toHaveBeenLastCalledWith(
            21,
            expect.objectContaining({ expected_revision: 4 }),
            expect.any(Object),
        );

        await user.click(screen.getByRole('button', { name: 'Prepare overwrite' }));
        const overwriteDialog = await screen.findByRole('dialog', {
            name: 'Prepare this draft to overwrite the latest state?',
        });
        await user.click(within(overwriteDialog).getByRole('button', { name: 'Prepare overwrite' }));
        await user.click(screen.getByRole('button', { name: 'Save' }));
        await waitFor(() => {
            expect(agentServiceMock.updateModelBinding).toHaveBeenLastCalledWith(
                21,
                expect.objectContaining({
                    expected_revision: 5,
                    tool_tags: ['code-edit', 'shell'],
                }),
                expect.any(Object),
            );
        });
    });
});
