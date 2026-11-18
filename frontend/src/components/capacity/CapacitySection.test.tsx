import type { ReactElement } from 'react';
import { screen, waitFor } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import { it, expect, vi } from 'vitest';
import i18n from '../../i18n/i18n';
import { IdentityContext } from '../../features/identity/identityContext';
import type { TeamMember } from '../../types/team';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { Iteration } from '../../types/iteration';
import { CapacitySection } from './CapacitySection';

vi.mock('./TeamList', () => ({ TeamList: () => <div>Capacity rows with time off</div> }));
vi.mock('./PlanQuickAddCapacity', () => ({ PlanQuickAddCapacity: () => null }));
vi.mock('../team/VacationCsvImport', () => ({ VacationCsvImport: ({ iterationId }: { iterationId: number }) => <div>Import time off for {iterationId}</div> }));

it('offers vacation CSV import in the capacity overflow', async () => {
    const iteration = { id: 9, start_date: '2026-01-01', end_date: '2026-01-31' } as Iteration;
    const view = renderWithProviders(<CapacitySection iteration={iteration} iterations={[iteration]} members={[]} primary />);
    expect(screen.getByText('Capacity rows with time off')).toBeInTheDocument();
    await view.user.click(screen.getByRole('button', { name: /capacity actions/i }));
    await view.user.click(screen.getByRole('menuitem', { name: /import.*csv/i }));
    expect(screen.getByText('Import time off for 9')).toBeInTheDocument();
});

const capacityApi = vi.hoisted(() => ({
    getByIteration: vi.fn(),
    create: vi.fn(),
    readInitial: vi.fn(),
}));
vi.mock('../../services/teamService', () => ({ teamService: { getByIteration: capacityApi.getByIteration, create: capacityApi.create } }));
vi.mock('../../services/planningInputService', () => ({ planningInputService: { readInitial: capacityApi.readInitial } }));
vi.mock('../team/ConnectAgentSteps', () => ({ ConnectAgentSteps: ({ showTitle }: { showTitle?: boolean }) => <p>Five questions to connect an agent{showTitle === false ? ' (no own title)' : ''}</p> }));

const withProfile = (ui: ReactElement) => (
    <IdentityContext.Provider value={{
        identity: { mode: 'trusted_local', authenticated: true, configured: true, principal: null, profile: { id: 7, display_name: 'Ada Lovelace' },
            workspace_role: 'owner', projects: {}, csrf_token: null },
        refresh: () => {}, signOut: async () => {},
    }}>{ui}</IdentityContext.Provider>
);

it('adds the chosen profile with Add me and connects an agent without leaving Plan', async () => {
    capacityApi.getByIteration.mockResolvedValue([]);
    capacityApi.readInitial.mockResolvedValue({ expected_revisions: { 9: 1 } });
    capacityApi.create.mockResolvedValue({ id: 31, profile_id: 7 });
    const iteration = { id: 9, start_date: '2026-01-01', end_date: '2026-01-31' } as Iteration;
    const view = renderWithProviders(withProfile(<CapacitySection iteration={iteration} iterations={[iteration]} members={[]} primary />));

    await view.user.click(screen.getByRole('button', { name: i18n.t('identity.addMe') }));
    await waitFor(() => expect(capacityApi.create).toHaveBeenCalledTimes(1));
    expect(capacityApi.create.mock.calls[0][0]).toBe(9);
    expect(capacityApi.create.mock.calls[0][1]).toMatchObject({ name: 'Ada Lovelace', profile_id: 7, availability_percent: 100 });

    // Plan links to a full page only for Tasks and Gantt: the agent is connected in a drawer over Plan.
    await view.user.click(screen.getByRole('button', { name: i18n.t('teamPage.connectAgent') }));
    const drawer = await screen.findByRole('dialog', { name: i18n.t('teamPage.connectAgent') });
    expect(drawer).toHaveTextContent('Five questions to connect an agent (no own title)');
    expect(screen.queryByRole('link')).not.toBeInTheDocument();
});

it('hides Add me once the chosen profile is on the iteration', () => {
    const iteration = { id: 9, start_date: '2026-01-01', end_date: '2026-01-31' } as Iteration;
    renderWithProviders(withProfile(<CapacitySection iteration={iteration} iterations={[iteration]}
        members={[{ id: 31, profile_id: 7 } as TeamMember]} primary />));
    expect(screen.queryByRole('button', { name: i18n.t('identity.addMe') })).not.toBeInTheDocument();
    expect(screen.getByRole('button', { name: i18n.t('teamPage.connectAgent') })).toBeInTheDocument();
});

it('keeps the Connect drawer in the address, so it is still open after the page is drawn again', async () => {
    const LocationProbe = () => <output data-testid="location">{useLocation().search}</output>;
    const iteration = { id: 9, start_date: '2026-01-01', end_date: '2026-01-31' } as Iteration;
    const view = renderWithProviders(<><CapacitySection iteration={iteration} iterations={[iteration]} members={[]} primary /><LocationProbe /></>,
        { initialEntries: ['/plan?project=1&iteration=9'] });
    await view.user.click(screen.getByRole('button', { name: i18n.t('teamPage.connectAgent') }));
    expect(await screen.findByRole('dialog', { name: i18n.t('teamPage.connectAgent') })).toBeInTheDocument();
    expect(screen.getByTestId('location')).toHaveTextContent('connect=1');
    view.unmount();

    // Saving the admin key inside the drawer redraws the whole app; the address brings the drawer back.
    renderWithProviders(<CapacitySection iteration={iteration} iterations={[iteration]} members={[]} primary />,
        { initialEntries: ['/plan?project=1&iteration=9&step=team&connect=1'] });
    expect(await screen.findByRole('dialog', { name: i18n.t('teamPage.connectAgent') })).toHaveTextContent('Five questions to connect an agent (no own title)');
});
