import { describe, expect, it, vi } from 'vitest';
import { fireEvent, screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TaskRow } from './TaskRow';

import { Button } from '../../components/common/Button';
describe('TaskRow', () => {
    it('shows the agent status on a line under the assignee name and the Reviewer beside it', () => {
        renderWithProviders(
            <TaskRow id={1} title="Task 1" status="resolved" assignee={{ id: 6, name: 'Build agent' }}
                assigneeOptions={[{ id: 6, name: 'Build agent', kind: 'agent' }]} onAssign={vi.fn()} onOpen={vi.fn()} menuItems={[]}
                dispatch="waitingForReview" reviewer={{ name: 'Review bot' }} />,
        );
        const row = screen.getByRole('button', { name: 'Task 1' }).closest<HTMLElement>('[data-task-row]')!;
        const picker = screen.getByRole('combobox', { name: 'Assignee: Task 1' });
        const line = row.querySelector<HTMLElement>('[data-agent-dispatch]')!;
        expect(line).toHaveTextContent('Agent status: Waiting for review');
        // The cell stacks two lines: the name line with the picker, then the status line under it.
        const cell = row.querySelector<HTMLElement>('[data-assignee-cell]')!;
        expect(cell).toHaveClass('flex-col');
        expect(Array.from(cell.children)).toEqual([picker.parentElement, line]);
        // Full text stays in the tooltips; the visible text truncates.
        expect(line).toHaveClass('truncate');
        expect(line).toHaveAttribute('title', 'Waiting for review');
        expect(picker).toHaveAttribute('title', 'Build agent');
        expect(row.textContent!.indexOf('Waiting for review')).toBeLessThan(row.textContent!.indexOf('Reviewer: Review bot'));
        // The status adds nothing to reach by keyboard.
        expect(row.querySelectorAll('button, select, input')).toHaveLength(2);
    });

    it('keeps every row at 44 px, with the two-line assignee cell of an agent or the one line of a person', () => {
        const { rerender } = renderWithProviders(
            <TaskRow id={1} title="Task 1" status="planned" assignee={{ id: 6, name: 'Build agent' }}
                assigneeOptions={[{ id: 6, name: 'Build agent', kind: 'agent' }]} onAssign={vi.fn()} onOpen={vi.fn()} menuItems={[]}
                dispatch="noAgentConnected" reviewer={null} />,
        );
        const rowOf = () => screen.getByRole('button', { name: 'Task 1' }).closest<HTMLElement>('[data-task-row]')!;
        // A fixed height, not a minimum, so nothing in the row can grow it past what the virtualized list measures.
        expect(rowOf()).toHaveClass('h-11');
        expect(rowOf().className).not.toMatch(/\bmin-h-/);
        const cell = rowOf().querySelector<HTMLElement>('[data-assignee-cell]')!;
        const [nameLine, statusLine] = Array.from(cell.children) as HTMLElement[];
        // 16 px for the name and 14 px for the status in the small text token: 30 px inside the 44 px row.
        expect(nameLine).toHaveClass('h-4');
        expect(screen.getByRole('combobox', { name: 'Assignee: Task 1' })).toHaveClass('h-4', 'leading-4', 'py-0');
        expect(statusLine).toHaveClass('h-3.5', 'text-wc-micro');
        // No vertical padding or margin adds to the two lines.
        for (const element of [cell, nameLine, statusLine]) expect(element.className).not.toMatch(/\b(?:p[ytb]|m[ytb])-(?!0\b)/);

        rerender(<TaskRow id={1} title="Task 1" status="planned" assignee={{ id: 5, name: 'Ada' }} onOpen={vi.fn()} menuItems={[]} />);
        expect(rowOf()).toHaveClass('h-11');
        expect(rowOf().querySelector('[data-agent-dispatch]')).toBeNull();
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
            <TaskRow id={1} title="Task 1" status="planned" onOpen={vi.fn()} menuItems={[]}
                onToggleSelect={vi.fn()} selectDisabledReason="Another iteration" />,
        );
        const box = screen.getByRole('checkbox', { name: 'Select: Task 1' });
        expect(box).toBeDisabled();
        expect(box).toHaveAttribute('title', 'Another iteration');
    });

    it('shows a checkbox that is off, with the reason as its description, on a row that cannot be selected at all', () => {
        renderWithProviders(
            <TaskRow id={1} title="Task 1" status="planned" onOpen={vi.fn()} menuItems={[]} selectDisabledReason="Select its subtasks instead." />,
        );
        const box = screen.getByRole('checkbox', { name: 'Select: Task 1' });
        expect(box).toBeDisabled();
        expect(box).not.toBeChecked();
        expect(box).toHaveAccessibleDescription('Select its subtasks instead.');
        // The slot carries the tooltip too, because a disabled control gets no pointer events.
        expect(box.parentElement).toHaveAttribute('title', 'Select its subtasks instead.');
    });

    it('leaves the slot empty only when there is neither a toggle nor a reason', () => {
        renderWithProviders(<TaskRow id={1} title="Task 1" status="planned" onOpen={vi.fn()} menuItems={[]} />);
        expect(screen.queryByRole('checkbox')).toBeNull();
    });

    it('shows the checkbox on every row at rest, but the menu only on hover and focus', () => {
        renderWithProviders(
            <TaskRow id={1} title="Task 1" status="planned" assignee={{ id: 5, name: 'Ada' }} onAssign={vi.fn()} onStatusChange={vi.fn()}
                onOpen={vi.fn()} menuItems={[{ label: 'Details', onSelect: vi.fn() }]} onToggleSelect={vi.fn()} />,
        );
        const row = screen.getByRole('button', { name: 'Task 1' }).closest<HTMLElement>('[data-task-row]')!;
        expect(screen.getByRole('checkbox', { name: 'Select: Task 1' })).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Actions for Task 1' })).toBeNull();
        // Checkbox, status, title and assignee: four parts on an untouched row.
        expect(row.querySelectorAll('button, a[href], input, select, textarea, [tabindex]:not([tabindex="-1"])')).toHaveLength(4);
        fireEvent.mouseOver(row);
        expect(screen.getByRole('button', { name: 'Actions for Task 1' })).toBeInTheDocument();
        fireEvent.mouseOut(row);
        expect(screen.queryByRole('button', { name: 'Actions for Task 1' })).toBeNull();
        expect(screen.getByRole('checkbox', { name: 'Select: Task 1' })).toBeInTheDocument();
    });

    it('shows the drag handle on hover and focus in a slot that keeps its width, and keeps it while the row is dragged', () => {
        const props = {
            id: 1, title: 'Task 1', status: 'planned' as const, assignee: { id: 5, name: 'Ada' }, onAssign: vi.fn(), onStatusChange: vi.fn(),
            onOpen: vi.fn(), menuItems: [{ label: 'Details', onSelect: vi.fn() }], onToggleSelect: vi.fn(),
            handle: <Button type="button" variant="secondary">Drag: Task 1</Button>,
        };
        const { rerender } = renderWithProviders(<TaskRow {...props} />);
        const row = screen.getByRole('button', { name: 'Task 1' }).closest<HTMLElement>('[data-task-row]')!;
        const slot = row.querySelector<HTMLElement>('[data-drag-slot]')!;
        expect(slot).toHaveClass('w-6', 'shrink-0');
        expect(screen.queryByRole('button', { name: 'Drag: Task 1' })).toBeNull();
        // Checkbox, status, title and assignee: still four parts with a handle slot and an active selection.
        expect(row.querySelectorAll('button, a[href], input, select, textarea, [tabindex]:not([tabindex="-1"])')).toHaveLength(4);
        fireEvent.mouseOver(row);
        expect(screen.getByRole('button', { name: 'Drag: Task 1' })).toBeInTheDocument();
        fireEvent.mouseOut(row);
        expect(screen.queryByRole('button', { name: 'Drag: Task 1' })).toBeNull();
        fireEvent.focus(screen.getByRole('button', { name: 'Task 1' }));
        expect(screen.getByRole('button', { name: 'Drag: Task 1' })).toBeInTheDocument();
        fireEvent.blur(screen.getByRole('button', { name: 'Task 1' }));
        expect(screen.queryByRole('button', { name: 'Drag: Task 1' })).toBeNull();
        rerender(<TaskRow {...props} revealed />);
        expect(screen.getByRole('button', { name: 'Drag: Task 1' })).toBeInTheDocument();
    });
});
