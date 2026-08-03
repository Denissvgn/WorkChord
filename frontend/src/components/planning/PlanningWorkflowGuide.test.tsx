import { screen, waitFor } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import { PlanningWorkflowGuide } from './PlanningWorkflowGuide';

describe('PlanningWorkflowGuide', () => {
    it('moves focus to the destination workspace after guide navigation', async () => {
        const { user } = renderWithProviders(
            <>
                <main id="workspace-main" tabIndex={-1}>Workspace</main>
                <PlanningWorkflowGuide surface="plan" />
            </>,
            { initialEntries: ['/plan'] },
        );

        await user.click(screen.getByRole('button', { name: 'Planning help' }));
        await user.click(screen.getByRole('link', { name: 'Continue Plan Work' }));

        await waitFor(() => {
            expect(screen.getByText('Workspace')).toHaveFocus();
        });
    });
});
