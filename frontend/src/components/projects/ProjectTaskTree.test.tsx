import { describe, expect, it } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { ProjectTaskTree } from './ProjectTaskTree';
import type { Task } from '../../types/task';

const task = (id: number, overrides: Partial<Task> = {}): Task => ({
    id, iteration_id: 1, project_id: 1, parent_id: null, title: `Task ${id}`, priority: 2, effort_days: 3, effort_hours: 24,
    assignee: { id: 5, name: 'Ada' }, status: 'planned', is_overdue: false, is_delayed: false, is_composite: false, is_optional: false,
    is_deferred: false, tags: [], sort_order: id, external_links: [], request_count: 0, version: 1, children: [], dependencies: [],
    agent_readiness: { is_ready: true, blockers: [], warnings: [], criteria: [] }, ...overrides,
});

describe('ProjectTaskTree', () => {
    it('shows each task as the shared row: status, priority, title, state, assignee and effort', () => {
        renderWithProviders(<ProjectTaskTree tasks={[task(1, { children: [task(2, { parent_id: 1, status: 'resolved' })], is_composite: true })]} />);
        const parent = screen.getByRole('button', { name: 'Task 1' }).closest<HTMLElement>('[data-task-row]')!;
        const child = screen.getByRole('button', { name: 'Task 2' }).closest<HTMLElement>('[data-task-row]')!;
        expect(parent.className).toContain('min-h-11');
        expect(parent).toHaveTextContent('P2');
        expect(parent).toHaveTextContent('Ada');
        expect(child).toHaveTextContent('In review');
        expect(child.style.paddingLeft).toBe('32px');
    });
});
