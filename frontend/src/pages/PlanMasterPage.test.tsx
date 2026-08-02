import { screen, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import i18n from '../i18n/i18n';
import { englishResources } from '../i18n/resources.en';
import { russianResources } from '../i18n/resources.ru';
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
const planShareServiceMock = vi.hoisted(() => ({
    getCurrent: vi.fn(),
    create: vi.fn(),
    revoke: vi.fn(),
}));

vi.mock('../features/planningMasters/usePlanningReadiness', () => planningReadinessMock);
vi.mock('../services/planShareService', () => ({
    planShareService: planShareServiceMock,
}));

type QueryKey = 'iterations' | 'team' | 'tasks' | 'gantt' | 'inbox';
type PlanningMember = {
    id: number;
    name: string;
    capacity_hours: number;
    planned_hours: number;
};

const iteration: Iteration = {
    id: 1,
    name: 'August plan',
    calendar_id: 1,
    start_date: '2026-08-01',
    end_date: '2026-08-14',
    working_days: 10,
};

const member: PlanningMember = {
    id: 7,
    name: 'Alex Rivera',
    capacity_hours: 64,
    planned_hours: 16,
};

const taskFixture = (overrides: Partial<Task> = {}): Task => ({
    id: 11,
    iteration_id: iteration.id,
    title: 'Scheduled task',
    priority: 3,
    effort_days: 2,
    effort_hours: 16,
    assignee: { id: member.id, name: member.name },
    status: 'planned',
    start_date: '2026-08-03',
    end_date: '2026-08-05',
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

const hasSavedDates = (task: Task) => (
    Boolean(task.start_date)
    && Boolean(task.end_date)
    && Number.isFinite(Number(task.effort_days))
    && Number(task.effort_days) > 0
);

const planningState = ({
    currentIteration = iteration as Iteration | null,
    teamMembers = [] as PlanningMember[],
    tasks = [] as Task[],
    readinessOverrides = {} as Partial<PlanReadiness>,
    queryOverrides = {} as Partial<Record<QueryKey, Partial<PlanningQueryFeedback>>>,
} = {}) => {
    const hasCurrentIteration = currentIteration !== null;
    const readinessData: PlanReadiness = {
        ...EMPTY_READINESS,
        iterationCount: hasCurrentIteration ? 1 : 0,
        hasCurrentIteration,
        currentIterationName: currentIteration?.name ?? '',
        currentIterationStart: currentIteration?.start_date ?? '',
        currentIterationEnd: currentIteration?.end_date ?? '',
        currentIterationDays: currentIteration?.working_days ?? 0,
        teamMemberCount: teamMembers.length,
        teamCapacity: teamMembers.reduce((sum, current) => sum + current.capacity_hours, 0),
        teamMembersNoCap: teamMembers.filter(current => current.capacity_hours <= 0).length,
        taskCount: tasks.length,
        tasksWithoutAssignee: tasks.filter(task => !task.assignee).length,
        tasksWithoutEffort: tasks.filter(task => (
            !Number.isFinite(Number(task.effort_days)) || Number(task.effort_days) <= 0
        )).length,
        hasGanttSchedule: tasks.length > 0 && tasks.every(hasSavedDates),
        riskCount: tasks.filter(task => task.is_overdue).length,
        ...readinessOverrides,
    };
    const status = deriveStatus(readinessData);
    const dependentEnabled = hasCurrentIteration;
    const queryStates: Record<QueryKey, PlanningQueryFeedback> = {
        iterations: queryFeedback(queryOverrides.iterations),
        team: queryFeedback({
            enabled: dependentEnabled,
            hasData: dependentEnabled,
            ...queryOverrides.team,
        }),
        tasks: queryFeedback({
            enabled: dependentEnabled,
            hasData: dependentEnabled,
            ...queryOverrides.tasks,
        }),
        gantt: queryFeedback({
            enabled: dependentEnabled,
            hasData: dependentEnabled,
            ...queryOverrides.gantt,
        }),
        inbox: queryFeedback({
            enabled: false,
            hasData: false,
            ...queryOverrides.inbox,
        }),
    };
    return {
        selectedIterationId: currentIteration?.id ?? 0,
        setSelectedIterationId: vi.fn(),
        selectIteration: vi.fn(),
        iterations: currentIteration ? [currentIteration] : [],
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
        isError: Object.values(queryStates).some(query => query.isBlockingError),
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
        isFetching: Object.values(queryStates).some(query => query.isFetching),
        queryStates,
        error: Object.values(queryStates).find(query => query.isBlockingError)?.error ?? null,
        refetch: vi.fn().mockResolvedValue([]),
    };
};

const stepSelect = () => screen.getByRole('combobox', {
    name: i18n.t('plan.master.selectStep'),
});

describe('PlanMasterPage orchestration checkpoint', () => {
    beforeEach(() => {
        planningReadinessMock.usePlanningReadiness.mockReset();
        planShareServiceMock.getCurrent.mockReset();
        planShareServiceMock.create.mockReset();
        planShareServiceMock.revoke.mockReset();
        planShareServiceMock.getCurrent.mockResolvedValue(null);
        planShareServiceMock.revoke.mockResolvedValue(undefined);
    });

    it('has English and Russian copy for every static translation key it renders', () => {
        const keys = Array.from(
            planMasterSource.matchAll(/\b(?:t)\(\s*['"]([^'"]+)['"]/g),
            match => match[1],
        );
        const hasKey = (locale: 'en' | 'ru', key: string) => {
            let value: unknown = locale === 'en'
                ? englishResources.translation
                : russianResources.translation;
            for (const segment of key.split('.')) {
                if (!value || typeof value !== 'object' || !(segment in value)) return false;
                value = (value as Record<string, unknown>)[segment];
            }
            return typeof value === 'string';
        };

        expect(keys.length).toBeGreaterThan(50);
        expect(keys.filter(key => !hasKey('en', key))).toEqual([]);
        expect(keys.filter(key => !hasKey('ru', key))).toEqual([]);
    });

    it('shows one authoritative action and carries a durable return checkpoint', () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState());
        const { container } = renderWithProviders(<PlanMasterPage />);

        expect(screen.getByRole('heading', {
            level: 2,
            name: i18n.t('plan.steps.team.title'),
        })).toBeVisible();
        expect(screen.queryByTestId('iteration-form')).not.toBeInTheDocument();
        expect(screen.queryByTestId('team-form')).not.toBeInTheDocument();

        const checkpoint = container.querySelector('.plan-checkpoint');
        expect(checkpoint).not.toBeNull();
        expect(checkpoint?.querySelectorAll('.btn.primary')).toHaveLength(1);
        expect(checkpoint?.querySelector('.plan-checkpoint-action'))
            .toHaveAttribute('data-blocked', 'false');
        const mobileContext = container.querySelector('.plan-master-mobile-context');
        expect(mobileContext).toHaveTextContent(iteration.name);
        expect(mobileContext).toHaveTextContent(i18n.t('plan.master.stepsComplete', {
            done: 1,
            total: 6,
        }));
        const action = within(checkpoint as HTMLElement).getByRole('link', {
            name: new RegExp(i18n.t('plan.steps.team.expert'), 'i'),
        });
        expect(action).toHaveAttribute('href', expect.stringContaining('/team?'));
        expect(action).toHaveAttribute('href', expect.stringContaining('fromPlanStep=team'));
    });

    it('sends a blocked checkpoint to its first incomplete owner and returns to the selected checkpoint', () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            currentIteration: null,
        }));
        const { container } = renderWithProviders(<PlanMasterPage />, {
            initialEntries: ['/plan/master?step=schedule'],
        });

        expect(screen.getByRole('heading', {
            level: 2,
            name: i18n.t('plan.steps.schedule.title'),
        })).toBeVisible();
        const action = screen.getByRole('link', {
            name: new RegExp(i18n.t('plan.steps.iteration.expert'), 'i'),
        });
        expect(action).toHaveAttribute('href', expect.stringContaining('/iterations?'));
        expect(action).toHaveAttribute('href', expect.stringContaining('fromPlanStep=schedule'));
        expect(container.querySelector('.plan-checkpoint-action'))
            .toHaveAttribute('data-blocked', 'true');
    });

    it('moves focus to the selected checkpoint', async () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState());
        const { user } = renderWithProviders(<PlanMasterPage />);

        await user.selectOptions(stepSelect(), 'work');

        const heading = screen.getByRole('heading', {
            level: 2,
            name: i18n.t('plan.steps.work.title'),
        });
        expect(heading).toHaveFocus();
        expect(stepSelect()).toHaveValue('work');
    });

    it('keeps an iterations error full-page and a dependent error inside the checkpoint', () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            currentIteration: null,
            queryOverrides: {
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
            queryOverrides: {
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
    });

    it('creates a read-only snapshot from the ready review checkpoint', async () => {
        const scheduledTask = taskFixture();
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            teamMembers: [member],
            tasks: [scheduledTask],
        }));
        planShareServiceMock.create.mockResolvedValue({
            id: 8,
            public_id: 'plan-share-token',
            iteration_id: iteration.id,
            iteration_name: iteration.name,
            created_by_display: 'Guest ABC123',
            snapshot_data: {
                iteration: {
                    id: iteration.id,
                    name: iteration.name,
                    start_date: iteration.start_date,
                    end_date: iteration.end_date,
                },
                team_members: [],
                tasks: [],
                snapshot_info: {
                    created_at: '2026-08-02T10:00:00Z',
                    reason: 'plan_share',
                },
            },
            created_at: '2026-08-02T10:00:00Z',
            revoked_at: null,
        });
        const { user } = renderWithProviders(<PlanMasterPage />);

        expect(screen.getByRole('heading', {
            level: 2,
            name: i18n.t('plan.steps.review.title'),
        })).toBeVisible();
        await user.click(await screen.findByRole('button', {
            name: i18n.t('plan.master.createShareLink'),
        }));

        expect(planShareServiceMock.create).toHaveBeenCalledWith(iteration.id);
        expect(await screen.findByText(i18n.t('plan.master.planSharedTitle'))).toBeVisible();
        expect(screen.getByDisplayValue(
            `${window.location.origin}/plan/share/plan-share-token`,
        )).toHaveAttribute('readonly');
    });

    it('keeps progress and six-step navigation in one rail without repeating exception prose', () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState());
        renderWithProviders(<PlanMasterPage />);

        const rail = screen.getByRole('complementary', {
            name: i18n.t('plan.master.steps'),
        });
        expect(within(rail).getByRole('navigation', {
            name: i18n.t('plan.master.steps'),
        })).toBeVisible();
        expect(within(rail).getAllByRole('button')).toHaveLength(6);
        expect(within(rail).getByRole('progressbar')).toHaveAttribute('aria-valuenow', '17');
        expect(within(rail).queryByText(
            i18n.t('plan.status.noPeople'),
        )).not.toBeInTheDocument();
    });
});
