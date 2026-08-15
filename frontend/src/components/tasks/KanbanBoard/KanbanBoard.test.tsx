import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import type { ReactNode } from 'react';
import type { Task } from '../../../types/task';
import type { TeamMember } from '../../../types/team';
import { renderWithProviders } from '../../../test/renderWithProviders';
import { KanbanBoard } from './KanbanBoard';

const dragState = vi.hoisted(() => ({
    activeId: 1,
    overId: 'planned-assigned' as string | number,
}));

const taskServiceMock = vi.hoisted(() => ({
    getByIteration: vi.fn(),
    update: vi.fn(),
    changeStatus: vi.fn(),
}));

const teamServiceMock = vi.hoisted(() => ({
    getByIteration: vi.fn(),
}));

const labelServiceMock = vi.hoisted(() => ({
    getGroups: vi.fn(),
}));

interface DndContextMockProps {
    children: ReactNode;
    onDragEnd?: (event: unknown) => void;
}

vi.mock('@dnd-kit/core', () => ({
    DndContext: ({ children, onDragEnd }: DndContextMockProps) => (
        <div>
            <button
                type="button"
                onClick={() => onDragEnd?.({
                    active: { id: dragState.activeId },
                    over: { id: dragState.overId },
                })}
            >
                Simulate board drop
            </button>
            {children}
        </div>
    ),
    DragOverlay: ({ children }: { children?: ReactNode }) => <>{children}</>,
    KeyboardSensor: class KeyboardSensor {},
    PointerSensor: class PointerSensor {},
    closestCorners: vi.fn(),
    defaultDropAnimationSideEffects: vi.fn(() => ({})),
    useSensor: vi.fn(() => ({})),
    useSensors: vi.fn(() => []),
}));

vi.mock('./KanbanColumn', () => ({
    KanbanColumn: () => null,
}));

vi.mock('./KanbanCard', () => ({
    KanbanCard: () => null,
}));

vi.mock('../../../services/taskService', () => ({
    taskService: taskServiceMock,
}));

vi.mock('../../../services/teamService', () => ({
    teamService: teamServiceMock,
}));

vi.mock('../../../services/labelService', () => ({
    labelService: labelServiceMock,
}));

const unassignedTask = (): Task => ({
    id: 1,
    iteration_id: 1,
    title: 'Unassigned task',
    priority: 5,
    effort_days: 1,
    effort_hours: 8,
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
    version: 7,
    children: [],
    dependencies: [],
});

const teamMember = (id: number, name: string): TeamMember => ({
    id,
    iteration_id: 1,
    name,
    position: 'Engineer',
    availability_percent: 100,
    professionalism_coefficient: 1,
    operational_utilization: 0,
    vacations: [],
});

const renderBoard = () => renderWithProviders(<KanbanBoard iterationId={1} />);

const openDrop = async (target: string | number, user: ReturnType<typeof renderBoard>['user']) => {
    dragState.overId = target;
    await user.click(await screen.findByRole('button', { name: 'Simulate board drop' }));
};

describe('KanbanBoard explicit ownership guard', () => {
    beforeEach(() => {
        dragState.activeId = 1;
        dragState.overId = 'planned-assigned';
        taskServiceMock.getByIteration.mockReset();
        taskServiceMock.update.mockReset();
        taskServiceMock.changeStatus.mockReset();
        teamServiceMock.getByIteration.mockReset();
        labelServiceMock.getGroups.mockReset();

        taskServiceMock.getByIteration.mockResolvedValue([unassignedTask()]);
        teamServiceMock.getByIteration.mockResolvedValue([
            teamMember(10, 'Alex'),
            teamMember(20, 'Bea'),
        ]);
        labelServiceMock.getGroups.mockResolvedValue([]);
        taskServiceMock.update.mockResolvedValue({
            ...unassignedTask(),
            assignee: { id: 20, name: 'Bea' },
            version: 8,
        });
        taskServiceMock.changeStatus.mockResolvedValue({
            task: { ...unassignedTask(), status: 'active', version: 9 },
            cascade_updates: [],
            notifications_sent: false,
        });
    });

    it.each([
        ['planned-assigned', 'Ready / Assigned'],
        ['active', 'In Progress'],
    ])('requires an explicit assignee before a drop into %s', async (target, column) => {
        const { user } = renderBoard();

        await openDrop(target, user);

        expect(await screen.findByRole('dialog', { name: 'Choose an assignee' })).toBeVisible();
        expect(screen.getByText(`Moving “Unassigned task” to ${column} also assigns ownership. Choose a team member to continue.`)).toBeVisible();
        expect(screen.getByLabelText('Assignee')).toHaveValue('');
        expect(screen.getByRole('button', { name: 'Assign and move' })).toBeDisabled();
        expect(taskServiceMock.update).not.toHaveBeenCalled();
        expect(taskServiceMock.changeStatus).not.toHaveBeenCalled();
    });

    it('uses the explicitly selected member before moving an unassigned task', async () => {
        const { user } = renderBoard();

        await openDrop('active', user);

        expect(taskServiceMock.update).not.toHaveBeenCalled();
        expect(taskServiceMock.changeStatus).not.toHaveBeenCalled();

        await user.selectOptions(screen.getByLabelText('Assignee'), '20');

        expect(taskServiceMock.update).not.toHaveBeenCalled();
        expect(taskServiceMock.changeStatus).not.toHaveBeenCalled();

        await user.click(screen.getByRole('button', { name: 'Assign and move' }));

        await waitFor(() => {
            expect(taskServiceMock.update).toHaveBeenCalledWith(1, {
                assignee_id: 20,
                expected_version: 7,
            });
        });
        await waitFor(() => {
            expect(taskServiceMock.changeStatus).toHaveBeenCalledWith(1, 'active', 'Moved on board', 8);
        });
    });

    it('cancels an ownership-selection drop without changing the task', async () => {
        const { user } = renderBoard();

        await openDrop('planned-assigned', user);
        await user.click(screen.getByRole('button', { name: 'Cancel' }));

        await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
        expect(taskServiceMock.update).not.toHaveBeenCalled();
        expect(taskServiceMock.changeStatus).not.toHaveBeenCalled();
    });

    it('offers team setup recovery for an empty team without mutating the task', async () => {
        teamServiceMock.getByIteration.mockResolvedValue([]);
        const { user } = renderBoard();

        await openDrop('planned-assigned', user);

        expect(await screen.findByRole('dialog', { name: 'No assignee available' })).toBeVisible();
        expect(screen.getByRole('link', { name: 'Add team member' })).toHaveAttribute(
            'href',
            '/team?action=assign&iterationId=1',
        );
        expect(taskServiceMock.update).not.toHaveBeenCalled();
        expect(taskServiceMock.changeStatus).not.toHaveBeenCalled();
    });
});
