import { describe, expect, it } from 'vitest';
import { defaultFilters } from '../../utils/taskFilterDefaults';
import {
    filtersFromSearchParams,
    searchParamsNameView,
    writeClearedViewMarker,
    writeFiltersToSearchParams,
} from './taskViewParams';

describe('task view parameters', () => {
    it('carries the milestone and needs-attention filters in the link and reads them back', () => {
        const filters = { ...defaultFilters, milestoneId: 11, needsAttention: true };
        const params = writeFiltersToSearchParams(new URLSearchParams(), filters);
        expect(params.toString()).toBe('milestone=11&attention=yes');
        expect(filtersFromSearchParams(params)).toEqual(filters);
        expect(filtersFromSearchParams(new URLSearchParams('milestone=x&attention=maybe'))).toEqual(defaultFilters);
    });

    it('marks a shown saved view whose every condition and order were removed', () => {
        const params = writeFiltersToSearchParams(new URLSearchParams('view=12&status=planned'), defaultFilters);

        writeClearedViewMarker(params, true);

        expect(params.toString()).toBe('view=12&filters=none');
        expect(searchParamsNameView(params)).toBe(true);
        expect(filtersFromSearchParams(params)).toEqual(defaultFilters);
    });

    it('drops the mark once a condition or an order is named, and never marks All tasks', () => {
        const withCondition = writeFiltersToSearchParams(new URLSearchParams('view=12&filters=none'), { ...defaultFilters, status: 'active' });
        expect(writeClearedViewMarker(withCondition, true).toString()).toBe('view=12&status=active');

        expect(writeClearedViewMarker(new URLSearchParams('view=12&filters=none&sort=title'), true).toString()).toBe('view=12&sort=title');
        expect(writeClearedViewMarker(new URLSearchParams('filters=none'), false).toString()).toBe('');
    });

    it('treats a plain view link as naming no view state of its own', () => {
        expect(searchParamsNameView(new URLSearchParams('view=12'))).toBe(false);
        expect(searchParamsNameView(new URLSearchParams('view=12&filters=other'))).toBe(false);
    });
});
