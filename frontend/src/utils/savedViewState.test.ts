import { describe, expect, it } from 'vitest';
import { defaultFilters } from './taskFilterDefaults';
import { filterSignature, savedViewModified } from './savedViewState';
import type { SavedView } from '../types/savedView';

describe('effective saved view state', () => {
    const view = { filters_json: {}, sort_json: {} } as SavedView;
    it('treats omitted defaults and reordered label selections as the same filter', () => {
        expect(savedViewModified(view, defaultFilters, 'priority')).toBe(false);
        expect(filterSignature({ ...defaultFilters, labelSlugs: ['one', 'two'] })).toBe(filterSignature({ ...defaultFilters, labelSlugs: ['two', 'one'] }));
    });
    it.each([
        { assigneeId: 9 }, { projectId: 2 }, { priority: 0 }, { status: 'closed' },
        { hasDependency: false }, { isOverdue: true }, { isIterationOverflow: false }, { agentReady: true },
        { startDateFrom: '2026-10-01' }, { startDateTo: '2026-10-02' }, { endDateFrom: '2026-10-03' }, { endDateTo: '2026-10-04' },
        { labelSlugs: ['urgent'] }, { labelGroupKeys: ['delivery'] }, { planningIssue: 'missing-effort' as const },
    ])('marks a changed filter as an unsaved modification: %j', change => {
        expect(savedViewModified(view, { ...defaultFilters, ...change }, 'priority')).toBe(true);
    });
    it('marks a changed ordering as modified', () => expect(savedViewModified(view, defaultFilters, 'title')).toBe(true));
});
