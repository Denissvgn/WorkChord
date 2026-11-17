import { act, screen, waitFor, within } from '@testing-library/react';
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
import TeamPage from '../../pages/TeamPage';
import { changeAppLanguage } from '../../i18n/i18n';

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
        agentServiceMock.getCapabilities.mockResolvedValue(capabilitiesFixture(['admin']));
        agentServiceMock.getActorRoster.mockResolvedValue([rosterFixture()]);
        agentServiceMock.getModelCatalog.mockResolvedValue([catalogFixture()]);
        agentServiceMock.getModelBindings.mockResolvedValue([bindingFixture()]);
        agentServiceMock.updateModelCatalogEntry.mockResolvedValue({});
        agentServiceMock.updateModelBinding.mockResolvedValue({});
    });

    it('lists catalog and bindings and saves both edits with an admin key and audit reason', async () => {
        const { user } = renderWithProviders(<TeamPage />, { initialEntries: ['/team?tab=models'] });
        expect(await screen.findByRole('heading', { name: 'Model catalog' })).toBeVisible();
        expect(screen.getAllByRole('table')).toHaveLength(2);
        expect(screen.getAllByText('Balanced Code').length).toBeGreaterThan(0);
        expect(screen.getByText('Worker Alpha')).toBeVisible();
        expect(screen.getByText('private-code')).toBeVisible();
        expect(screen.queryByLabelText('Change rationale')).not.toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: /Edit model catalog entry Balanced Code/i }));
        let drawer = screen.getByRole('dialog', { name: /Edit catalog entry/i });
        await user.clear(within(drawer).getByRole('textbox', { name: /provider/i }));
        await user.type(within(drawer).getByRole('textbox', { name: /provider/i }), 'new-provider');
        await user.click(within(drawer).getByRole('button', { name: 'Save' }));
        let dialog = screen.getByRole('dialog', { name: 'Audited change controls' });
        await user.type(within(dialog).getByLabelText('Change rationale'), 'Update catalog');
        await user.click(within(dialog).getByRole('button', { name: 'Save' }));
        await waitFor(() => expect(agentServiceMock.updateModelCatalogEntry).toHaveBeenCalledWith(11, expect.objectContaining({ provider: 'new-provider', expected_revision: 3 }), expect.objectContaining({ rationale: 'Update catalog' })));

        await user.click(screen.getByRole('button', { name: /Edit binding/i }));
        drawer = screen.getByRole('dialog', { name: /Edit model binding/i });
        await user.clear(within(drawer).getByLabelText('Tools'));
        await user.type(within(drawer).getByLabelText('Tools'), 'shell');
        await user.click(within(drawer).getByRole('button', { name: 'Save' }));
        dialog = screen.getByRole('dialog', { name: 'Audited change controls' });
        await user.type(within(dialog).getByLabelText('Change rationale'), 'Update binding');
        await user.click(within(dialog).getByRole('button', { name: 'Save' }));
        await waitFor(() => expect(agentServiceMock.updateModelBinding).toHaveBeenCalledWith(21, expect.objectContaining({ tool_tags: ['shell'], expected_revision: 4 }), expect.objectContaining({ rationale: 'Update binding' })));
    });

    it.each([
        [false, false, 'Add a model'],
        [false, true, 'Add a model'],
        [true, false, 'Add a binding'],
        [true, true, 'Add a binding'],
    ])('shows one primary action for catalog %s and bindings %s', async (hasCatalog, hasBindings, action) => {
        agentServiceMock.getModelCatalog.mockResolvedValue(hasCatalog ? [catalogFixture()] : []);
        agentServiceMock.getModelBindings.mockResolvedValue(hasBindings ? [bindingFixture()] : []);
        const { container } = renderWithProviders(<TeamPage />, { initialEntries: ['/team?tab=models'] });
        expect(await within(screen.getByTestId('page-header')).findByRole('button', { name: action })).toBeVisible();
        expect(container.querySelectorAll('.btn-primary')).toHaveLength(1);
        expect(within(screen.getByTestId('page-header')).getByRole('button', { name: action })).toHaveClass('btn-primary');
    });

    it.each([
        ['checking access', 'Checking model-routing access…'],
        ['access error', 'Model-routing access could not be confirmed.'],
        ['access denied', 'Model-routing access denied'],
        ['loading evidence', 'Loading model and actor evidence…'],
        ['evidence error', 'Model and actor evidence could not be loaded.'],
    ])('omits header creation actions while %s', async (state, message) => {
        const pending = () => new Promise<never>(() => {});
        const error = { response: { status: 503 } };
        if (state === 'checking access') agentServiceMock.getCapabilities.mockImplementation(pending);
        if (state === 'access error') agentServiceMock.getCapabilities.mockRejectedValue(error);
        if (state === 'access denied') agentServiceMock.getCapabilities.mockResolvedValue(capabilitiesFixture([]));
        if (state === 'loading evidence') agentServiceMock.getModelCatalog.mockImplementation(pending);
        if (state === 'evidence error') agentServiceMock.getModelCatalog.mockRejectedValue(error);

        const { container } = renderWithProviders(<TeamPage />, { initialEntries: ['/team?tab=models'] });
        expect(await screen.findByText(message)).toBeVisible();
        const header = within(screen.getByTestId('page-header'));
        expect(header.queryByRole('button', { name: /Add a (model|binding)/ })).not.toBeInTheDocument();
        expect(header.queryByRole('button', { name: 'More actions' })).not.toBeInTheDocument();
        expect(container.querySelectorAll('.btn-primary')).toHaveLength(0);
    });

    it('removes known header actions when a catalog refresh fails', async () => {
        const { container, queryClient } = renderWithProviders(<TeamPage />, { initialEntries: ['/team?tab=models'] });
        const header = within(screen.getByTestId('page-header'));
        await header.findByRole('button', { name: 'Add a binding' });
        agentServiceMock.getModelCatalog.mockRejectedValue({ response: { status: 503 } });
        await act(async () => {
            await queryClient.refetchQueries({ queryKey: ['agent-model-catalog'] });
        });
        expect(await screen.findByText('Model and actor evidence could not be loaded.')).toBeVisible();
        expect(container.querySelectorAll('.btn-primary')).toHaveLength(0);
        expect(header.queryByRole('button', { name: 'More actions' })).not.toBeInTheDocument();
    });

    it('shows one unlock primary when no agent key is saved', () => {
        agentAccessMock.useAgentAccess.mockReturnValue({ hasAgentKey: false });
        const { container } = renderWithProviders(<TeamPage />, { initialEntries: ['/team?tab=models'] });
        expect(screen.getByRole('link', { name: 'Unlock editing' })).toHaveClass('btn-primary');
        expect(container.querySelectorAll('.btn-primary')).toHaveLength(1);
        expect(screen.getByTestId('page-header').querySelector('.btn-primary')).toBeNull();
    });

    it.each([
        ['en', 'Add a model', 'More actions', 'New model', 'New binding', 'Create catalog entry', 'Create model binding'],
        ['ru', 'Добавить модель', 'Другие действия', 'Новая модель', 'Новая привязка', 'Создать запись каталога', 'Создать привязку модели'],
    ])('opens both creation drawers from the header overflow in %s', async (language, primaryLabel, overflowLabel, modelLabel, bindingLabel, catalogTitle, bindingTitle) => {
        await changeAppLanguage(language);
        agentServiceMock.getModelCatalog.mockResolvedValue([]);
        agentServiceMock.getModelBindings.mockResolvedValue([]);
        const { user, container } = renderWithProviders(<TeamPage />, { initialEntries: ['/team?tab=models'] });
        const header = screen.getByTestId('page-header');
        const primary = await within(header).findByRole('button', { name: primaryLabel });
        expect(primary.parentElement).toHaveClass('wc-page-primary');
        expect(primary.parentElement?.children).toHaveLength(1);
        const overflow = within(header).getByRole('button', { name: overflowLabel });
        expect(overflow.closest('.wc-page-overflow')).not.toBeNull();
        expect(overflow.closest('.wc-page-primary')).toBeNull();
        expect(header.querySelectorAll('.wc-page-overflow')).toHaveLength(1);
        await user.click(overflow);
        await user.click(screen.getByRole('menuitem', { name: modelLabel }));
        const catalogDrawer = screen.getByRole('dialog', { name: catalogTitle });
        expect(catalogDrawer).toBeVisible();
        expect(container.querySelectorAll('.btn-primary')).toHaveLength(1);
        expect(catalogDrawer.querySelectorAll('.btn-primary')).toHaveLength(1);
        await user.keyboard('{Escape}');
        expect(overflow).toHaveFocus();
        await user.click(overflow);
        await user.click(screen.getByRole('menuitem', { name: bindingLabel }));
        const bindingDrawer = screen.getByRole('dialog', { name: bindingTitle });
        expect(bindingDrawer).toBeVisible();
        expect(container.querySelectorAll('.btn-primary')).toHaveLength(1);
        expect(bindingDrawer.querySelectorAll('.btn-primary')).toHaveLength(1);
    });

    it.each([false, true])('shows one header unlock primary to a planning reader with catalog %s', async hasCatalog => {
        agentServiceMock.getCapabilities.mockResolvedValue(capabilitiesFixture(['planning:read']));
        agentServiceMock.getModelCatalog.mockResolvedValue(hasCatalog ? [catalogFixture()] : []);
        agentServiceMock.getModelBindings.mockResolvedValue([]);
        const { container } = renderWithProviders(<TeamPage />, { initialEntries: ['/team?tab=models'] });
        const header = within(screen.getByTestId('page-header'));
        expect(await header.findByRole('link', { name: 'Unlock editing' })).toHaveClass('btn-primary');
        expect(container.querySelectorAll('.btn-primary')).toHaveLength(1);
        expect(header.queryByRole('button', { name: 'More actions' })).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: /^Edit / })).not.toBeInTheDocument();
    });

    it.each([
        [false, 'Добавить модель'],
        [true, 'Добавить привязку'],
    ])('shows one Russian next-step primary with catalog %s', async (hasCatalog, label) => {
        await changeAppLanguage('ru');
        agentServiceMock.getModelCatalog.mockResolvedValue(hasCatalog ? [catalogFixture()] : []);
        const { container } = renderWithProviders(<TeamPage />, { initialEntries: ['/team?tab=models'] });
        expect(await within(screen.getByTestId('page-header')).findByRole('button', { name: label })).toHaveClass('btn-primary');
        expect(container.querySelectorAll('.btn-primary')).toHaveLength(1);
    });

    it('keeps mutation controls unavailable to a planning reader', async () => {
        agentServiceMock.getCapabilities.mockResolvedValue(capabilitiesFixture(['planning:read']));
        renderWithProviders(<AgentModelAdministration />);
        expect(await screen.findByRole('heading', { name: 'Model catalog' })).toBeVisible();
        expect(screen.queryByRole('button', { name: /^Edit / })).not.toBeInTheDocument();
    });
});
