import { describe, expect, it } from 'vitest';
import { defaultFilters } from './taskFilterDefaults';
import { filterSignature, savedViewFilters, savedViewModified, unsavedConditionKeys } from './savedViewState';
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
    it('keeps the milestone and needs-attention conditions out of a saved view', () => {
        const shown = { ...defaultFilters, milestoneId: 4, needsAttention: true, status: 'active' };
        expect(savedViewFilters(shown)).not.toHaveProperty('milestoneId');
        expect(savedViewFilters(shown)).not.toHaveProperty('needsAttention');
        expect(savedViewFilters(shown)).toMatchObject({ status: 'active' });
        expect(savedViewModified(view, { ...defaultFilters, milestoneId: 4, needsAttention: true }, 'priority')).toBe(false);
    });
    it('names the unsaved conditions that are set', () => {
        expect(unsavedConditionKeys(defaultFilters)).toEqual([]);
        expect(unsavedConditionKeys({ ...defaultFilters, needsAttention: false })).toEqual(['needsAttention']);
        expect(unsavedConditionKeys({ ...defaultFilters, milestoneId: 4, needsAttention: true, status: 'active' })).toEqual(['milestoneId', 'needsAttention']);
    });
    it('marks a changed ordering as modified', () => expect(savedViewModified(view, defaultFilters, 'title')).toBe(true));
    it('does not count a condition applied by a hand-over as a change while it keeps its value', () => {
        const handedOver = { planningIssue: 'unassigned' as const };
        expect(savedViewModified(null, { ...defaultFilters, planningIssue: 'unassigned' }, 'priority', handedOver)).toBe(false);
        expect(savedViewModified(null, defaultFilters, 'priority', handedOver)).toBe(false);
        expect(savedViewModified(null, { ...defaultFilters, planningIssue: 'missing-effort' }, 'priority', handedOver)).toBe(true);
        expect(savedViewModified(null, { ...defaultFilters, planningIssue: 'unassigned', status: 'active' }, 'priority', handedOver)).toBe(true);
    });
});
