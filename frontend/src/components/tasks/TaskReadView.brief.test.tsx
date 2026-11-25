import { afterEach, beforeEach, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import i18n, { ensureLanguageResources } from '../../i18n/i18n';
import type { Task } from '../../types/task';
import { emptyTaskBrief } from './taskEditorContract';
import { TaskReadView } from './TaskReadView';
const service = vi.hoisted(() => ({ writeBrief: vi.fn(), actions: vi.fn(), getDetail: vi.fn() }));
vi.mock('../../services/taskService', () => ({ taskService: service }));
vi.mock('../../services/iterationService', () => ({ iterationService: { getAll: vi.fn().mockResolvedValue([]) } }));
vi.mock('./DeliveryDependencies', () => ({ DeliveryDependencies: () => null }));
vi.mock('./GitHubReconciliationPanel', () => ({ GitHubReconciliationPanel: () => null }));
vi.mock('./TaskDiscussion', () => ({ TaskDiscussion: () => null }));
vi.mock('./TimeEntriesPanel', () => ({ TimeEntriesPanel: () => null }));
vi.mock('./TaskTimelinePanel', () => ({ TaskTimelinePanel: () => null }));
const task = {
    id: 312, title: 'Import holidays from a CSV file', status: 'active', version: 4, priority: 2, effort_days: 3,
    assignee: { id: 7, name: 'Sam Ortiz' }, owner: { id: 3, name: 'Priya Nair' }, end_date: '2026-11-21', start_date: '2026-11-17',
    project_id: 1, iteration_id: 2, dependencies: [298], children: [], tags: [], is_overdue: false, is_delayed: false,
    is_composite: false, is_optional: false, is_deferred: false, sort_order: 0, external_links: [], request_count: 0,
    agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] }, effort_hours: null,
    brief: { ...emptyTaskBrief(), goal: 'Load a year of holidays from a CSV file.', scope: 'One CSV with date and name columns.',
        acceptance_criteria: [
            { id: 'preview', revision: 1, text: 'A valid file shows a preview.', verification: '' },
            { id: 'errors', revision: 1, text: 'An invalid row names its line.', verification: '' },
        ] },
    progress: { criteria: [{ criterion_id: 'preview', criterion_revision: 1, state: 'completed', evidence: 'Screenshot' }], artifacts: [], brief_revision: 1, artifact_revision: 0 },
} as unknown as Task;


beforeEach(() => {
    vi.clearAllMocks();
    service.actions.mockResolvedValue({ actions: [{ action: 'resolve_manual', allowed: true, blockers: [] }] });
    service.getDetail.mockResolvedValue({ task, reviewer_name: null });
    service.writeBrief.mockResolvedValue({ ...task, version: 5 });
});
afterEach(async () => { await i18n.changeLanguage('en'); });
it.each(['en', 'ru'])('opens Goal and Add criterion in one action from the Submit message without a brief in %s', async language => {
    await ensureLanguageResources(language);
    await i18n.changeLanguage(language);
    const onEditAll = vi.fn();
    const { user } = renderWithProviders(<TaskReadView task={{ ...task, brief: null, description: 'Keep the original context' }}
        draftKey={null} onTaskUpdated={vi.fn()} onEditAll={onEditAll} onDirty={vi.fn()} onPending={vi.fn()} onReload={vi.fn()} />);
    const submit = screen.getByRole('button', { name: i18n.t('domain.action_resolve_manual') });
    await waitFor(() => expect(submit).toBeEnabled());
    await user.click(submit);
    const message = screen.getByRole('alert');
    expect(message).toHaveTextContent(i18n.t('domain.submitNeedsCriterion'));
    await user.click(within(message).getByRole('button', { name: i18n.t('taskView.editBrief') }));
    expect(screen.getByLabelText(i18n.t('domain.goal'))).toBeVisible();
    await user.click(screen.getByRole('button', { name: i18n.t('domain.addCriterion') }));
    await user.type(screen.getByLabelText(i18n.t('domain.criterion', { number: 1 })), 'The preview works');
    await user.click(screen.getByRole('button', { name: i18n.t('taskView.saveBrief') }));
    await waitFor(() => expect(service.writeBrief).toHaveBeenCalledWith(task.id, task.version, expect.objectContaining({
        context: 'Keep the original context', acceptance_criteria: [expect.objectContaining({ text: 'The preview works' })],
    })));
    expect(onEditAll).not.toHaveBeenCalled();
});
