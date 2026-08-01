import { screen, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import i18n from '../i18n/i18n';
import { resources } from '../i18n/resources';
import {
    deriveStatus,
    EMPTY_READINESS,
    nextStep,
    readiness,
} from '../features/planningMasters/masters';
import type { PlanReadiness } from '../features/planningMasters/masters';
import type { PlanningQueryFeedback } from '../features/planningMasters/usePlanningReadiness';
import { renderWithProviders } from '../test/renderWithProviders';
import type { Iteration } from '../types/iteration';
import type { Task } from '../types/task';
import PlanMasterPage from './PlanMasterPage';
import planMasterSource from './PlanMasterPage.tsx?raw';

const planningReadinessMock = vi.hoisted(() => ({
    usePlanningReadiness: vi.fn(),
}));

vi.mock('../features/planningMasters/usePlanningReadiness', () => planningReadinessMock);

vi.mock('../components/iteration/IterationForm', () => ({
    IterationForm: ({
        onStateChange,
    }: {
        onStateChange?: (state: { dirty: boolean; pending: boolean }) => void;
    }) => (
        <div data-testid="iteration-form">
            <button
                type="button"
                onClick={() => onStateChange?.({ dirty: true, pending: false })}
            >
                Make period dirty
            </button>
            <button
                type="button"
                onClick={() => onStateChange?.({ dirty: false, pending: true })}
            >
                Start period save
            </button>
        </div>
    ),
}));

vi.mock('../components/team/TeamForm', () => ({
    TeamForm: ({
        iterationId,
        onStateChange,
    }: {
        iterationId: number;
        onStateChange?: (state: { dirty: boolean; pending: boolean }) => void;
    }) => (
        <div data-testid="team-form">
            <p>Team form iteration {iterationId}</p>
            <button
                type="button"
                onClick={() => onStateChange?.({ dirty: true, pending: false })}
            >
                Make team dirty
            </button>
        </div>
    ),
}));

vi.mock('../components/team/ImportTeamModal', () => ({
    ImportTeamModal: ({
        iterationId,
    }: {
        iterationId: number;
    }) => <div data-testid="team-import">Team import iteration {iterationId}</div>,
}));

type QueryKey = 'iterations' | 'team' | 'tasks' | 'gantt' | 'inbox';
type PlanningMember = {
    id: number;
    name: string;
    position?: string;
    capacity_hours: number;
    planned_hours: number;
};

const iterationOne: Iteration = {
    id: 1,
    name: 'August plan',
    calendar_id: 1,
    start_date: '2026-08-01',
    end_date: '2026-08-14',
    working_days: 10,
};

const iterationTwo: Iteration = {
    ...iterationOne,
    id: 2,
    name: 'September plan',
    start_date: '2026-09-01',
    end_date: '2026-09-14',
};

const memberOne: PlanningMember = {
    id: 7,
    name: 'Alex Rivera',
    position: 'Engineer',
    capacity_hours: 64,
    planned_hours: 16,
};

const taskFixture = (overrides: Partial<Task> = {}): Task => ({
    id: 11,
    iteration_id: 1,
    title: 'Saved date task',
    priority: 3,
    effort_days: 2,
    effort_hours: 16,
    assignee: { id: memberOne.id, name: memberOne.name },
    status: 'planned',
    is_overdue: false,
    is_delayed: false,
    is_composite: false,
    is_optional: false,
    is_deferred: false,
    tags: [],
    sort_order: 0,
    external_links: [],
    request_count: 0,
    agent_readiness: {
        is_ready: true,
        blockers: [],
        warnings: [],
        criteria: [],
    },
    version: 1,
    children: [],
    dependencies: [],
    ...overrides,
});

const queryFeedback = (
    overrides: Partial<PlanningQueryFeedback> = {},
): PlanningQueryFeedback => ({
    enabled: true,
    hasData: true,
    isLoading: false,
    isFetching: false,
    isError: false,
    isBlockingError: false,
    isRefetchError: false,
    error: null,
    refetch: vi.fn().mockResolvedValue(undefined),
    ...overrides,
});

interface PlanningStateOptions {
    iterations?: Iteration[];
    currentIteration?: Iteration | null;
    teamMembers?: PlanningMember[];
    tasks?: Task[];
    readiness?: Partial<PlanReadiness>;
    queries?: Partial<Record<QueryKey, Partial<PlanningQueryFeedback>>>;
}

const hasSavedDates = (task: Task) => (
    Boolean(task.start_date)
    && Boolean(task.end_date)
    && Number.isFinite(Number(task.effort_days))
    && Number(task.effort_days) > 0
);

const planningState = (options: PlanningStateOptions = {}) => {
    const currentIteration = options.currentIteration === undefined
        ? iterationOne
        : options.currentIteration;
    const iterations = options.iterations
        ?? (currentIteration ? [currentIteration] : []);
    const teamMembers = options.teamMembers ?? [];
    const tasks = options.tasks ?? [];
    const hasCurrentIteration = currentIteration !== null;
    const readinessData: PlanReadiness = {
        ...EMPTY_READINESS,
        iterationCount: iterations.length,
        hasCurrentIteration,
        currentIterationName: currentIteration?.name ?? '',
        currentIterationStart: currentIteration?.start_date ?? '',
        currentIterationEnd: currentIteration?.end_date ?? '',
        currentIterationDays: currentIteration?.working_days ?? 0,
        teamMemberCount: teamMembers.length,
        teamCapacity: teamMembers.reduce((total, member) => (
            total + member.capacity_hours
        ), 0),
        teamMembersNoCap: teamMembers.filter(member => member.capacity_hours <= 0).length,
        taskCount: tasks.length,
        tasksWithoutAssignee: tasks.filter(task => !task.assignee).length,
        tasksWithoutEffort: tasks.filter(task => (
            !Number.isFinite(Number(task.effort_days)) || Number(task.effort_days) <= 0
        )).length,
        hasGanttSchedule: tasks.length > 0 && tasks.every(hasSavedDates),
        riskCount: tasks.filter(task => task.is_overdue).length,
        ...options.readiness,
    };
    const status = deriveStatus(readinessData);
    const dependentEnabled = hasCurrentIteration;
    const queryStates: Record<QueryKey, PlanningQueryFeedback> = {
        iterations: queryFeedback(options.queries?.iterations),
        team: queryFeedback({
            enabled: dependentEnabled,
            hasData: dependentEnabled,
            ...options.queries?.team,
        }),
        tasks: queryFeedback({
            enabled: dependentEnabled,
            hasData: dependentEnabled,
            ...options.queries?.tasks,
        }),
        gantt: queryFeedback({
            enabled: dependentEnabled,
            hasData: dependentEnabled,
            ...options.queries?.gantt,
        }),
        inbox: queryFeedback({
            enabled: false,
            hasData: false,
            ...options.queries?.inbox,
        }),
    };
    const blockingError = Object.values(queryStates).find(query => query.isBlockingError);
    const isFetching = Object.values(queryStates).some(query => query.isFetching);

    return {
        selectedIterationId: currentIteration?.id ?? 0,
        setSelectedIterationId: vi.fn(),
        selectIteration: vi.fn(),
        iterations,
        currentIteration,
        hasCurrentIteration,
        teamMembers,
        tasks,
        allTasks: tasks,
        planningLeafTasks: tasks,
        gantt: undefined,
        inboxItems: [],
        readinessData,
        status,
        ready: readiness(status),
        nextId: nextStep(status),
        isLoading: Object.values(queryStates).some(query => query.isLoading),
        isError: Boolean(blockingError),
        isIterationsLoading: queryStates.iterations.isLoading,
        isIterationsError: queryStates.iterations.isBlockingError,
        isIterationsFetching: queryStates.iterations.isFetching,
        isReadinessLoading: Object.entries(queryStates).some(([key, query]) => (
            key !== 'iterations' && query.enabled && query.isLoading
        )),
        isReadinessError: Object.entries(queryStates).some(([key, query]) => (
            key !== 'iterations' && query.isBlockingError
        )),
        isReadinessFetching: Object.entries(queryStates).some(([key, query]) => (
            key !== 'iterations' && query.enabled && query.isFetching
        )),
        isFetching,
        queryStates,
        error: blockingError?.error ?? null,
        refetch: vi.fn().mockResolvedValue([]),
    };
};

const stepSelect = () => screen.getByRole('combobox', {
    name: i18n.t('plan.master.selectStep'),
});

const stepRail = () => screen.getByRole('navigation', {
    name: i18n.t('plan.master.steps'),
});

describe('PlanMasterPage hardening', () => {
    beforeEach(() => {
        planningReadinessMock.usePlanningReadiness.mockReset();
    });

    it('has English and Russian copy for every static translation key it renders', () => {
        const keys = Array.from(
            planMasterSource.matchAll(/\b(?:t|tr)\(\s*['"]([^'"]+)['"]/g),
            match => match[1],
        );
        const hasKey = (locale: 'en' | 'ru', key: string) => {
            let value: unknown = resources[locale].translation;
            for (const segment of key.split('.')) {
                if (!value || typeof value !== 'object' || !(segment in value)) return false;
                value = (value as Record<string, unknown>)[segment];
            }
            return typeof value === 'string';
        };

        expect(keys.length).toBeGreaterThan(100);
        expect(keys.filter(key => !hasKey('en', key))).toEqual([]);
        expect(keys.filter(key => !hasKey('ru', key))).toEqual([]);
    });

    it('keeps an iterations error full-page while a dependent query error stays inside the workspace shell', () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            currentIteration: null,
            queries: {
                iterations: {
                    hasData: false,
                    isError: true,
                    isBlockingError: true,
                    error: new Error('Iterations unavailable'),
                },
            },
        }));

        const firstRender = renderWithProviders(<PlanMasterPage />);

        expect(screen.getByRole('alert')).toHaveTextContent(
            i18n.t('plan.master.planningDataUnavailable'),
        );
        expect(screen.queryByRole('heading', {
            level: 1,
            name: i18n.t('plan.hub.planIterationTitle'),
        })).not.toBeInTheDocument();

        firstRender.unmount();
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            queries: {
                team: {
                    hasData: false,
                    isError: true,
                    isBlockingError: true,
                    error: new Error('Team unavailable'),
                },
            },
        }));

        renderWithProviders(<PlanMasterPage />);

        expect(screen.getByRole('heading', {
            level: 1,
            name: i18n.t('plan.hub.planIterationTitle'),
        })).toBeVisible();
        expect(screen.getByRole('alert')).toHaveTextContent(
            i18n.t('plan.master.sectionUnavailableTitle', {
                section: i18n.t('plan.steps.team.title'),
            }),
        );
        expect(screen.queryByText(
            i18n.t('plan.master.planningDataUnavailable'),
        )).not.toBeInTheDocument();
    });

    it('uses the labeled step selector and gates team and work when no period is selected', async () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            currentIteration: null,
            iterations: [iterationOne],
        }));
        const { user } = renderWithProviders(<PlanMasterPage />);

        const selector = stepSelect();
        expect(selector).toHaveAccessibleName(i18n.t('plan.master.selectStep'));

        await user.selectOptions(selector, 'team');
        expect(screen.getByRole('heading', {
            level: 2,
            name: i18n.t('plan.steps.team.title'),
        })).toBeVisible();
        expect(screen.getByText(i18n.t('plan.master.createPeriodFirst'))).toBeVisible();
        expect(screen.getByText(i18n.t('plan.master.teamNeedsPeriod'))).toBeVisible();
        expect(screen.queryByRole('button', {
            name: i18n.t('plan.master.addPerson'),
        })).not.toBeInTheDocument();

        await user.selectOptions(selector, 'work');
        expect(screen.getByRole('heading', {
            level: 2,
            name: i18n.t('plan.steps.work.title'),
        })).toBeVisible();
        expect(screen.getByText(i18n.t('plan.master.createPeriodFirst'))).toBeVisible();
        expect(screen.getByText(i18n.t('plan.master.workNeedsPeriod'))).toBeVisible();
        expect(screen.queryByRole('link', {
            name: new RegExp(i18n.t('plan.master.addTask'), 'i'),
        })).not.toBeInTheDocument();
    });

    it('does not fabricate a timeline when no saved schedule exists', () => {
        const unscheduledTask = taskFixture({
            start_date: null,
            end_date: null,
        });
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            teamMembers: [memberOne],
            tasks: [unscheduledTask],
            readiness: { hasGanttSchedule: false },
        }));

        const { container } = renderWithProviders(<PlanMasterPage />);

        expect(screen.getByRole('heading', {
            level: 2,
            name: i18n.t('plan.steps.schedule.title'),
        })).toBeVisible();
        expect(screen.getByText(i18n.t('plan.master.scheduleUnavailableTitle'))).toBeVisible();
        expect(container.querySelector('.plan-master-gantt')).not.toBeInTheDocument();
        expect(screen.queryByText(unscheduledTask.title)).not.toBeInTheDocument();
    });

    it('renders the task range from real saved schedule dates', async () => {
        const scheduledTask = taskFixture({
            start_date: '2026-08-03',
            end_date: '2026-08-05',
        });
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            teamMembers: [memberOne],
            tasks: [scheduledTask],
            readiness: { hasGanttSchedule: true },
        }));
        const { user } = renderWithProviders(<PlanMasterPage />);

        await user.selectOptions(stepSelect(), 'schedule');

        const schedule = screen.getByRole('region', {
            name: i18n.t('plan.master.savedScheduleDates'),
        });
        expect(schedule).toBeVisible();
        expect(within(schedule).getByRole('img', {
            name: new RegExp(`^${scheduledTask.title} is scheduled for`),
        })).toHaveAttribute('title', expect.stringContaining(scheduledTask.title));
        expect(within(schedule).getAllByText(scheduledTask.title)).not.toHaveLength(0);
    });

    it('treats nonpositive effort as missing work readiness', async () => {
        const taskWithoutEffort = taskFixture({
            title: 'Unestimated task',
            effort_days: -1,
            effort_hours: 0,
        });
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            teamMembers: [memberOne],
            tasks: [taskWithoutEffort],
        }));
        const { user } = renderWithProviders(<PlanMasterPage />);

        const missingFilter = screen.getByRole('button', {
            name: i18n.t('plan.master.missingEffortCount', { count: 1 }),
        });
        expect(missingFilter).toBeVisible();
        expect(screen.getByText(i18n.t('plan.master.missingFields', {
            fields: i18n.t('plan.master.effort'),
        }))).toBeVisible();

        await user.click(missingFilter);

        expect(screen.getByText(taskWithoutEffort.title)).toBeVisible();
        expect(missingFilter).toHaveAttribute('aria-pressed', 'true');
    });

    it('confirms dirty period navigation before changing steps', async () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            currentIteration: null,
        }));
        const { user } = renderWithProviders(<PlanMasterPage />);

        await user.click(screen.getByRole('button', { name: 'Make period dirty' }));
        await user.click(within(stepRail()).getByRole('button', {
            name: new RegExp(i18n.t('plan.steps.team.title')),
        }));

        expect(screen.getByRole('dialog', {
            name: new RegExp(i18n.t('plan.master.draftDiscardTitle')),
        })).toBeVisible();
        expect(screen.getByRole('heading', {
            level: 2,
            name: i18n.t('plan.steps.iteration.title'),
        })).toBeVisible();

        await user.click(screen.getByRole('button', {
            name: i18n.t('plan.master.draftDiscardConfirm'),
        }));

        expect(screen.getByRole('heading', {
            level: 2,
            name: i18n.t('plan.steps.team.title'),
        })).toBeVisible();
    });

    it('prevents period navigation while a save is pending', async () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            currentIteration: null,
        }));
        const { user } = renderWithProviders(<PlanMasterPage />);

        await user.click(screen.getByRole('button', { name: 'Start period save' }));

        const teamStep = within(stepRail()).getByRole('button', {
            name: new RegExp(i18n.t('plan.steps.team.title')),
        });
        expect(teamStep).toBeDisabled();
        expect(stepSelect()).toBeDisabled();

        const expertLink = screen.getAllByRole('link', {
            name: new RegExp(i18n.t('plan.steps.iteration.expert')),
        })[0];
        await user.click(expertLink);

        expect(screen.getByText(i18n.t('plan.master.savePendingNavigation'))).toBeVisible();
        expect(screen.getByRole('heading', {
            level: 2,
            name: i18n.t('plan.steps.iteration.title'),
        })).toBeVisible();
        expect(screen.queryByRole('dialog', {
            name: new RegExp(i18n.t('plan.master.draftDiscardTitle')),
        })).not.toBeInTheDocument();
    });

    it('keeps an open team workflow bound to the iteration that launched it', async () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            iterations: [iterationOne, iterationTwo],
            currentIteration: iterationOne,
        }));
        const { rerender, user } = renderWithProviders(<PlanMasterPage />);

        await user.click(screen.getByRole('button', {
            name: i18n.t('plan.master.addPerson'),
        }));
        expect(screen.getByText(`Team form iteration ${iterationOne.id}`)).toBeVisible();

        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            iterations: [iterationOne, iterationTwo],
            currentIteration: iterationTwo,
        }));
        rerender(<PlanMasterPage />);

        const drawer = screen.getByRole('dialog', {
            name: i18n.t('plan.master.addPersonToIteration'),
        });
        expect(within(drawer).getByText(
            `Team form iteration ${iterationOne.id}`,
        )).toBeVisible();
        expect(within(drawer).queryByText(
            `Team form iteration ${iterationTwo.id}`,
        )).not.toBeInTheDocument();
    });
});
