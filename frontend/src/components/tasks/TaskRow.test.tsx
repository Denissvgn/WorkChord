import { describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TaskRow } from './TaskRow';

describe('TaskRow', () => {
    it('shows the agent status line under the assignee and the Reviewer beside it', () => {
        renderWithProviders(
            <TaskRow id={1} title="Task 1" status="resolved" assignee={{ id: 6, name: 'Build agent' }}
                assigneeOptions={[{ id: 6, name: 'Build agent', kind: 'agent' }]} onAssign={vi.fn()} onOpen={vi.fn()} menuItems={[]}
                dispatch="waitingForReview" reviewer={{ name: 'Review bot' }} />,
        );
        const row = screen.getByRole('button', { name: 'Task 1' }).closest<HTMLElement>('[data-task-row]')!;
        const picker = screen.getByRole('combobox', { name: 'Assignee: Task 1' });
        const line = row.querySelector<HTMLElement>('[data-agent-dispatch]')!;
        expect(line).toHaveTextContent('Agent status: Waiting for review');
        // The line sits under the name, in the assignee cell, and the Reviewer follows that cell.
        expect(picker.closest('span.flex-col')).toContainElement(line);
        expect(row.textContent!.indexOf('Waiting for review')).toBeLessThan(row.textContent!.indexOf('Reviewer: Review bot'));
        // The row stays 44 px and the status line adds nothing to reach by keyboard.
        expect(row.className).toContain('min-h-11');
        expect(row.querySelectorAll('button, select, input')).toHaveLength(2);
    });

    it('names anyone as Reviewer when no reviewer agent holds the review, and keeps the cell empty before submission', () => {
        const { rerender } = renderWithProviders(
            <TaskRow id={1} title="Task 1" status="resolved" assignee={{ id: 5, name: 'Ada' }} onOpen={vi.fn()} menuItems={[]} reviewer={{ name: null }} />,
        );
        expect(screen.getByText('Reviewer: anyone')).toHaveAttribute('title', 'Any authorized person reviews; no reviewer agent is assigned');
        rerender(<TaskRow id={1} title="Task 1" status="planned" assignee={{ id: 5, name: 'Ada' }} onOpen={vi.fn()} menuItems={[]} reviewer={null} />);
        expect(screen.queryByText(/Reviewer/)).toBeNull();
        // A person has no status line.
        expect(document.querySelector('[data-agent-dispatch]')).toBeNull();
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
