import { describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { defaultFilters } from '../../utils/taskFilterDefaults';
import { TaskFiltersBar } from './TaskFiltersBar';

vi.mock('../../services/teamService', () => ({ teamService: { getByIteration: vi.fn().mockResolvedValue([]) } }));
vi.mock('../../services/projectService', () => ({ projectService: { getAll: vi.fn().mockResolvedValue([]) } }));
vi.mock('../../services/labelService', () => ({
    labelService: {
        getGroups: vi.fn().mockResolvedValue([{ key: 'area', name: 'Area', labels: [{ slug: 'backend', name: 'Backend' }] }]),
    },
}));

describe('visible task filters', () => {
    it('shows a removable chip for every active condition, including dates and labels', async () => {
        const onFiltersChange = vi.fn();
        const { user } = renderWithProviders(<TaskFiltersBar iterationId={1} onFiltersChange={onFiltersChange}
            filters={{ ...defaultFilters, isBlocked: true, startDateFrom: '2026-01-05', labelSlugs: ['backend'], priority: 2, status: 'planned' }} />);
        expect(await screen.findByRole('button', { name: 'Remove Labels filter' })).toBeInTheDocument();
        for (const label of ['Blocked', 'Start from', 'Priority', 'Status']) {
            expect(screen.getByRole('button', { name: `Remove ${label} filter` })).toBeInTheDocument();
        }
        expect(screen.queryByText(/more$/)).not.toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Remove Start from filter' }));
        expect(onFiltersChange).toHaveBeenCalledWith(expect.objectContaining({ startDateFrom: '', labelSlugs: ['backend'] }));
    });
});
