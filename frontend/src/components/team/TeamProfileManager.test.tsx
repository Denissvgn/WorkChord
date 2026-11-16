import { screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { AgentActorRosterItem, AgentModelBinding } from '../../types/agent';
import type {
    TeamMemberProfile,
    TeamMemberProfileCreate,
    TeamMemberProfileUpdate,
} from '../../types/team';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TeamProfileManager } from './TeamProfileManager';
import { buildDirectory, type DirectoryRow } from './directoryModel';

const teamServiceMock = vi.hoisted(() => ({
    createProfile: vi.fn(),
    updateProfile: vi.fn(),
    deleteProfile: vi.fn(),
    createProfileSkill: vi.fn(),
    updateProfileSkill: vi.fn(),
    deleteProfileSkill: vi.fn(),
}));
const planningMock = vi.hoisted(() => ({ readInitial: vi.fn() }));
vi.mock('../../services/planningInputService', () => ({ planningInputService: planningMock }));
vi.mock('../../services/teamService', () => ({ teamService: teamServiceMock }));

const profileFixture = (overrides: Partial<TeamMemberProfile> = {}): TeamMemberProfile => ({
    id: 42,
    seed_key: 'frontend-worker',
    display_name: 'Frontend Worker',
    email: null,
    headline: 'React implementation worker',
    summary: null,
    notes: null,
    automation_enabled: true,
    profile_kind: 'agent',
    assignment_modes: ['execution'],
    skills: [],
    created_at: '2026-07-28T10:00:00Z',
    updated_at: '2026-07-28T10:00:00Z',
    ...overrides,
});

const bindingFixture = (): AgentModelBinding => ({
    id: 5, actor_id: 9, model_catalog_id: 3, is_default: true, enabled: true, tool_tags: [], data_policy_tags: [],
    revision: 1, model_catalog_key: 'sonnet', selectable: true, live_assignment_count: 0, historical_assignment_count: 0,
    run_reference_count: 0, created_at: '', updated_at: '',
    model_catalog: {
        id: 3, key: 'sonnet', provider: 'anthropic', configured_model_alias: 'claude-sonnet-5-5', reasoning_tier: 3,
        context_tier: 'large', modality_tags: [], cost_tier: 'medium', latency_tier: 'balanced', enabled: true, revision: 1,
        last_verified_at: null, created_at: '', updated_at: '',
    },
});

const actorFixture = (): AgentActorRosterItem => ({
    id: 9, name: 'frontend-worker', display_name: 'Frontend Worker', scopes: [], enabled: true, role: 'worker', profile_id: 42,
    work_policy: 'default', max_parallel_work: 1, queue_revision: 1, created_at: '', last_seen_at: '2026-07-28T10:00:00Z',
    actor_revision: 1, profile_revision: null, profile: null, eligible_model_bindings: [bindingFixture()],
    queued_assignments: 0, accepted_assignments: 0, running_runs: 0,
});

const rowFor = (profile: TeamMemberProfile, roster: AgentActorRosterItem[] = [], state: 'loaded' | 'unavailable' = 'loaded'): DirectoryRow => (
    buildDirectory([profile], roster, state, Date.parse('2026-07-28T10:05:00Z'))[0]
);

const renderDrawer = (row: DirectoryRow | null, extra: { rosterUnavailable?: boolean; onCreated?: (id: number) => void; onClose?: () => void } = {}) => renderWithProviders(
    <TeamProfileManager row={row} rosterUnavailable={extra.rosterUnavailable ?? false}
        onClose={extra.onClose ?? vi.fn()} onCreated={extra.onCreated ?? vi.fn()} />,
);

describe('team profile drawer', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        planningMock.readInitial.mockImplementation(async (_kind: string, id: number) => ({
            resource_id: id, resource: profileFixture({ id }), expected_revisions: { 1: 7, 2: 3 }, complete: true,
        }));
        teamServiceMock.createProfile.mockImplementation(async (data: TeamMemberProfileCreate) => profileFixture({ id: 101, ...data }));
        teamServiceMock.updateProfile.mockImplementation(async (_id: number, data: TeamMemberProfileUpdate) => profileFixture(data));
    });

    it('round-trips seed key, profile kind, and assignment modes in create payloads', async () => {
        const onCreated = vi.fn();
        const { user } = renderDrawer(null, { onCreated });

        expect(screen.getByRole('dialog', { name: 'Add person' })).toBeVisible();
        expect(screen.queryByRole('heading', { name: 'Capabilities' })).not.toBeInTheDocument();
        await user.type(screen.getByRole('textbox', { name: 'Seed key' }), 'frontend-specialist');
        await user.type(screen.getByRole('textbox', { name: 'Display name' }), 'Frontend Specialist');
        await user.selectOptions(screen.getByRole('combobox', { name: 'Profile kind' }), 'agent');
        await user.click(screen.getByRole('checkbox', { name: 'Execution' }));
        await user.click(screen.getByRole('checkbox', { name: 'Verification' }));
        await user.click(screen.getByRole('button', { name: 'Create' }));

        await waitFor(() => expect(teamServiceMock.createProfile).toHaveBeenCalledWith({
            seed_key: 'frontend-specialist',
            display_name: 'Frontend Specialist',
            email: null,
            headline: null,
            summary: null,
            notes: null,
            automation_enabled: true,
            profile_kind: 'agent',
            assignment_modes: ['execution', 'verification'],
        }));
        await waitFor(() => expect(onCreated).toHaveBeenCalledWith(101));
    });

    it('omits immutable seed key from updates while preserving kind and modes', async () => {
        const profile = profileFixture({ seed_key: 'immutable-hybrid', profile_kind: 'hybrid', assignment_modes: ['execution', 'verification'] });
        const { user } = renderDrawer(rowFor(profile));

        expect(screen.getByRole('textbox', { name: 'Seed key' })).toHaveAttribute('readonly');
        expect(screen.getByRole('combobox', { name: 'Profile kind' })).toHaveValue('hybrid');
        expect(screen.getByRole('checkbox', { name: 'Execution' })).toBeChecked();
        expect(screen.getByRole('checkbox', { name: 'Verification' })).toBeChecked();

        await waitFor(() => expect(screen.getByRole('button', { name: 'Save' })).toBeEnabled());
        await user.click(screen.getByRole('button', { name: 'Save' }));

        await waitFor(() => expect(teamServiceMock.updateProfile).toHaveBeenCalledTimes(1));
        const [profileId, payload, revisions] = teamServiceMock.updateProfile.mock.calls[0] as [number, TeamMemberProfileUpdate, Record<number, number>];
        expect(profileId).toBe(profile.id);
        expect(payload).toEqual({
            display_name: profile.display_name,
            email: null,
            headline: profile.headline,
            summary: null,
            notes: null,
            automation_enabled: true,
            profile_kind: 'hybrid',
            assignment_modes: ['execution', 'verification'],
        });
        expect(payload).not.toHaveProperty('seed_key');
        expect(revisions).toEqual({ 1: 7, 2: 3 });
    });

    it('shows an agent its read-only model binding and one sentence about when it receives work', async () => {
        const profile = profileFixture();
        renderDrawer(rowFor(profile, [actorFixture()]));

        const binding = await screen.findByRole('list', { name: 'Model binding' });
        expect(binding).toHaveTextContent('claude-sonnet-5-5');
        expect(binding).toHaveTextContent('anthropic');
        expect(screen.getByText(/An agent receives work only while it is connected/)).toBeVisible();
        expect(screen.queryByText(/Automation is only one routing prerequisite/)).not.toBeInTheDocument();
        expect(screen.queryByRole('note')).not.toBeInTheDocument();
        expect(screen.getByText('Default availability')).toBeVisible();
    });

    it('says Unknown for the model and connection when the roster cannot be read', () => {
        renderDrawer(rowFor(profileFixture(), [], 'unavailable'), { rosterUnavailable: true });

        expect(screen.getAllByText('Unknown')).toHaveLength(2);
        expect(screen.getByText(/need the admin key/)).toBeVisible();
    });

    it('does not describe a person with a model or routing sentence', () => {
        renderDrawer(rowFor(profileFixture({ profile_kind: 'human' })));

        expect(screen.queryByRole('heading', { name: 'Model binding' })).not.toBeInTheDocument();
        expect(screen.queryByText(/An agent receives work/)).not.toBeInTheDocument();
    });

    it('adds a capability with the observed revisions', async () => {
        teamServiceMock.createProfileSkill.mockResolvedValue({});
        const { user } = renderDrawer(rowFor(profileFixture({ profile_kind: 'human' })));

        await waitFor(() => expect(screen.getByRole('button', { name: 'Add capability' })).toBeEnabled());
        await user.click(screen.getByRole('button', { name: 'Add capability' }));
        await user.type(screen.getByRole('textbox', { name: /^Capability/ }), 'Cryptography');
        const form = screen.getByRole('form', { name: 'Capabilities' });
        await user.click(within(form).getByRole('button', { name: 'Add capability' }));

        await waitFor(() => expect(teamServiceMock.createProfileSkill).toHaveBeenCalledTimes(1));
        const [profileId, data, revisions] = teamServiceMock.createProfileSkill.mock.calls[0];
        expect(profileId).toBe(42);
        expect(data).toMatchObject({ skill_name: 'Cryptography', skill_key: 'cryptography', level: 3 });
        expect(revisions).toEqual({ 1: 7, 2: 3 });
    });

    it('announces profile mutation failures to assistive technology', async () => {
        teamServiceMock.createProfile.mockRejectedValueOnce({ response: { status: 400, data: { detail: 'Profile save failed.' } } });
        const { user } = renderDrawer(null);

        await user.type(screen.getByRole('textbox', { name: 'Display name' }), 'Unavailable Worker');
        await user.click(screen.getByRole('button', { name: 'Create' }));

        expect(await screen.findByRole('alert')).toHaveTextContent('Profile save failed.');
    });
});

describe('profile conflict observation', () => {
    it('keeps the typed value and original complete map until explicit reapply', async () => {
        const profile = profileFixture();
        planningMock.readInitial.mockResolvedValue({ resource: profile, expected_revisions: { 1: 7, 2: 3 }, complete: true });
        teamServiceMock.updateProfile.mockRejectedValue({ response: { status: 409, data: { detail: 'Scope changed' } } });
        const { user } = renderDrawer(rowFor(profile));
        await waitFor(() => expect(screen.getByRole('button', { name: 'Save' })).toBeEnabled());
        const input = screen.getByRole('textbox', { name: 'Display name' });
        await user.clear(input); await user.type(input, 'Retained draft');
        const reads = planningMock.readInitial.mock.calls.length;
        planningMock.readInitial.mockResolvedValue({ resource: { ...profile, display_name: 'Peer update' }, expected_revisions: { 1: 8, 2: 4, 3: 1 }, complete: true });
        await user.click(screen.getByRole('button', { name: 'Save' }));
        await screen.findByRole('alert');
        expect(input).toHaveValue('Retained draft');
        expect(planningMock.readInitial.mock.calls.length).toBe(reads);
        expect(teamServiceMock.updateProfile.mock.lastCall?.[2]).toEqual({ 1: 7, 2: 3 });
        await user.click(screen.getByRole('button', { name: 'Keep draft with current version' }));
        await waitFor(() => expect(planningMock.readInitial.mock.calls.length).toBe(reads + 1));
        await user.click(screen.getByRole('button', { name: 'Save' }));
        await waitFor(() => expect(teamServiceMock.updateProfile.mock.lastCall?.[2]).toEqual({ 1: 8, 2: 4, 3: 1 }));
        expect(input).toHaveValue('Retained draft');
    });
});
