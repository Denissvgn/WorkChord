import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, expect, it } from 'vitest';
import { MemoryRouter } from 'react-router-dom';
import type { TaskAgentReadiness } from '../../types/task';
import { TaskAgentReadinessBadge } from './TaskAgentReadinessBadge';

const readiness: TaskAgentReadiness = {
    is_ready: false,
    blockers: ['Add acceptance criteria'],
    warnings: [],
    criteria: [{
        key: 'acceptance-criteria',
        label: 'Acceptance criteria',
        passed: false,
        reason: 'No acceptance criteria are defined.',
    }],
};

describe('TaskAgentReadinessBadge', () => {
    it('associates the compact trigger with its announced details region', async () => {
        const user = userEvent.setup();
        render(
            <MemoryRouter>
                <TaskAgentReadinessBadge readiness={readiness} />
            </MemoryRouter>,
        );

        const trigger = screen.getByRole('button', { name: 'Not agent-ready' });
        expect(trigger).toHaveAttribute('aria-expanded', 'false');

        await user.click(trigger);

        const details = screen.getByRole('region', { name: 'Not agent-ready details' });
        expect(trigger).toHaveAttribute('aria-expanded', 'true');
        expect(trigger).toHaveAttribute('aria-controls', details.id);
        expect(details).toHaveAttribute('aria-live', 'polite');
        expect(screen.getByText('Add acceptance criteria')).toBeVisible();
    });
});
