import { describe, expect, it } from 'vitest';
import { englishResources } from './resources.en';

const englishStrings = (value: unknown): string[] => {
    if (typeof value === 'string') return [value];
    if (value && typeof value === 'object') return Object.values(value).flatMap(englishStrings);
    return [];
};

describe('English names', () => {
    it('uses no "Sprint" in any English string', () => {
        const sprintStrings = englishStrings(englishResources).filter(text => /sprint/i.test(text));
        expect(sprintStrings).toEqual([]);
    });

    it('names the iteration example "Iteration 1"', () => {
        expect(englishResources.translation.iterations.iterationNamePlaceholder).toBe('e.g. Iteration 1');
    });

    it('labels the Triage list column "Request"', () => {
        expect(englishResources.translation.surfaces.triagePage.item).toBe('Request');
    });
});
