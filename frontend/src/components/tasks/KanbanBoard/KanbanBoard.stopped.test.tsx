import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import type { ReactNode } from 'react';
import type { Task } from '../../../types/task';
import { renderWithProviders } from '../../../test/renderWithProviders';
import i18n, { ensureLanguageResources } from '../../../i18n/i18n';
import { defaultFilters } from '../../../utils/taskFilterDefaults';
import { KanbanBoard } from './KanbanBoard';

const taskServiceMock = vi.hoisted(() => ({ getByIteration: vi.fn(), update: vi.fn(), changeStatus: vi.fn(), batchUpdate: vi.fn() }));
vi.mock('@dnd-kit/core', () => ({
    DndContext: ({ children }: { children: ReactNode }) => <div>{children}</div>,
    DragOverlay: ({ children }: { children?: ReactNode }) => <>{children}</>,
    KeyboardSensor: class KeyboardSensor {},
    PointerSensor: class PointerSensor {},
    closestCorners: vi.fn(),
    defaultDropAnimationSideEffects: vi.fn(() => ({})),
    useSensor: vi.fn(() => ({})),
    useSensors: vi.fn(() => []),
}));
// A column lists the titles it holds, so what the board puts in each column can be read.
vi.mock('./KanbanColumn', () => ({
    KanbanColumn: ({ id, title, tasks }: { id: string; title: string; tasks: Task[] }) => (
        <section aria-label={`column ${id}`} data-title={title}><ul>{tasks.map(task => <li key={task.id}>{task.title}</li>)}</ul></section>
    ),
}));
vi.mock('./KanbanCard', () => ({ KanbanCard: () => null }));
vi.mock('../TaskEditorDrawer', () => ({ TaskEditorDrawer: ({ taskId }: { taskId: number | null }) => <div data-testid="drawer">{taskId}</div> }));
vi.mock('../../../services/taskService', () => ({ taskService: taskServiceMock }));
vi.mock('../../../services/teamService', () => ({ teamService: { getByIteration: vi.fn().mockResolvedValue([]) } }));
vi.mock('../../../services/planningInputService', () => ({ planningInputService: { readInitial: vi.fn() } }));
vi.mock('../../../services/labelService', () => ({ labelService: { getGroups: vi.fn().mockResolvedValue([]) } }));

const task = (id: number, title: string, overrides: Partial<Task> = {}): Task => ({
    id, iteration_id: 1, title, priority: 5, effort_days: 1, effort_hours: 8, status: 'planned', is_overdue: false, is_delayed: false,
    is_composite: false, is_optional: false, is_deferred: false, tags: [], sort_order: 0, external_links: [], request_count: 0,
    agent_readiness: { is_ready: true, blockers: [], warnings: [], criteria: [] }, version: 1, children: [], dependencies: [], ...overrides,
} as Task);

const tasks = [
    task(1, 'Planned work', { assignee: { id: 4, name: 'Ada' } }),
    task(2, 'Active work', { status: 'active' }),
    task(3, 'Paused work', { status: 'postponed', displayed_state: 'postponed' }),
    // A canceled task keeps the status it had; it must not be read as active.
    task(4, 'Dropped work', { status: 'active', displayed_state: 'canceled', canceled_at: '2026-11-20T00:00:00Z' }),
    task(5, 'Replaced work', { status: 'planned', displayed_state: 'superseded', successor_task_id: 9, successor_kind: 'supersession' }),
];

const columnTitles = (id: string) => within(screen.getByRole('region', { name: `column ${id}` })).queryAllByRole('listitem').map(item => item.textContent);

beforeEach(async () => {
    taskServiceMock.getByIteration.mockReset();
    taskServiceMock.getByIteration.mockResolvedValue(tasks);
    await ensureLanguageResources('en');
    await i18n.changeLanguage('en');
});

describe('Board lanes for stopped work', () => {
    it('keeps postponed, canceled and superseded work out of every active column', async () => {
        renderWithProviders(<KanbanBoard iterationId={1} />);
        await screen.findByRole('region', { name: 'column active' });
        expect(columnTitles('planned-assigned')).toEqual(['Planned work']);
        expect(columnTitles('planned-unassigned')).toEqual([]);
        // The canceled task stored as active is not in the Active column.
        expect(columnTitles('active')).toEqual(['Active work']);
        for (const column of ['planned-unassigned', 'planned-assigned', 'active', 'resolved', 'closed']) {
            expect(columnTitles(column)).not.toContain('Paused work');
            expect(columnTitles(column)).not.toContain('Dropped work');
            expect(columnTitles(column)).not.toContain('Replaced work');
        }
    });

    it('gives postponed work its own collapsed lane that opens from the keyboard', async () => {
        const { user } = renderWithProviders(<KanbanBoard iterationId={1} />);
        const toggle = await screen.findByRole('button', { name: /^Postponed\s*1$/ });
        expect(toggle).toHaveAttribute('aria-expanded', 'false');
        expect(screen.getByText('Paused work')).not.toBeVisible();
        toggle.focus();
        await user.keyboard('{Enter}');
        expect(toggle).toHaveAttribute('aria-expanded', 'true');
        const lane = screen.getByRole('region', { name: /Postponed/ });
        expect(within(lane).getByText('Paused work')).toBeVisible();
        // The state is written out, not only coloured.
        expect(within(lane).getByText('Postponed', { selector: '[data-task-state]' })).toBeVisible();
    });

    it('lists canceled and superseded work apart, with a link to the successor', async () => {
        const { user } = renderWithProviders(<KanbanBoard iterationId={1} />);
        await user.click(await screen.findByRole('button', { name: /^Canceled and superseded\s*2$/ }));
        const lane = screen.getByRole('region', { name: /Canceled and superseded/ });
        expect(within(lane).getByText('Canceled', { selector: '[data-task-state]' })).toBeVisible();
        expect(within(lane).getByText('Superseded', { selector: '[data-task-state]' })).toBeVisible();
        await user.click(within(lane).getByRole('button', { name: 'Superseded by #9' }));
        expect(screen.getByTestId('drawer')).toHaveTextContent('9');
    });

    it('opens the lane that a state filter asks for', async () => {
        renderWithProviders(<KanbanBoard iterationId={1} filters={{ ...defaultFilters, status: 'postponed' }} />);
        expect(await screen.findByRole('button', { name: /^Postponed\s*1$/ })).toHaveAttribute('aria-expanded', 'true');
    });

    it('names the lanes in Russian', async () => {
        await ensureLanguageResources('ru');
        await i18n.changeLanguage('ru');
        renderWithProviders(<KanbanBoard iterationId={1} />);
        expect(await screen.findByRole('button', { name: /^Отложено\s*1$/ })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: /^Отменено и заменено\s*2$/ })).toBeInTheDocument();
    });
});
