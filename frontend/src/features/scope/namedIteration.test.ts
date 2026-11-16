import { describe, expect, it } from 'vitest';
import { forgetCompletedSearchUnless, recordCompletedSearch, urlNamesIteration } from './namedIteration';

describe('urlNamesIteration', () => {
    it('is true for an iteration or Backlog the URL names', () => {
        expect(urlNamesIteration('?task=42&project=1&iteration=12')).toBe(true);
        expect(urlNamesIteration('?from=overview&returnTask=42&iteration=backlog')).toBe(true);
    });

    it('is false when the URL names no valid iteration', () => {
        expect(urlNamesIteration('?task=42')).toBe(false);
        expect(urlNamesIteration('?task=42&iteration=soon')).toBe(false);
    });

    it('is false for the iteration the shell added, until the URL moves on', () => {
        recordCompletedSearch('?task=42&project=1&iteration=12');
        expect(urlNamesIteration('?task=42&project=1&iteration=12')).toBe(false);
        expect(urlNamesIteration('task=42&project=1&iteration=12')).toBe(false);

        forgetCompletedSearchUnless('?task=42&project=1&iteration=12');
        expect(urlNamesIteration('?task=42&project=1&iteration=12')).toBe(false);

        forgetCompletedSearchUnless('?task=42&project=1&iteration=11');
        expect(urlNamesIteration('?task=42&project=1&iteration=12')).toBe(true);
    });
});
