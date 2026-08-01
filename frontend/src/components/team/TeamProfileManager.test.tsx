import { screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type {
    TeamMemberProfile,
    TeamMemberProfileCreate,
    TeamMemberProfileUpdate,
} from '../../types/team';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TeamProfileManager } from './TeamProfileManager';

const teamServiceMock = vi.hoisted(() => ({
    getProfiles: vi.fn(),
    createProfile: vi.fn(),
    updateProfile: vi.fn(),
    deleteProfile: vi.fn(),
    createProfileSkill: vi.fn(),
    updateProfileSkill: vi.fn(),
    deleteProfileSkill: vi.fn(),
}));

vi.mock('../../services/teamService', () => ({
    teamService: teamServiceMock,
}));

const profileFixture = (
    overrides: Partial<TeamMemberProfile> = {},
): TeamMemberProfile => ({
    id: 42,
    seed_key: 'frontend-worker',
    display_name: 'Frontend Worker',
    email: null,
    headline: 'React implementation worker',
    summary: null,
    notes: null,
    automation_enabled: true,
    profile_kind: 'agent',
    assignment_modes: ['execution'],
    skills: [],
    created_at: '2026-07-28T10:00:00Z',
    updated_at: '2026-07-28T10:00:00Z',
    ...overrides,
});

describe('TeamProfileManager profile parity', () => {
    beforeEach(() => {
        teamServiceMock.getProfiles.mockResolvedValue([]);
        teamServiceMock.createProfile.mockImplementation(
            async (data: TeamMemberProfileCreate) => profileFixture({
                id: 101,
                ...data,
            }),
        );
        teamServiceMock.updateProfile.mockImplementation(
            async (_profileId: number, data: TeamMemberProfileUpdate) => profileFixture(data),
        );
    });

    it('round-trips seed key, profile kind, and assignment modes in create payloads', async () => {
        const { user } = renderWithProviders(<TeamProfileManager />);

        await screen.findByText('No capability profiles yet.');
        await user.type(screen.getByRole('textbox', { name: 'Seed key' }), 'frontend-specialist');
        await user.type(screen.getByRole('textbox', { name: 'Display name' }), 'Frontend Specialist');
        await user.selectOptions(screen.getByRole('combobox', { name: 'Profile kind' }), 'agent');
        await user.click(screen.getByRole('checkbox', { name: 'Execution' }));
        await user.click(screen.getByRole('checkbox', { name: 'Verification' }));
        await user.click(screen.getByRole('button', { name: 'Create' }));

        await waitFor(() => {
            expect(teamServiceMock.createProfile).toHaveBeenCalledWith({
                seed_key: 'frontend-specialist',
                display_name: 'Frontend Specialist',
                email: null,
                headline: null,
                summary: null,
                notes: null,
                automation_enabled: true,
                profile_kind: 'agent',
                assignment_modes: ['execution', 'verification'],
            });
        });
    });

    it('omits immutable seed key from updates while preserving kind and modes', async () => {
        const existingProfile = profileFixture({
            seed_key: 'immutable-hybrid',
            profile_kind: 'hybrid',
            assignment_modes: ['execution', 'verification'],
        });
        teamServiceMock.getProfiles.mockResolvedValue([existingProfile]);
        teamServiceMock.updateProfile.mockResolvedValue(existingProfile);

        const { user } = renderWithProviders(<TeamProfileManager />);

        await screen.findByTestId('profile-card');
        await user.click(screen.getByRole('button', { name: 'Edit' }));

        expect(screen.getByRole('textbox', { name: 'Seed key' })).toHaveAttribute('readonly');
        expect(screen.getByRole('combobox', { name: 'Profile kind' })).toHaveValue('hybrid');
        expect(screen.getByRole('checkbox', { name: 'Execution' })).toBeChecked();
        expect(screen.getByRole('checkbox', { name: 'Verification' })).toBeChecked();

        await user.click(screen.getByRole('button', { name: 'Save' }));

        await waitFor(() => {
            expect(teamServiceMock.updateProfile).toHaveBeenCalledTimes(1);
        });
        const [profileId, payload] = teamServiceMock.updateProfile.mock.calls[0] as [
            number,
            TeamMemberProfileUpdate,
        ];
        expect(profileId).toBe(existingProfile.id);
        expect(payload).toEqual({
            display_name: existingProfile.display_name,
            email: existingProfile.email,
            headline: existingProfile.headline,
            summary: existingProfile.summary,
            notes: existingProfile.notes,
            automation_enabled: true,
            profile_kind: 'hybrid',
            assignment_modes: ['execution', 'verification'],
        });
        expect(payload).not.toHaveProperty('seed_key');
    });

    it('does not label an automation-enabled human profile with no modes as dispatch eligible', async () => {
        teamServiceMock.getProfiles.mockResolvedValue([
            profileFixture({
                seed_key: 'human-reviewer',
                display_name: 'Human Reviewer',
                profile_kind: 'human',
                assignment_modes: [],
                automation_enabled: true,
            }),
        ]);

        renderWithProviders(<TeamProfileManager />);

        const card = await screen.findByTestId('profile-card');
        expect(screen.getByRole('note')).toHaveTextContent(
            'Automation is only one routing prerequisite. Dispatch also requires an enabled agent actor',
        );
        expect(within(card).getByText('Human')).toBeInTheDocument();
        expect(within(card).getByText('Recommendations enabled')).toBeInTheDocument();
        expect(within(card).getByText('No assignment modes')).toBeInTheDocument();
        expect(within(card).queryByText(/dispatch eligible/i)).not.toBeInTheDocument();
        expect(within(card).queryByText(/dispatchable/i)).not.toBeInTheDocument();
    });

    it('announces profile mutation failures to assistive technology', async () => {
        teamServiceMock.createProfile.mockRejectedValueOnce({
            response: {
                status: 400,
                data: { detail: 'Profile save failed.' },
            },
        });
        const { user } = renderWithProviders(<TeamProfileManager />);

        await screen.findByText('No capability profiles yet.');
        await user.type(
            screen.getByRole('textbox', { name: 'Display name' }),
            'Unavailable Worker',
        );
        await user.click(screen.getByRole('button', { name: 'Create' }));

        expect(await screen.findByRole('alert')).toHaveTextContent('Profile save failed.');
    });
});
