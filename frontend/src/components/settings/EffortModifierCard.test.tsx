import { screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import type { EffortModifier } from '../../types/schedulingRules';
import { renderWithProviders } from '../../test/renderWithProviders';
import { EffortModifierCard } from './EffortModifierCard';

const modifierFixture = (
    overrides: Partial<EffortModifier> = {},
): EffortModifier => ({
    id: 'custom_modifier',
    enabled: true,
    operation: 'ceil',
    formula: null,
    fallback: 'effort',
    min_value: 0,
    ...overrides,
});

describe('EffortModifierCard', () => {
    it('switches from an operation to a safe formula default atomically', async () => {
        const onChange = vi.fn();
        const { user } = renderWithProviders(
            <EffortModifierCard
                modifier={modifierFixture()}
                onChange={onChange}
                onRemove={vi.fn()}
            />,
        );

        await user.click(screen.getByRole('button', { name: 'custom_modifier' }));
        await user.selectOptions(screen.getByLabelText('Type'), 'multiply');

        expect(onChange).toHaveBeenLastCalledWith(expect.objectContaining({
            operation: null,
            formula: 'effort * 1',
        }));
    });

    it('preserves zero constants instead of replacing them with a fallback', async () => {
        const { user } = renderWithProviders(
            <EffortModifierCard
                modifier={modifierFixture({
                    operation: null,
                    formula: 'effort * 0',
                })}
                onChange={vi.fn()}
                onRemove={vi.fn()}
            />,
        );

        await user.click(screen.getByRole('button', { name: 'custom_modifier' }));

        expect(screen.getByRole('spinbutton', { name: 'Multiplier' })).toHaveValue(0);
    });

    it.each([
        'effort / 4',
        'effort / (1 - assignee.operational_utilization / 100)',
    ])('exposes a positive UI minimum for divisor template %s', async (formula) => {
        const { user } = renderWithProviders(
            <EffortModifierCard
                modifier={modifierFixture({
                    operation: null,
                    formula,
                })}
                onChange={vi.fn()}
                onRemove={vi.fn()}
            />,
        );

        await user.click(screen.getByRole('button', { name: 'custom_modifier' }));

        expect(screen.getByRole('spinbutton', { name: 'Divisor' })).toHaveAttribute('min', '0.1');
    });
});
