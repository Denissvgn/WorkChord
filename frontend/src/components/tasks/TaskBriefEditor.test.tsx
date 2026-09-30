import { useState } from 'react';
import { describe, expect, it } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TaskBriefEditor } from './TaskBriefEditor';
import { buildTaskEditorDefaults, emptyTaskBrief, toTaskCreate } from './taskEditorContract';

describe('structured task drafting', () => {
    it('keeps criterion identity attached to its text when reordered', async () => {
        const Harness = () => {
            const [brief, setBrief] = useState({ ...emptyTaskBrief(), acceptance_criteria: [
                { id: 'first', revision: 2, text: 'First result', verification: '' },
                { id: 'second', revision: 1, text: 'Second result', verification: '' },
            ] });
            return <><TaskBriefEditor value={brief} onChange={setBrief} /><output aria-label="Draft IDs">{brief.acceptance_criteria.map(item => `${item.id}:${item.revision}:${item.text}`).join('|')}</output></>;
        };
        const { user } = renderWithProviders(<Harness />);
        await user.type(screen.getByRole('textbox', { name: 'Criterion 1' }), ' clarified');
        await user.click(screen.getByRole('button', { name: 'Move criterion 1 down' }));
        expect(screen.getByLabelText('Draft IDs')).toHaveTextContent('second:1:Second result|first:2:First result clarified');
        expect(screen.getByRole('textbox', { name: 'Criterion 2' })).toHaveValue('First result clarified');
    });

    it('captures new work with unknown effort and no fabricated verdict', () => {
        const draft = buildTaskEditorDefaults();
        draft.title = 'Urgent human work';
        const payload = toTaskCreate(draft);
        expect(payload.effort_hours).toBeNull();
        expect(payload.effort_days).toBeNull();
        expect(payload.estimate_provenance).toBe('unknown');
        expect(payload.brief?.acceptance_criteria).toEqual([]);
        expect(payload).not.toHaveProperty('progress');
        expect(payload).not.toHaveProperty('accepted_at');
    });
});
