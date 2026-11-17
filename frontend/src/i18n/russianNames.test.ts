import { describe, expect, it } from 'vitest';
import { russianResources } from './resources.ru';

const russianStrings = (value: unknown): string[] => {
    if (typeof value === 'string') return [value];
    if (value && typeof value === 'object') return Object.values(value).flatMap(russianStrings);
    return [];
};

// Retired Russian terms and the shared word that replaced each one
// (config/workflow-vocabulary.json). Matches whole words only, so "трудоёмкость"
// and "независимый" are not flagged.
const RETIRED_TERMS = /(?<![\p{L}])(ёмкост\p{L}*|период\p{L}*|зависим\p{L}*|webhook\p{L}*|sprint\p{L}*|спринт\p{L}*)/iu;

// Exceptions, each with a reason:
// - A sample URL is an address, not interface wording.
const ALLOWED_STRINGS = new Set([
    'https://example.com/webhooks/workchord',
]);

describe('Russian names', () => {
    it('uses no retired term (ёмкость, период, зависимость, webhook, Sprint) in any Russian string', () => {
        const flagged = russianStrings(russianResources.translation)
            .filter(text => !ALLOWED_STRINGS.has(text))
            .filter(text => RETIRED_TERMS.test(text));
        expect(flagged).toEqual([]);
    });

    it('names the iteration example "Итерация 1"', () => {
        expect(russianResources.translation.iterations.iterationNamePlaceholder).toBe('например, Итерация 1');
    });
});
