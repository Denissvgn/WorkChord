import { screen, within } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import i18n from '../../i18n/i18n';
import { renderWithProviders } from '../../test/renderWithProviders';
import { PlanningWorkbenchFrame } from './PlanningWorkbenchFrame';

describe('PlanningWorkbenchFrame', () => {
    it('keeps context, supporting actions, the primary action, and overflow in a stable order', () => {
        renderWithProviders(
            <PlanningWorkbenchFrame
                title="Schedule"
                description="Review the current plan."
                facts={[{ id: 'period', label: 'Period', value: 'Iteration 1' }]}
                contextControl={<button type="button">Choose period</button>}
                secondaryActions={<button type="button">Help</button>}
                primaryAction={<button type="button">Preview changes</button>}
                overflowAction={<button type="button">More actions</button>}
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

    it('renders every action the planning pages hand it, including several inside one fragment', () => {
        renderWithProviders(
            <PlanningWorkbenchFrame
                title="Calendar"
                secondaryActions={(
                    <>
                        <button type="button">Discard</button>
                        <button type="button">New calendar</button>
                        <button type="button">Fullscreen</button>
                    </>
                )}
                primaryAction={(
                    <>
                        <button type="button">Save</button>
                        <button type="button">Apply</button>
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
            'Apply',
        ]);
    });
});
