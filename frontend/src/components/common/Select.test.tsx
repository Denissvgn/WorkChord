import { describe, expect, it, vi } from 'vitest';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { Select } from './Select';
import { Textarea } from './Textarea';
import { SegmentedControl } from '../ui/SegmentedControl';

describe('shared form parts', () => {
    it('labels a select and describes its help and error', () => {
        render(<Select label="Status" help="Where the work stands" error="Pick a status" required><option>Active</option></Select>);
        const select = screen.getByRole('combobox', { name: /Status/ });
        expect(select).toBeRequired();
        expect(select).toHaveAttribute('aria-invalid', 'true');
        expect(select).toHaveAccessibleDescription('Where the work stands Pick a status');
    });

    it('labels a textarea the same way', () => {
        render(<Textarea label="Description" help="Optional" />);
        expect(screen.getByRole('textbox', { name: 'Description' })).toHaveAccessibleDescription('Optional');
    });

    it('marks the chosen segment as pressed and reports a new choice', async () => {
        const onChange = vi.fn();
        render(<SegmentedControl label="View" value="list" onChange={onChange}
            options={[{ value: 'list', label: 'List' }, { value: 'board', label: 'Board' }]} />);
        expect(screen.getByRole('group', { name: 'View' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'List' })).toHaveAttribute('aria-pressed', 'true');
        expect(screen.getByRole('button', { name: 'Board' })).toHaveAttribute('aria-pressed', 'false');
        await userEvent.click(screen.getByRole('button', { name: 'Board' }));
        expect(onChange).toHaveBeenCalledWith('board');
    });
});
