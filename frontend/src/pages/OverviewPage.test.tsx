import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import type { UserEvent } from '@testing-library/user-event';
import { renderWithProviders } from '../test/renderWithProviders';
import type { Iteration, IterationSummary } from '../types/iteration';
import type { Task, TaskStatus } from '../types/task';
import type { PlanningTeamMember } from '../features/planningMasters/usePlanningReadiness';
import { selectWorkNowTasks } from '../utils/selectWorkNowTasks';
import OverviewPage from './OverviewPage';

const planningReadinessMock = vi.hoisted(() => ({
    usePlanningReadiness: vi.fn(),
}));

const serviceMocks = vi.hoisted(() => ({
    getIterationSummary: vi.fn(),
    getProjectSummary: vi.fn(),
}));

vi.mock('../features/planningMasters/usePlanningReadiness', () => planningReadinessMock);
vi.mock('../services/iterationService', () => ({
    iterationService: {
        getSummary: serviceMocks.getIterationSummary,
    },
}));
vi.mock('../services/projectService', () => ({
    projectService: {
        getSummary: serviceMocks.getProjectSummary,
    },
}));
const task = (
    id: number,
    status: TaskStatus,
    options: Pick<Task, 'assignee' | 'is_overdue'> = {
        assignee: null,
        is_overdue: false,
    },
) => ({
    id,
    title: `Task ${id}`,
    status,
    assignee: options.assignee,
    is_overdue: options.is_overdue,
    effort_days: 4,
} as Task);

const iteration: Iteration = {
    id: 1,
    name: 'August plan',
    calendar_id: 1,
    project_id: null,
    project: null,
    start_date: '2026-08-01',
    end_date: '2026-08-14',
    working_days: 10,
};

const iterationSummary: IterationSummary = {
    id: iteration.id,
    name: iteration.name,
    project_id: null,
    project: null,
    start_date: iteration.start_date,
    end_date: iteration.end_date,
    working_days: iteration.working_days,
    total_tasks: 1,
    completed_tasks: 0,
    total_effort_days: 2,
    team_capacity_days: 0,
    overdue_tasks_count: 0,
};

const queryState = (overrides: Record<string, unknown> = {}) => ({
    enabled: true,
    hasData: true,
    dataUpdatedAt: Date.parse('2026-08-03T12:00:00Z'),
    isLoading: false,
    isFetching: false,
    isError: false,
    isBlockingError: false,
    isRefetchError: false,
    error: null,
    refetch: vi.fn().mockResolvedValue({ isError: false }),
    ...overrides,
});

const expectTabOrder = async (
    user: UserEvent,
    elements: HTMLElement[],
) => {
    for (const element of elements) {
        await user.tab();
        expect(element).toHaveFocus();
    }
};

const overviewPlanningState = ({
    currentIteration = iteration as Iteration | null,
    tasks = [] as Task[],
    teamMembers = [] as PlanningTeamMember[],
    inboxCount = 0,
    queryOverrides = {} as Record<string, Record<string, unknown>>,
} = {}) => {
    const hasCurrentIteration = currentIteration !== null;
    return {
        selectedIterationId: currentIteration?.id ?? 0,
        iterations: currentIteration ? [currentIteration] : [],
        currentIteration,
        teamMembers,
        allTasks: tasks,
        readinessData: {
            inboxCount,
        },
        ready: {
            done: 6,
            total: 6,
            pct: 100,
        },
        nextId: 'review',
        queryStates: {
            iterations: queryState(queryOverrides.iterations),
            team: queryState({
                enabled: hasCurrentIteration,
                hasData: hasCurrentIteration,
                ...queryOverrides.team,
            }),
            tasks: queryState({
                enabled: hasCurrentIteration,
                hasData: hasCurrentIteration,
                ...queryOverrides.tasks,
            }),
            gantt: queryState({
                enabled: hasCurrentIteration,
                hasData: hasCurrentIteration,
                ...queryOverrides.gantt,
            }),
            inbox: queryState({
                enabled: hasCurrentIteration,
                hasData: hasCurrentIteration,
                ...queryOverrides.inbox,
            }),
        },
    };
};

describe('selectWorkNowTasks', () => {
    it('keeps the daily preview bounded and prioritizes overdue and active work', () => {
        const tasks = [
            task(1, 'planned', {
                assignee: { id: 1, name: 'Ada' },
                is_overdue: false,
            }),
            task(2, 'resolved'),
            task(3, 'active', {
                assignee: { id: 2, name: 'Lin' },
                is_overdue: false,
            }),
            task(4, 'planned', {
                assignee: { id: 3, name: 'Sam' },
                is_overdue: true,
            }),
            task(5, 'planned'),
        ];

        expect(selectWorkNowTasks(tasks).map(item => item.id)).toEqual([4, 3, 5]);
    });

    it('preserves source order between tasks with the same attention rank', () => {
        const tasks = [
            task(6, 'active'),
            task(7, 'active'),
            task(8, 'closed'),
        ];

        expect(selectWorkNowTasks(tasks).map(item => item.id)).toEqual([6, 7]);
    });
});

describe('Overview partial-data resilience', () => {
    beforeEach(() => {
        planningReadinessMock.usePlanningReadiness.mockReset();
        serviceMocks.getIterationSummary.mockReset();
        serviceMocks.getIterationSummary.mockResolvedValue(iterationSummary);
        serviceMocks.getProjectSummary.mockReset();
    });

    it('announces the initial loading state without adding inactive controls to the tab order', async () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(
            overviewPlanningState({
                currentIteration: null,
                queryOverrides: {
                    iterations: {
                        hasData: false,
                        isLoading: true,
                    },
                },
            }),
        );

        const { user } = renderWithProviders(<OverviewPage />);

        expect(screen.getByRole('status')).toHaveAttribute('aria-busy', 'true');
        expect(screen.queryByRole('button')).not.toBeInTheDocument();
        expect(screen.queryByRole('link')).not.toBeInTheDocument();

        await user.tab();
        expect(document.body).toHaveFocus();
    });

    it('keeps cached task content visible with source freshness and retries only the failed query', async () => {
        const tasksRefetch = vi.fn().mockResolvedValue({ isError: false });
        const state = overviewPlanningState({
            tasks: [
                task(11, 'active', {
                    assignee: { id: 7, name: 'Ada Lovelace' },
                    is_overdue: false,
                }),
                task(13, 'resolved', {
                    assignee: { id: 7, name: 'Ada Lovelace' },
                    is_overdue: false,
                }),
            ],
            queryOverrides: {
                tasks: {
                    isError: true,
                    isRefetchError: true,
                    error: new Error('refresh failed'),
                    refetch: tasksRefetch,
                },
            },
        });
        planningReadinessMock.usePlanningReadiness.mockReturnValue(state);

        const { user } = renderWithProviders(<OverviewPage />);

        expect(await screen.findByText('Task 11')).toBeVisible();
        const statusTitle = screen.getByRole('heading', {
            name: 'Some Overview data could not be refreshed',
        });
        const status = statusTitle.closest('section');
        expect(status).not.toBeNull();
        expect(within(status as HTMLElement).getByText('Iteration tasks')).toBeVisible();
        expect(within(status as HTMLElement).getByText(/Last confirmed/)).toBeVisible();

        await expectTabOrder(user, [
            screen.getByRole('button', { name: 'Retry affected data' }),
            screen.getByRole('link', { name: 'Check system status' }),
            screen.getByRole('link', { name: 'Review plan' }),
            screen.getByRole('link', { name: 'Open task board' }),
            screen.getByRole('link', {
                name: 'Open “Task 11” in the task drawer',
            }),
        ]);

        await user.click(screen.getByRole('button', { name: 'Retry affected data' }));

        expect(tasksRefetch).toHaveBeenCalledTimes(1);
        expect(state.queryStates.team.refetch).not.toHaveBeenCalled();
        expect(state.queryStates.gantt.refetch).not.toHaveBeenCalled();
        expect(state.queryStates.inbox.refetch).not.toHaveBeenCalled();
        await waitFor(() => {
            expect(screen.getByText('Overview data updated.')).toHaveAttribute(
                'role',
                'status',
            );
            expect(screen.getByText('Overview')).toHaveFocus();
        });
    });

    it('keeps recovery focus in place when a partial-data retry fails', async () => {
        let finishRetry: ((result: { isError: boolean }) => void) | undefined;
        const tasksRefetch = vi.fn(() => new Promise<{ isError: boolean }>(resolve => {
            finishRetry = resolve;
        }));
        planningReadinessMock.usePlanningReadiness.mockReturnValue(
            overviewPlanningState({
                tasks: [task(14, 'active', {
                    assignee: { id: 7, name: 'Ada Lovelace' },
                    is_overdue: false,
                })],
                queryOverrides: {
                    tasks: {
                        isError: true,
                        isRefetchError: true,
                        error: new Error('refresh failed'),
                        refetch: tasksRefetch,
                    },
                },
            }),
        );

        const { user } = renderWithProviders(<OverviewPage />);
        const retry = await screen.findByRole('button', {
            name: 'Retry affected data',
        });

        await user.click(retry);

        expect(retry).toBeDisabled();
        expect(retry).toHaveAttribute('aria-busy', 'true');
        expect(retry).toHaveAccessibleName('Retrying affected data…');

        finishRetry?.({ isError: true });
        await waitFor(() => expect(retry).toBeEnabled());

        expect(retry).toHaveFocus();
        expect(screen.queryByText('Overview data updated.')).not.toBeInTheDocument();
        expect(screen.getByRole('heading', {
            name: 'Some Overview data could not be refreshed',
        })).toBeVisible();
    });

    it('does not present unavailable tasks as a confirmed empty state', async () => {
        const state = overviewPlanningState({
            queryOverrides: {
                tasks: {
                    hasData: false,
                    isError: true,
                    isBlockingError: true,
                    error: new Error('tasks unavailable'),
                },
            },
        });
        planningReadinessMock.usePlanningReadiness.mockReturnValue(state);

        renderWithProviders(<OverviewPage />);

        expect(await screen.findByRole('heading', { name: 'Overview' })).toBeVisible();
        expect(screen.getAllByRole('alert')).toHaveLength(1);
        expect(screen.getAllByRole('button', { name: 'Retry affected data' })).toHaveLength(1);
        expect(screen.getAllByRole('link', { name: 'Check system status' })).toHaveLength(1);
        expect(screen.getByRole('link', { name: 'Open task board' }))
            .toHaveAttribute('href', '/tasks');
        expect(screen.queryByRole('link', { name: 'Add first task' }))
            .not.toBeInTheDocument();
        expect(screen.queryByText('No open tasks need attention in this planning period.'))
            .not.toBeInTheDocument();
        expect(screen.queryByText('No tasks scoped to this iteration yet.'))
            .not.toBeInTheDocument();
    });

    it('keeps a usable delivery snapshot visible when planning signals are unavailable', async () => {
        serviceMocks.getIterationSummary.mockResolvedValue({
            ...iterationSummary,
            total_tasks: 4,
            completed_tasks: 3,
        });
        planningReadinessMock.usePlanningReadiness.mockReturnValue(
            overviewPlanningState({
                tasks: [task(41, 'resolved', {
                    assignee: { id: 7, name: 'Ada Lovelace' },
                    is_overdue: false,
                })],
                queryOverrides: {
                    team: {
                        hasData: false,
                        isError: true,
                        isBlockingError: true,
                        error: new Error('team unavailable'),
                    },
                },
            }),
        );

        const { container } = renderWithProviders(<OverviewPage />);

        expect(await screen.findByText('3 / 4 tasks complete')).toBeVisible();
        expect(screen.getByRole('progressbar', {
            name: 'Task completion',
        })).toHaveAttribute('aria-valuenow', '75');
        expect(container.querySelector('.overview-focus-progress')).not.toBeNull();
        expect(container.querySelector('.overview-thread-flow'))
            .not.toHaveClass('has-focus-panel');
        expect(screen.queryByRole('heading', {
            name: 'Plan ready for review',
        })).not.toBeInTheDocument();
    });

    it('reduces iteration details to actionable exception and commitment clusters', async () => {
        const completedIteration: Iteration = {
            ...iteration,
            start_date: '2020-01-01',
            end_date: '2020-01-14',
        };
        const overloadedMember: PlanningTeamMember = {
            id: 17,
            iteration_id: completedIteration.id,
            name: 'Ada Lovelace',
            position: 'Engineer',
            availability_percent: 100,
            professionalism_coefficient: 1,
            operational_utilization: 0,
            vacations: [],
            capacity_hours: 16,
            planned_hours: 24,
        };
        planningReadinessMock.usePlanningReadiness.mockReturnValue(
            overviewPlanningState({
                currentIteration: completedIteration,
                teamMembers: [overloadedMember],
                tasks: [
                    task(21, 'active', {
                        assignee: { id: overloadedMember.id, name: overloadedMember.name },
                        is_overdue: true,
                    }),
                    task(22, 'active'),
                ],
            }),
        );

        const { user, container } = renderWithProviders(<OverviewPage />);
        await screen.findByText('Task 21');
        const detailsLabel = screen.getByText('Iteration details');
        const details = detailsLabel.closest('details');
        const summary = detailsLabel.closest('summary');

        expect(details).not.toBeNull();
        expect(summary).not.toBeNull();
        expect(details).not.toHaveAttribute('open');
        expect(summary).toHaveAccessibleName(/Iteration details/);

        const reviewTasks = screen.getByRole('link', { name: 'Review tasks' });
        const remainingExceptions = screen.getByRole('button', {
            name: 'Review 3 remaining exceptions',
        });
        expect(reviewTasks).toHaveAttribute(
            'href',
            '/tasks?layout=board&task=21&from=overview&returnTask=21&thread=attention',
        );
        expect(remainingExceptions).toHaveAttribute(
            'aria-controls',
            'overview-iteration-details',
        );
        expect(remainingExceptions).toHaveAttribute('aria-expanded', 'false');

        await expectTabOrder(user, [
            reviewTasks,
            remainingExceptions,
            screen.getByRole('link', { name: 'Open task board' }),
            screen.getByRole('link', {
                name: 'Open “Task 21” in the task drawer',
            }),
            screen.getByRole('link', {
                name: 'Open “Task 22” in the task drawer',
            }),
            summary as HTMLElement,
        ]);
        await user.click(remainingExceptions);

        expect(details).toHaveAttribute('open');
        expect(remainingExceptions).toHaveAttribute('aria-expanded', 'true');
        expect(summary).toHaveFocus();

        const exceptions = screen.getByRole('region', { name: 'Other exceptions' });
        const commitments = screen.getByRole('region', { name: 'Iteration risks' });
        expect(exceptions).toBeVisible();
        expect(commitments).toBeVisible();
        expect(within(exceptions).getByRole('heading', {
            level: 2,
            name: 'Other exceptions',
        })).toBeVisible();
        expect(within(exceptions).getByRole('heading', {
            level: 3,
            name: 'Capacity warnings',
        })).toBeVisible();
        expect(within(commitments).getByRole('heading', {
            level: 2,
            name: 'Iteration risks',
        })).toBeVisible();
        expect(screen.getByText('Ada Lovelace')).toBeVisible();
        expect(within(exceptions).getByRole('link', {
            name: /Ada Lovelace.*over capacity.*Review team/,
        })).toBeVisible();
        expect(within(commitments).getByRole('link', {
            name: /trails elapsed time.*Review schedule/,
        })).toBeVisible();

        await expectTabOrder(user, [
            ...within(exceptions).getAllByRole('link'),
            ...within(commitments).getAllByRole('link'),
        ]);

        await user.click(remainingExceptions);
        expect(details).toHaveAttribute('open');
        expect(summary).toHaveFocus();

        // jsdom does not implement native <details> keyboard activation.
        await user.click(summary as HTMLElement);
        expect(details).not.toHaveAttribute('open');
        expect(remainingExceptions).toHaveAttribute('aria-expanded', 'false');

        expect(container.querySelector('.overview-details-count')).not.toBeInTheDocument();
        expect(screen.queryByText('Team Workload')).not.toBeInTheDocument();
        expect(screen.queryByText('Task Distribution')).not.toBeInTheDocument();
        expect(screen.queryByText('Iteration pace')).not.toBeInTheDocument();
        expect(screen.queryByText('Effort burned')).not.toBeInTheDocument();
        expect(screen.queryByText('Saved view signals')).not.toBeInTheDocument();
        expect(screen.queryByText('Velocity')).not.toBeInTheDocument();
        expect(screen.queryByText('Burn-up')).not.toBeInTheDocument();
    });

    it('promotes a warning signal above an advisory regardless of construction order', async () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(
            overviewPlanningState({
                inboxCount: 2,
                tasks: [
                    task(23, 'active'),
                    task(24, 'resolved', {
                        assignee: { id: 7, name: 'Ada Lovelace' },
                        is_overdue: false,
                    }),
                ],
            }),
        );

        renderWithProviders(<OverviewPage />);

        expect(await screen.findByRole('heading', {
            name: '2 intake items need triage',
        })).toBeVisible();
        expect(screen.getByRole('link', { name: 'Open Triage' }))
            .toHaveAttribute('href', '/triage');
        expect(screen.getByRole('button', {
            name: 'Review 1 remaining exception',
        })).toBeVisible();
    });

    it('excludes completed tasks from overdue and unassigned attention', async () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(
            overviewPlanningState({
                tasks: [
                    task(25, 'resolved', {
                        assignee: null,
                        is_overdue: true,
                    }),
                    task(26, 'closed'),
                ],
            }),
        );

        renderWithProviders(<OverviewPage />);

        expect(await screen.findByRole('heading', { name: 'Plan ready for review' }))
            .toBeVisible();
        expect(screen.queryByText(/overdue task/)).not.toBeInTheDocument();
        expect(screen.queryByText(/unassigned task/)).not.toBeInTheDocument();
        expect(screen.queryByRole('button', {
            name: /remaining exception/,
        })).not.toBeInTheDocument();
    });

    it('announces task-based completion and keeps healthy actions in reading order', async () => {
        serviceMocks.getIterationSummary.mockResolvedValue({
            ...iterationSummary,
            total_tasks: 4,
            completed_tasks: 1,
        });
        planningReadinessMock.usePlanningReadiness.mockReturnValue(
            overviewPlanningState({
                tasks: [
                    task(31, 'active', {
                        assignee: { id: 7, name: 'Ada Lovelace' },
                        is_overdue: false,
                    }),
                    task(32, 'resolved', {
                        assignee: { id: 7, name: 'Ada Lovelace' },
                        is_overdue: false,
                    }),
                ],
            }),
        );

        const { user, container } = renderWithProviders(<OverviewPage />);
        const progress = await screen.findByRole('progressbar', {
            name: 'Task completion',
        });
        expect(await screen.findByText('1 / 4 tasks complete')).toBeVisible();

        expect(screen.getAllByRole('progressbar')).toHaveLength(1);
        expect(progress).toHaveAttribute('aria-valuemin', '0');
        expect(progress).toHaveAttribute('aria-valuemax', '100');
        await waitFor(() => {
            expect(progress).toHaveAttribute('aria-valuenow', '25');
            expect(progress).toHaveAttribute(
                'aria-valuetext',
                '25% complete — 1 of 4 tasks complete',
            );
        });
        expect(screen.getByText('25%')).toBeVisible();
        expect(screen.getByRole('link', {
            name: 'Open “Task 31” in the task drawer',
        })).toHaveAttribute(
            'href',
            '/tasks?layout=board&task=31&from=overview&returnTask=31&thread=work-now',
        );

        const focusPanel = screen.getByRole('heading', {
            level: 2,
            name: 'Plan ready for review',
        }).closest('section');
        const workNowHeading = screen.getByRole('heading', {
            level: 2,
            name: 'Work now',
        });
        const workNowPanel = screen.getByRole('region', {
            name: 'Work now',
        });
        const deliverySnapshot = container.querySelector('.overview-focus-progress');
        expect(focusPanel).not.toBeNull();
        expect(workNowPanel).toContainElement(workNowHeading);
        expect(screen.queryByRole('heading', {
            level: 3,
            name: 'Work now',
        })).not.toBeInTheDocument();
        expect(deliverySnapshot).not.toBeNull();
        expect(
            focusPanel!.compareDocumentPosition(workNowPanel!)
            & Node.DOCUMENT_POSITION_FOLLOWING,
        ).toBeTruthy();
        expect(
            workNowPanel!.compareDocumentPosition(deliverySnapshot!)
            & Node.DOCUMENT_POSITION_FOLLOWING,
        ).toBeTruthy();

        await expectTabOrder(user, [
            screen.getByRole('link', { name: 'Review plan' }),
            screen.getByRole('link', { name: 'Open task board' }),
            screen.getByRole('link', {
                name: 'Open “Task 31” in the task drawer',
            }),
        ]);
    });

    it('isolates an unavailable delivery summary and retries only that source', async () => {
        const state = overviewPlanningState({
            tasks: [task(12, 'active', {
                assignee: { id: 8, name: 'Grace Hopper' },
                is_overdue: false,
            })],
        });
        planningReadinessMock.usePlanningReadiness.mockReturnValue(state);
        serviceMocks.getIterationSummary.mockRejectedValueOnce(new Error('summary unavailable'));

        const { user } = renderWithProviders(<OverviewPage />);

        expect(await screen.findByText('Delivery summary')).toBeVisible();
        expect(screen.getByText('Task 12')).toBeVisible();
        expect(screen.queryByText('The requested data could not be loaded.'))
            .not.toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: 'Retry affected data' }));
        await waitFor(() => expect(serviceMocks.getIterationSummary).toHaveBeenCalledTimes(2));

        expect(state.queryStates.tasks.refetch).not.toHaveBeenCalled();
        expect(state.queryStates.team.refetch).not.toHaveBeenCalled();
    });

    it('uses full-page recovery only when planning-period scope has no usable value', async () => {
        const iterationsRefetch = vi.fn().mockResolvedValue({ isError: false });
        planningReadinessMock.usePlanningReadiness.mockReturnValue(
            overviewPlanningState({
                currentIteration: null,
                queryOverrides: {
                    iterations: {
                        hasData: false,
                        isError: true,
                        isBlockingError: true,
                        error: new Error('periods unavailable'),
                        refetch: iterationsRefetch,
                    },
                },
            }),
        );

        const { user } = renderWithProviders(<OverviewPage />);

        expect(screen.getByRole('alert'))
            .toHaveTextContent('Iterations could not be loaded');
        const systemStatusLink = screen.getByRole('link', { name: 'Check system status' });
        expect(systemStatusLink)
            .toHaveAttribute('href', '/settings?tab=about');
        expect(screen.queryByText('Set up planning period')).not.toBeInTheDocument();
        expect(screen.queryByText('Work now')).not.toBeInTheDocument();

        await expectTabOrder(user, [
            screen.getByRole('button', { name: 'Retry' }),
            systemStatusLink,
        ]);
    });

    it('keeps blocking recovery stable and skips its busy retry control', async () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(
            overviewPlanningState({
                currentIteration: null,
                queryOverrides: {
                    iterations: {
                        hasData: false,
                        isError: true,
                        isBlockingError: true,
                        isFetching: true,
                        error: new Error('periods unavailable'),
                    },
                },
            }),
        );

        const { user } = renderWithProviders(<OverviewPage />);
        const retryButton = screen.getByRole('button', { name: 'Retry' });
        const systemStatusLink = screen.getByRole('link', {
            name: 'Check system status',
        });

        expect(retryButton).toBeDisabled();
        expect(retryButton).toHaveAttribute('aria-busy', 'true');
        await expectTabOrder(user, [systemStatusLink]);
    });

    it('shows one keyboard-reachable setup path after a confirmed empty planning-period result', async () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(
            overviewPlanningState({ currentIteration: null }),
        );

        const { user } = renderWithProviders(<OverviewPage />);

        expect(screen.getByText('No planning periods yet')).toBeVisible();
        const setupLink = screen.getByRole('link', { name: 'Create planning period' });
        expect(setupLink)
            .toHaveAttribute('href', '/plan');
        expect(screen.queryByText('Iterations could not be loaded')).not.toBeInTheDocument();

        await expectTabOrder(user, [setupLink]);
    });

    it('distinguishes first-use work from a planning period whose tasks are complete', async () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(
            overviewPlanningState(),
        );

        const { rerender } = renderWithProviders(<OverviewPage />);

        expect(await screen.findByText(
            'No tasks have been added to this planning period.',
        )).toBeVisible();
        expect(screen.getByRole('link', { name: 'Add first task' }))
            .toHaveAttribute('href', '/tasks?create=1');

        planningReadinessMock.usePlanningReadiness.mockReturnValue(
            overviewPlanningState({
                tasks: [task(41, 'resolved')],
            }),
        );
        rerender(<OverviewPage />);

        expect(await screen.findByText(
            'No open tasks remain in this planning period.',
        )).toBeVisible();
        expect(screen.getByRole('link', { name: 'Add task' }))
            .toHaveAttribute('href', '/tasks?create=1');
        expect(screen.queryByRole('link', { name: 'Add first task' }))
            .not.toBeInTheDocument();
    });
});
