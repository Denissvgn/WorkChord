import { act, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { TeamMember, TeamMemberCreate } from '../../types/team';
import { TeamForm } from './TeamForm';

const planningMock = vi.hoisted(() => ({ readInitial: vi.fn() }));
vi.mock('../../services/planningInputService', () => ({ planningInputService: planningMock }));

const teamServiceMock = vi.hoisted(() => ({
    getProfiles: vi.fn(),
    create: vi.fn(),
    update: vi.fn(),
}));

vi.mock('../../services/teamService', () => ({
    teamService: teamServiceMock,
}));

const memberFixture = (overrides: Partial<TeamMember> = {}): TeamMember => ({
    id: 17,
    iteration_id: 9,
    profile_id: null,
    name: 'Ada Lovelace',
    position: 'Developer',
    email: '',
    availability_percent: 100,
    professionalism_coefficient: 1,
    operational_utilization: 20,
    profile: null,
    vacations: [],
    ...overrides,
});

const deferred = <T,>() => {
    let resolve!: (value: T) => void;
    const promise = new Promise<T>(next => {
        resolve = next;
    });
    return { promise, resolve };
};

describe('TeamForm', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        planningMock.readInitial.mockResolvedValue({ resource: memberFixture(), resource_id: 9, expected_revisions: { 9: 4, 10: 8 }, complete: true });
        teamServiceMock.getProfiles.mockResolvedValue([]);
        teamServiceMock.create.mockResolvedValue(memberFixture());
        teamServiceMock.update.mockResolvedValue(memberFixture());
    });

    it('keeps manual entry available when capability profiles fail to load', async () => {
        teamServiceMock.getProfiles.mockRejectedValueOnce(new Error('Profiles are offline'));
        const onSuccess = vi.fn();
        const { user } = renderWithProviders(
            <TeamForm
                iterationId={9}
                onSuccess={onSuccess}
                onCancel={vi.fn()}
            />,
        );

        expect(await screen.findByRole('alert')).toHaveTextContent(
            'Existing profiles could not be loaded. Retry, or enter person details manually below.',
        );
        expect(await screen.findByRole('combobox', { name: 'Existing profile' })).toBeDisabled();

        await user.type(await screen.findByRole('textbox', { name: 'Person' }), 'Grace Hopper');
        await user.click(screen.getByRole('button', { name: 'Add capacity' }));

        await waitFor(() => {
            expect(teamServiceMock.create).toHaveBeenCalledWith(9, {
                name: 'Grace Hopper',
                position: 'Developer',
                email: '',
                profile_id: null,
                availability_percent: 100,
                professionalism_coefficient: 1,
                operational_utilization: 20,
            } satisfies TeamMemberCreate, { 9: 4, 10: 8 });
        });
        expect(onSuccess).toHaveBeenCalledOnce();
    });

    it('reports dirty and pending state while freezing fields and cancel during submission', async () => {
        const createRequest = deferred<TeamMember>();
        teamServiceMock.create.mockReturnValueOnce(createRequest.promise);
        const onCancel = vi.fn();
        const onSuccess = vi.fn();
        const onStateChange = vi.fn();
        const { user } = renderWithProviders(
            <TeamForm
                iterationId={9}
                onSuccess={onSuccess}
                onCancel={onCancel}
                onStateChange={onStateChange}
            />,
        );

        const nameInput = await screen.findByRole('textbox', { name: 'Person' });
        await waitFor(() => {
            expect(onStateChange).toHaveBeenLastCalledWith({ dirty: false, pending: false });
        });

        await user.type(nameInput, 'Ada Lovelace');
        await waitFor(() => {
            expect(onStateChange).toHaveBeenLastCalledWith({ dirty: true, pending: false });
        });

        await user.click(screen.getByRole('button', { name: 'Add capacity' }));
        await waitFor(() => {
            expect(onStateChange).toHaveBeenLastCalledWith({ dirty: true, pending: true });
        });

        const cancelButton = screen.getByRole('button', { name: 'Cancel' });
        expect(nameInput).toBeDisabled();
        expect(screen.getByRole('textbox', { name: 'Iteration role' })).toBeDisabled();
        expect(cancelButton).toBeDisabled();
        await user.click(cancelButton);
        expect(onCancel).not.toHaveBeenCalled();

        await act(async () => {
            createRequest.resolve(memberFixture());
        });

        await waitFor(() => {
            expect(onSuccess).toHaveBeenCalledOnce();
            expect(onStateChange).toHaveBeenLastCalledWith({ dirty: true, pending: false });
        });
        expect(nameInput).toBeEnabled();
    });

    it('announces mutation failures while preserving the editable draft', async () => {
        teamServiceMock.create.mockRejectedValueOnce({
            response: {
                status: 400,
                data: { detail: 'This profile is already assigned.' },
            },
        });
        const { user } = renderWithProviders(
            <TeamForm
                iterationId={9}
                onSuccess={vi.fn()}
                onCancel={vi.fn()}
            />,
        );

        const nameInput = await screen.findByRole('textbox', { name: 'Person' });
        await user.type(nameInput, 'Duplicate Person');
        await user.click(screen.getByRole('button', { name: 'Add capacity' }));

        expect(await screen.findByRole('alert')).toHaveTextContent(
            'This profile is already assigned.',
        );
        expect(nameInput).toHaveValue('Duplicate Person');
        expect(nameInput).toBeEnabled();
    });

    it('starts a new agent capacity row with no overhead and says what its number means', async () => {
        teamServiceMock.getProfiles.mockResolvedValue([
            { id: 3, display_name: 'Build agent', profile_kind: 'agent', email: null, headline: null, skills: [] },
            { id: 4, display_name: 'Grace Hopper', profile_kind: 'human', email: null, headline: null, skills: [] },
        ]);
        const { user } = renderWithProviders(<TeamForm iterationId={9} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        const profile = await screen.findByRole('combobox', { name: 'Existing profile' });
        await waitFor(() => expect(profile).toBeEnabled());
        await user.selectOptions(profile, '3');
        expect(screen.getByText(/For an agent, capacity is the hours it can take work/)).toBeInTheDocument();
        expect(screen.getByRole('spinbutton', { name: /Overhead|Utilization/i })).toHaveValue(0);
        await user.selectOptions(profile, '4');
        expect(screen.getByRole('spinbutton', { name: /Overhead|Utilization/i })).toHaveValue(20);
        expect(screen.getByText(/working hours on the calendar/)).toBeInTheDocument();
    });
});
