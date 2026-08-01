import { screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import i18n from '../../i18n/i18n';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { GanttTask, SchedulePreviewResponse, ScheduleResult } from '../../types/gantt';
import { formatDate } from '../../utils/formatDate';
import { GanttChart } from './GanttChart';

const ganttServiceMock = vi.hoisted(() => ({
    previewSchedule: vi.fn(),
    schedule: vi.fn(),
}));

vi.mock('../../services/ganttService', () => ({ ganttService: ganttServiceMock }));

vi.mock('@tanstack/react-virtual', () => ({
    useVirtualizer: (options: { count: number; horizontal?: boolean }) => ({
        getTotalSize: () => options.count * 50,
        getVirtualItems: () => options.horizontal
            ? []
            : Array.from({ length: options.count }, (_, index) => ({
                index,
                start: index * 50,
                size: 50,
            })),
    }),
}));

vi.mock('./TaskEditModal', () => ({ TaskEditModal: () => null }));

const taskFixture: GanttTask = {
    id: 101,
    title: 'Current task',
    start_date: '2026-01-05',
    end_date: '2026-01-06',
    effort_days: 2,
    calculated_effort_days: 2,
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
};

const scheduleResult: ScheduleResult = {
    success: true,
    decisions: [],
    workload_balanced: true,
    workload_issues: [],
};

const previewFixture: SchedulePreviewResponse = {
    tasks: [{
        ...taskFixture,
        title: 'Projected task',
        start_date: '2026-01-12',
        end_date: '2026-01-13',
    }],
    overdue_task_ids: [],
    schedule_result: scheduleResult,
};

const scheduledTaskName = (task: GanttTask) => i18n.t('gantt.openScheduledTask', {
    title: task.title,
    start: formatDate(task.start_date),
    end: formatDate(task.end_date),
    assignee: task.assignee?.name ?? i18n.t('common.unassigned'),
    priority: task.priority,
});

const renderChart = (sandboxMode = false, chartTasks: GanttTask[] = [taskFixture]) => renderWithProviders(
    <GanttChart
        iterationId={42}
        startDate="2026-01-05"
        endDate="2026-01-16"
        tasks={chartTasks}
        weekends={[]}
        holidays={[]}
        memberVacations={{}}
        sandboxMode={sandboxMode}
    />,
);

describe('GanttChart schedule preview', () => {
    beforeEach(() => {
        ganttServiceMock.previewSchedule.mockReset();
        ganttServiceMock.schedule.mockReset();
        ganttServiceMock.previewSchedule.mockResolvedValue(previewFixture);
        ganttServiceMock.schedule.mockResolvedValue(scheduleResult);
    });

    it('shows proposed dates without saving, then explicitly recalculates and saves', async () => {
        const { user } = renderChart();

        await user.click(screen.getByRole('button', { name: i18n.t('surfaces.ganttChart.chartActions') }));
        await user.click(screen.getByRole('menuitem', { name: i18n.t('surfaces.ganttChart.previewSchedule') }));

        await waitFor(() => expect(ganttServiceMock.previewSchedule).toHaveBeenCalledWith(42, []));
        expect(ganttServiceMock.schedule).not.toHaveBeenCalled();

        await screen.findByRole('heading', { name: i18n.t('gantt.schedulePreviewReady') });
        expect(screen.getByText(i18n.t('gantt.schedulePreviewBody'))).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /Projected task/ })).toHaveAttribute('aria-disabled', 'true');
        expect(ganttServiceMock.schedule).not.toHaveBeenCalled();

        let resolveSchedule!: (result: ScheduleResult) => void;
        ganttServiceMock.schedule.mockReturnValue(new Promise(resolve => {
            resolveSchedule = resolve;
        }));
        await user.click(screen.getByRole('button', { name: i18n.t('gantt.applySchedulePreview') }));

        await waitFor(() => expect(ganttServiceMock.schedule).toHaveBeenCalledWith(42));
        expect(screen.getByRole('heading', { name: i18n.t('gantt.scheduleApplyPending') })).toBeInTheDocument();
        resolveSchedule(scheduleResult);
        await screen.findByText(i18n.t('gantt.scheduleApplied'));
    });

    it('returns to the saved schedule without running the scheduler', async () => {
        const { user } = renderChart();

        await user.click(screen.getByRole('button', { name: i18n.t('surfaces.ganttChart.chartActions') }));
        await user.click(screen.getByRole('menuitem', { name: i18n.t('surfaces.ganttChart.previewSchedule') }));
        await screen.findByRole('heading', { name: i18n.t('gantt.schedulePreviewReady') });

        await user.click(screen.getByRole('button', { name: i18n.t('gantt.discardSchedulePreview') }));

        await waitFor(() => expect(screen.queryByRole('heading', {
            name: i18n.t('gantt.schedulePreviewReady'),
        })).not.toBeInTheDocument());
        expect(screen.getByRole('button', { name: scheduledTaskName(taskFixture) })).toBeEnabled();
        expect(ganttServiceMock.schedule).not.toHaveBeenCalled();
    });

    it('does not expose schedule preview in sandbox mode', async () => {
        const { user } = renderChart(true);

        await user.click(screen.getByRole('button', { name: i18n.t('surfaces.ganttChart.chartActions') }));

        expect(screen.queryByRole('menuitem', {
            name: i18n.t('surfaces.ganttChart.previewSchedule'),
        })).not.toBeInTheDocument();
        expect(ganttServiceMock.previewSchedule).not.toHaveBeenCalled();
        expect(ganttServiceMock.schedule).not.toHaveBeenCalled();
    });

    it('keeps preview generation visible after the action menu closes', async () => {
        let resolvePreview!: (preview: SchedulePreviewResponse) => void;
        ganttServiceMock.previewSchedule.mockReturnValue(new Promise(resolve => {
            resolvePreview = resolve;
        }));
        const { user } = renderChart();

        await user.click(screen.getByRole('button', { name: i18n.t('surfaces.ganttChart.chartActions') }));
        await user.click(screen.getByRole('menuitem', { name: i18n.t('surfaces.ganttChart.previewSchedule') }));

        expect(await screen.findByText(i18n.t('gantt.schedulePreviewPending'))).toBeInTheDocument();
        expect(ganttServiceMock.schedule).not.toHaveBeenCalled();

        resolvePreview(previewFixture);
        await screen.findByRole('heading', { name: i18n.t('gantt.schedulePreviewReady') });
    });

    it('uses a schedule-specific preview failure and retry action', async () => {
        ganttServiceMock.previewSchedule.mockRejectedValueOnce(new Error('Unavailable'));
        const { user } = renderChart();

        await user.click(screen.getByRole('button', { name: i18n.t('surfaces.ganttChart.chartActions') }));
        await user.click(screen.getByRole('menuitem', { name: i18n.t('surfaces.ganttChart.previewSchedule') }));

        expect(await screen.findByText(i18n.t('gantt.schedulePreviewFailedTitle'))).toBeInTheDocument();
        expect(screen.getByText(i18n.t('gantt.schedulePreviewFailed'))).toBeInTheDocument();
        expect(screen.getByRole('button', { name: i18n.t('gantt.retrySchedulePreview') })).toBeInTheDocument();
        expect(ganttServiceMock.schedule).not.toHaveBeenCalled();
    });

    it('refreshes the saved schedule after an unconfirmed save instead of rerunning it', async () => {
        ganttServiceMock.schedule.mockRejectedValueOnce(new Error('Connection lost'));
        const { user } = renderChart();

        await user.click(screen.getByRole('button', { name: i18n.t('surfaces.ganttChart.chartActions') }));
        await user.click(screen.getByRole('menuitem', { name: i18n.t('surfaces.ganttChart.previewSchedule') }));
        await screen.findByRole('heading', { name: i18n.t('gantt.schedulePreviewReady') });
        await user.click(screen.getByRole('button', { name: i18n.t('gantt.applySchedulePreview') }));

        await screen.findByText(i18n.t('gantt.scheduleSaveUnconfirmedTitle'));
        await user.click(screen.getByRole('button', { name: i18n.t('gantt.refreshSavedSchedule') }));

        await waitFor(() => expect(screen.queryByText(
            i18n.t('gantt.scheduleSaveUnconfirmedTitle'),
        )).not.toBeInTheDocument());
        expect(ganttServiceMock.schedule).toHaveBeenCalledTimes(1);
    });
});

describe('GanttChart clarity states', () => {
    beforeEach(() => {
        ganttServiceMock.previewSchedule.mockReset();
        ganttServiceMock.schedule.mockReset();
        ganttServiceMock.previewSchedule.mockResolvedValue(previewFixture);
        ganttServiceMock.schedule.mockResolvedValue(scheduleResult);
    });

    it('names the chart as a scrollable region and provides complete task dates', () => {
        renderChart();

        expect(screen.queryByRole('grid')).not.toBeInTheDocument();
        expect(screen.getByRole('region', { name: i18n.t('gantt.chartRegion') })).toHaveAccessibleDescription(
            i18n.t('gantt.chartInstructions'),
        );
        expect(screen.getByTitle(i18n.t('gantt.taskDateRange', {
            title: taskFixture.title,
            start: formatDate(taskFixture.start_date),
            end: formatDate(taskFixture.end_date),
        }))).toBeInTheDocument();
    });

    it('shows an explicit unscheduled action instead of fabricating a calendar bar', () => {
        const unscheduledTask: GanttTask = {
            ...taskFixture,
            title: 'Needs an owner',
            start_date: null,
            end_date: null,
            calculated_effort_days: null,
        };
        renderChart(false, [unscheduledTask]);

        expect(screen.getByRole('button', {
            name: i18n.t('gantt.openUnscheduledTask', { title: unscheduledTask.title }),
        })).toHaveTextContent(i18n.t('gantt.notScheduled'));
        expect(screen.getByText(i18n.t('common.unassigned'))).toBeInTheDocument();
    });

    it('distinguishes an empty iteration from an empty filtered result', async () => {
        const emptyRender = renderChart(false, []);
        expect(screen.getByRole('heading', { name: i18n.t('gantt.noTasksTitle') })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: i18n.t('gantt.addTask') })).toHaveAttribute('href', '/tasks?create=1');
        emptyRender.unmount();

        const { user } = renderChart();
        await user.click(screen.getByRole('button', { name: i18n.t('taskFilters.filters') }));
        await user.click(screen.getByRole('checkbox', {
            name: i18n.t('surfaces.ganttChart.hideTasksWithoutAssignee'),
        }));
        await user.click(screen.getByRole('button', { name: i18n.t('surfaces.slideOver.close') }));

        expect(screen.getByRole('heading', { name: i18n.t('gantt.noFilteredTasksTitle') })).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: i18n.t('surfaces.ganttChart.clearFilters') }));
        expect(screen.getByRole('button', { name: scheduledTaskName(taskFixture) })).toBeInTheDocument();
    });

    it('uses state-changing labels for sort and timeline density', async () => {
        const { user } = renderChart();

        await user.click(screen.getByRole('button', { name: i18n.t('surfaces.ganttChart.chartActions') }));
        await user.click(screen.getByRole('menuitem', { name: i18n.t('surfaces.ganttChart.sortByStartDate') }));

        await user.click(screen.getByRole('button', { name: i18n.t('surfaces.ganttChart.chartActions') }));
        expect(screen.getByRole('menuitem', {
            name: i18n.t('surfaces.ganttChart.restoreTaskOrder'),
        })).toBeInTheDocument();
        await user.click(screen.getByRole('menuitem', {
            name: i18n.t('surfaces.ganttChart.condenseLongTaskSpans'),
        }));

        await user.click(screen.getByRole('button', { name: i18n.t('surfaces.ganttChart.chartActions') }));
        expect(screen.getByRole('menuitem', {
            name: i18n.t('surfaces.ganttChart.showEveryDate'),
        })).toBeInTheDocument();
    });
});
