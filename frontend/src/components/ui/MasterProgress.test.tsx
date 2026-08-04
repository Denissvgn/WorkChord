import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { MasterProgress } from './MasterProgress';

describe('MasterProgress', () => {
    it('exposes completion in the workflow unit while deriving the visual ratio', () => {
        render(
            <MasterProgress
                completed={1}
                label="Plan readiness progress"
                total={6}
                valueText="1 of 6 checkpoints complete"
            />,
        );

        const progress = screen.getByRole('progressbar', {
            name: 'Plan readiness progress',
        });
        expect(progress).toHaveAttribute('aria-valuemin', '0');
        expect(progress).toHaveAttribute('aria-valuenow', '1');
        expect(progress).toHaveAttribute('aria-valuemax', '6');
        expect(progress).toHaveAttribute(
            'aria-valuetext',
            '1 of 6 checkpoints complete',
        );
        expect(progress.firstElementChild).toHaveStyle({
            transform: 'scaleX(0.16666666666666666)',
        });
    });

    it('bounds invalid completion without inventing a percentage scale', () => {
        const { rerender } = render(
            <MasterProgress
                completed={9}
                label="Setup check completion"
                total={7}
                valueText="7 of 7 setup checks complete"
            />,
        );

        expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuenow', '7');
        expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuemax', '7');

        rerender(
            <MasterProgress
                completed={Number.NaN}
                label="Setup check completion"
                total={0}
                valueText="Completion unavailable"
            />,
        );

        expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuenow', '0');
        expect(screen.getByRole('progressbar')).toHaveAttribute('aria-valuemax', '1');
    });
});
