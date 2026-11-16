import { createHash } from 'node:crypto';
import { fireEvent, screen, waitFor, within } from '@testing-library/react';
import { AxiosError } from 'axios';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import { agentService } from '../../services/agentService';
import type { AgentModelCatalogEntry, AgentTeamMaster, AgentTeamMemberSpec, AgentTeamStatus } from '../../types/agent';
import { ConnectAgentSteps } from './ConnectAgentSteps';
import i18n from '../../i18n/i18n';
import { AGENT_TEAM_STEP_IDS } from '../../features/agentTeamSetup/masters';
import { runtimeSnippet } from '../../features/agentTeamSetup/connectAgent';

vi.mock('../../services/agentService', () => ({ agentService: {
    getAgentTeamStatus: vi.fn(), getAgentTeamStartingPoints: vi.fn(), getModelCatalog: vi.fn(), createModelCatalogEntry: vi.fn(),
    validateAgentTeamMaster: vi.fn(), planAgentTeamMaster: vi.fn(), applyAgentTeamAction: vi.fn(),
} }));
vi.mock('../../hooks/useAdminAccess', () => ({ useAdminAccess: () => ({ hasAdminKey: true }), useKeylessReader: () => ({ settings: false }) }));
const service = vi.mocked(agentService);
const member = (role: AgentTeamMemberSpec['role'], key: string): AgentTeamMemberSpec => ({
    actor_key: key, actor_name: `workchord-${key}`, display_name: key, role,
    scope_preset: `${role}-v1`, profile_key: `${role}-profile`, skill_package: { name: `workchord-${role === 'verifier' ? 'reviewer' : role}`, version: '1.8.0', sha256: 'a'.repeat(64) },
    assignment_modes: [role === 'pm' ? 'ownership' : role === 'worker' ? 'execution' : 'verification'], model_binding_keys: ['catalog-model'], default_model_binding_key: 'catalog-model', runtime_ref: `runtime://${key}`, credential_ref: `private-sink/${key}`,
});
const current: AgentTeamMaster = {
    schema_version: 'agent-team-master-v1', topology_key: 'team', server_url: 'https://workchord.example', credential_sink_ref: 'private-sink', required_server_features: ['agent-team-master-v1'],
    controller: member('pm', 'primary-pm'), workers: [member('worker', 'existing-worker')], verifiers: [member('verifier', 'existing-reviewer')],
    readiness_policy: { minimum_execution_workers: 1, require_independent_verifier_when_assessed: true, maximum_runtime_staleness_seconds: 300 },
};
const status: AgentTeamStatus = { schema_version: 'agent-team-status-v1', topology_key: 'team', topology_revision: 7, manifest_digest: 'a'.repeat(64), topology_state: 'configured', runtime_ready: false, availability: 'availability_unknown', blocker_codes: [], steps: [], members: [], pending_action_ids: [], can_mutate: true, next_action: null };
const model: AgentModelCatalogEntry = { id: 1, key: 'catalog-model', provider: 'OpenAI', configured_model_alias: 'Catalog model', reasoning_tier: 2, context_tier: 'large', cost_tier: 'medium', latency_tier: 'balanced', modality_tags: ['text'], enabled: true, revision: 1, last_verified_at: null, created_at: '', updated_at: '' };

async function toReview() {
    const view = renderWithProviders(<ConnectAgentSteps />);
    await screen.findByRole('radio', { name: 'Worker' });
    expect(screen.queryByRole('radio', { name: 'PM' })).not.toBeInTheDocument();
    await view.user.click(screen.getByRole('button', { name: 'Continue' }));
    await view.user.click(screen.getByRole('radio', { name: 'Codex', exact: true }));
    await view.user.click(screen.getByRole('button', { name: 'Continue' }));
    await view.user.selectOptions(screen.getByRole('combobox', { name: 'Which model will it use?' }), 'catalog-model');
    await view.user.click(screen.getByRole('button', { name: 'Review change' }));
    return view;
}
async function connect() {
    const view = await toReview();
    await view.user.click(await screen.findByRole('button', { name: 'Continue to Connect' }));
    await view.user.click(screen.getByRole('button', { name: 'Connect agent' }));
    await screen.findByText('Waiting for the runtime acknowledgement…');
    return view;
}

beforeEach(() => {
    vi.clearAllMocks(); localStorage.clear(); sessionStorage.clear();
    service.getAgentTeamStatus.mockResolvedValue(structuredClone(status));
    service.getAgentTeamStartingPoints.mockResolvedValue({ current: structuredClone(current), template: structuredClone(current) });
    service.getModelCatalog.mockResolvedValue([model]);
    service.validateAgentTeamMaster.mockImplementation(async manifest => ({ schema_version: 'agent-team-validation-v1', valid: true, manifest_digest: 'a'.repeat(64), normalized_manifest: manifest, blocker_codes: [] }));
    service.planAgentTeamMaster.mockImplementation(async manifest => ({ schema_version: 'agent-team-reconciliation-plan-v1', topology_key: 'team', expected_topology_revision: 7, manifest_digest: 'a'.repeat(64), plan_digest: 'b'.repeat(64), blocker_codes: [], actions: [{ action_id: 'create-new', action_digest: 'c'.repeat(64), reconciliation_class: 'create', operation: 'create_member', actor_key: manifest.workers.at(-1)!.actor_key, target_actor_id: null, expected_object_revision: null, expected_actor_revision: null, before: null, after: null, preconditions: {}, blocker_code: null, requires_explicit_confirmation: false, authority_change: true }] }));
    service.applyAgentTeamAction.mockResolvedValue({ schema_version: 'agent-team-apply-receipt-v1', apply_id: 'apply', topology_key: 'team', manifest_digest: 'a'.repeat(64), plan_digest: 'b'.repeat(64), expected_topology_revision: 7, resulting_topology_revision: 8, status: 'completed', replayed: false, receipts: [{ action_id: 'create-new', action_digest: 'c'.repeat(64), reconciliation_class: 'create', operation: 'create_member', actor_key: 'codex-worker-1', status: 'applied', target_actor_id: 9, before_revision: null, after_revision: 1, blocker_code: null, next_action: null }], pending_action_ids: [], blocker_codes: [] });
});

describe('Connect agent steps', () => {
    it('connects a Worker on Codex in five steps while preserving every existing member in validate, plan and apply', async () => {
        const view = await connect();
        expect(within(screen.getByRole('list', { name: 'Connection steps' })).getAllByRole('listitem')).toHaveLength(5);
        const sent = service.validateAgentTeamMaster.mock.calls[0][0];
        expect(sent.controller).toEqual(current.controller);
        expect(sent.workers.slice(0, -1)).toEqual(current.workers);
        expect(sent.verifiers).toEqual(current.verifiers);
        expect(sent.workers.at(-1)).toMatchObject({ role: 'worker', default_model_binding_key: 'catalog-model', runtime_ref: 'runtime://codex/codex-worker-1' });
        expect(service.planAgentTeamMaster).toHaveBeenCalledWith(sent, 7);
        expect(service.applyAgentTeamAction).toHaveBeenCalledWith(sent, expect.objectContaining({ expected_topology_revision: 7 }), 'create-new', true, expect.any(Object));
        const newStatus = { ...status, members: [{ ...member('worker', 'codex-worker-1'), package_acknowledged: true, acknowledgement_state: 'stale', connection_state: 'observed' }] } as AgentTeamStatus;
        service.getAgentTeamStatus.mockResolvedValue(newStatus);
        await view.user.click(screen.getByRole('button', { name: 'Check connection' }));
        expect(screen.queryByText('Connected', { exact: true })).not.toBeInTheDocument();
        service.getAgentTeamStatus.mockResolvedValue({ ...newStatus, members: [{ ...newStatus.members[0], acknowledgement_state: 'current' }] });
        await view.user.click(screen.getByRole('button', { name: 'Check connection' }));
        expect(await screen.findByText('Connected', { exact: true })).toBeVisible();
    });

    it('shows a plain validation error beside the model answer and reveals the server code on demand', async () => {
        service.validateAgentTeamMaster.mockRejectedValue(new AxiosError('Validation failed', '422', undefined, undefined, { status: 422, data: { detail: [{ loc: ['body', 'manifest', 'workers', 1, 'default_model_binding_key'], type: 'model_catalog_entry_missing', msg: 'Internal diagnostic' }] } } as never));
        const view = await toReview();
        const alert = await screen.findByRole('alert');
        expect(screen.getByRole('heading', { name: '3. Model' })).toBeVisible();
        expect(alert).toHaveTextContent('Choose an enabled catalog model');
        expect(screen.getByRole('combobox', { name: 'Which model will it use?' })).toHaveValue('catalog-model');
        expect(screen.getByText('model_catalog_entry_missing')).not.toBeVisible();
        await view.user.click(within(alert).getByText('Server code'));
        expect(screen.getByText('model_catalog_entry_missing')).toBeVisible();
        expect(service.planAgentTeamMaster).not.toHaveBeenCalled();
        expect(service.applyAgentTeamAction).not.toHaveBeenCalled();
    });

    it('keeps the server-only agent key out of browser storage, URL, console and page and names its exact sink file', async () => {
        const secret = 'pmag_server_only_credential_never_transmitted';
        const serverSink = new Map<string, string>();
        const originalApply = service.applyAgentTeamAction.getMockImplementation()!;
        service.applyAgentTeamAction.mockImplementation(async (...args) => {
            serverSink.set('private-sink/codex-worker-1', secret);
            return originalApply(...args);
        });
        const spies = ['log', 'info', 'warn', 'error', 'debug'].map(method => vi.spyOn(console, method as 'log'));
        const view = await connect();
        expect(serverSink.get('private-sink/codex-worker-1')).toBe(secret);
        const filename = `${createHash('sha256').update('private-sink/codex-worker-1').digest('hex').slice(0, 24)}-codex-worker-1.json`;
        expect(screen.getByText('private-sink', { exact: true })).toBeVisible();
        expect(screen.getByText(filename, { exact: true })).toBeVisible();
        expect(screen.getByLabelText('Codex configuration')).toHaveTextContent(filename);
        expect(screen.getByLabelText('Codex configuration')).toHaveTextContent("jq -er '.api_key'");
        expect(screen.getByLabelText('Codex configuration')).toHaveTextContent('https://workchord.example/api/mcp');
        expect(JSON.stringify(localStorage)).not.toContain(secret);
        expect(JSON.stringify(sessionStorage)).not.toContain(secret);
        expect(window.location.href).not.toContain(secret);
        expect(document.documentElement.outerHTML).not.toContain(secret);
        expect(JSON.stringify(view.queryClient.getQueryCache().getAll().map(query => query.state.data))).not.toContain(secret);
        for (const spy of spies) { expect(JSON.stringify(spy.mock.calls)).not.toContain(secret); spy.mockRestore(); }
    });

    it('retries an interrupted apply with the same idempotency key and prevents changing the candidate', async () => {
        service.applyAgentTeamAction.mockRejectedValueOnce(new Error('connection interrupted'));
        const view = await toReview();
        await view.user.click(await screen.findByRole('button', { name: 'Continue to Connect' }));
        await view.user.click(screen.getByRole('button', { name: 'Connect agent' }));
        await view.user.click(await screen.findByRole('button', { name: 'Retry connection' }));
        await screen.findByText('Waiting for the runtime acknowledgement…');
        expect(service.applyAgentTeamAction.mock.calls[0]).toEqual(service.applyAgentTeamAction.mock.calls[1]);
        expect(screen.queryByRole('button', { name: 'Back' })).not.toBeInTheDocument();
    });

    it('offers PM only without an existing PM and adds a catalog entry in a drawer', async () => {
        service.getAgentTeamStartingPoints.mockResolvedValue({ current: null, template: current });
        const view = renderWithProviders(<ConnectAgentSteps />);
        expect(await screen.findByRole('radio', { name: 'PM' })).toBeVisible();
        await view.user.click(screen.getByRole('button', { name: 'Continue' }));
        await view.user.click(screen.getByRole('button', { name: 'Continue' }));
        await view.user.click(screen.getByRole('button', { name: 'Add a model entry' }));
        const drawer = screen.getByRole('dialog', { name: 'Add a model entry' });
        fireEvent.change(within(drawer).getByLabelText('Catalog key'), { target: { value: 'local-model' } });
        fireEvent.change(within(drawer).getByLabelText('Provider'), { target: { value: 'local' } });
        fireEvent.change(within(drawer).getByLabelText('Model name'), { target: { value: 'Local model' } });
        service.createModelCatalogEntry.mockResolvedValue({ result: { ...model, key: 'local-model' } } as never);
        service.getModelCatalog.mockResolvedValue([model, { ...model, key: 'local-model' }]);
        await view.user.click(within(drawer).getByRole('button', { name: 'Add model' }));
        await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
        expect(screen.getByRole('combobox', { name: 'Which model will it use?' })).toHaveValue('local-model');
    });

    it('completes the advanced manifest workflow through all seven server-reported steps', async () => {
        service.getAgentTeamStatus.mockResolvedValue({ ...status, steps: AGENT_TEAM_STEP_IDS.map(id => ({ id, state: 'todo', blocker_codes: [], next_action: null })) });
        const view = renderWithProviders(<ConnectAgentSteps />);
        await screen.findByRole('radio', { name: 'Worker' });
        await view.user.click(screen.getByText('Advanced: apply a team manifest'));
        await view.user.click(await screen.findByRole('button', { name: i18n.t('agentTeamSetup.start.current') }));
        expect(document.querySelectorAll('.agent-team-setup-steps .step-item')).toHaveLength(7);
        await view.user.click(screen.getByRole('button', { name: i18n.t('agentTeamSetup.validate') }));
        await view.user.click(await screen.findByRole('button', { name: i18n.t('agentTeamSetup.dryRun') }));
        await view.user.type(screen.getByRole('textbox', { name: i18n.t('agentTeamSetup.rationale') }), 'Connect the reviewed team members');
        service.getAgentTeamStatus.mockResolvedValue({ ...status, runtime_ready: true, topology_state: 'runtime_ready', steps: AGENT_TEAM_STEP_IDS.map(id => ({ id, state: 'done', blocker_codes: [], next_action: null })) });
        await view.user.click(screen.getByRole('button', { name: i18n.t('agentTeamSetup.applyActionFor', {
            action: i18n.t('agentTeamSetup.operations.createMember'), actionId: 'create-new', actor: 'existing-worker',
        }) }));
        await waitFor(() => expect(service.applyAgentTeamAction).toHaveBeenCalled());
        const complete = await screen.findByRole('region', { name: i18n.t('agentTeamSetup.readinessTitle') });
        expect(within(complete).getByRole('progressbar')).toHaveAttribute('aria-valuenow', '7');
        expect(within(complete).getByRole('progressbar')).toHaveAttribute('aria-valuemax', '7');
        expect(within(complete).getByText(i18n.t('agentTeamSetup.allChecksCompleteBody'))).toBeVisible();
    });

    it('reads the sink file in configuration for every runtime', () => {
        for (const runtime of ['codex', 'claude-code', 'antigravity', 'pi', 'other'] as const) {
            expect(runtimeSnippet(runtime, current.server_url, 'member.json')).toContain("jq -er '.api_key'");
            expect(runtimeSnippet(runtime, current.server_url, 'member.json')).toContain('https://workchord.example');
        }
    });
});
