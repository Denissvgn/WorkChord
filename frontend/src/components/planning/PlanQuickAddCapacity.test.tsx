import { describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { Iteration } from '../../types/iteration';
import type { TeamMember } from '../../types/team';
import { PlanQuickAddCapacity } from './PlanQuickAddCapacity';

const team = vi.hoisted(() => ({ getProfiles: vi.fn(), create: vi.fn() }));
const planning = vi.hoisted(() => ({ readInitial: vi.fn() }));
vi.mock('../../services/teamService', () => ({ teamService: team }));
vi.mock('../../services/planningInputService', () => ({ planningInputService: planning }));

const iteration = { id: 4, name: 'Sprint 4' } as Iteration;

describe('adding capacity from the plan', () => {
    it('adds an agent profile without leaving the page, with no meeting overhead', async () => {
        team.getProfiles.mockResolvedValue([
            { id: 1, display_name: 'Sam', profile_kind: 'human' },
            { id: 2, display_name: 'Build agent', profile_kind: 'agent' },
        ]);
        planning.readInitial.mockResolvedValue({ expected_revisions: { 4: 3 } });
        team.create.mockResolvedValue({ id: 9 });
        const { user } = renderWithProviders(<PlanQuickAddCapacity iteration={iteration}
            members={[{ id: 5, profile_id: 1 } as TeamMember]} />);
        const select = await screen.findByRole('combobox', { name: 'Profile' });
        expect(screen.queryByRole('option', { name: 'Sam' })).not.toBeInTheDocument();
        await user.selectOptions(select, '2');
        await user.click(screen.getByRole('button', { name: 'Add capacity' }));
        await waitFor(() => expect(team.create).toHaveBeenCalled());
        expect(planning.readInitial).toHaveBeenCalledWith('member', 4, true, { profile_id: 2 });
        expect(team.create).toHaveBeenCalledWith(4, expect.objectContaining({ profile_id: 2, operational_utilization: 0 }), { 4: 3 });
    });
});
