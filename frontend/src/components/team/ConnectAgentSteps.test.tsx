import { createHash } from 'node:crypto';
import { fireEvent, screen, waitFor, within } from '@testing-library/react';
import { AxiosError } from 'axios';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import { agentService } from '../../services/agentService';
import type {
    AgentModelCatalogEntry, AgentTeamMaster, AgentTeamMemberSpec, AgentTeamMemberStatus, AgentTeamPlan, AgentTeamStatus,
} from '../../types/agent';
import { ConnectAgentSteps } from './ConnectAgentSteps';
import i18n from '../../i18n/i18n';
import { AGENT_TEAM_STEP_DEFINITIONS, AGENT_TEAM_STEP_IDS } from '../../features/agentTeamSetup/masters';
import { hasPM, runtimeSnippet } from '../../features/agentTeamSetup/connectAgent';

vi.mock('../../services/agentService', () => ({ agentService: {
    getAgentTeamStatus: vi.fn(), getAgentTeamStartingPoints: vi.fn(), getModelCatalog: vi.fn(), createModelCatalogEntry: vi.fn(),
    validateAgentTeamMaster: vi.fn(), planAgentTeamMaster: vi.fn(), applyAgentTeamAction: vi.fn(), applyAgentTeamActions: vi.fn(),
} }));
vi.mock('../../hooks/useAdminAccess', () => ({ useAdminAccess: () => ({ hasAdminKey: true }), useKeylessReader: () => ({ settings: false }) }));
const service = vi.mocked(agentService);

const member = (role: AgentTeamMemberSpec['role'], key: string): AgentTeamMemberSpec => ({
    actor_key: key, actor_name: `workchord-${key}`, display_name: key, role,
    scope_preset: `${role}-v1`, profile_key: `${role}-profile`,
    skill_package: { name: `workchord-${role === 'verifier' ? 'reviewer' : role}`, version: '1.8.0', sha256: 'a'.repeat(64) },
    assignment_modes: [role === 'pm' ? 'ownership' : role === 'worker' ? 'execution' : 'verification'],
    model_binding_keys: ['catalog-model'], default_model_binding_key: 'catalog-model', runtime_ref: `runtime://${key}`, credential_ref: `private-sink/${key}`,
});
const memberStatus = (spec: AgentTeamMemberSpec, overrides: Partial<AgentTeamMemberStatus> = {}): AgentTeamMemberStatus => ({
    actor_key: spec.actor_key, actor_id: 9, actor_name: spec.actor_name, display_name: spec.display_name, role: spec.role,
    desired: true, configured: true, lifecycle_state: 'connected', enabled: true, profile_key: spec.profile_key, profile_revision: null,
    binding_revisions: {}, skill_package: spec.skill_package, package_acknowledged: false, acknowledgement_state: 'missing',
    credential_delivery_state: 'delivered', connection_state: 'unobserved', last_seen_at: null, queued_assignments: 0,
    accepted_assignments: 0, running_runs: 0, runtime_ready: false, availability: 'availability_unknown', blocker_codes: [], handoff: null,
    ...overrides,
});
const current: AgentTeamMaster = {
    schema_version: 'agent-team-master-v1', topology_key: 'team', server_url: 'https://workchord.example', credential_sink_ref: 'private-sink',
    required_server_features: ['agent-team-master-v1'],
    controller: member('pm', 'primary-pm'), workers: [member('worker', 'existing-worker')], verifiers: [member('verifier', 'existing-reviewer')],
    readiness_policy: { minimum_execution_workers: 1, require_independent_verifier_when_assessed: true, maximum_runtime_staleness_seconds: 300 },
};
const status: AgentTeamStatus = {
    schema_version: 'agent-team-status-v1', topology_key: 'team', topology_revision: 7, manifest_digest: 'a'.repeat(64), topology_state: 'configured',
    runtime_ready: false, availability: 'availability_unknown', blocker_codes: [], steps: [], members: [], pending_action_ids: [], can_mutate: true, next_action: null,
};
const model: AgentModelCatalogEntry = {
    id: 1, key: 'catalog-model', provider: 'OpenAI', configured_model_alias: 'Catalog model', reasoning_tier: 2, context_tier: 'large', cost_tier: 'medium',
    latency_tier: 'balanced', modality_tags: ['text'], enabled: true, revision: 1, last_verified_at: null, created_at: '', updated_at: '',
};
const planFor = (manifest: AgentTeamMaster, actorKey = manifest.workers.at(-1)!.actor_key): AgentTeamPlan => ({
    schema_version: 'agent-team-reconciliation-plan-v1', topology_key: 'team', expected_topology_revision: 7, manifest_digest: 'a'.repeat(64),
    plan_digest: 'b'.repeat(64), blocker_codes: [],
    actions: [{
        action_id: 'create-new', action_digest: 'c'.repeat(64), reconciliation_class: 'create', operation: 'create_member',
        actor_key: actorKey, target_actor_id: null, expected_object_revision: null, expected_actor_revision: null,
        before: null, after: null, preconditions: {}, blocker_code: null, requires_explicit_confirmation: false, authority_change: true,
    }],
});

async function toReview() {
    const view = renderWithProviders(<ConnectAgentSteps />);
    await screen.findByRole('radio', { name: 'Worker' });
    expect(screen.getByRole('radio', { name: 'Reviewer' })).toBeVisible();
    expect(screen.queryByRole('radio', { name: 'PM' })).not.toBeInTheDocument();
    await view.user.click(screen.getByRole('button', { name: 'Continue' }));
    await view.user.click(screen.getByRole('radio', { name: 'Codex' }));
    await view.user.click(screen.getByRole('button', { name: 'Continue' }));
    await view.user.selectOptions(screen.getByRole('combobox', { name: 'Which model will it use?' }), 'catalog-model');
    await view.user.click(screen.getByRole('button', { name: 'Review change' }));
    return view;
}
const blockedReceipt = (code: string) => ({
    schema_version: 'agent-team-apply-receipt-v1' as const, apply_id: 'apply', topology_key: 'team', manifest_digest: 'a'.repeat(64), plan_digest: 'b'.repeat(64),
    expected_topology_revision: 7, resulting_topology_revision: 7, status: 'blocked' as const, replayed: false,
    receipts: [{
        action_id: 'create-new', action_digest: 'c'.repeat(64), reconciliation_class: 'create' as const, operation: 'create_member', actor_key: 'codex-worker-1',
        status: 'blocked' as const, target_actor_id: null, before_revision: null, after_revision: null, blocker_code: code, next_action: 'Server guidance',
    }],
    pending_action_ids: [], blocker_codes: [code],
});
async function toConnect() {
    const view = await toReview();
    await view.user.click(await screen.findByRole('button', { name: 'Continue to connect' }));
    await view.user.click(screen.getByRole('button', { name: 'Connect agent' }));
    return view;
}
async function connect() {
    const view = await toReview();
    await view.user.click(await screen.findByRole('button', { name: 'Continue to connect' }));
    await view.user.click(screen.getByRole('button', { name: 'Connect agent' }));
    await screen.findByText('Waiting for the runtime acknowledgement…');
    return view;
}

beforeEach(() => {
    vi.clearAllMocks(); localStorage.clear(); sessionStorage.clear();
    service.getAgentTeamStatus.mockResolvedValue(structuredClone(status));
    service.getAgentTeamStartingPoints.mockResolvedValue({ current: structuredClone(current), template: structuredClone(current) });
    service.getModelCatalog.mockResolvedValue([model]);
    service.validateAgentTeamMaster.mockImplementation(async manifest => ({
        schema_version: 'agent-team-validation-v1', valid: true, manifest_digest: 'a'.repeat(64), normalized_manifest: manifest, blocker_codes: [],
    }));
    service.planAgentTeamMaster.mockImplementation(async manifest => planFor(manifest));
    service.applyAgentTeamAction.mockResolvedValue({
        schema_version: 'agent-team-apply-receipt-v1', apply_id: 'apply', topology_key: 'team', manifest_digest: 'a'.repeat(64), plan_digest: 'b'.repeat(64),
        expected_topology_revision: 7, resulting_topology_revision: 8, status: 'completed', replayed: false,
        receipts: [{
            action_id: 'create-new', action_digest: 'c'.repeat(64), reconciliation_class: 'create', operation: 'create_member', actor_key: 'codex-worker-1',
            status: 'applied', target_actor_id: 9, before_revision: null, after_revision: 1, blocker_code: null, next_action: null,
        }],
        pending_action_ids: [], blocker_codes: [],
    });
});
afterEach(() => { vi.restoreAllMocks(); });

describe('Connect agent steps', () => {
    it('connects a Worker on Codex in five steps while preserving every existing member in validate, plan and apply', async () => {
        const view = await connect();
        expect(within(screen.getByRole('list', { name: 'Connection steps' })).getAllByRole('listitem').map(item => item.textContent))
            .toEqual(['1. Role', '2. Runtime', '3. Model', '4. Review', '5. Connect']);

        expect(service.validateAgentTeamMaster).toHaveBeenCalledTimes(1);
        const sent = service.validateAgentTeamMaster.mock.calls[0][0];
        expect(sent.controller).toEqual(current.controller);
        expect(sent.workers).toHaveLength(2);
        expect(sent.workers[0]).toEqual(current.workers[0]);
        expect(sent.verifiers).toEqual(current.verifiers);
        expect({ ...sent, controller: undefined, workers: undefined, verifiers: undefined })
            .toEqual({ ...current, controller: undefined, workers: undefined, verifiers: undefined });
        expect(sent.workers[1]).toMatchObject({
            role: 'worker', actor_key: 'codex-worker-1', default_model_binding_key: 'catalog-model', model_binding_keys: ['catalog-model'],
            runtime_ref: 'runtime://codex/codex-worker-1', credential_ref: 'private-sink/codex-worker-1', skill_package: { name: 'workchord-worker' },
        });
        expect(service.planAgentTeamMaster).toHaveBeenCalledWith(sent, 7);
        expect(service.applyAgentTeamAction).toHaveBeenCalledTimes(1);
        expect(service.applyAgentTeamAction).toHaveBeenCalledWith(sent, expect.objectContaining({ expected_topology_revision: 7 }), 'create-new', true, expect.any(Object));

        const added = member('worker', 'codex-worker-1');
        service.getAgentTeamStatus.mockResolvedValue({ ...status, members: [memberStatus(added, { package_acknowledged: true, acknowledgement_state: 'stale', connection_state: 'observed' })] });
        await view.user.click(screen.getByRole('button', { name: 'Check connection' }));
        await waitFor(() => expect(service.getAgentTeamStatus.mock.results.length).toBeGreaterThan(3));
        expect(screen.queryByText('Connected', { exact: true })).not.toBeInTheDocument();
        service.getAgentTeamStatus.mockResolvedValue({ ...status, members: [memberStatus(added, { package_acknowledged: true, acknowledgement_state: 'current', connection_state: 'observed' })] });
        await view.user.click(screen.getByRole('button', { name: 'Check connection' }));
        expect(await screen.findByText('Connected', { exact: true })).toBeVisible();
    });

    it('shows a plain validation error beside the model answer and reveals the server code on demand', async () => {
        service.validateAgentTeamMaster.mockRejectedValue(new AxiosError('Validation failed', '422', undefined, undefined, {
            status: 422, data: { detail: [{ loc: ['body', 'manifest', 'workers', 1, 'default_model_binding_key'], type: 'model_catalog_entry_missing', msg: 'Internal diagnostic' }] },
        } as never));
        const view = await toReview();
        const alert = await screen.findByRole('alert');
        const stepSection = screen.getByRole('region', { name: '3. Model' });
        expect(stepSection).toContainElement(alert);
        expect(within(stepSection).getByRole('combobox', { name: 'Which model will it use?' })).toHaveValue('catalog-model');
        expect(alert).toHaveTextContent('This model cannot be used. Choose an enabled catalog model.');
        expect(alert).not.toHaveTextContent('Internal diagnostic');
        expect(within(alert).getByText('model_catalog_entry_missing')).not.toBeVisible();
        await view.user.click(within(alert).getByText('Server code'));
        expect(within(alert).getByText('model_catalog_entry_missing')).toBeVisible();
        expect(service.planAgentTeamMaster).not.toHaveBeenCalled();
        expect(service.applyAgentTeamAction).not.toHaveBeenCalled();
    });

    it('shows a server blocker for a role beside the Role answer', async () => {
        service.validateAgentTeamMaster.mockImplementation(async manifest => ({
            schema_version: 'agent-team-validation-v1', valid: false, manifest_digest: 'a'.repeat(64), normalized_manifest: manifest, blocker_codes: ['role_package_missing'],
        }));
        await toReview();
        const stepSection = await screen.findByRole('region', { name: '1. Role' });
        expect(within(stepSection).getByRole('alert')).toHaveTextContent('This role cannot be set up on this server.');
        expect(within(stepSection).getByText('role_package_missing')).toBeInTheDocument();
        expect(within(stepSection).getByRole('radio', { name: 'Worker' })).toBeChecked();
    });

    it('keeps the server-only agent key out of browser storage, URL, console and page and names its exact sink file', async () => {
        const secret = 'pmag_server_only_credential_never_transmitted';
        const serverSink = new Map<string, string>();
        const originalApply = service.applyAgentTeamAction.getMockImplementation()!;
        service.applyAgentTeamAction.mockImplementation(async (...args) => {
            serverSink.set('private-sink/codex-worker-1', secret);
            return originalApply(...args);
        });
        const spies = (['log', 'info', 'warn', 'error', 'debug'] as const).map(method => vi.spyOn(console, method));
        const view = await connect();

        expect(serverSink.get('private-sink/codex-worker-1')).toBe(secret);
        const filename = `${createHash('sha256').update('private-sink/codex-worker-1').digest('hex').slice(0, 24)}-codex-worker-1.json`;
        const reference = screen.getByText('Credential folder reference').nextElementSibling;
        expect(reference).toHaveTextContent('private-sink');
        expect(screen.getByText('Credential file').nextElementSibling).toHaveTextContent(filename);
        const snippet = screen.getByLabelText('Codex configuration');
        expect(snippet).toHaveTextContent(`"$WORKCHORD_CREDENTIAL_DIR/${filename}"`);
        expect(snippet).toHaveTextContent("jq -er '.api_key'");
        expect(snippet).toHaveTextContent("WORKCHORD_BASE_URL='https://workchord.example'");
        expect(snippet).toHaveTextContent('https://workchord.example/api/mcp');
        expect(screen.getByText('Skill package to install').nextElementSibling).toHaveTextContent('workchord-worker 1.8.0');

        for (const call of service.applyAgentTeamAction.mock.calls) expect(JSON.stringify(call)).not.toContain(secret);
        expect(JSON.stringify({ ...localStorage })).not.toContain(secret);
        expect(JSON.stringify({ ...sessionStorage })).not.toContain(secret);
        expect(window.location.href).not.toContain(secret);
        expect(document.documentElement.outerHTML).not.toContain(secret);
        expect(document.documentElement.outerHTML).not.toMatch(/pmag_/);
        expect(JSON.stringify(view.queryClient.getQueryCache().getAll().map(query => query.state.data))).not.toContain(secret);
        for (const spy of spies) expect(JSON.stringify(spy.mock.calls)).not.toContain(secret);
    });

    it('retries an interrupted apply with the same idempotency key and prevents changing the candidate', async () => {
        service.applyAgentTeamAction.mockRejectedValueOnce(new Error('connection interrupted'));
        const view = await toReview();
        await view.user.click(await screen.findByRole('button', { name: 'Continue to connect' }));
        await view.user.click(screen.getByRole('button', { name: 'Connect agent' }));
        expect(await screen.findByRole('alert')).toHaveTextContent('Retry this same request to get its receipt');
        await view.user.click(screen.getByRole('button', { name: 'Retry connection' }));
        await screen.findByText('Waiting for the runtime acknowledgement…');
        expect(service.applyAgentTeamAction).toHaveBeenCalledTimes(2);
        expect(service.applyAgentTeamAction.mock.calls[0]).toEqual(service.applyAgentTeamAction.mock.calls[1]);
        expect(screen.queryByRole('button', { name: 'Back' })).not.toBeInTheDocument();
    });

    it('treats a rejected apply as settled and reviews again with a fresh topology, plan and request', async () => {
        service.applyAgentTeamAction.mockRejectedValueOnce(new AxiosError('Conflict', '409', undefined, undefined, {
            status: 409, data: { detail: { code: 'agent_team_plan_digest_conflict', message: 'Plan digest is stale' } },
        } as never));
        const view = await toConnect();
        const reviewStep = await screen.findByRole('region', { name: '4. Review' });
        const alert = within(reviewStep).getByRole('alert');
        expect(alert).toHaveTextContent('The team changed while you were reviewing. Review again to get the current plan.');
        expect(alert).not.toHaveTextContent('Plan digest is stale');
        await view.user.click(within(alert).getByText('Server code'));
        expect(within(alert).getByText('agent_team_plan_digest_conflict')).toBeVisible();
        expect(screen.queryByRole('button', { name: 'Retry connection' })).not.toBeInTheDocument();
        expect(screen.getByRole('button', { name: '1. Role' })).toBeEnabled();
        expect(screen.getByRole('button', { name: 'Back' })).toBeEnabled();

        const reads = service.getAgentTeamStatus.mock.calls.length;
        service.getAgentTeamStatus.mockResolvedValue({ ...status, topology_revision: 8 });
        service.planAgentTeamMaster.mockImplementation(async manifest => ({ ...planFor(manifest), expected_topology_revision: 8, plan_digest: 'd'.repeat(64) }));
        await view.user.click(screen.getByRole('button', { name: 'Review change' }));
        await view.user.click(await screen.findByRole('button', { name: 'Continue to connect' }));
        expect(service.getAgentTeamStatus.mock.calls.length).toBeGreaterThan(reads);
        expect(service.planAgentTeamMaster).toHaveBeenLastCalledWith(expect.anything(), 8);
        await view.user.click(screen.getByRole('button', { name: 'Connect agent' }));
        await screen.findByText('Waiting for the runtime acknowledgement…');
        expect(service.applyAgentTeamAction).toHaveBeenCalledTimes(2);
        const [first, second] = service.applyAgentTeamAction.mock.calls;
        expect(second[1]).toMatchObject({ expected_topology_revision: 8, plan_digest: 'd'.repeat(64) });
        expect(second[4].idempotencyKey).not.toBe(first[4].idempotencyKey);
    });

    it('reviews a blocked apply again and drops the member the blocked request left declared but unconfigured', async () => {
        service.applyAgentTeamAction.mockResolvedValueOnce(blockedReceipt('action_blocked'));
        const view = await toConnect();
        const reviewStep = await screen.findByRole('region', { name: '4. Review' });
        expect(within(reviewStep).getByRole('alert')).toHaveTextContent('The server could not approve this change.');
        expect(within(reviewStep).getByText('action_blocked')).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Retry connection' })).not.toBeInTheDocument();

        // The server stored the blocked manifest, so the attempted member is now declared but not configured.
        const attempted = service.validateAgentTeamMaster.mock.calls[0][0].workers[1];
        service.getAgentTeamStartingPoints.mockResolvedValue({ current: { ...current, workers: [...current.workers, attempted] }, template: current });
        service.getAgentTeamStatus.mockResolvedValue({ ...status, members: [memberStatus(attempted, { configured: false, actor_id: null })] });
        await view.user.click(screen.getByRole('button', { name: 'Review change' }));
        await screen.findByRole('button', { name: 'Continue to connect' });
        const resent = service.validateAgentTeamMaster.mock.calls[1][0];
        expect(resent.workers.map(item => item.actor_key)).toEqual(['existing-worker', 'codex-worker-1']);
        expect(resent.controller).toEqual(current.controller);
        expect(resent.verifiers).toEqual(current.verifiers);
    });

    it('stops at an unconfirmed key delivery with recovery guidance instead of an endless retry', async () => {
        service.applyAgentTeamAction.mockResolvedValueOnce(blockedReceipt('credential_delivery_uncertain'));
        const view = await toConnect();
        const connectStep = await screen.findByRole('region', { name: '5. Connect' });
        const alert = within(connectStep).getByRole('alert');
        expect(alert).toHaveTextContent('could not confirm that it wrote the key to the credential folder');
        expect(alert).toHaveTextContent('Retrying will not change that.');
        expect(within(alert).getByText('credential_delivery_uncertain')).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Retry connection' })).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Connect agent' })).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Back' })).not.toBeInTheDocument();
        expect(screen.getByRole('button', { name: '1. Role' })).toBeDisabled();
        expect(service.applyAgentTeamAction).toHaveBeenCalledTimes(1);

        await view.user.click(within(alert).getByRole('button', { name: 'Open advanced setup' }));
        expect(screen.queryByRole('list', { name: 'Connection steps' })).not.toBeInTheDocument();
        expect(await screen.findByRole('complementary', { name: i18n.t('agentTeamSetup.readinessTitle') })).toBeInTheDocument();
    });

    it('lets the guided flow connect a PM that the team declares but never configured', async () => {
        const configured = memberStatus(current.workers[0]);
        service.getAgentTeamStatus.mockResolvedValue({
            ...status, members: [memberStatus(current.controller, { configured: false, actor_id: null }), configured, memberStatus(current.verifiers[0])],
        });
        service.planAgentTeamMaster.mockImplementation(async manifest => planFor(manifest, manifest.controller.actor_key));
        const view = renderWithProviders(<ConnectAgentSteps />);
        await view.user.click(await screen.findByRole('radio', { name: 'PM' }));
        expect(screen.queryByText('This team already has a PM. A team has one PM.')).not.toBeInTheDocument();
        await view.user.click(screen.getByRole('button', { name: 'Continue' }));
        await view.user.click(screen.getByRole('radio', { name: 'Codex' }));
        await view.user.click(screen.getByRole('button', { name: 'Continue' }));
        await view.user.selectOptions(screen.getByRole('combobox', { name: 'Which model will it use?' }), 'catalog-model');
        await view.user.click(screen.getByRole('button', { name: 'Review change' }));
        expect(await screen.findByText('This replaces primary-pm, a PM the team declares but never connected.')).toBeVisible();
        const sent = service.validateAgentTeamMaster.mock.calls[0][0];
        expect(sent.controller).toMatchObject({ role: 'pm', actor_key: 'codex-pm-1', skill_package: { name: 'workchord-pm' } });
        expect(sent.workers).toEqual(current.workers);
        expect(sent.verifiers).toEqual(current.verifiers);
        await view.user.click(screen.getByRole('button', { name: 'Continue to connect' }));
        await view.user.click(screen.getByRole('button', { name: 'Connect agent' }));
        await screen.findByText('Waiting for the runtime acknowledgement…');
        expect(service.applyAgentTeamAction).toHaveBeenCalledWith(sent, expect.anything(), 'create-new', true, expect.any(Object));
    });

    it('counts a PM as present only when it is configured or not reported as pending', () => {
        const pending = { ...status, members: [memberStatus(current.controller, { configured: false })] };
        expect(hasPM(current, pending)).toBe(false);
        expect(hasPM(current, { ...status, members: [memberStatus(current.controller)] })).toBe(true);
        expect(hasPM(current, status)).toBe(true);
        expect(hasPM(null, status)).toBe(false);
        expect(hasPM(null, { ...status, members: [memberStatus(current.controller)] })).toBe(true);
    });

    it('offers PM only while the team has no PM and adds a catalog entry in a drawer', async () => {
        service.getAgentTeamStartingPoints.mockResolvedValue({ current: null, template: current });
        const view = renderWithProviders(<ConnectAgentSteps />);
        expect(await screen.findByRole('radio', { name: 'PM' })).toBeVisible();
        expect(screen.getByText('Plans the work, assigns it and keeps the team moving.')).toBeVisible();
        await view.user.click(screen.getByRole('button', { name: 'Continue' }));
        await view.user.click(screen.getByRole('button', { name: 'Continue' }));
        await view.user.click(screen.getByRole('button', { name: 'Add a model entry' }));
        const drawer = screen.getByRole('dialog', { name: 'Add a model entry' });
        fireEvent.change(within(drawer).getByLabelText(/Stable catalog key/), { target: { value: 'local-model' } });
        fireEvent.change(within(drawer).getByLabelText(/Configured provider/), { target: { value: 'local' } });
        fireEvent.change(within(drawer).getByLabelText(/Configured model alias/), { target: { value: 'Local model' } });
        service.createModelCatalogEntry.mockResolvedValue({ result: { ...model, key: 'local-model' } } as never);
        service.getModelCatalog.mockResolvedValue([model, { ...model, key: 'local-model' }]);
        await view.user.click(within(drawer).getByRole('button', { name: 'Add a model entry' }));
        await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
        expect(service.createModelCatalogEntry).toHaveBeenCalledWith(expect.objectContaining({ key: 'local-model', provider: 'local' }), expect.any(Object));
        expect(screen.getByRole('combobox', { name: 'Which model will it use?' })).toHaveValue('local-model');
    });

    it('completes the advanced manifest workflow through all seven steps with validate, plan and apply', async () => {
        service.getAgentTeamStatus.mockResolvedValue({ ...status, steps: AGENT_TEAM_STEP_IDS.map(id => ({ id, state: 'todo', blocker_codes: [], next_action: null })) });
        const view = renderWithProviders(<ConnectAgentSteps />);
        await screen.findByRole('radio', { name: 'Worker' });
        await view.user.click(screen.getByText('Advanced: apply a team manifest'));
        expect(screen.queryByRole('list', { name: 'Connection steps' })).not.toBeInTheDocument();

        // The step list is rendered twice (desktop rail and compact summary); read the rail's copy only.
        const rail = await screen.findByRole('complementary', { name: i18n.t('agentTeamSetup.readinessTitle') });
        const railSteps = () => within(rail).getAllByRole('list')
            .filter(list => list.hasAttribute('aria-labelledby'))
            .flatMap(list => within(list).getAllByRole('listitem'));
        await waitFor(() => expect(railSteps()).toHaveLength(7));
        AGENT_TEAM_STEP_DEFINITIONS.forEach((definition, index) => {
            expect(railSteps()[index]).toHaveTextContent(i18n.t(definition.titleKey));
            expect(railSteps()[index]).toHaveTextContent(i18n.t('agentTeamSetup.stepStates.todo'));
        });

        await view.user.click(await screen.findByRole('button', { name: i18n.t('agentTeamSetup.start.current') }));
        await view.user.click(screen.getByRole('button', { name: i18n.t('agentTeamSetup.validate') }));
        await waitFor(() => expect(service.validateAgentTeamMaster).toHaveBeenCalledWith(current));
        await view.user.click(await screen.findByRole('button', { name: i18n.t('agentTeamSetup.dryRun') }));
        await waitFor(() => expect(service.planAgentTeamMaster).toHaveBeenCalledWith(current, 7));
        const apply = await screen.findByRole('button', { name: i18n.t('agentTeamSetup.applyActionFor', {
            action: i18n.t('agentTeamSetup.operations.createMember'), actionId: 'create-new', actor: 'existing-worker',
        }) });
        expect(apply).toBeDisabled();
        await view.user.type(screen.getByRole('textbox', { name: i18n.t('agentTeamSetup.rationale') }), 'Connect the reviewed team members');
        service.getAgentTeamStatus.mockResolvedValue({
            ...status, runtime_ready: true, topology_state: 'runtime_ready', topology_revision: 8,
            steps: AGENT_TEAM_STEP_IDS.map(id => ({ id, state: 'done', blocker_codes: [], next_action: null })),
        });
        expect(apply).toBeEnabled();
        await view.user.click(apply);
        await waitFor(() => expect(service.applyAgentTeamAction).toHaveBeenCalledWith(
            current, expect.objectContaining({ plan_digest: 'b'.repeat(64) }), 'create-new', false,
            expect.objectContaining({ rationale: 'Connect the reviewed team members' }),
        ));

        const progress = await within(rail).findByRole('progressbar');
        await waitFor(() => expect(progress).toHaveAttribute('aria-valuenow', '7'));
        expect(progress).toHaveAttribute('aria-valuemax', '7');
        expect(railSteps()).toHaveLength(7);
        for (const step of railSteps()) expect(step).toHaveTextContent(i18n.t('agentTeamSetup.stepStates.done'));
    });

    it('reads the sink file in the configuration for every runtime and never embeds a key', () => {
        for (const runtime of ['codex', 'claude-code', 'antigravity', 'pi', 'other'] as const) {
            const snippet = runtimeSnippet(runtime, current.server_url, 'member.json');
            expect(snippet).toContain(`jq -er '.api_key' "$WORKCHORD_CREDENTIAL_DIR/member.json"`);
            expect(snippet).toContain("WORKCHORD_BASE_URL='https://workchord.example'");
            expect(snippet).not.toMatch(/AGENT_API_KEY=['"]?[a-z]/i);
        }
    });
});
