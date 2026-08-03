import { describe, expect, it } from 'vitest';
import type { Task, TaskStatus } from '../types/task';
import { selectWorkNowTasks } from '../utils/selectWorkNowTasks';

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
} as Task);

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
