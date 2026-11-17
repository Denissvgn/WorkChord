import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TaskForm } from './TaskForm';
import { emptyTaskBrief } from './taskEditorContract';
import type { Task } from '../../types/task';

const api = vi.hoisted(() => ({ get: vi.fn(), post: vi.fn(), put: vi.fn() }));
vi.mock('../../services/api', () => ({ default: api }));
vi.mock('./TaskWorkPanel', () => ({ TaskWorkPanel: () => null }));
vi.mock('./DeliveryDependencies', () => ({ DeliveryDependencies: () => null }));
vi.mock('./TaskDiscussion', () => ({ TaskDiscussion: () => null }));
vi.mock('./TimeEntriesPanel', () => ({ TimeEntriesPanel: () => null }));
vi.mock('./TaskTimelinePanel', () => ({ TaskTimelinePanel: () => null }));
vi.mock('./StatusChangeControl', () => ({ StatusChangeControl: () => null }));
vi.mock('../team/AssigneeRecommendationsPanel', () => ({ AssigneeRecommendationsPanel: () => null }));

const iteration = { id: 2, name: 'November', revision: 3, nominal_day_hours: 8, project_id: 1, project: { id: 1, name: 'Calendar' } };
const task = {
    id: 101, version: 3, iteration_id: 2, project_id: 1, title: 'Import holidays', status: 'planned', priority: 3,
    effort_days: 1, effort_hours: 8, tags: ['backend'], dependencies: [], children: [], brief: emptyTaskBrief(),
    agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] },
} as unknown as Task;

describe('editing an existing task goes by section', () => {
    beforeEach(() => {
        api.get.mockReset();
        api.get.mockImplementation(async (path: string) => {
            if (path === '/iterations/2') return { data: iteration };
            if (path === '/projects/page') return { data: { items: [iteration.project], has_more: false, upper_id: 1 } };
            if (path === '/tasks/owner-options' || path === '/tasks/lookup') return { data: { items: [], has_more: false } };
            return { data: [] };
        });
    });

    it('keeps the essentials open and every other field in its section', async () => {
        const { user } = renderWithProviders(<TaskForm iterationId={2} initialData={task} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        expect(await screen.findByRole('textbox', { name: 'Task title' })).toHaveValue('Import holidays');
        for (const name of ['Priority', 'Assignee', 'Project', 'Effort (hours)', 'Goal', 'Context', 'Scope', 'Out of scope', 'Verification approach', 'Expected artifacts']) {
            expect(screen.getByLabelText(name)).toBeInTheDocument();
        }
        expect(screen.getByRole('button', { name: 'Optional AI assistance' })).toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: /Dates & effort/ }));
        for (const name of ['Milestone', 'Earliest start', 'Due by']) expect(screen.getByLabelText(name)).toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: 'More' }));
        for (const name of ['Owner', 'Optional task', 'Deferred']) expect(screen.getByLabelText(name)).toBeInTheDocument();
        expect(screen.getByText('Waits for')).toBeInTheDocument();
        expect(screen.getByText('Labels')).toBeInTheDocument();
        expect(screen.queryByRole('combobox', { name: 'Template' })).not.toBeInTheDocument();
    });
});
