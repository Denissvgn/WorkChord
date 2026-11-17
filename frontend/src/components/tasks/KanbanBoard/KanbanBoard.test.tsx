import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
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
    batchUpdate: vi.fn(),
}));

const teamServiceMock = vi.hoisted(() => ({
    getByIteration: vi.fn(),
    getProfiles: vi.fn(),
    getWorkload: vi.fn(),
    create: vi.fn(),
}));

const planningMock = vi.hoisted(() => ({
    readInitial: vi.fn(),
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

vi.mock('../../../services/planningInputService', () => ({
    planningInputService: planningMock,
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

const teamMember = (id: number, name: string, profileKind: 'human' | 'agent' = 'human'): TeamMember => ({
    id,
    profile_id: id + 100,
    profile: { id: id + 100, display_name: name, profile_kind: profileKind, automation_enabled: false, assignment_modes: [], skills: [] },
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
        taskServiceMock.batchUpdate.mockReset();
        taskServiceMock.batchUpdate.mockResolvedValue({ results: [{ success: true }] });
        taskServiceMock.changeStatus.mockReset();
        teamServiceMock.getByIteration.mockReset();
        teamServiceMock.getProfiles.mockReset();
        teamServiceMock.getWorkload.mockReset();
        teamServiceMock.create.mockReset();
        planningMock.readInitial.mockReset();
        teamServiceMock.getProfiles.mockResolvedValue([]);
        teamServiceMock.getWorkload.mockResolvedValue({ workload_percent: 40 });
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
        ['planned-assigned', 'Planned, assigned'],
        ['active', 'Active'],
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

        await waitFor(() => expect(taskServiceMock.batchUpdate).toHaveBeenCalledWith(1, {
            expected_revision: undefined,
            tasks: [{ task_id: 1, expected_version: 7, update: { assignee_id: 20, status: 'active' }, status_reason: 'Moved on board' }],
        }));
        expect(taskServiceMock.update).not.toHaveBeenCalled();
        expect(taskServiceMock.changeStatus).not.toHaveBeenCalled();
    });

    it('cancels an ownership-selection drop without changing the task', async () => {
        const { user } = renderBoard();

        await openDrop('planned-assigned', user);
        await user.click(screen.getByRole('button', { name: 'Cancel' }));

        await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
        expect(taskServiceMock.update).not.toHaveBeenCalled();
        expect(taskServiceMock.changeStatus).not.toHaveBeenCalled();
    });

    it('moves a nested task: dropping its card opens the picker', async () => {
        const child = { ...unassignedTask(), id: 2, title: 'Nested task' };
        taskServiceMock.getByIteration.mockResolvedValue([{ ...unassignedTask(), id: 3, title: 'Parent', is_composite: true, children: [child] }]);
        dragState.activeId = 2;
        const { user } = renderBoard();

        await openDrop('active', user);

        expect(await screen.findByRole('dialog', { name: 'Choose an assignee' })).toBeVisible();
        expect(screen.getByText(/Moving “Nested task” to Active/)).toBeVisible();
        await user.selectOptions(screen.getByLabelText('Assignee'), '20');
        await user.click(screen.getByRole('button', { name: 'Assign and move' }));
        await waitFor(() => expect(taskServiceMock.batchUpdate).toHaveBeenCalledWith(1, expect.objectContaining({
            tasks: [expect.objectContaining({ task_id: 2, update: { assignee_id: 20, status: 'active' } })],
        })));
    });

    it('shows the shared picker with people and agents grouped, their load, and people outside the iteration', async () => {
        teamServiceMock.getByIteration.mockResolvedValue([teamMember(10, 'Alex'), teamMember(20, 'Builder', 'agent')]);
        teamServiceMock.getProfiles.mockResolvedValue([{ id: 900, display_name: 'Casey', profile_kind: 'human' }]);
        const { user } = renderBoard();

        await openDrop('active', user);

        const select = await screen.findByRole('combobox', { name: 'Assignee' });
        expect(await within(select).findByRole('option', { name: 'Alex · 40% load' })).toBeInTheDocument();
        expect(within(select).getByRole('group', { name: 'People' })).toBeInTheDocument();
        expect(within(select).getByRole('group', { name: 'Agents' })).toBeInTheDocument();
        expect(await within(select).findByRole('group', { name: 'Not in this iteration' })).toBeInTheDocument();
        expect(within(select).getByRole('option', { name: 'Casey · Add to iteration and assign' })).toBeInTheDocument();
    });

    it('adds an outside profile to the iteration and then moves the task with the new revision', async () => {
        teamServiceMock.getProfiles.mockResolvedValue([{ id: 900, display_name: 'Casey', profile_kind: 'human' }]);
        planningMock.readInitial.mockImplementation(async (kind: string) => ({ expected_revisions: { 1: kind === 'iteration' ? 12 : 11 } }));
        teamServiceMock.create.mockResolvedValue({ ...teamMember(30, 'Casey'), profile_id: 900 });
        const { user } = renderBoard();

        await openDrop('active', user);
        await user.selectOptions(await screen.findByRole('combobox', { name: 'Assignee' }), 'profile:900');
        expect(teamServiceMock.create).not.toHaveBeenCalled();
        await user.click(await screen.findByRole('button', { name: 'Add to iteration and assign' }));

        await waitFor(() => expect(taskServiceMock.batchUpdate).toHaveBeenCalledWith(1, expect.objectContaining({
            expected_revision: 12,
            tasks: [expect.objectContaining({ task_id: 1, update: { assignee_id: 30, status: 'active' } })],
        })));
        expect(teamServiceMock.create).toHaveBeenCalledWith(1, expect.objectContaining({ profile_id: 900, name: 'Casey' }), { 1: 11 });
    });

    it('still shows the picker when the iteration has no team, with a link to set one up', async () => {
        teamServiceMock.getByIteration.mockResolvedValue([]);
        teamServiceMock.getProfiles.mockResolvedValue([{ id: 900, display_name: 'Casey', profile_kind: 'human' }]);
        const { user } = renderBoard();

        await openDrop('planned-assigned', user);

        expect(await screen.findByRole('dialog', { name: 'Choose an assignee' })).toBeVisible();
        expect(await screen.findByRole('option', { name: 'Casey · Add to iteration and assign' })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Add team member' })).toHaveAttribute('href', '/plan?step=team&iteration=1');
        expect(taskServiceMock.update).not.toHaveBeenCalled();
        expect(taskServiceMock.changeStatus).not.toHaveBeenCalled();
    });
});
