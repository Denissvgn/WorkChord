import { screen, within } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';
import i18n from '../../i18n/i18n';
import { renderWithProviders } from '../../test/renderWithProviders';
import { PlanningWorkbenchFrame } from './PlanningWorkbenchFrame';

import { Button } from '../../components/common/Button';
describe('PlanningWorkbenchFrame', () => {
    afterEach(() => {
        vi.restoreAllMocks();
    });

    it('keeps context, supporting actions, the primary action, and overflow in a stable order', () => {
        renderWithProviders(
            <PlanningWorkbenchFrame
                title="Schedule"
                description="Review the current plan."
                facts={[{ id: 'period', label: 'Period', value: 'Iteration 1' }]}
                contextControl={<Button type="button" variant="secondary">Choose period</Button>}
                secondaryActions={<Button type="button" variant="secondary">Help</Button>}
                primaryAction={<Button type="button" variant="secondary">Preview changes</Button>}
                overflowAction={<Button type="button" variant="secondary">More actions</Button>}
            >
                <div>Planning canvas</div>
            </PlanningWorkbenchFrame>,
            { initialEntries: ['/gantt?fromPlanStep=schedule'] },
        );

        expect(screen.getByRole('heading', { name: 'Schedule' })).toBeVisible();
        expect(screen.getByText('Planning canvas')).toBeVisible();
        expect(screen.getByRole('complementary', {
            name: i18n.t('plan.master.planReturnContext'),
        })).toBeVisible();

        const header = screen.getByTestId('page-header');
        expect(within(header).getAllByRole('button').map(button => button.textContent)).toEqual([
            'Choose period',
            'Help',
            'Preview changes',
            'More actions',
        ]);
        expect(within(header).getByText('Period').tagName).toBe('DT');
        expect(within(header).getByText('Iteration 1').tagName).toBe('DD');
    });

    it('keeps every supporting action but renders one primary action and logs when given two', () => {
        const error = vi.spyOn(console, 'error').mockImplementation(() => undefined);
        renderWithProviders(
            <PlanningWorkbenchFrame
                title="Calendar"
                secondaryActions={(
                    <>
                        <Button type="button" variant="secondary">Discard</Button>
                        <Button type="button" variant="secondary">New calendar</Button>
                        <Button type="button" variant="secondary">Fullscreen</Button>
                    </>
                )}
                primaryAction={(
                    <>
                        <Button type="button" variant="secondary">Save</Button>
                        <Button type="button" variant="secondary">Apply</Button>
                    </>
                )}
            >
                <div>Planning canvas</div>
            </PlanningWorkbenchFrame>,
        );

        const header = screen.getByTestId('page-header');
        expect(within(header).getAllByRole('button').map(button => button.textContent)).toEqual([
            'Discard',
            'New calendar',
            'Fullscreen',
            'Save',
        ]);
        expect(error).toHaveBeenCalledTimes(1);
        expect(error.mock.calls[0][0]).toContain('one primary action');
    });
});
