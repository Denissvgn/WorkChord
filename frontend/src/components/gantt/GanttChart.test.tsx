import { fireEvent, screen, within } from '@testing-library/react';
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

vi.mock('./TaskEditDrawer', () => ({ TaskEditDrawer: () => null }));
const teamServiceMock = vi.hoisted(() => ({ getByIteration: vi.fn().mockResolvedValue([{ id: 7, name: 'Sam' }]) }));
vi.mock('../../services/teamService', () => ({ teamService: teamServiceMock }));

const taskFixture: GanttTask = {
    id: 101,
    title: 'Current task',
    start_date: '2026-01-05',
    end_date: '2026-01-06',
    effort_days: 2,
    effort_hours: 16,
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
        expect(screen.getByRole('button', { name: scheduledTaskName(taskFixture) })).toHaveAttribute('title', i18n.t('gantt.taskBarSummary', {
            title: taskFixture.title,
            status: i18n.t('statuses.planned'),
            start: formatDate(taskFixture.start_date),
            end: formatDate(taskFixture.end_date),
            flags: '',
        }) + ` · ${i18n.t('taskList.assignee')}: ${i18n.t('common.unassigned')}`);
    });

    it('keeps its sticky header and task column inside its own stacking context', () => {
        renderChart();

        // The header (z-40) and the task column (z-50) would otherwise cover menus opened above the chart.
        const chart = screen.getByRole('region', { name: i18n.t('gantt.chartRegion') });
        expect(chart).toHaveClass('isolate');
        expect(chart.querySelector('.sticky.top-0.z-40')).not.toBeNull();
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

    it('lists postponed work with its state and never draws it as scheduled work', () => {
        // The server still sends dates for stopped work; the chart does not draw them.
        const stopped = { ...taskFixture, id: 300, title: 'Stopped postponed', status: 'postponed', displayed_state: 'postponed' } as unknown as GanttTask;
        renderChart(false, [stopped, { ...taskFixture, id: 301, title: 'Live work' }]);

        expect(screen.getByRole('button', { name: scheduledTaskName({ ...taskFixture, title: 'Live work' }) })).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: /^Open scheduled task.*Stopped postponed/ })).not.toBeInTheDocument();
        // The state is written out beside the row, not only coloured.
        expect(screen.getByRole('button', { name: i18n.t('gantt.openUnscheduledTask', { title: stopped.title }) })).toHaveTextContent('Postponed, not scheduled');
    });

    it('keeps canceled and superseded work off the chart unless the state filter asks for it', () => {
        const canceled = { ...taskFixture, id: 300, title: 'Dropped idea', status: 'active', displayed_state: 'canceled' } as unknown as GanttTask;
        const superseded = { ...taskFixture, id: 302, title: 'Replaced work', status: 'planned', displayed_state: 'superseded' } as unknown as GanttTask;
        const view = renderChart(false, [canceled, superseded, { ...taskFixture, id: 301, title: 'Live work' }]);
        expect(screen.queryByText('Dropped idea')).not.toBeInTheDocument();
        expect(screen.queryByText('Replaced work')).not.toBeInTheDocument();
        expect(screen.getByText('Live work')).toBeInTheDocument();
        fireEvent.change(screen.getByRole('combobox', { name: i18n.t('surfaces.ganttChart.statusFilter') }), { target: { value: 'canceled' } });
        expect(screen.getByText('Dropped idea')).toBeInTheDocument();
        expect(screen.queryByText('Replaced work')).not.toBeInTheDocument();
        expect(screen.getByRole('button', { name: i18n.t('gantt.openUnscheduledTask', { title: 'Dropped idea' }) })).toHaveTextContent('Canceled, not scheduled');
        view.unmount();
    });

    it('does not count stopped work as unscheduled or as unassigned work waiting for a plan', () => {
        const stopped = [
            { ...taskFixture, id: 300, title: 'Paused', status: 'postponed', displayed_state: 'postponed' },
            { ...taskFixture, id: 303, title: 'Dropped', status: 'planned', displayed_state: 'canceled' },
        ] as unknown as GanttTask[];
        renderChart(false, stopped);
        // No summary above the chart, so no "Assign N tasks" prompt for work that will not be scheduled.
        expect(screen.queryByRole('status')).not.toBeInTheDocument();
        expect(screen.queryByRole('link', { name: /Assign \d+ task/ })).not.toBeInTheDocument();
    });

    it('distinguishes an empty iteration from an empty filtered result', async () => {
        const emptyRender = renderChart(false, []);
        expect(screen.getByRole('heading', { name: i18n.t('gantt.noTasksTitle') })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: i18n.t('gantt.addTask') })).toHaveAttribute('href', '/tasks?create=1');
        emptyRender.unmount();

        const { user } = renderChart();
        await user.selectOptions(screen.getByRole('combobox', { name: 'Assignee' }), 'assigned');

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
    it('offers zoom, Today and Fit directly in the toolbar with named tooltips', async () => {
        const { user } = renderChart();
        const toolbar = within(screen.getByTestId('page-toolbar'));
        for (const name of ['Zoom timeline in', 'Zoom timeline out', 'Fit iteration', 'Today']) {
            expect(toolbar.getByRole('button', { name })).toHaveAttribute('title', name);
        }
        const zoomOut = toolbar.getByRole('button', { name: 'Zoom timeline out' });
        await user.click(zoomOut);
        await user.click(zoomOut);
        expect(zoomOut).toBeDisabled();
        await user.click(toolbar.getByRole('button', { name: 'Zoom timeline in' }));
        expect(zoomOut).toBeEnabled();
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
        expect(screen.getByRole('searchbox', { name: 'Search tasks' })).toHaveValue('release');
    });

    it('shows removable chips for each active filter', async () => {
        const { user } = renderChart(false, tasks);
        await user.selectOptions(screen.getByRole('combobox', { name: 'Status' }), 'planned');
        await user.selectOptions(screen.getByRole('combobox', { name: 'Assignee' }), 'assigned');
        await user.selectOptions(screen.getByRole('combobox', { name: 'Hide tasks without dates' }), 'yes');
        const chips = screen.getByRole('list', { name: /active filters/i });
        expect(within(chips).getAllByRole('button', { name: /remove/i })).toHaveLength(3);
        await user.click(within(chips).getByRole('button', { name: /remove filter status/i }));
        expect(screen.getByRole('combobox', { name: 'Status' })).toHaveValue('');
        expect(within(chips).getAllByRole('button', { name: /remove/i })).toHaveLength(2);
        await user.click(within(chips).getByRole('button', { name: /remove filter assignee/i }));
        await user.click(within(chips).getByRole('button', { name: /remove filter hide tasks without dates/i }));
        expect(screen.queryByRole('list', { name: /active filters/i })).not.toBeInTheDocument();
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

describe('Gantt plans that are not staffed yet', () => {
    it('says once that dated work without an assignee is not a calculated schedule', () => {
        renderChart();

        expect(screen.getByText(i18n.t('surfaces.ganttChart.provisionalSummary', { count: 1 }))).toBeInTheDocument();
        expect(screen.getByRole('link', { name: i18n.t('surfaces.ganttChart.assignOwners', { count: 1 }) })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: scheduledTaskName(taskFixture) })).toHaveClass('border-dashed');
    });

    it('draws assigned work as a solid bar without the summary', () => {
        const assigned: GanttTask = { ...taskFixture, assignee: { id: 7, name: 'Sam' } };
        renderChart(false, [assigned]);

        expect(screen.queryByText(i18n.t('surfaces.ganttChart.provisionalSummary', { count: 1 }))).not.toBeInTheDocument();
        expect(screen.getByRole('button', { name: scheduledTaskName(assigned) })).not.toHaveClass('border-dashed');
    });
});

describe('Gantt overview of a large plan', () => {
    const largePlan: GanttTask[] = Array.from({ length: 24 }, (_, index) => ({
        ...taskFixture,
        id: 400 + index,
        title: `${index < 12 ? 'CORE' : 'UI'}-${String(index + 1).padStart(3, '0')} Task ${index + 1}`,
        start_date: index < 12 ? '2026-01-05' : '2026-01-08',
        end_date: index < 12 ? '2026-01-07' : '2026-01-12',
        assignee: index < 12 ? null : { id: 7, name: 'Sam' },
    }));

    it('opens grouped and collapsed, with the span and unassigned count on each group', async () => {
        const { user } = renderChart(false, largePlan);

        expect(screen.getByRole('combobox', { name: 'Group by' })).toHaveValue('prefix');
        const core = screen.getByRole('button', { name: 'CORE (12)' });
        expect(core).toHaveAttribute('aria-expanded', 'false');
        expect(screen.queryByText('CORE-001 Task 1')).not.toBeInTheDocument();
        expect(screen.getByText(i18n.t('surfaces.ganttChart.groupUnassigned', { count: 12 }))).toBeInTheDocument();
        expect(screen.getByText(i18n.t('surfaces.ganttChart.groupRange', {
            start: formatDate('2026-01-08'),
            end: formatDate('2026-01-12'),
        }))).toBeInTheDocument();

        await user.click(core);
        expect(screen.getByText('CORE-001 Task 1')).toBeInTheDocument();
        expect(screen.queryByText('UI-013 Task 13')).not.toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: i18n.t('surfaces.ganttChart.chartActions') }));
        await user.click(screen.getByRole('menuitem', { name: i18n.t('surfaces.ganttChart.expandAllGroups') }));
        expect(screen.getByText('UI-013 Task 13')).toBeInTheDocument();
    });

    it('shows search matches even inside a collapsed group', async () => {
        const { user } = renderChart(false, largePlan);
        await user.type(screen.getByRole('searchbox', { name: 'Search tasks' }), 'Task 13');
        expect(screen.getByText('UI-013 Task 13')).toBeInTheDocument();
    });

    it('groups by assignee and remembers an explicit choice', async () => {
        const { user } = renderChart(false, largePlan);
        await user.selectOptions(screen.getByRole('combobox', { name: 'Group by' }), 'assignee');

        expect(screen.getByRole('button', { name: 'Sam (12)' })).toHaveAttribute('aria-expanded', 'true');
        expect(screen.getByRole('button', { name: `${i18n.t('common.unassigned')} (12)` })).toBeInTheDocument();
        expect(window.localStorage.getItem('workchord:gantt-group-by')).toBe('assignee');
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
        expect(screen.getByRole('button', { name: /Build the importer.*Waits for 1; 0 wait for it\./ })).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: i18n.t('surfaces.ganttChart.chartActions') }));
        await user.click(screen.getByRole('menuitem', { name: /Dependency links/ }));
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
        expect(within(dialog).getByRole('combobox', { name: 'Assignee' })).toHaveFocus();
        expect(dialog).toHaveTextContent('Dates are calculated.');
        await screen.findByRole('option', { name: 'Sam' });
        await user.selectOptions(within(dialog).getByRole('combobox', { name: 'Assignee' }), '7');
        const effort = screen.getByRole('spinbutton', { name: 'Effort (hours)' });
        expect(dialog).toHaveTextContent('= 2 days at 8 hours per day');
        await user.clear(effort);
        await user.type(effort, '24');
        expect(dialog).toHaveTextContent('= 3 days at 8 hours per day');
        await user.click(screen.getByRole('button', { name: 'Recalculate with these' }));
        expect(onSaveSandbox).toHaveBeenCalledWith(101, expect.objectContaining({
            assignee: { id: 7, name: 'Sam' }, effort_hours: 24, sandbox_update: undefined,
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

describe('Gantt drag in Try changes', () => {
    it('pins the earliest start when a bar is dragged, without opening the popover', async () => {
        const onSaveSandbox = vi.fn();
        renderWithProviders(
            <GanttChart iterationId={42} iterationRevision={1} startDate="2026-01-05" endDate="2026-01-16"
                tasks={[taskFixture]} weekends={[]} holidays={[]} memberVacations={{}} sandboxMode onSaveSandbox={onSaveSandbox} />,
        );
        const bar = screen.getByRole('button', { name: scheduledTaskName(taskFixture) });
        fireEvent.pointerDown(bar, { clientX: 100, clientY: 10, button: 0 });
        fireEvent.pointerMove(window, { clientX: 180, clientY: 10 });
        fireEvent.pointerUp(window, { clientX: 180, clientY: 10 });
        fireEvent.click(bar);
        // Default zoom is 40 px a day, so 80 px moves the earliest start by two days.
        expect(onSaveSandbox).toHaveBeenCalledWith(101, expect.objectContaining({ min_start_date: '2026-01-07', sandbox_update: undefined }));
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });

    it('does not drag outside Try changes', () => {
        const onSaveSandbox = vi.fn();
        renderWithProviders(
            <GanttChart iterationId={42} iterationRevision={1} startDate="2026-01-05" endDate="2026-01-16"
                tasks={[taskFixture]} weekends={[]} holidays={[]} memberVacations={{}} onSaveSandbox={onSaveSandbox} />,
        );
        const bar = screen.getByRole('button', { name: scheduledTaskName(taskFixture) });
        fireEvent.pointerDown(bar, { clientX: 100, clientY: 10, button: 0 });
        fireEvent.pointerUp(window, { clientX: 180, clientY: 10 });
        expect(onSaveSandbox).not.toHaveBeenCalled();
    });
});
