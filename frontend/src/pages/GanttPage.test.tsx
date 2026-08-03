import { screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import i18n from '../i18n/i18n';
import { renderWithProviders } from '../test/renderWithProviders';
import { useIterationStore } from '../store/iterationStore';
import type { GanttResponse, GanttTask } from '../types/gantt';
import type { Iteration } from '../types/iteration';
import GanttPage from './GanttPage';

const ganttServiceMock = vi.hoisted(() => ({
    getChart: vi.fn(),
    previewSchedule: vi.fn(),
    explainSchedule: vi.fn(),
}));
const iterationServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
}));
const taskServiceMock = vi.hoisted(() => ({
    batchUpdate: vi.fn(),
}));

vi.mock('../services/ganttService', () => ({ ganttService: ganttServiceMock }));
vi.mock('../services/iterationService', () => ({ iterationService: iterationServiceMock }));
vi.mock('../services/taskService', () => ({ taskService: taskServiceMock }));
vi.mock('../components/gantt/GanttChart', () => ({
    GanttChart: ({
        sandboxMode,
        onSaveSandbox,
    }: {
        sandboxMode: boolean;
        onSaveSandbox: (taskId: number, changes: Partial<GanttTask>) => void;
    }) => (
        <div>
            <p>Gantt chart</p>
            {sandboxMode && (
                <button type="button" onClick={() => onSaveSandbox(1, { title: 'Draft task' })}>
                    Make draft edit
                </button>
            )}
        </div>
    ),
}));

const iterationFixture: Iteration = {
    id: 1,
    name: 'Iteration 1',
    calendar_id: 1,
    start_date: '2026-01-05',
    end_date: '2026-01-16',
    working_days: 10,
};

const taskFixture: GanttTask = {
    id: 1,
    title: 'Task one',
    start_date: '2026-01-05',
    end_date: '2026-01-06',
    effort_days: 1,
    calculated_effort_days: 1,
    progress: 0,
    priority: 5,
    status: 'planned',
    is_composite: false,
    is_overdue: false,
    is_delayed: false,
    is_optional: false,
    is_outside_constraints: false,
    tags: [],
    assignees: [],
    children: [],
    dependencies: [],
    version: 1,
};

const ganttFixture: GanttResponse = {
    iteration: iterationFixture,
    tasks: [taskFixture],
    overdue_task_ids: [],
    holidays: [],
    weekends: [],
    member_vacations: {},
    schedule_result: null,
};

describe('GanttPage hardening', () => {
    beforeEach(() => {
        useIterationStore.setState({ selectedIterationId: 1 });
        iterationServiceMock.getAll.mockResolvedValue([iterationFixture]);
        ganttServiceMock.getChart.mockResolvedValue(ganttFixture);
        ganttServiceMock.previewSchedule.mockReset();
        ganttServiceMock.explainSchedule.mockReset();
        taskServiceMock.batchUpdate.mockReset();
    });

    it('explains saved schedules and temporary sandbox edits on demand', async () => {
        const { user } = renderWithProviders(<GanttPage />);

        await screen.findByText('Gantt chart');
        await user.click(screen.getByRole('button', { name: i18n.t('gantt.help.trigger') }));

        const guide = screen.getByRole('dialog', { name: i18n.t('gantt.help.title') });
        expect(within(guide).getByText(i18n.t('gantt.help.savedTitle'))).toBeVisible();
        expect(within(guide).getByText(i18n.t('gantt.help.sandboxTitle'))).toBeVisible();
        expect(within(guide).getByRole('link', { name: i18n.t('gantt.help.action') }))
            .toHaveAttribute('href', '/plan');
    });

    it('keeps failed sandbox previews recoverable and prevents applying unvalidated edits', async () => {
        ganttServiceMock.previewSchedule.mockRejectedValue(new Error('Preview unavailable'));
        const { user } = renderWithProviders(<GanttPage />);

        await screen.findByText('Gantt chart');
        await user.click(screen.getByRole('button', { name: i18n.t('gantt.sandboxMode') }));
        await user.click(screen.getByRole('button', { name: 'Make draft edit' }));

        const previewAlert = await screen.findByRole('alert');
        expect(previewAlert).toHaveTextContent(i18n.t('gantt.simulationWarning'));
        expect(previewAlert).toHaveTextContent(i18n.t('gantt.simulationFailedDescription'));
        expect(screen.getByRole('button', { name: i18n.t('gantt.applyChanges') })).toBeDisabled();
        expect(taskServiceMock.batchUpdate).not.toHaveBeenCalled();

        await user.click(screen.getByRole('button', { name: i18n.t('gantt.retrySimulation') }));
        await waitFor(() => expect(ganttServiceMock.previewSchedule).toHaveBeenCalledTimes(2));

        await user.click(within(previewAlert).getByRole('button', { name: i18n.t('gantt.discardEdits') }));
        await waitFor(() => expect(screen.queryByRole('alert')).not.toBeInTheDocument());
        expect(screen.getByRole('button', { name: i18n.t('gantt.applyChanges') })).toBeDisabled();
    });

    it('offers retry and an explicit safe exit when a schedule explanation fails', async () => {
        ganttServiceMock.explainSchedule.mockRejectedValue(new Error('Explanation unavailable'));
        const { user } = renderWithProviders(<GanttPage />);

        await screen.findByText('Gantt chart');
        await user.click(screen.getByRole('button', { name: i18n.t('actions.moreActions') }));
        await user.click(screen.getByRole('menuitem', { name: i18n.t('gantt.explainSchedule') }));

        const explanationAlert = await screen.findByRole('alert');
        expect(explanationAlert).toHaveTextContent(i18n.t('gantt.explanationFailed'));
        expect(explanationAlert).toHaveTextContent(i18n.t('gantt.explanationUnavailableDescription'));

        await user.click(screen.getByRole('button', { name: i18n.t('gantt.retryExplanation') }));
        await waitFor(() => expect(ganttServiceMock.explainSchedule).toHaveBeenCalledTimes(2));

        await user.click(screen.getByRole('button', { name: i18n.t('gantt.continueWithoutExplanation') }));
        await waitFor(() => expect(screen.queryByRole('alert')).not.toBeInTheDocument());
        expect(screen.getByText('Gantt chart')).toBeVisible();
    });
});
