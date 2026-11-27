import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { IdentityContext } from '../../features/identity/identityContext';
import type { WorkspaceIdentity } from '../../features/identity/identityService';
import i18n, { ensureLanguageResources } from '../../i18n/i18n';
import type { RefusalNextStep, Task } from '../../types/task';
import { getApiNextStep } from '../../utils/apiError';
import { emptyTaskBrief } from './taskEditorContract';
import { TaskWorkPanel } from './TaskWorkPanel';

const service = vi.hoisted(() => ({ actions: vi.fn(), progress: vi.fn(), command: vi.fn(), review: vi.fn(), getDetail: vi.fn(), ownerAccept: vi.fn(), reviews: vi.fn(), recordProvenance: vi.fn() }));
vi.mock('../../services/taskService', () => ({ taskService: service }));
vi.mock('../../services/iterationService', () => ({ iterationService: { getAll: vi.fn().mockResolvedValue([]) } }));

const resolved = {
    id: 42, iteration_id: null, project_id: 2, title: 'Human work', priority: 5, effort_days: null, effort_hours: null,
    status: 'resolved', execution_mode: 'manual', is_overdue: false, is_delayed: false, is_composite: false,
    is_optional: false, is_deferred: false, tags: [], sort_order: 0, external_links: [], request_count: 0,
    agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] }, version: 3, children: [], dependencies: [],
    brief_revision: 2, artifact_revision: 1, assignee: { id: 7, name: 'Sam' },
    brief: { ...emptyTaskBrief(), acceptance_criteria: [{ id: 'criterion', revision: 1, text: 'Inspect the result', verification: '' }] },
} as Task;

const identity = (overrides: Partial<WorkspaceIdentity>): WorkspaceIdentity => ({ mode: 'managed', authenticated: true, configured: true,
    principal: { id: 9, kind: 'human', display_name: 'Olga' }, profile: null, workspace_role: 'owner', projects: {}, csrf_token: 'x', access: 'full', ...overrides });

const provenanceStep: RefusalNextStep = { kind: 'record_provenance', authority: 'owner_operator_project_manager_or_pm_agent',
    message: 'Link exactly one pull request to the task, or record who executed the work and its exact commits with Record provenance.',
    commands: { rest: 'POST /api/tasks/42/manual-provenance', mcp: 'agent_record_manual_provenance' }, ui_action: 'record_provenance' };
const ownerStep: RefusalNextStep = { kind: 'accept_as_owner', authority: 'workspace_owner_or_operator',
    message: 'Assign an agent verifier to review this work, or accept it as owner with a reason.',
    commands: { rest: 'POST /api/tasks/42/owner-acceptance' }, ui_action: 'accept_as_owner' };
const candidateBlocker = { code: 'verification_candidate_unverifiable', message: 'An exact submitted candidate is required.', next_step: provenanceStep };
const publisherBlocker = { code: 'verified_publisher_review_required', message: 'Use an assigned agent verifier for formal review.', next_step: ownerStep };
const recordable = { action: 'record_provenance', allowed: true, blockers: [] as { code: string; message: string }[] };
const actionsWith = (blocker: { code: string; message: string; next_step?: RefusalNextStep }, record = recordable) => ({ task_id: 42, version: 3, claim_generation: 0,
    running_run_ids: [], live_assignment_ids: [], actions: [{ action: 'review', allowed: false, blockers: [blocker] }, { action: 'accept_review', allowed: false, blockers: [blocker] }, record] });

const renderPanel = (who: WorkspaceIdentity, onUpdated = vi.fn()) => ({ onUpdated, ...renderWithProviders(
    <IdentityContext.Provider value={{ identity: who, refresh: vi.fn(), signOut: vi.fn() }}>
        <TaskWorkPanel task={resolved} disabled={false} draftKey={null} onDirty={vi.fn()} onPending={vi.fn()} onUpdated={onUpdated} onReload={vi.fn()} />
    </IdentityContext.Provider>) });

describe('the next step beside a verification refusal', () => {
    beforeEach(async () => {
        vi.clearAllMocks();
        await i18n.changeLanguage('en');
        service.actions.mockResolvedValue(actionsWith(candidateBlocker));
        service.getDetail.mockResolvedValue({ task: { ...resolved, version: 4 }, reviewer_name: null });
        service.reviews.mockResolvedValue([]);
        service.recordProvenance.mockResolvedValue({ event_id: 1, task_version: 4 });
    });

    it('names the step and its commands beside the refusal and offers Record provenance to an owner', async () => {
        renderPanel(identity({}));
        expect((await screen.findAllByTestId('refusal-next-step'))[0]).toHaveTextContent(/Next step:.*Record who executed the work/);
        expect(screen.getAllByText('POST /api/tasks/42/manual-provenance').length).toBeGreaterThan(0);
        expect(screen.getByRole('button', { name: 'Record provenance' })).toBeDisabled();
        expect(screen.queryByRole('button', { name: 'Accept as owner' })).not.toBeInTheDocument();
    });

    it('records provenance with the keyboard alone, naming what is still missing, and refreshes the task', async () => {
        const { user, onUpdated } = renderPanel(identity({}));
        const button = await screen.findByRole('button', { name: 'Record provenance' });
        expect(button).toHaveAccessibleDescription(expect.stringContaining('Add the head commit URL.'));
        expect(screen.getByRole('textbox', { name: /Person ID/ })).toHaveValue('');
        await user.type(screen.getByRole('textbox', { name: /Person ID/ }), '9');
        const head = screen.getByRole('textbox', { name: /Head commit URL/ });
        for (let step = 0; step < 60 && document.activeElement !== head; step += 1) await user.tab();
        expect(head).toHaveFocus();
        await user.keyboard('https://github.com/acme/app/commit/abc1234');
        await user.tab(); await user.tab();
        await user.keyboard('https://github.com/acme/app/pull/7');
        await user.tab(); await user.tab();
        await user.keyboard('Delivered by hand');
        expect(button).toBeEnabled();
        await user.keyboard('{Enter}');
        await waitFor(() => expect(service.recordProvenance).toHaveBeenCalledWith(42, {
            expected_version: 3, artifact_revision: 1, executor: { kind: 'human', principal_id: 9 },
            head_commit_url: 'https://github.com/acme/app/commit/abc1234', commit_urls: [],
            pr_url: 'https://github.com/acme/app/pull/7', reason: 'Delivered by hand' }));
        await waitFor(() => expect(onUpdated).toHaveBeenCalledWith(expect.objectContaining({ version: 4 })));
    });

    it('sends an agent executor with its binding and every extra commit', async () => {
        const { user } = renderPanel(identity({}));
        await user.selectOptions(await screen.findByRole('combobox', { name: 'Who executed the work' }), 'agent');
        await user.type(screen.getByRole('textbox', { name: /Agent ID/ }), '5');
        await user.type(screen.getByRole('textbox', { name: /Model binding ID/ }), '8');
        await user.type(screen.getByRole('textbox', { name: /Head commit URL/ }), 'https://github.com/acme/app/commit/abc1234');
        await user.type(screen.getByRole('textbox', { name: /Other commits/ }), 'https://github.com/acme/app/commit/def5678{Enter}https://github.com/acme/app/commit/0a1b2c3');
        await user.type(screen.getByRole('textbox', { name: /Base commit URL/ }), 'https://github.com/acme/app/commit/9999999');
        await user.type(screen.getByRole('textbox', { name: /Why the work was executed/ }), 'Agent ran outside the platform');
        await user.click(screen.getByRole('button', { name: 'Record provenance' }));
        await waitFor(() => expect(service.recordProvenance).toHaveBeenCalledWith(42, expect.objectContaining({
            executor: { kind: 'agent', actor_id: 5, model_binding_id: 8 }, base_commit_url: 'https://github.com/acme/app/commit/9999999',
            commit_urls: ['https://github.com/acme/app/commit/def5678', 'https://github.com/acme/app/commit/0a1b2c3'] })));
    });

    it('shows a refusal of the record with its own next step and keeps what was typed', async () => {
        service.recordProvenance.mockRejectedValue({ response: { status: 409, data: { detail: { code: 'manual_provenance_candidate_unverifiable',
            message: 'The head commit is not part of the pull request.', next_step: { ...provenanceStep, message: 'Correct the head commit so it belongs to the pull request.' } } } } });
        const { user } = renderPanel(identity({}));
        await user.type(await screen.findByRole('textbox', { name: /Person ID/ }), '9');
        await user.type(screen.getByRole('textbox', { name: /Head commit URL/ }), 'https://github.com/acme/app/commit/abc1234');
        await user.type(screen.getByRole('textbox', { name: /Pull request URL/ }), 'https://github.com/acme/app/pull/7');
        await user.type(screen.getByRole('textbox', { name: /Why the work was executed/ }), 'Because');
        await user.click(screen.getByRole('button', { name: 'Record provenance' }));
        const alert = await screen.findByRole('alert');
        expect(alert).toHaveTextContent('The head commit is not part of the pull request.');
        expect(within(alert).getByTestId('refusal-next-step')).toHaveTextContent('Record who executed the work');
        expect(screen.getByRole('textbox', { name: /Why the work was executed/ })).toHaveValue('Because');
    });

    it('hides the form when the server says a record would be refused, and says why the step stands', async () => {
        service.actions.mockResolvedValue(actionsWith(candidateBlocker, { action: 'record_provenance', allowed: false,
            blockers: [{ code: 'manual_provenance_execution_recorded', message: 'This task has recorded agent execution.' }] }));
        renderPanel(identity({}));
        expect((await screen.findAllByTestId('refusal-next-step')).length).toBeGreaterThan(0);
        expect(screen.queryByRole('button', { name: 'Record provenance' })).not.toBeInTheDocument();
    });

    it('closes the form after a record and shows each step once', async () => {
        const { user } = renderPanel(identity({}));
        await user.type(await screen.findByRole('textbox', { name: /Person ID/ }), '9');
        await user.type(screen.getByRole('textbox', { name: /Head commit URL/ }), 'https://github.com/acme/app/commit/abc1234');
        await user.type(screen.getByRole('textbox', { name: /Pull request URL/ }), 'https://github.com/acme/app/pull/7');
        await user.type(screen.getByRole('textbox', { name: /Why the work was executed/ }), 'By hand');
        await user.click(screen.getByRole('button', { name: 'Record provenance' }));
        expect(await screen.findByText('Provenance recorded for the current artifact.')).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Record provenance' })).not.toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Record again' }));
        expect(screen.getByRole('button', { name: 'Record provenance' })).toBeInTheDocument();
        expect(screen.getAllByTestId('refusal-next-step')).toHaveLength(1);
    });

    it('offers Record provenance to a project manager who is only a workspace member', async () => {
        renderPanel(identity({ workspace_role: 'member', projects: { '2': 'manager' } }));
        expect(await screen.findByRole('button', { name: 'Record provenance' })).toBeInTheDocument();
    });

    it.each([
        ['a member', identity({ workspace_role: 'member', projects: { '2': 'editor' } }), /Only a signed-in workspace owner, operator or project manager can record provenance/],
        ['a trusted-local browser', identity({ mode: 'trusted_local', authenticated: false, principal: null, workspace_role: null }), /Nobody is signed in to this browser, so provenance cannot be recorded here/],
    ])('tells %s why it cannot record provenance and shows the step', async (_name, who, text) => {
        renderPanel(who);
        expect(await screen.findByText(text)).toBeInTheDocument();
        expect(screen.getAllByTestId('refusal-next-step').length).toBeGreaterThan(0);
        expect(screen.queryByRole('button', { name: 'Record provenance' })).not.toBeInTheDocument();
    });

    it('offers neither action to a paired observer', async () => {
        renderPanel(identity({ access: 'observe' }));
        expect((await screen.findAllByTestId('refusal-next-step')).length).toBeGreaterThan(0);
        expect(screen.queryByRole('button', { name: 'Record provenance' })).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Accept as owner' })).not.toBeInTheDocument();
    });

    it('offers Accept as owner and Record provenance for the verified-publisher refusal', async () => {
        service.actions.mockResolvedValue(actionsWith(publisherBlocker));
        renderPanel(identity({}));
        expect(await screen.findByRole('button', { name: 'Accept as owner' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Record provenance' })).toBeInTheDocument();
        expect((await screen.findAllByTestId('refusal-next-step'))[0]).toHaveTextContent('Assign an agent verifier');
    });

    it('shows the next step of a refused Accept command', async () => {
        service.actions.mockResolvedValue({ ...actionsWith({ code: 'x', message: 'x' }), actions: [
            { action: 'review', allowed: true, blockers: [] }, { action: 'accept_review', allowed: true, blockers: [] }, recordable] });
        service.review.mockRejectedValue({ response: { status: 409, data: { detail: { code: 'verification_candidate_unverifiable',
            message: 'An exact submitted candidate is required for acceptance.', next_step: provenanceStep } } } });
        const { user } = renderPanel(identity({}));
        await screen.findByRole('button', { name: 'Accept' });
        await user.type(screen.getByRole('textbox', { name: /^Reason/ }), 'Looks right');
        await user.selectOptions(screen.getByRole('combobox', { name: /Result: Inspect the result/ }), 'pass');
        await user.click(screen.getByRole('button', { name: 'Accept' }));
        expect(await screen.findByText('An exact submitted candidate is required for acceptance.')).toBeInTheDocument();
        expect(await screen.findByRole('button', { name: 'Record provenance' })).toBeInTheDocument();
    });

    it('renders the step and the form in Russian', async () => {
        await ensureLanguageResources('ru');
        await i18n.changeLanguage('ru');
        renderPanel(identity({}));
        expect((await screen.findAllByTestId('refusal-next-step'))[0]).toHaveTextContent(/Следующий шаг:.*Запишите, кто выполнил работу/);
        expect(screen.getByRole('button', { name: 'Записать происхождение' })).toBeDisabled();
        expect(screen.getByRole('textbox', { name: /Ссылка на головной коммит/ })).toBeInTheDocument();
    });
});

describe('getApiNextStep', () => {
    it('reads the step from a structured detail and ignores a malformed one', () => {
        expect(getApiNextStep({ response: { data: { detail: { code: 'x', message: 'm', next_step: provenanceStep } } } })).toEqual(provenanceStep);
        expect(getApiNextStep({ response: { data: { detail: { next_step: { kind: 'k' } } } } })).toBeNull();
        expect(getApiNextStep({ response: { data: { detail: 'plain' } } })).toBeNull();
        expect(getApiNextStep(new Error('offline'))).toBeNull();
    });
});
