import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { Iteration } from '../../types/iteration';
import type { TeamMember } from '../../types/team';
import { PlanQuickAddCapacity } from './PlanQuickAddCapacity';

const team = vi.hoisted(() => ({ getProfiles: vi.fn(), create: vi.fn(), getByIteration: vi.fn() }));
const planning = vi.hoisted(() => ({ readInitial: vi.fn() }));
vi.mock('../../services/teamService', () => ({ teamService: team }));
vi.mock('../../services/planningInputService', () => ({ planningInputService: planning }));
const iteration = { id: 4, name: 'Iteration 4' } as Iteration;

beforeEach(() => {
    vi.clearAllMocks();
    team.getProfiles.mockResolvedValue([
        { id: 1, display_name: 'Sam', profile_kind: 'human' },
        { id: 2, display_name: 'Build agent', profile_kind: 'agent' },
    ]);
    planning.readInitial.mockResolvedValue({ expected_revisions: { 4: 3 } });
    team.create.mockResolvedValue({ id: 9, profile_id: 2 });
    team.getByIteration.mockResolvedValue([]);
});

describe('adding capacity from the plan', () => {
    it('excludes existing members and adds an agent without meeting overhead', async () => {
        const { user } = renderWithProviders(<PlanQuickAddCapacity iteration={iteration} members={[{ id: 5, profile_id: 1 } as TeamMember]} />);
        await user.click(screen.getByRole('button', { name: 'Add capacity' }));
        expect(await screen.findByRole('checkbox', { name: /Build agent/ })).toBeVisible();
        expect(screen.queryByRole('checkbox', { name: /Sam/ })).not.toBeInTheDocument();
        await user.click(screen.getByRole('checkbox', { name: /Build agent/ }));
        await user.click(screen.getByRole('button', { name: 'Add selected' }));
        await waitFor(() => expect(team.create).toHaveBeenCalledWith(4, expect.objectContaining({ profile_id: 2, operational_utilization: 0 }), { 4: 3 }));
        expect(planning.readInitial).toHaveBeenCalledWith('member', 4, true, expect.objectContaining({ profile_id: 2 }));
    });

    it('retries remaining selections after a partial failure without adding a duplicate', async () => {
        const saved: TeamMember[] = [];
        team.getByIteration.mockImplementation(async () => [...saved]);
        team.create.mockImplementationOnce(async () => { const row = { id: 9, profile_id: 1 } as TeamMember; saved.push(row); return row; })
            .mockRejectedValueOnce(new Error('Connection interrupted'))
            .mockResolvedValue({ id: 10, profile_id: 2 });
        const { user } = renderWithProviders(<PlanQuickAddCapacity iteration={iteration} members={[]} />);
        await user.click(screen.getByRole('button', { name: 'Add capacity' }));
        await user.click(await screen.findByRole('checkbox', { name: /Sam/ }));
        await user.click(screen.getByRole('checkbox', { name: /Build agent/ }));
        await user.click(screen.getByRole('button', { name: 'Add selected' }));
        expect(await screen.findByRole('alert')).toHaveTextContent('Some capacity rows could not be added. Retry to add the remaining selections.');
        await user.click(screen.getByRole('button', { name: 'Add selected' }));
        await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
        expect(team.create.mock.calls.map(call => call[1].profile_id)).toEqual([1, 2, 2]);
    });
});
