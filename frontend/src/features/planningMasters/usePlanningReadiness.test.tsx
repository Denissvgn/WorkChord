import type { ReactNode } from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { act, renderHook, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { GanttResponse, GanttTask } from '../../types/gantt';
import type { Iteration } from '../../types/iteration';
import type { Task } from '../../types/task';
import type { TeamMember } from '../../types/team';
import { useIterationStore } from '../../store/iterationStore';
import {
    countPlanningExceptions,
    enrichPlanningTeamMembers,
    hasSavedPlanningSchedule,
    planningLeafTasks,
    usePlanningReadiness,
} from './usePlanningReadiness';

const serviceMocks = vi.hoisted(() => ({
    getIterations: vi.fn(),
    getTeam: vi.fn(),
    getTasks: vi.fn(),
    getGantt: vi.fn(),
    getInbox: vi.fn(),
}));

vi.mock('../../services/iterationService', () => ({
    iterationService: { getAll: serviceMocks.getIterations },
}));
vi.mock('../../services/teamService', () => ({
    teamService: { getByIteration: serviceMocks.getTeam },
}));
vi.mock('../../services/taskService', () => ({
    taskService: { getByIteration: serviceMocks.getTasks },
}));
vi.mock('../../services/ganttService', () => ({
    ganttService: { getChart: serviceMocks.getGantt },
}));
vi.mock('../../services/triageService', () => ({
    triageService: { getAll: serviceMocks.getInbox },
}));

const iteration: Iteration = {
    id: 17,
    name: 'August plan',
    calendar_id: 1,
    start_date: '2026-08-03',
    end_date: '2026-08-14',
    working_days: 10,
};

const member: TeamMember = {
    id: 41,
    iteration_id: iteration.id,
    name: 'Alex Morgan',
    position: 'Engineer',
    availability_percent: 100,
    professionalism_coefficient: 1.25,
    operational_utilization: 20,
    profile: null,
    vacations: [{
        id: 5,
        start_date: '2026-08-06',
        end_date: '2026-08-10',
    }],
};

const taskFixture = (overrides: Partial<Task> = {}): Task => ({
    id: 1,
    iteration_id: iteration.id,
    project_id: null,
    milestone_id: null,
    parent_id: null,
    title: 'Ready task',
    description: '',
    priority: 5,
    effort_days: 2,
    effort_hours: 16,
    project: null,
    milestone: null,
    assignee: { id: member.id, name: member.name },
    status: 'planned',
    start_date: '2026-08-03',
    end_date: '2026-08-04',
    actual_start_date: null,
    actual_end_date: null,
    min_start_date: null,
    max_end_date: null,
    is_overdue: false,
    is_delayed: false,
    is_composite: false,
    is_optional: false,
    is_deferred: false,
    is_outside_constraints: false,
    tags: [],
    sort_order: 0,
    external_key: null,
    source: null,
    source_url: null,
    external_links: [],
    request_count: 0,
    agent_readiness: {
        is_ready: false,
        blockers: [],
        warnings: [],
        criteria: [],
    },
    version: 1,
    claimed_by: null,
    claim_expires_at: null,
    updated_at: '2026-08-01T10:00:00Z',
    children: [],
    dependencies: [],
    ...overrides,
});

const ganttTaskFixture = (task: Task): GanttTask => ({
    id: task.id,
    title: task.title,
    start_date: task.start_date ?? null,
    end_date: task.end_date ?? null,
    effort_days: task.effort_days,
    effort_hours: task.effort_hours,
    calculated_effort_days: task.effort_days,
    progress: 0,
    priority: task.priority,
    status: task.status,
    is_composite: task.is_composite,
    is_overdue: task.is_overdue,
    is_delayed: task.is_delayed,
    is_optional: task.is_optional,
    is_deferred: task.is_deferred,
    is_outside_constraints: task.is_outside_constraints ?? false,
    tags: task.tags,
    assignee: task.assignee,
    assignees: task.assignee ? [task.assignee] : [],
    children: task.children.map(ganttTaskFixture),
    dependencies: task.dependencies,
    version: task.version,
});

const ganttFixture = (tasks: Task[]): GanttResponse => ({
    iteration,
    tasks: tasks.filter(task => !task.is_deferred).map(ganttTaskFixture),
    overdue_task_ids: [],
    holidays: [],
    weekends: [
        '2026-08-08',
        '2026-08-09',
    ],
    member_vacations: {
        [member.id]: [
            '2026-08-06',
            '2026-08-07',
            '2026-08-08',
            '2026-08-09',
            '2026-08-10',
        ],
    },
    schedule_result: null,
});

const taskTree = () => {
    const child = taskFixture({ id: 2, parent_id: 10 });
    const composite = taskFixture({
        id: 10,
        title: 'Composite parent',
        effort_days: 0,
        effort_hours: 0,
        assignee: null,
        start_date: null,
        end_date: null,
        is_composite: true,
        children: [child],
    });
    const deferred = taskFixture({
        id: 20,
        title: 'Deferred task',
        assignee: null,
        start_date: null,
        end_date: null,
        is_deferred: true,
    });
    return [composite, deferred];
};

const makeWrapper = (client: QueryClient) => (
    ({ children }: { children: ReactNode }) => (
        <QueryClientProvider client={client}>{children}</QueryClientProvider>
    )
);

describe('planning readiness helpers', () => {
    it('uses only non-deferred leaves for capacity, workload, and schedule readiness', () => {
        const tasks = taskTree();
        const gantt = ganttFixture(tasks);
        const enriched = enrichPlanningTeamMembers({
            members: [member],
            tasks,
            iteration,
            gantt,
        });

        expect(planningLeafTasks(tasks).map(task => task.id)).toEqual([2]);
        expect(enriched[0]).toMatchObject({
            capacity_hours: 56,
            planned_hours: 16,
        });
        expect(hasSavedPlanningSchedule(tasks)).toBe(true);
    });

    it('requires every relevant task to have positive effort and an ordered saved date range', () => {
        expect(hasSavedPlanningSchedule([
            taskFixture(),
            taskFixture({ id: 2, start_date: null, end_date: null }),
        ])).toBe(false);
        expect(hasSavedPlanningSchedule([
            taskFixture({ effort_days: Number.NaN }),
        ])).toBe(false);
        expect(hasSavedPlanningSchedule([
            taskFixture({ start_date: '2026-08-05', end_date: '2026-08-04' }),
        ])).toBe(false);
        expect(hasSavedPlanningSchedule([
            taskFixture(),
            taskFixture({ id: 2, is_deferred: true, start_date: null, end_date: null }),
        ])).toBe(true);
        expect(hasSavedPlanningSchedule([
            taskFixture(),
            taskFixture({
                id: 2,
                is_composite: true,
                effort_days: 0,
                start_date: null,
                end_date: null,
            }),
        ])).toBe(true);
    });

    it('promotes task and capacity exceptions into review readiness', () => {
        const tasks = [
            taskFixture({ is_delayed: true }),
            taskFixture({ id: 2, is_outside_constraints: true }),
        ];
        const members = enrichPlanningTeamMembers({
            members: [member],
            tasks,
            iteration: { ...iteration, working_days: 1 },
        });

        expect(countPlanningExceptions(tasks, members)).toBe(3);
    });
});

describe('usePlanningReadiness query contract', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        useIterationStore.setState({ selectedIterationId: iteration.id });
    });

    it('returns enriched API-shaped data without relying on aggregate schedule_result', async () => {
        const tasks = taskTree();
        serviceMocks.getIterations.mockResolvedValue([iteration]);
        serviceMocks.getTeam.mockResolvedValue([member]);
        serviceMocks.getTasks.mockResolvedValue(tasks);
        serviceMocks.getGantt.mockResolvedValue(ganttFixture(tasks));
        serviceMocks.getInbox.mockResolvedValue([]);
        const client = new QueryClient({
            defaultOptions: { queries: { retry: false } },
        });

        const { result } = renderHook(() => usePlanningReadiness(), {
            wrapper: makeWrapper(client),
        });

        await waitFor(() => expect(result.current.isLoading).toBe(false));

        expect(result.current.teamMembers[0]).toMatchObject({
            id: member.id,
            capacity_hours: 56,
            planned_hours: 16,
        });
        expect(result.current.readinessData).toMatchObject({
            taskCount: 1,
            tasksWithoutAssignee: 0,
            tasksWithoutEffort: 0,
            hasGanttSchedule: true,
            teamCapacity: 56,
            teamMembersNoCap: 0,
        });
        expect(result.current.status.schedule.state).toBe('done');
        expect(result.current.planningLeafTasks.map(task => task.id)).toEqual([2]);
    });

    it('keeps cached data usable and exposes a query-specific background error', async () => {
        const tasks = [taskFixture()];
        serviceMocks.getIterations.mockResolvedValue([iteration]);
        serviceMocks.getTeam.mockResolvedValue([member]);
        serviceMocks.getTasks.mockResolvedValue(tasks);
        serviceMocks.getGantt.mockResolvedValue(ganttFixture(tasks));
        serviceMocks.getInbox.mockResolvedValue([]);
        const client = new QueryClient({
            defaultOptions: { queries: { retry: false } },
        });
        const { result } = renderHook(() => usePlanningReadiness(), {
            wrapper: makeWrapper(client),
        });

        await waitFor(() => expect(result.current.isLoading).toBe(false));
        serviceMocks.getTeam.mockRejectedValueOnce(new Error('refresh failed'));

        await act(async () => {
            await result.current.queryStates.team.refetch();
        });

        await waitFor(() => {
            expect(result.current.queryStates.team.isRefetchError).toBe(true);
        });
        expect(result.current.queryStates.team.isBlockingError).toBe(false);
        expect(result.current.isError).toBe(false);
        expect(result.current.isReadinessError).toBe(false);
        expect(result.current.teamMembers).toHaveLength(1);
        expect(result.current.error).toBeNull();
    });
});
