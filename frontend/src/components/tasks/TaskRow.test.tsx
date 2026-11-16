import { describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TaskRow } from './TaskRow';

describe('TaskRow', () => {
    it('leaves room right after the assignee for what a later view adds to it', () => {
        renderWithProviders(
            <TaskRow id={1} title="Task 1" status="planned" assignee={{ id: 5, name: 'Ada' }} onOpen={vi.fn()} menuItems={[]}
                afterAssignee={<span data-testid="dispatch-state">Working</span>} />,
        );
        const row = screen.getByRole('button', { name: 'Task 1' }).closest<HTMLElement>('[data-task-row]')!;
        const slot = screen.getByTestId('dispatch-state');
        expect(row).toContainElement(slot);
        expect(row.textContent!.indexOf('Ada')).toBeLessThan(row.textContent!.indexOf('Working'));
    });

    it('shows a checkbox that cannot be ticked, with the reason, when the row cannot join the selection', () => {
        renderWithProviders(
            <TaskRow id={1} title="Task 1" status="planned" onOpen={vi.fn()} menuItems={[]} selectionActive
                onToggleSelect={vi.fn()} selectDisabledReason="Another iteration" />,
        );
        const box = screen.getByRole('checkbox', { name: 'Select: Task 1' });
        expect(box).toBeDisabled();
        expect(box).toHaveAttribute('title', 'Another iteration');
    });
});
