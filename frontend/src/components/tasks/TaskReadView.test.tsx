import { describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { Task } from '../../types/task';
import { emptyTaskBrief } from './taskEditorContract';
import { TaskReadView } from './TaskReadView';

const service = vi.hoisted(() => ({ writeBrief: vi.fn() }));
vi.mock('../../services/taskService', () => ({ taskService: service }));
vi.mock('./TaskWorkPanel', () => ({ TaskWorkPanel: ({ initialAction }: { initialAction?: string }) => <p>Work panel {initialAction ?? 'none'}</p> }));
vi.mock('./DeliveryDependencies', () => ({ DeliveryDependencies: () => null }));
vi.mock('./TaskDiscussion', () => ({ TaskDiscussion: () => <p>Discussion</p> }));
vi.mock('./TimeEntriesPanel', () => ({ TimeEntriesPanel: () => null }));
vi.mock('./TaskTimelinePanel', () => ({ TaskTimelinePanel: () => <p>History</p> }));

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

const Location = () => <p data-testid="location">{useLocation().search}</p>;

const renderView = (overrides: Partial<Parameters<typeof TaskReadView>[0]> = {}) => renderWithProviders(<>
    <TaskReadView task={task} draftKey={null} onTaskUpdated={vi.fn()} onEditAll={vi.fn()} onDirty={vi.fn()} onPending={vi.fn()} onReload={vi.fn()} {...overrides} />
    <Location />
</>, { initialEntries: ['/tasks?task=312'] });

describe('read-first task view', () => {
    it('reads the brief without any input and links to the evidence', () => {
        renderView();
        expect(screen.getByText('Load a year of holidays from a CSV file.')).toBeInTheDocument();
        expect(screen.queryByRole('textbox')).not.toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Work & review · 1 of 2 criteria' })).toBeInTheDocument();
        expect(screen.getByText('Sam Ortiz')).toBeInTheDocument();
    });

    it('keeps the part in the URL and sends the header transition to Work & review', async () => {
        const { user } = renderView();
        await user.click(screen.getByRole('button', { name: 'Submit for review' }));
        expect(screen.getByText('Work panel resolve_manual')).toBeInTheDocument();
        expect(screen.getByTestId('location')).toHaveTextContent('task=312&part=work');
        await user.click(screen.getByRole('button', { name: 'Activity' }));
        expect(screen.getByText('Discussion')).toBeInTheDocument();
    });

    it('edits only the brief, pauses the status change, and saves with the task version', async () => {
        const onTaskUpdated = vi.fn();
        service.writeBrief.mockResolvedValue({ ...task, version: 5 });
        const { user } = renderView({ onTaskUpdated });
        await user.click(screen.getByRole('button', { name: 'Edit brief' }));
        expect(screen.getByText('Save or discard your edits to change status.')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Submit for review' })).toBeDisabled();
        await user.click(screen.getByRole('button', { name: 'Save brief' }));
        await waitFor(() => expect(service.writeBrief).toHaveBeenCalledWith(312, 4, expect.objectContaining({ goal: 'Load a year of holidays from a CSV file.' })));
        await waitFor(() => expect(onTaskUpdated).toHaveBeenCalledWith(expect.objectContaining({ version: 5 })));
    });
});
