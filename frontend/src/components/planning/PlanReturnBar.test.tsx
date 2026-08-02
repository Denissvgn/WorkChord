import { screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import i18n from '../../i18n/i18n';
import { renderWithProviders } from '../../test/renderWithProviders';
import { PlanReturnBar } from './PlanReturnBar';

describe('PlanReturnBar', () => {
    it('returns a valid planning origin to the exact checkpoint', () => {
        renderWithProviders(<PlanReturnBar />, {
            initialEntries: ['/tasks?fromPlanStep=schedule'],
        });

        expect(screen.getByRole('complementary', {
            name: i18n.t('plan.master.planReturnContext'),
        })).toHaveTextContent(i18n.t('plan.steps.schedule.title'));
        expect(screen.getByRole('link', {
            name: i18n.t('plan.master.returnToCheckpoint'),
        })).toHaveAttribute('href', '/plan/master?step=schedule');
    });

    it('ignores unknown or path-like return values', () => {
        renderWithProviders(<PlanReturnBar />, {
            initialEntries: ['/tasks?fromPlanStep=%2Fsettings'],
        });
        expect(screen.queryByRole('complementary')).not.toBeInTheDocument();
    });
});
