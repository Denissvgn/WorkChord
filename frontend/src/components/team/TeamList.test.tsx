import { describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TeamList } from './TeamList';
import { IterationCapacityLine } from '../iteration/IterationCapacityLine';
import type { TeamMember } from '../../types/team';

const team = vi.hoisted(() => ({ getByIteration: vi.fn(), getWorkload: vi.fn(), getCapacity: vi.fn() }));
vi.mock('../../services/teamService', () => ({ teamService: team }));
const iterations = vi.hoisted(() => ({ getPlanningReadiness: vi.fn() }));
vi.mock('../../services/iterationService', () => ({ iterationService: iterations }));

const member = (id: number, name: string): TeamMember => ({ id, iteration_id: 9, profile_id: null, name, position: 'Developer', email: '',
    availability_percent: 100, professionalism_coefficient: 1, operational_utilization: 20, profile: null, vacations: [] });
const workload = (id: number, capacity: number, planned: number) => ({ team_member_id: id, name: '', capacity_days: capacity / 8, allocated_days: planned / 8,
    free_days: (capacity - planned) / 8, workload_status: 'green', workload_percent: 0, capacity_hours: capacity, allocated_hours: planned,
    free_hours: capacity - planned, nominal_day_hours: 8 });

describe('capacity picture', () => {
    it('shows each person on one scale with hours, a team total, who is over, and the conversion once', async () => {
        team.getByIteration.mockResolvedValue([member(1, 'Ada'), member(2, 'Grace'), member(3, 'Linus')]);
        team.getWorkload.mockImplementation(async (id: number) => id === 1 ? workload(1, 64, 32) : id === 2 ? workload(2, 32, 40) : workload(3, 0, 6));
        renderWithProviders(<TeamList iterationId={9} onEdit={vi.fn()} />);
        expect(await screen.findByText('32 h of 64 h · 32 h free')).toBeInTheDocument();
        expect(screen.getByText('40 h of 32 h · 8 h over')).toBeInTheDocument();
        expect(screen.getByText(/Capacity unknown · 6 h planned/)).toBeInTheDocument();
        expect(await screen.findByText('78 h of 96 h')).toBeInTheDocument();
        expect(screen.getByText('1 person over capacity')).toBeInTheDocument();
        expect(screen.getByText('Hours throughout. One day is 8 h on these calendars.')).toBeInTheDocument();
    });

    it('labels an iteration card with planned hours against capacity, tasks and schedule state', async () => {
        iterations.getPlanningReadiness.mockResolvedValue({ iteration_id: 9, team_member_count: 2, team_capacity_hours: 160, planned_hours: 120,
            assigned_hours: 100, team_members_no_capacity: 0, task_count: 24, tasks_without_assignee: 2, tasks_without_effort: 0, has_schedule: false, risk_count: 0 });
        renderWithProviders(<IterationCapacityLine iterationId={9} />);
        expect(await screen.findByText('Planned 120 h of 160 h · 24 tasks · no schedule saved')).toBeInTheDocument();
    });
});
