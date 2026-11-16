import { act, screen, waitFor, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import type { AgentActorRosterItem, AgentModelBinding } from '../types/agent';
import type { TeamMemberProfile, TeamMemberProfileSkill } from '../types/team';
import { clearAdminApiKey, setAdminApiKey } from '../utils/adminAccess';
import { expectPageChrome } from '../test/pageChrome';
import { renderWithProviders } from '../test/renderWithProviders';
import TeamPage from './TeamPage';

const services = vi.hoisted(() => ({
    team: { getProfiles: vi.fn() },
    agent: { getActorRoster: vi.fn() },
    planning: { readInitial: vi.fn() },
}));
vi.mock('../services/teamService', () => ({ teamService: services.team }));
vi.mock('../services/agentService', () => ({ agentService: services.agent }));
vi.mock('../services/planningInputService', () => ({ planningInputService: services.planning }));

const skill = (id: number, name: string, level = 3, weak = false): TeamMemberProfileSkill => ({
    id, profile_id: 1, skill_key: name.toLowerCase(), skill_name: name, category: null, level, interest: 3,
    is_weakness: weak, keywords_json: [], notes: null, created_at: '', updated_at: '',
});

const profile = (overrides: Partial<TeamMemberProfile>): TeamMemberProfile => ({
    id: 1, seed_key: null, display_name: 'Ada Lovelace', email: null, headline: null, summary: null, notes: null,
    automation_enabled: true, profile_kind: 'human', assignment_modes: [], skills: [], created_at: '', updated_at: '',
    ...overrides,
});

const binding: AgentModelBinding = {
    id: 5, actor_id: 9, model_catalog_id: 3, is_default: true, enabled: true, tool_tags: [], data_policy_tags: [],
    revision: 1, model_catalog_key: 'sonnet', selectable: true, live_assignment_count: 0, historical_assignment_count: 0,
    run_reference_count: 0, created_at: '', updated_at: '',
    model_catalog: {
        id: 3, key: 'sonnet', provider: 'anthropic', configured_model_alias: 'claude-sonnet-5-5', reasoning_tier: 3,
        context_tier: 'large', modality_tags: [], cost_tier: 'medium', latency_tier: 'balanced', enabled: true, revision: 1,
        last_verified_at: null, created_at: '', updated_at: '',
    },
};

const recently = () => new Date(Date.now() - 60_000).toISOString();

const actor = (overrides: Partial<AgentActorRosterItem>): AgentActorRosterItem => ({
    id: 9, name: 'builder', display_name: 'Builder', scopes: [], enabled: true, role: 'worker', profile_id: 2,
    work_policy: 'default', max_parallel_work: 1, queue_revision: 1, created_at: '', last_seen_at: recently(),
    actor_revision: 1, profile_revision: null, profile: null, eligible_model_bindings: [binding],
    queued_assignments: 0, accepted_assignments: 0, running_runs: 0,
    ...overrides,
});

const PEOPLE = [
    profile({ id: 1, display_name: 'Ada Lovelace', assignment_modes: ['verification'], skills: [skill(1, 'Cryptography', 5), skill(2, 'Frontend', 4), skill(3, 'Design', 3), skill(4, 'Testing', 2), skill(5, 'Docs', 1, true)] }),
    profile({ id: 2, display_name: 'Builder', profile_kind: 'agent', assignment_modes: ['execution'], skills: [skill(6, 'React', 4)] }),
    profile({ id: 3, display_name: 'Idle Agent', profile_kind: 'agent' }),
];

const rowFor = (name: string) => screen.getByRole('button', { name: `Open ${name}` }).closest('tr') as HTMLElement;

const renderTeam = (entry = '/team') => renderWithProviders(<TeamPage />, { initialEntries: [entry] });

describe('Team page', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        services.team.getProfiles.mockResolvedValue(PEOPLE);
        services.agent.getActorRoster.mockResolvedValue([actor({}), actor({ id: 10, name: 'idle', display_name: 'Idle Agent', profile_id: 3, last_seen_at: null, eligible_model_bindings: [] })]);
        services.planning.readInitial.mockImplementation(async (_kind: string, id: number) => ({
            resource_id: id, resource: PEOPLE.find(item => item.id === id), expected_revisions: { 1: 1 }, complete: true,
        }));
    });
    afterEach(() => { clearAdminApiKey(); });

    it('lists people and agents in one table with the model and connection state of each agent', async () => {
        setAdminApiKey('operator-key');
        renderTeam();

        await screen.findByRole('button', { name: 'Open Ada Lovelace' });
        expect(screen.getAllByRole('table')).toHaveLength(1);
        expect(screen.getAllByTestId('team-row')).toHaveLength(3);
        expect(screen.getAllByRole('columnheader').map(header => header.textContent))
            .toEqual(['Name', 'Kind', 'Role', 'Capabilities', 'Model', 'Connection']);

        const person = within(rowFor('Ada Lovelace'));
        expect(person.getByText('Person')).toBeVisible();
        expect(person.getByText('Reviewer')).toBeVisible();
        expect(person.queryByText('Connected')).not.toBeInTheDocument();

        await waitFor(() => expect(within(rowFor('Builder')).getByText('Connected')).toBeVisible());
        const builder = within(rowFor('Builder'));
        expect(builder.getByText('Agent')).toBeVisible();
        expect(builder.getByText('Worker')).toBeVisible();
        expect(builder.getByText('claude-sonnet-5-5')).toBeVisible();

        const idle = within(rowFor('Idle Agent'));
        expect(idle.getByText('Not connected')).toBeVisible();
        expect(idle.getByText('No model')).toBeVisible();
    });

    it('keeps every agent of a shared profile on its row and shows each one in the drawer', async () => {
        setAdminApiKey('operator-key');
        const opusBinding: AgentModelBinding = {
            ...binding, id: 6, actor_id: 12, model_catalog_key: 'opus',
            model_catalog: { ...binding.model_catalog!, id: 4, key: 'opus', configured_model_alias: 'claude-opus-5-5' },
        };
        services.agent.getActorRoster.mockResolvedValue([
            actor({}),
            actor({ id: 12, name: 'builder-review', display_name: 'Builder Review', role: 'verifier', profile_id: 2, last_seen_at: null, eligible_model_bindings: [opusBinding] }),
        ]);
        const { user } = renderTeam();

        await screen.findByRole('button', { name: 'Open Builder' });
        await waitFor(() => expect(within(rowFor('Builder')).getAllByTestId('actor-connection')).toHaveLength(2));
        expect(screen.getAllByTestId('team-row')).toHaveLength(3);
        const row = within(rowFor('Builder'));
        expect(row.getByText('Worker, Reviewer')).toBeVisible();
        expect(row.getAllByTestId('actor-model').map(item => item.textContent)).toEqual(['Worker · claude-sonnet-5-5', 'Reviewer · claude-opus-5-5']);
        expect(row.getAllByTestId('actor-connection').map(item => item.textContent)).toEqual(['WorkerConnected', 'ReviewerNot connected']);

        await user.click(screen.getByRole('button', { name: 'Open Builder' }));
        const drawer = within(await screen.findByRole('dialog', { name: 'Builder' }));
        const worker = within(drawer.getByRole('group', { name: 'Worker · Builder' }));
        expect(worker.getByText('Connected')).toBeVisible();
        expect(worker.getByRole('list', { name: 'Model binding' })).toHaveTextContent('claude-sonnet-5-5');
        const reviewer = within(drawer.getByRole('group', { name: 'Reviewer · Builder Review' }));
        expect(reviewer.getByText('Not connected')).toBeVisible();
        expect(reviewer.getByRole('list', { name: 'Model binding' })).toHaveTextContent('claude-opus-5-5');
    });

    it('shows at most three capability chips and counts the rest', async () => {
        renderTeam();
        await screen.findByRole('button', { name: 'Open Ada Lovelace' });

        const row = within(rowFor('Ada Lovelace'));
        expect(row.getAllByTestId('capability-chip').map(chip => chip.textContent)).toEqual(['Cryptography', 'Frontend', 'Design']);
        expect(row.getByText('+2 more')).toBeVisible();
    });

    it('stays readable without the admin key and shows Unknown, never 0 or an error', async () => {
        renderTeam();

        await screen.findByRole('button', { name: 'Open Builder' });
        expect(services.agent.getActorRoster).not.toHaveBeenCalled();
        expect(screen.queryByRole('alert')).not.toBeInTheDocument();
        for (const name of ['Builder', 'Idle Agent']) {
            const row = within(rowFor(name));
            expect(row.getAllByText('Unknown')).toHaveLength(2);
            expect(row.queryByText(/^0$/)).not.toBeInTheDocument();
            expect(row.queryByText('Not connected')).not.toBeInTheDocument();
        }
        expect(screen.getByText(/need the admin key/)).toBeVisible();
        // People are still listed and readable.
        expect(within(rowFor('Ada Lovelace')).getByText('Person')).toBeVisible();
    });

    it('shows Unknown rather than an error when the roster refuses the request', async () => {
        setAdminApiKey('wrong-key');
        services.agent.getActorRoster.mockRejectedValue({ response: { status: 401, data: { detail: 'Invalid' } } });
        renderTeam();

        await screen.findByRole('button', { name: 'Open Builder' });
        await waitFor(() => expect(services.agent.getActorRoster).toHaveBeenCalled());
        await waitFor(() => expect(within(rowFor('Builder')).getAllByText('Unknown')).toHaveLength(2));
        expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    });

    it('shows Unknown for every agent, row and drawer, when a refresh fails after the roster was read', async () => {
        setAdminApiKey('operator-key');
        const opusBinding: AgentModelBinding = {
            ...binding, id: 6, actor_id: 12, model_catalog_key: 'opus',
            model_catalog: { ...binding.model_catalog!, id: 4, key: 'opus', configured_model_alias: 'claude-opus-5-5' },
        };
        services.agent.getActorRoster.mockResolvedValue([
            actor({}),
            actor({ id: 12, name: 'builder-review', display_name: 'Builder Review', role: 'verifier', profile_id: 2, last_seen_at: null, eligible_model_bindings: [opusBinding] }),
            actor({ id: 10, name: 'idle', display_name: 'Idle Agent', profile_id: 3, eligible_model_bindings: [] }),
        ]);
        const { user, queryClient } = renderTeam();

        await screen.findByRole('button', { name: 'Open Builder' });
        await waitFor(() => expect(within(rowFor('Builder')).getAllByTestId('actor-connection')).toHaveLength(2));
        expect(within(rowFor('Idle Agent')).getByText('Connected')).toBeVisible();

        // The roster stays cached; only the refresh fails.
        services.agent.getActorRoster.mockRejectedValue({ response: { status: 503, data: { detail: 'Unavailable' } } });
        await act(async () => { await queryClient.refetchQueries({ queryKey: ['agent-actor-roster'] }); });
        expect(queryClient.getQueryState(['agent-actor-roster', true])?.status).toBe('error');
        expect(queryClient.getQueryData(['agent-actor-roster', true])).toHaveLength(3);

        await waitFor(() => expect(within(rowFor('Builder')).queryByText('Connected')).not.toBeInTheDocument());
        const shared = within(rowFor('Builder'));
        expect(shared.getAllByTestId('actor-model').map(item => item.textContent)).toEqual(['Worker · Unknown', 'Reviewer · Unknown']);
        expect(shared.getAllByTestId('actor-connection').map(item => item.textContent)).toEqual(['WorkerUnknown', 'ReviewerUnknown']);
        const single = within(rowFor('Idle Agent'));
        expect(single.getAllByText('Unknown')).toHaveLength(2);
        expect(single.queryByText('Connected')).not.toBeInTheDocument();
        expect(single.queryByText('No model')).not.toBeInTheDocument();
        for (const text of ['Connected', 'Not connected', 'claude-sonnet-5-5', 'claude-opus-5-5']) {
            expect(screen.queryByText(text)).not.toBeInTheDocument();
        }
        expect(screen.queryByRole('alert')).not.toBeInTheDocument();
        expect(screen.getByText(/need the admin key/)).toBeVisible();

        await user.click(screen.getByRole('button', { name: 'Open Builder' }));
        const drawer = within(await screen.findByRole('dialog', { name: 'Builder' }));
        const agent = within(drawer.getByRole('region', { name: 'Model binding' }));
        expect(agent.getAllByText('Unknown')).toHaveLength(2);
        for (const text of ['Connected', 'Not connected', 'claude-sonnet-5-5', 'claude-opus-5-5', 'Last seen']) {
            expect(agent.queryByText(text)).not.toBeInTheDocument();
        }
        expect(agent.queryByRole('list', { name: 'Model binding' })).not.toBeInTheDocument();
    });

    it('passes the page chrome check, holds no iteration capacity table, and says where capacity is set', async () => {
        const { container } = renderTeam();
        await screen.findByRole('button', { name: 'Open Ada Lovelace' });

        expectPageChrome(container, { status: 'migrated' });
        expect(screen.getByRole('heading', { level: 1, name: 'Team' })).toBeVisible();
        expect(screen.getByText('Capacity is set per iteration in Plan.')).toBeVisible();
        expect(screen.queryByRole('table', { name: 'Iteration capacity' })).not.toBeInTheDocument();
        expect(screen.queryByText('Iteration capacity')).not.toBeInTheDocument();
        expect(screen.queryByText('Capability profiles')).not.toBeInTheDocument();
        expect(screen.queryByRole('note')).not.toBeInTheDocument();
        const header = within(screen.getByTestId('page-header'));
        expect(header.getByRole('button', { name: 'Add person' })).toHaveClass('btn-primary');
        expect(header.getByRole('button', { name: 'Connect an agent' })).not.toHaveClass('btn-primary');
    });

    it('opens Connect from the header and keeps Models and Connect as placeholders', async () => {
        const { user } = renderTeam();
        await screen.findByRole('button', { name: 'Open Ada Lovelace' });
        expect(screen.getAllByRole('tab').map(tab => tab.textContent)).toEqual(['Members', 'Models', 'Connect']);
        expect(screen.getByRole('tab', { name: 'Members' })).toHaveAttribute('aria-selected', 'true');

        await user.click(screen.getByRole('button', { name: 'Connect an agent' }));
        expect(screen.getByRole('tab', { name: 'Connect' })).toHaveAttribute('aria-selected', 'true');
        expect(screen.getByRole('tabpanel')).toHaveTextContent('Connecting agents is not on this page yet');
        expect(screen.queryByRole('table')).not.toBeInTheDocument();

        await user.click(screen.getByRole('tab', { name: 'Models' }));
        expect(screen.getByRole('tabpanel')).toHaveTextContent('Models are not on this page yet');
    });

    it('opens the Connect tab straight from the address', async () => {
        renderTeam('/team?tab=connect');
        expect(await screen.findByRole('tab', { name: 'Connect' })).toHaveAttribute('aria-selected', 'true');
    });

    it('opens the drawer for a row, and for Add person', async () => {
        setAdminApiKey('operator-key');
        const { user } = renderTeam();
        await screen.findByRole('button', { name: 'Open Builder' });

        await user.click(screen.getByRole('button', { name: 'Open Builder' }));
        const drawer = await screen.findByRole('dialog', { name: 'Builder' });
        expect(within(drawer).getByRole('list', { name: 'Model binding' })).toHaveTextContent('claude-sonnet-5-5');
        expect(within(drawer).getByRole('heading', { name: 'Capabilities' })).toBeVisible();
        expect(within(drawer).getByText('Default availability')).toBeVisible();
        await user.click(within(drawer).getByRole('button', { name: 'Close' }));
        await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());

        await user.click(screen.getByRole('button', { name: 'Add person' }));
        expect(await screen.findByRole('dialog', { name: 'Add person' })).toBeVisible();
    });

    it('lists an agent that has no profile yet', async () => {
        setAdminApiKey('operator-key');
        services.agent.getActorRoster.mockResolvedValue([actor({ id: 11, display_name: 'Loose Agent', name: 'loose', profile_id: null, role: 'verifier' })]);
        renderTeam();

        const row = await screen.findByRole('button', { name: 'Open Loose Agent' });
        expect(within(row.closest('tr') as HTMLElement).getByText('Reviewer')).toBeVisible();
    });

    it('treats an agent not seen recently as not connected', async () => {
        setAdminApiKey('operator-key');
        services.agent.getActorRoster.mockResolvedValue([actor({ last_seen_at: new Date(Date.now() - 3_600_000).toISOString() })]);
        renderTeam();

        await screen.findByRole('button', { name: 'Open Builder' });
        await waitFor(() => expect(within(rowFor('Builder')).getByText('Not connected')).toBeVisible());
    });

    it('shows an empty directory with a way to start', async () => {
        services.team.getProfiles.mockResolvedValue([]);
        renderTeam();
        expect(await screen.findByText('No one on the team yet')).toBeVisible();
        await act(async () => {});
        expect(screen.queryByRole('table')).not.toBeInTheDocument();
    });
});
