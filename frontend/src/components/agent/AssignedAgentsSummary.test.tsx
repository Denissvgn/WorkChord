import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { AgentAssignmentReadItem } from '../../types/agent';
import { AssignedAgentsSummary } from './AssignedAgentsSummary';

const agentServiceMock = vi.hoisted(() => ({ listTaskAssignmentsAsPerson: vi.fn() }));
vi.mock('../../services/agentService', () => ({ agentService: agentServiceMock }));

const row = (overrides: Partial<AgentAssignmentReadItem> = {}): AgentAssignmentReadItem => ({
    id: 1, task_id: 42, actor_id: 3, actor: { id: 3, name: 'reviewer-1', display_name: null, role: 'verifier' },
    team_member_id: null, purpose: 'verification', queue_class: 'normal', state: 'queued', queue_rank: 1000,
    not_before: null, task_version: 1, model_binding_id: null, model_binding_revision: null,
    model_binding_status: 'not_selected', model_binding_stale_reasons: [], model: null,
    created_at: '2026-11-15T10:00:00Z', updated_at: '2026-11-15T10:00:00Z', ...overrides,
});

describe('assigned agents for a person', () => {
    beforeEach(() => { vi.resetAllMocks(); });

    it('names each agent, what it does, its state and a stale model binding', async () => {
        agentServiceMock.listTaskAssignmentsAsPerson.mockResolvedValue([
            row(),
            row({ id: 2, actor_id: 9, actor: null, purpose: 'execution', state: 'fulfilled', model_binding_status: 'stale',
                model: { model_catalog_key: 'fast', provider: 'configured', configured_model_alias: 'fast-code' } }),
        ]);
        renderWithProviders(<AssignedAgentsSummary taskId={42} />);
        expect(await screen.findByText('reviewer-1')).toBeInTheDocument();
        expect(screen.getByText(/Reviewing · Queued/)).toBeInTheDocument();
        expect(screen.getByText('Agent #9')).toBeInTheDocument();
        expect(screen.getByText(/Doing the work · Done/)).toBeInTheDocument();
        expect(screen.getByText(/Model: fast-code · Model binding is out of date/)).toBeInTheDocument();
    });

    it('says when no agent is assigned', async () => {
        agentServiceMock.listTaskAssignmentsAsPerson.mockResolvedValue([]);
        renderWithProviders(<AssignedAgentsSummary taskId={42} />);
        expect(await screen.findByText('No agent is assigned to this task.')).toBeInTheDocument();
    });

    it('keeps a failed read recoverable', async () => {
        // A refused read is not retried automatically, so the error and its retry show at once.
        agentServiceMock.listTaskAssignmentsAsPerson.mockRejectedValue({ isAxiosError: true, response: { status: 403, data: {} } });
        renderWithProviders(<AssignedAgentsSummary taskId={42} />);
        expect(await screen.findByRole('alert')).toBeInTheDocument();
        expect(agentServiceMock.listTaskAssignmentsAsPerson).toHaveBeenCalledTimes(1);
    });
});
