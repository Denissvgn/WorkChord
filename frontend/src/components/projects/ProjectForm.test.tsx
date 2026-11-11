import { describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { AxiosError } from 'axios';
import { renderWithProviders } from '../../test/renderWithProviders';
import { ProjectForm } from './ProjectForm';
import type { Project } from '../../types/project';

const projects = vi.hoisted(() => ({ getInitiatives: vi.fn(), create: vi.fn(), update: vi.fn() }));
vi.mock('../../services/projectService', () => ({ projectService: projects }));
vi.mock('../../services/teamService', () => ({ teamService: { getProfiles: vi.fn().mockResolvedValue([{ id: 5, display_name: 'Priya Nair', profile_kind: 'human' }]) } }));
vi.mock('../../services/templateService', () => ({ templateService: { getAll: vi.fn().mockResolvedValue([]) } }));
const planning = vi.hoisted(() => ({ readInitial: vi.fn() }));
vi.mock('../../services/planningInputService', () => ({ planningInputService: planning }));

const project = { id: 3, name: 'Calendar import', description: '', status: 'active', health: 'on_track', owner_id: null, owner: null, owner_profile_id: null,
    owner_profile: null, initiative_id: null, initiative: null, start_date: null, target_date: null, completed_at: null, sort_order: 10,
    created_at: '2026-11-01T00:00:00Z', updated_at: '2026-11-01T00:00:00Z' } as unknown as Project;

describe('ProjectForm', () => {
    it('shows dates and owner without expanding anything', async () => {
        projects.getInitiatives.mockResolvedValue([]);
        renderWithProviders(<ProjectForm onSuccess={vi.fn()} onCancel={vi.fn()} />);
        expect(await screen.findByLabelText('Start date')).toBeVisible();
        expect(screen.getByLabelText('Target date')).toBeVisible();
        expect(screen.getByRole('combobox', { name: 'Owner' })).toBeVisible();
    });

    it('shows the revision controls only after a save meets a newer version', async () => {
        projects.getInitiatives.mockResolvedValue([]);
        planning.readInitial.mockResolvedValue({ resource: project, resource_id: 3, expected_revisions: { 3: 2 }, complete: true });
        projects.update.mockRejectedValue(new AxiosError('Conflict', '409', undefined, undefined, { status: 409, data: { detail: 'Project changed.' } } as never));
        const { user } = renderWithProviders(<ProjectForm initialData={project} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        const save = await screen.findByRole('button', { name: /Update project/ });
        expect(screen.queryByText(/Someone changed this project/)).toBeNull();
        await user.click(save);
        expect(await screen.findByText(/Someone changed this project/)).toBeInTheDocument();
    });
});
