import { describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { defaultFilters } from '../../utils/taskFilterDefaults';
import { TaskFiltersBar } from './TaskFiltersBar';

vi.mock('../../services/teamService', () => ({ teamService: { getByIteration: vi.fn().mockResolvedValue([{ id: 7, name: 'Ana' }]) } }));
vi.mock('../../services/projectService', () => ({ projectService: { getAll: vi.fn().mockResolvedValue([]) } }));
vi.mock('../../services/labelService', () => ({
    labelService: {
        getGroups: vi.fn().mockResolvedValue([{ key: 'area', name: 'Area', labels: [{ slug: 'backend', name: 'Backend' }, { slug: 'web', name: 'Web' }] }]),
    },
}));

describe('visible task filters', () => {
    it('shows a removable chip for every active condition, including dates and each label', async () => {
        const onFiltersChange = vi.fn();
        const { user } = renderWithProviders(<TaskFiltersBar iterationId={1} onFiltersChange={onFiltersChange}
            filters={{ ...defaultFilters, isBlocked: true, startDateFrom: '2026-01-05', labelSlugs: ['backend'], priority: 2, status: 'planned' }} />);
        const chips = screen.getByRole('list', { name: 'Active filters' });
        expect(await within(chips).findByText('Labels: Backend · Area')).toBeInTheDocument();
        for (const text of ['Blocked: Yes', 'Priority: 2', 'Status: Planned']) {
            expect(within(chips).getByText(text)).toBeInTheDocument();
        }
        expect(within(chips).getByText(/^Start from: /)).toBeInTheDocument();

        await user.click(within(chips).getByRole('button', { name: /^Remove filter Start from/ }));
        expect(onFiltersChange).toHaveBeenLastCalledWith(expect.objectContaining({ startDateFrom: '', labelSlugs: ['backend'] }));

        await user.click(within(chips).getByRole('button', { name: 'Remove filter Labels: Backend · Area' }));
        expect(onFiltersChange).toHaveBeenLastCalledWith(expect.objectContaining({ labelSlugs: [], isBlocked: true }));
    });

    it('keeps the most used conditions in the row and adds labels one at a time', async () => {
        const onFiltersChange = vi.fn();
        const { user } = renderWithProviders(<TaskFiltersBar iterationId={1} onFiltersChange={onFiltersChange}
            filters={{ ...defaultFilters, labelSlugs: ['backend'] }} />);
        for (const name of ['Assignee', 'Status', 'Blocked']) {
            expect(screen.getByRole('combobox', { name })).toBeInTheDocument();
        }
        expect(screen.queryByRole('combobox', { name: 'Planning readiness' })).not.toBeInTheDocument();
        expect(await screen.findByRole('option', { name: 'Ana' })).toBeInTheDocument();
        await user.selectOptions(screen.getByRole('combobox', { name: 'Assignee' }), 'Ana');
        expect(onFiltersChange).toHaveBeenLastCalledWith(expect.objectContaining({ assigneeId: 7 }));

        await user.click(screen.getByRole('button', { name: /More filters/ }));
        const panel = screen.getByRole('dialog', { name: 'More filters' });
        expect(within(panel).getByRole('combobox', { name: 'Planning readiness' })).toBeInTheDocument();
        const labels = within(panel).getByRole('combobox', { name: 'Labels' });
        expect(within(labels).queryByRole('option', { name: 'Backend · Area' })).not.toBeInTheDocument();
        await user.selectOptions(labels, 'Web · Area');
        expect(onFiltersChange).toHaveBeenLastCalledWith(expect.objectContaining({ labelSlugs: ['backend', 'web'] }));
    });
});
