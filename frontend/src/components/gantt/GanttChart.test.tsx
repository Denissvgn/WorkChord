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
const teamServiceMock = vi.hoisted(() => ({ getByIteration: vi.fn().mockResolvedValue([{ id: 7, name: 'Sam' }]) }));
vi.mock('../../services/teamService', () => ({ teamService: teamServiceMock }));

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
    input_revision: 1, input_planning_revision: 19,
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
    status: i18n.t(`statuses.${task.status}`),
    start: formatDate(task.start_date),
    end: formatDate(task.end_date),
    assignee: task.assignee?.name ?? i18n.t('common.unassigned'),
    priority: task.priority,
});

const renderChart = (sandboxMode = false, chartTasks: GanttTask[] = [taskFixture]) => renderWithProviders(
    <GanttChart
        iterationId={42}
        iterationRevision={1}
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

        await waitFor(() => expect(ganttServiceMock.previewSchedule).toHaveBeenCalledWith(42, [], 1));
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

        await waitFor(() => expect(ganttServiceMock.schedule).toHaveBeenCalledWith(42, 1, 19));
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
        expect(screen.getByTitle(i18n.t('gantt.taskBarSummary', {
            title: taskFixture.title,
            status: i18n.t('statuses.planned'),
            start: formatDate(taskFixture.start_date),
            end: formatDate(taskFixture.end_date),
            flags: '',
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

describe('Gantt timeline controls', () => {
    it('zooms with visible buttons and with + and - shortcuts', async () => {
        const { user } = renderChart();
        expect(screen.getByText('Zoom 100%')).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Zoom timeline in' }));
        expect(screen.getByText('Zoom 125%')).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Zoom timeline out' }));
        await user.click(screen.getByRole('button', { name: 'Zoom timeline out' }));
        expect(screen.getByText('Zoom 75%')).toBeInTheDocument();
        screen.getByRole('region', { name: 'Schedule chart' }).focus();
        await user.keyboard('+');
        expect(screen.getByText('Zoom 100%')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Fit iteration' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /Today/ })).toBeInTheDocument();
    });
});

describe('Gantt finding and grouping', () => {
    const tasks: GanttTask[] = [
        { ...taskFixture, id: 201, title: 'WC-1 Build the importer', status: 'active' },
        { ...taskFixture, id: 202, title: 'WC-2 Review the importer', status: 'planned' },
        { ...taskFixture, id: 203, title: 'Write release notes', status: 'planned' },
    ];

    it('narrows rows by search and counts it as an active filter', async () => {
        const { user } = renderChart(false, tasks);
        await user.type(screen.getByRole('searchbox', { name: 'Search tasks' }), 'release');
        expect(screen.getByText('Write release notes')).toBeInTheDocument();
        expect(screen.queryByText('WC-1 Build the importer')).not.toBeInTheDocument();
        expect(screen.getByRole('button', { name: /1/ , expanded: false })).toBeInTheDocument();
    });

    it('groups top-level tasks by ID prefix with counts and collapses a group', async () => {
        const { user } = renderChart(false, tasks);
        await user.selectOptions(screen.getByRole('combobox', { name: 'Group by' }), 'prefix');
        const group = screen.getByRole('button', { name: 'WC (2)' });
        expect(screen.getByRole('button', { name: 'No ID prefix (1)' })).toBeInTheDocument();
        await user.click(group);
        expect(group).toHaveAttribute('aria-expanded', 'false');
        expect(screen.queryByText('WC-1 Build the importer')).not.toBeInTheDocument();
        expect(screen.getByText('Write release notes')).toBeInTheDocument();
    });
});

describe('Gantt dependency links', () => {
    const predecessor: GanttTask = { ...taskFixture, id: 301, title: 'Design the schema', start_date: '2026-01-05', end_date: '2026-01-06' };
    const successor: GanttTask = { ...taskFixture, id: 302, title: 'Build the importer', start_date: '2026-01-07', end_date: '2026-01-08', dependencies: [301] };

    it('draws a link, counts it on both tasks, and remembers the toggle', async () => {
        window.localStorage.removeItem('workchord:gantt-show-dependency-links');
        const { user, container } = renderChart(false, [predecessor, successor]);
        expect(container.querySelectorAll('svg path[marker-end]')).toHaveLength(1);
        expect(screen.getAllByText('1 link')).toHaveLength(2);
        expect(screen.getByRole('button', { name: /Build the importer.*Depends on 1; 0 depend on it\./ })).toBeInTheDocument();
        const toggle = screen.getByRole('button', { name: 'Dependency links' });
        expect(toggle).toHaveAttribute('aria-pressed', 'true');
        await user.click(toggle);
        expect(container.querySelectorAll('svg path[marker-end]')).toHaveLength(0);
        expect(window.localStorage.getItem('workchord:gantt-show-dependency-links')).toBe('false');
    });
});


describe('Gantt bar inputs in Try changes', () => {
    it('opens the five date inputs from a bar and recalculates with them', async () => {
        const onSaveSandbox = vi.fn();
        const { user } = renderWithProviders(
            <GanttChart iterationId={42} iterationRevision={1} startDate="2026-01-05" endDate="2026-01-16"
                tasks={[taskFixture]} weekends={[]} holidays={[]} memberVacations={{}} sandboxMode onSaveSandbox={onSaveSandbox} />,
        );
        await user.click(screen.getByRole('button', { name: scheduledTaskName(taskFixture) }));
        const dialog = await screen.findByRole('dialog', { name: 'Current task' });
        expect(screen.getByRole('combobox', { name: 'Who does it' })).toHaveFocus();
        expect(dialog).toHaveTextContent('Dates are calculated.');
        await screen.findByRole('option', { name: 'Sam' });
        await user.selectOptions(screen.getByRole('combobox', { name: 'Who does it' }), '7');
        const effort = screen.getByRole('spinbutton', { name: 'Effort (days)' });
        await user.clear(effort);
        await user.type(effort, '3');
        await user.click(screen.getByRole('button', { name: 'Recalculate with these' }));
        expect(onSaveSandbox).toHaveBeenCalledWith(101, expect.objectContaining({
            assignee: { id: 7, name: 'Sam' }, effort_days: 3, sandbox_update: undefined,
        }));
        expect(screen.queryByRole('dialog', { name: 'Current task' })).not.toBeInTheDocument();
    });

    it('closes with Escape', async () => {
        const { user } = renderWithProviders(
            <GanttChart iterationId={42} iterationRevision={1} startDate="2026-01-05" endDate="2026-01-16"
                tasks={[taskFixture]} weekends={[]} holidays={[]} memberVacations={{}} sandboxMode onSaveSandbox={vi.fn()} />,
        );
        await user.click(screen.getByRole('button', { name: scheduledTaskName(taskFixture) }));
        await screen.findByRole('dialog', { name: 'Current task' });
        await user.keyboard('{Escape}');
        expect(screen.queryByRole('dialog', { name: 'Current task' })).not.toBeInTheDocument();
    });
});
