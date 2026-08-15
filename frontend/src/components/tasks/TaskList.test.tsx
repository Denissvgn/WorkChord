import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import type { Task } from '../../types/task';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TaskList } from './TaskList';

const taskServiceMock = vi.hoisted(() => ({
    getByIteration: vi.fn(),
    delete: vi.fn(),
    reorder: vi.fn(),
    mergeTasks: vi.fn(),
    unmergeTask: vi.fn(),
}));

const labelServiceMock = vi.hoisted(() => ({
    getGroups: vi.fn(),
}));

vi.mock('../../services/taskService', () => ({
    taskService: taskServiceMock,
}));

vi.mock('../../services/labelService', () => ({
    labelService: labelServiceMock,
}));

vi.mock('./TaskAgentReadinessBadge', () => ({
    TaskAgentReadinessBadge: () => null,
}));

const task = (id: number): Task => ({
    id,
    iteration_id: 1,
    project_id: null,
    milestone_id: null,
    parent_id: null,
    title: `Task ${id}`,
    description: '',
    priority: id,
    effort_days: 1,
    effort_hours: 8,
    project: null,
    milestone: null,
    assignee: null,
    status: 'planned',
    start_date: null,
    end_date: null,
    actual_start_date: null,
    actual_end_date: null,
    min_start_date: null,
    max_end_date: null,
    is_overdue: false,
    is_delayed: false,
    is_composite: false,
    is_optional: false,
    is_deferred: false,
    tags: [],
    sort_order: id,
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
});

describe('TaskList accessibility', () => {
    beforeEach(() => {
        Object.values(taskServiceMock).forEach(mock => mock.mockReset());
        labelServiceMock.getGroups.mockReset();
        labelServiceMock.getGroups.mockResolvedValue([]);
    });

    it('announces the inner task loading state', () => {
        taskServiceMock.getByIteration.mockReturnValue(new Promise(() => undefined));

        renderWithProviders(
            <TaskList
                iterationId={1}
                sortKey="priority"
                onSortKeyChange={() => undefined}
            />,
        );

        expect(screen.getByRole('status')).toHaveTextContent('Loading tasks');
        expect(screen.getByRole('status')).toHaveAttribute('aria-busy', 'true');
    });

    it('associates the merge parent title label with its input', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([task(1), task(2)]);
        const { user } = renderWithProviders(
            <TaskList
                iterationId={1}
                sortKey="priority"
                onSortKeyChange={() => undefined}
                requestedMode="merge"
            />,
        );

        const selections = await screen.findAllByRole('checkbox', {
            name: 'Select for merge',
        });
        await user.click(selections[0]!);
        await user.click(selections[1]!);
        await user.click(screen.getByRole('button', { name: 'Merge (2)' }));

        expect(screen.getByRole('textbox', {
            name: 'New parent task title',
        })).toHaveFocus();
    });
});
