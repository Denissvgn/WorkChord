import { screen } from '@testing-library/react';
import { expect, it, vi } from 'vitest';
import { useIterationStore } from '../store/iterationStore';
import type { GanttResponse, GanttTask } from '../types/gantt';
import type { Iteration } from '../types/iteration';
import GanttPage from '../pages/GanttPage';
import { expectPageChrome } from './pageChrome';
import { renderWithProviders } from './renderWithProviders';
const services = vi.hoisted(() => ({ getChart: vi.fn(), getAll: vi.fn() }));
vi.mock('../services/ganttService', () => ({ ganttService: services }));
vi.mock('../services/iterationService', () => ({ iterationService: services }));

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

it('checks the loaded Gantt page and chart chrome', async () => {
    useIterationStore.setState({ selectedIterationId: 1 });
    services.getAll.mockResolvedValue([iterationFixture]);
    services.getChart.mockResolvedValue(ganttFixture);
    const { container, user } = renderWithProviders(<GanttPage />);
    await screen.findByTestId('page-toolbar');
    expect(screen.getByRole('searchbox', { name: 'Search tasks' })).toBeInTheDocument();
    expectPageChrome(container);
    expect(screen.getAllByRole('button', { name: /more actions/i })).toHaveLength(1);
    await user.click(screen.getByRole('button', { name: /more actions/i }));
    expect(screen.getByRole('menuitem', { name: 'Zoom timeline in' })).toBeInTheDocument();
});
