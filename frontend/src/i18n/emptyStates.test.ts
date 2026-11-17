import { describe, expect, it } from 'vitest';
import { emptyStatesEnglish, emptyStatesRussian } from './emptyStates';

const keysOf = (value: unknown, prefix = ''): string[] => (
    value && typeof value === 'object'
        ? Object.entries(value).flatMap(([key, child]) => keysOf(child, `${prefix}${key}.`))
        : [prefix.slice(0, -1)]
);

describe('empty state copy', () => {
    it('has the same keys in English and Russian', () => {
        expect(keysOf(emptyStatesRussian).sort()).toEqual(keysOf(emptyStatesEnglish).sort());
    });

    it('keeps every string non-empty in both languages', () => {
        for (const key of keysOf(emptyStatesEnglish)) {
            const en = key.split('.').reduce<unknown>((node, part) => (node as Record<string, unknown>)[part], emptyStatesEnglish);
            const ru = key.split('.').reduce<unknown>((node, part) => (node as Record<string, unknown>)[part], emptyStatesRussian);
            expect(String(en).trim(), key).not.toBe('');
            expect(String(ru).trim(), key).not.toBe('');
        }
    });
});
