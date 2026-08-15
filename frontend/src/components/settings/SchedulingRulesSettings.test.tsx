import { act, fireEvent, screen, waitFor, within } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import type { SchedulingRules, SchedulingRulesResponse } from '../../types/schedulingRules';
import { renderWithProviders } from '../../test/renderWithProviders';
import { SchedulingRulesSettings } from './SchedulingRulesSettings';

const adminAccessMock = vi.hoisted(() => ({
    useAdminAccess: vi.fn(),
}));

const schedulingRulesServiceMock = vi.hoisted(() => ({
    getRules: vi.fn(),
    updateRules: vi.fn(),
    resetRules: vi.fn(),
}));

vi.mock('../../hooks/useAdminAccess', () => adminAccessMock);
vi.mock('../../services/schedulingRulesService', () => ({
    schedulingRulesService: schedulingRulesServiceMock,
}));

const rulesFixture = (
    overrides: Partial<SchedulingRules> = {},
): SchedulingRules => ({
    schema_version: '1.0',
    effort_modifiers: [{
        id: 'professionalism',
        enabled: true,
        formula: 'effort / assignee.professionalism_coefficient',
        fallback: 'effort',
        min_value: 0,
    }],
    scheduling_passes: [{
        id: 'critical_deadline',
        description: 'Nearest deadline first',
        enabled: true,
        filter: { all: ['task.is_deferred == false'] },
        sort: [{ field: 'max_finish_date', order: 'asc' }],
    }],
    constraints: {
        sequential_per_assignee: true,
        respect_dependencies: true,
        min_start_date: true,
        max_finish_date: true,
        prefer_uninterrupted: true,
        balance_workload: {
            enabled: true,
            max_overload_percent: 10,
        },
    },
    ...overrides,
});

const responseFixture = (rules = rulesFixture()): SchedulingRulesResponse => ({
    rules,
    source: 'database',
});

describe('SchedulingRulesSettings', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        adminAccessMock.useAdminAccess.mockReturnValue({ hasAdminKey: true });
        schedulingRulesServiceMock.getRules.mockResolvedValue(responseFixture());
        schedulingRulesServiceMock.updateRules.mockImplementation(
            async (rules: SchedulingRules) => responseFixture(rules),
        );
        schedulingRulesServiceMock.resetRules.mockResolvedValue(responseFixture());
    });

    it('blocks out-of-range workload rules before sending a save request', async () => {
        const { user } = renderWithProviders(<SchedulingRulesSettings />);
        const overload = await screen.findByRole('spinbutton', {
            name: 'Max allowable overload:',
        });

        fireEvent.change(overload, { target: { value: '101' } });
        await user.click(screen.getByRole('button', { name: 'Save changes' }));

        expect(schedulingRulesServiceMock.updateRules).not.toHaveBeenCalled();
        expect(screen.getByRole('alert')).toHaveTextContent(
            'Maximum allowable overload must be between 0 and 100 percent.',
        );
        expect(overload).toHaveAttribute('max', '100');
    });

    it.each([
        ['zero direct divisor', 'effort / 0'],
        ['negative inverse-percentage divisor', 'effort / (1 - assignee.operational_utilization / -100)'],
    ])('blocks a %s before sending a save request', async (_caseName, formula) => {
        schedulingRulesServiceMock.getRules.mockResolvedValue(responseFixture(rulesFixture({
            effort_modifiers: [{
                id: 'unsafe_divisor',
                enabled: true,
                formula,
                fallback: 'effort',
                min_value: 0,
            }],
        })));
        const { user } = renderWithProviders(<SchedulingRulesSettings />);
        const overload = await screen.findByRole('spinbutton', {
            name: 'Max allowable overload:',
        });

        fireEvent.change(overload, { target: { value: '11' } });
        await user.click(screen.getByRole('button', { name: 'Save changes' }));

        expect(schedulingRulesServiceMock.updateRules).not.toHaveBeenCalled();
        expect(screen.getByRole('alert')).toHaveTextContent(
            'Modifier “unsafe_divisor” needs a divisor greater than zero.',
        );
    });

    it('freezes the draft during save and keeps the saved snapshot authoritative', async () => {
        let resolveSave: ((response: SchedulingRulesResponse) => void) | undefined;
        schedulingRulesServiceMock.updateRules.mockImplementation(() => (
            new Promise<SchedulingRulesResponse>(resolve => {
                resolveSave = resolve;
            })
        ));

        const { user } = renderWithProviders(<SchedulingRulesSettings />);
        const overload = await screen.findByRole('spinbutton', {
            name: 'Max allowable overload:',
        });
        fireEvent.change(overload, { target: { value: '25' } });

        await user.click(screen.getByRole('button', { name: 'Save changes' }));
        await waitFor(() => {
            expect(schedulingRulesServiceMock.updateRules).toHaveBeenCalledOnce();
        });
        expect(overload).toBeDisabled();
        expect(screen.getByRole('button', { name: /discard/i })).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Reset to defaults' })).toBeDisabled();

        const savedRules = schedulingRulesServiceMock.updateRules.mock.calls[0]?.[0];
        await act(async () => {
            resolveSave?.(responseFixture(savedRules));
        });

        await waitFor(() => {
            expect(overload).toBeEnabled();
            expect(overload).toHaveValue(25);
        });
        expect(screen.queryByText('Unsaved changes')).not.toBeInTheDocument();
    });

    it('keeps cards mounted while editable persisted IDs change', async () => {
        const { user } = renderWithProviders(<SchedulingRulesSettings />);

        const modifierToggle = await screen.findByRole('button', { name: 'professionalism' });
        await user.click(modifierToggle);
        const modifierCard = modifierToggle.closest('.rounded-lg') as HTMLElement | null;
        if (!modifierCard) throw new Error('Modifier card not found');
        const modifierId = within(modifierCard).getByLabelText('ID');
        await user.clear(modifierId);
        await user.type(modifierId, 'custom_modifier');
        expect(modifierId).toHaveValue('custom_modifier');
        expect(modifierToggle).toHaveAttribute('aria-expanded', 'true');

        const passToggle = screen.getByRole('button', {
            name: 'critical_deadline Nearest deadline first',
        });
        await user.click(passToggle);
        const passCard = passToggle.closest('.rounded-lg') as HTMLElement | null;
        if (!passCard) throw new Error('Scheduling pass card not found');
        const passId = within(passCard).getByLabelText('ID');
        await user.clear(passId);
        await user.type(passId, 'deadline_first');
        expect(passId).toHaveValue('deadline_first');
        expect(passToggle).toHaveAttribute('aria-expanded', 'true');
    });
});
