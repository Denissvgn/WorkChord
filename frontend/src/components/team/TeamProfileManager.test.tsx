import { screen, waitFor, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createHash } from 'node:crypto';
import type { AgentActorRosterItem, AgentModelBinding, AgentTeamMaster, AgentTeamMemberSpec, AgentTeamMemberStatus, AgentTeamStatus } from '../../types/agent';
import type {
    TeamMemberProfile,
    TeamMemberProfileCreate,
    TeamMemberProfileUpdate,
} from '../../types/team';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TeamProfileManager } from './TeamProfileManager';
import { buildDirectory, type DirectoryRow } from './directoryModel';
import { clearAdminApiKey, setAdminApiKey } from '../../utils/adminAccess';

const teamServiceMock = vi.hoisted(() => ({
    createProfile: vi.fn(),
    updateProfile: vi.fn(),
    deleteProfile: vi.fn(),
    createProfileSkill: vi.fn(),
    updateProfileSkill: vi.fn(),
    deleteProfileSkill: vi.fn(),
}));
const planningMock = vi.hoisted(() => ({ readInitial: vi.fn() }));
const agentServiceMock = vi.hoisted(() => ({ linkActorProfile: vi.fn(), getAgentTeamStatus: vi.fn(), getAgentTeamStartingPoints: vi.fn() }));
vi.mock('../../services/agentService', () => ({ agentService: agentServiceMock }));
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

const renderDrawer = (row: DirectoryRow | null, extra: { onCreated?: (id: number) => void; onClose?: () => void } = {}) => renderWithProviders(
    <TeamProfileManager row={row}
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
        planningMock.readInitial.mockResolvedValue({ resource: profile, expected_revisions: { 1: 7, 2: 3 }, complete: true });
        const { user } = renderDrawer(rowFor(profile));

        expect(await screen.findByRole('textbox', { name: 'Seed key' })).toHaveAttribute('readonly');
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

    it('says Unknown for the model and connection when the roster cannot be read', async () => {
        renderDrawer(rowFor(profileFixture(), [], 'unavailable'));
        await screen.findByRole('textbox', { name: 'Display name' });

        expect(screen.getAllByText('Unknown')).toHaveLength(2);
        expect(screen.getByText(/need the admin key/)).toBeVisible();
    });

    it('does not describe a person with a model or routing sentence', async () => {
        renderDrawer(rowFor(profileFixture({ profile_kind: 'human' })));
        await screen.findByRole('textbox', { name: 'Display name' });

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


describe('profile drawer keeps its values and revisions together', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        teamServiceMock.updateProfile.mockImplementation(async (_id: number, data: TeamMemberProfileUpdate) => profileFixture(data));
    });

    it('fills the form from the profile as observed, not from the cached row, and saves it at the same revisions', async () => {
        const cached = profileFixture({ display_name: 'Cached Name', headline: 'Cached headline' });
        planningMock.readInitial.mockResolvedValue({
            resource: profileFixture({ display_name: 'Peer Name', headline: 'Peer headline' }), expected_revisions: { 1: 9 }, complete: true,
        });
        const { user } = renderDrawer(rowFor(cached));

        expect(await screen.findByRole('textbox', { name: 'Display name' })).toHaveValue('Peer Name');
        expect(screen.getByRole('textbox', { name: 'Headline' })).toHaveValue('Peer headline');
        await user.click(screen.getByRole('button', { name: 'Save' }));

        await waitFor(() => expect(teamServiceMock.updateProfile).toHaveBeenCalledTimes(1));
        const [, payload, revisions] = teamServiceMock.updateProfile.mock.calls[0] as [number, TeamMemberProfileUpdate, Record<number, number>];
        expect(payload).toMatchObject({ display_name: 'Peer Name', headline: 'Peer headline' });
        expect(revisions).toEqual({ 1: 9 });
    });

    it('does not show the cached values while the profile is still being read', async () => {
        let release: (value: unknown) => void = () => {};
        planningMock.readInitial.mockReturnValue(new Promise(resolve => { release = resolve; }));
        renderDrawer(rowFor(profileFixture({ display_name: 'Cached Name' })));

        expect(await screen.findByRole('status')).toHaveTextContent('Loading');
        expect(screen.queryByRole('textbox', { name: 'Display name' })).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Save' })).not.toBeInTheDocument();
        release({ resource: profileFixture({ display_name: 'Observed Name' }), expected_revisions: { 1: 2 }, complete: true });
        expect(await screen.findByRole('textbox', { name: 'Display name' })).toHaveValue('Observed Name');
    });

    it('moves the saved revisions on after a capability change only when nobody else changed the profile', async () => {
        const profile = profileFixture({ profile_kind: 'human' });
        planningMock.readInitial.mockResolvedValue({ resource: profile, expected_revisions: { 1: 7 }, complete: true });
        teamServiceMock.createProfileSkill.mockResolvedValue({});
        const { user } = renderDrawer(rowFor(profile));
        await user.click(await screen.findByRole('button', { name: 'Add capability' }));
        await user.type(screen.getByRole('textbox', { name: /^Capability/ }), 'Cryptography');
        planningMock.readInitial.mockResolvedValue({ resource: profile, expected_revisions: { 1: 8 }, complete: true });
        await user.click(within(screen.getByRole('form', { name: 'Capabilities' })).getByRole('button', { name: 'Add capability' }));
        await waitFor(() => expect(teamServiceMock.createProfileSkill).toHaveBeenCalledTimes(1));
        await waitFor(() => expect(screen.queryByRole('form', { name: 'Capabilities' })).not.toBeInTheDocument());

        await user.click(screen.getByRole('button', { name: 'Save' }));
        await waitFor(() => expect(teamServiceMock.updateProfile).toHaveBeenCalledTimes(1));
        expect(teamServiceMock.updateProfile.mock.lastCall?.[2]).toEqual({ 1: 8 });
    });

    it('keeps the older revisions after a capability change when someone else edited the profile fields', async () => {
        const profile = profileFixture({ profile_kind: 'human' });
        planningMock.readInitial.mockResolvedValue({ resource: profile, expected_revisions: { 1: 7 }, complete: true });
        teamServiceMock.createProfileSkill.mockResolvedValue({});
        const { user } = renderDrawer(rowFor(profile));
        await user.click(await screen.findByRole('button', { name: 'Add capability' }));
        await user.type(screen.getByRole('textbox', { name: /^Capability/ }), 'Cryptography');
        planningMock.readInitial.mockResolvedValue({
            resource: { ...profile, display_name: 'Peer edit' }, expected_revisions: { 1: 8 }, complete: true,
        });
        await user.click(within(screen.getByRole('form', { name: 'Capabilities' })).getByRole('button', { name: 'Add capability' }));
        await waitFor(() => expect(screen.queryByRole('form', { name: 'Capabilities' })).not.toBeInTheDocument());

        await user.click(screen.getByRole('button', { name: 'Save' }));
        await waitFor(() => expect(teamServiceMock.updateProfile).toHaveBeenCalledTimes(1));
        expect(teamServiceMock.updateProfile.mock.lastCall?.[2]).toEqual({ 1: 7 });
    });
});

describe('agent without a profile', () => {
    const profilelessActor = (): AgentActorRosterItem => ({ ...actorFixture(), id: 11, name: 'review-bot', display_name: 'Review Bot', role: 'verifier', profile_id: null });
    const profilelessRow = () => buildDirectory([], [profilelessActor()], 'loaded', Date.parse('2026-07-28T10:05:00Z'))[0];

    beforeEach(() => {
        vi.clearAllMocks();
        setAdminApiKey('operator-key');
        teamServiceMock.createProfile.mockImplementation(async (data: TeamMemberProfileCreate) => profileFixture({ id: 101, ...data }));
        agentServiceMock.linkActorProfile.mockResolvedValue(undefined);
    });
    afterEach(() => { clearAdminApiKey(); });

    it('says there is no profile and offers no way to create a person', () => {
        renderDrawer(profilelessRow());

        expect(screen.getByText(/has no profile yet/)).toBeVisible();
        expect(screen.getByRole('button', { name: 'Create and link profile' })).toBeEnabled();
        expect(screen.getByRole('list', { name: 'Model binding' })).toHaveTextContent('claude-sonnet-5-5');
        expect(screen.queryByRole('textbox', { name: 'Display name' })).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Create' })).not.toBeInTheDocument();
        expect(screen.queryByRole('heading', { name: 'Capabilities' })).not.toBeInTheDocument();
        expect(planningMock.readInitial).not.toHaveBeenCalled();
    });

    it('creates an agent profile for the agent and links it', async () => {
        const onCreated = vi.fn();
        const { user } = renderDrawer(profilelessRow(), { onCreated });

        await user.click(screen.getByRole('button', { name: 'Create and link profile' }));

        await waitFor(() => expect(onCreated).toHaveBeenCalledWith(101));
        expect(teamServiceMock.createProfile).toHaveBeenCalledWith(expect.objectContaining({
            display_name: 'Review Bot', profile_kind: 'agent', assignment_modes: ['verification'], seed_key: null,
        }));
        expect(agentServiceMock.linkActorProfile).toHaveBeenCalledWith(11, 101);
    });

    it('retries only the link when linking failed after the profile was created', async () => {
        agentServiceMock.linkActorProfile.mockRejectedValueOnce({ response: { status: 403, data: { detail: 'Admin key required.' } } });
        const onCreated = vi.fn();
        const { user } = renderDrawer(profilelessRow(), { onCreated });

        await user.click(screen.getByRole('button', { name: 'Create and link profile' }));
        expect(await screen.findByRole('alert')).toHaveTextContent('could not be linked');
        expect(onCreated).not.toHaveBeenCalled();

        await user.click(screen.getByRole('button', { name: 'Create and link profile' }));
        await waitFor(() => expect(onCreated).toHaveBeenCalledWith(101));
        expect(teamServiceMock.createProfile).toHaveBeenCalledTimes(1);
        expect(agentServiceMock.linkActorProfile).toHaveBeenCalledTimes(2);
    });

    it('cannot create the profile without the admin key and says why', () => {
        clearAdminApiKey();
        renderDrawer(profilelessRow());

        expect(screen.getByRole('button', { name: 'Create and link profile' })).toBeDisabled();
        expect(screen.getByText(/needs the admin key/)).toBeVisible();
    });

    describe('an agent that waits for its runtime', () => {
        const waitingSpec: AgentTeamMemberSpec = {
            actor_key: 'codex-worker-1', actor_name: 'workchord-codex-worker-1', display_name: 'Codex Worker 1', role: 'worker',
            scope_preset: 'worker-v1', profile_key: 'worker-profile',
            skill_package: { name: 'workchord-worker', version: '1.8.0', sha256: 'a'.repeat(64) },
            assignment_modes: ['execution'], model_binding_keys: ['sonnet'], default_model_binding_key: 'sonnet',
            runtime_ref: 'runtime://codex/codex-worker-1', credential_ref: 'private-sink/codex-worker-1',
        };
        const waitingStatus = (): AgentTeamMemberStatus => ({
            actor_key: 'codex-worker-1', actor_id: 9, actor_name: waitingSpec.actor_name, display_name: waitingSpec.display_name, role: 'worker',
            desired: true, configured: true, lifecycle_state: 'onboarding', enabled: true, profile_key: 'worker-profile', profile_revision: null,
            binding_revisions: {}, skill_package: waitingSpec.skill_package, package_acknowledged: false, acknowledgement_state: 'missing',
            credential_delivery_state: 'delivered', connection_state: 'unobserved', last_seen_at: null, queued_assignments: 0,
            accepted_assignments: 0, running_runs: 0, runtime_ready: false, availability: 'availability_unknown', blocker_codes: [],
            handoff: {
                schema_version: 'agent-team-runtime-handoff-v1', topology_key: 'team', topology_revision: 8, actor_key: 'codex-worker-1', actor_id: 9,
                role: 'worker', server_url: 'https://workchord.example', required_server_features: [], skill_package: waitingSpec.skill_package,
                profile_key: 'worker-profile', profile_revision: 'r1', model_binding_revisions: {}, supported_assignment_modes: ['execution'],
                startup_instructions: [], credential_ref: 'private-sink/codex-worker-1',
            },
        });
        const topology: AgentTeamMaster = {
            schema_version: 'agent-team-master-v1', topology_key: 'team', server_url: 'https://workchord.example', credential_sink_ref: 'private-sink',
            required_server_features: [], controller: { ...waitingSpec, actor_key: 'pm-1', role: 'pm', scope_preset: 'pm-v1' },
            workers: [waitingSpec], verifiers: [], readiness_policy: { minimum_execution_workers: 1, require_independent_verifier_when_assessed: false, maximum_runtime_staleness_seconds: 300 },
        };
        const teamStatus = (members: AgentTeamMemberStatus[]): AgentTeamStatus => ({
            schema_version: 'agent-team-status-v1', topology_key: 'team', topology_revision: 8, manifest_digest: 'a'.repeat(64), topology_state: 'onboarding',
            runtime_ready: false, availability: 'availability_unknown', blocker_codes: [], steps: [], members, pending_action_ids: [], can_mutate: true, next_action: null,
        });

        beforeEach(() => {
            setAdminApiKey('operator-key');
            agentServiceMock.getAgentTeamStatus.mockResolvedValue(teamStatus([waitingStatus()]));
            agentServiceMock.getAgentTeamStartingPoints.mockResolvedValue({ current: topology, template: topology });
        });
        afterEach(() => { clearAdminApiKey(); });

        it('shows its credential file, package, snippet and handoff in the drawer after Connect was left', async () => {
            const actor: AgentActorRosterItem = { ...actorFixture(), name: 'workchord-codex-worker-1', display_name: 'Codex Worker 1', profile_id: 77 };
            renderDrawer(rowFor(profileFixture({ id: 77, display_name: 'Codex Worker 1' }), [actor]));

            expect(await screen.findByRole('heading', { name: 'Connection steps' })).toBeVisible();
            const filename = `${createHash('sha256').update('private-sink/codex-worker-1').digest('hex').slice(0, 24)}-codex-worker-1.json`;
            await waitFor(() => expect(screen.getByText('Credential file').nextElementSibling).toHaveTextContent(filename));
            expect(screen.getByText('Skill package to install').nextElementSibling).toHaveTextContent('workchord-worker 1.8.0');
            expect(screen.getByLabelText('Codex configuration')).toHaveTextContent(`"$WORKCHORD_CREDENTIAL_DIR/${filename}"`);
            expect(screen.getByText('Runtime handoff')).toBeVisible();
            expect(screen.getByText('Waiting for the runtime acknowledgement…')).toBeVisible();
            expect(screen.getByRole('button', { name: 'Check connection' })).toBeVisible();
        });

        it('shows no connection steps for an agent that is not waiting', async () => {
            agentServiceMock.getAgentTeamStatus.mockResolvedValue(teamStatus([{ ...waitingStatus(), package_acknowledged: true, acknowledgement_state: 'current', connection_state: 'observed' }]));
            const actor: AgentActorRosterItem = { ...actorFixture(), name: 'workchord-codex-worker-1' };
            renderDrawer(rowFor(profileFixture(), [actor]));

            await screen.findByRole('list', { name: 'Model binding' });
            await waitFor(() => expect(agentServiceMock.getAgentTeamStatus).toHaveBeenCalled());
            expect(screen.queryByRole('heading', { name: 'Connection steps' })).not.toBeInTheDocument();
        });
    });
});
