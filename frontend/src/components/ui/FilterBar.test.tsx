import { describe, expect, it } from 'vitest';
import { useState } from 'react';
import { screen, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { FilterBar, type FilterBarFilter } from './FilterBar';

const tasks = [
    { id: 1, title: 'Write spec', status: 'active', owner: 'ana', team: 'core', label: 'docs', size: 's', risk: 'low' },
    { id: 2, title: 'Fix login', status: 'planned', owner: 'ana', team: 'core', label: 'bug', size: 'm', risk: 'low' },
    { id: 3, title: 'Ship build', status: 'active', owner: 'ben', team: 'ops', label: 'bug', size: 'l', risk: 'high' },
];

const definitions = [
    { id: 'status', label: 'Status', options: [{ value: 'active', label: 'Active' }, { value: 'planned', label: 'Planned' }] },
    { id: 'owner', label: 'Owner', options: [{ value: 'ana', label: 'Ana' }, { value: 'ben', label: 'Ben' }] },
    { id: 'team', label: 'Team', options: [{ value: 'core', label: 'Core' }, { value: 'ops', label: 'Ops' }] },
    { id: 'label', label: 'Label', options: [{ value: 'bug', label: 'Bug' }, { value: 'docs', label: 'Docs' }] },
    { id: 'size', label: 'Size', options: [{ value: 's', label: 'Small' }, { value: 'm', label: 'Medium' }] },
    { id: 'risk', label: 'Risk', options: [{ value: 'low', label: 'Low' }, { value: 'high', label: 'High' }] },
] as const;

const Harness = ({ initial = {} }: { initial?: Record<string, string> }) => {
    const [values, setValues] = useState<Record<string, string>>(initial);
    const filters: FilterBarFilter[] = definitions.map(definition => ({
        id: definition.id,
        label: definition.label,
        options: [...definition.options],
        value: values[definition.id] ?? '',
    }));
    const visible = tasks.filter(task => filters.every(filter => !filter.value || String(task[filter.id as keyof typeof task]) === filter.value));
    return (
        <>
            <FilterBar
                filters={filters}
                onChange={(id, value) => setValues(current => ({ ...current, [id]: value }))}
                onClear={() => setValues({})}
            />
            <ul aria-label="Results">
                {visible.map(task => <li key={task.id}>{task.title}</li>)}
            </ul>
        </>
    );
};

describe('FilterBar', () => {
    it('shows five quick filters and puts the rest under More filters', async () => {
        const { user } = renderWithProviders(<Harness />);

        for (const name of ['Status', 'Owner', 'Team', 'Label', 'Size']) {
            expect(screen.getByRole('combobox', { name })).toBeInTheDocument();
        }
        expect(screen.queryByRole('combobox', { name: 'Risk' })).not.toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: /More filters/ }));
        const panel = screen.getByRole('dialog', { name: 'More filters' });
        expect(within(panel).getByRole('combobox', { name: 'Risk' })).toBeInTheDocument();

        await user.keyboard('{Escape}');
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
        expect(screen.getByRole('button', { name: /More filters/ })).toHaveFocus();
    });

    it('shows one removable chip per active condition and returns the default list after the last one is removed', async () => {
        const { user } = renderWithProviders(<Harness />);
        expect(screen.getAllByRole('listitem')).toHaveLength(3);
        expect(screen.queryByRole('list', { name: 'Active filters' })).not.toBeInTheDocument();

        await user.selectOptions(screen.getByRole('combobox', { name: 'Status' }), 'active');
        await user.selectOptions(screen.getByRole('combobox', { name: 'Owner' }), 'ana');

        const chips = screen.getByRole('list', { name: 'Active filters' });
        expect(within(chips).getByText('Status: Active')).toBeInTheDocument();
        expect(within(chips).getByText('Owner: Ana')).toBeInTheDocument();
        expect(within(chips).getAllByRole('button', { name: /Remove filter/ })).toHaveLength(2);
        expect(within(screen.getByRole('list', { name: 'Results' })).getAllByRole('listitem')).toHaveLength(1);

        await user.click(screen.getByRole('button', { name: 'Remove filter Status: Active' }));
        expect(screen.queryByText('Status: Active')).not.toBeInTheDocument();
        expect(screen.getByRole('combobox', { name: 'Status' })).toHaveValue('');
        expect(within(screen.getByRole('list', { name: 'Results' })).getAllByRole('listitem')).toHaveLength(2);

        await user.click(screen.getByRole('button', { name: 'Remove filter Owner: Ana' }));
        expect(screen.queryByRole('list', { name: 'Active filters' })).not.toBeInTheDocument();
        expect(within(screen.getByRole('list', { name: 'Results' })).getAllByRole('listitem')).toHaveLength(3);
    });

    it('clears every condition at once, including one set under More filters', async () => {
        const { user } = renderWithProviders(<Harness initial={{ status: 'planned', risk: 'low' }} />);

        const chips = screen.getByRole('list', { name: 'Active filters' });
        expect(within(chips).getByText('Risk: Low')).toBeInTheDocument();
        expect(within(screen.getByRole('list', { name: 'Results' })).getAllByRole('listitem')).toHaveLength(1);

        await user.click(within(chips).getByRole('button', { name: 'Clear' }));
        expect(screen.queryByRole('list', { name: 'Active filters' })).not.toBeInTheDocument();
        expect(within(screen.getByRole('list', { name: 'Results' })).getAllByRole('listitem')).toHaveLength(3);
    });
});
