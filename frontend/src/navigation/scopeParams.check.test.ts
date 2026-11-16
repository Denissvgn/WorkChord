import { describe, it } from 'node:test';
import assert from 'node:assert';
import { formatScope, parseScope } from './scopeParams.ts';

// Specification for parseScope(search) and formatScope(scope, search).
// - search may be given with or without a leading '?'. Results use '?' only when the query is non-empty.
// - parseScope: project is a positive integer or 'all'; iteration is a positive integer or 'backlog'.
//   A value that does not match is dropped, which means its key is absent from the result.
//   Only the first occurrence of each key is read. Other parameters are ignored.
// - formatScope: writes both project and iteration. An existing key is replaced in place.
//   A missing key is appended, project before iteration. Other pairs keep their order and raw text.
type Scope = { project: number | 'all'; iteration: number | 'backlog' };
type ParsedScope = Partial<Scope>;

const parseCases: ReadonlyArray<readonly [search: string, expected: ParsedScope]> = [
  // Valid values.
  ['?project=3&iteration=2', { project: 3, iteration: 2 }],
  ['?project=all&iteration=backlog', { project: 'all', iteration: 'backlog' }],
  ['?project=12', { project: 12 }],
  ['?iteration=backlog', { iteration: 'backlog' }],
  ['?iteration=1', { iteration: 1 }],
  ['project=3&iteration=4', { project: 3, iteration: 4 }],

  // Empty search.
  ['?', {}],
  ['', {}],

  // Invalid project values are dropped.
  ['?project=0', {}],
  ['?project=-1', {}],
  ['?project=1.5', {}],
  ['?project=abc', {}],
  ['?project=', {}],
  ['?project=All', {}],
  ['?project=1e3', {}],
  ['?project=3%20', {}],

  // Invalid iteration values are dropped.
  ['?iteration=0', {}],
  ['?iteration=-3', {}],
  ['?iteration=all', {}],
  ['?iteration=Backlog', {}],
  ['?iteration=2.0', {}],

  // A dropped value does not affect the other key.
  ['?project=0&iteration=5', { iteration: 5 }],
  ['?project=all&iteration=none', { project: 'all' }],

  // Other parameters are ignored.
  ['?tab=cal&project=2&x=1', { project: 2 }],
  ['?iteration=3&other=ignored', { iteration: 3 }],
  ['?q=a%20b&project=4', { project: 4 }],
  ['?tab=plan', {}],
];

const formatCases: ReadonlyArray<readonly [scope: Scope, search: string, expected: string]> = [
  // Empty search.
  [{ project: 3, iteration: 'backlog' }, '', '?project=3&iteration=backlog'],
  [{ project: 'all', iteration: 2 }, '', '?project=all&iteration=2'],

  // Other parameters are kept.
  [{ project: 'all', iteration: 2 }, '?tab=a', '?tab=a&project=all&iteration=2'],
  [{ project: 3, iteration: 2 }, '?tab=a&project=1&x=2&iteration=9', '?tab=a&project=3&x=2&iteration=2'],
  [{ project: 3, iteration: 'backlog' }, '?iteration=5&project=1', '?iteration=backlog&project=3'],
  [{ project: 'all', iteration: 'backlog' }, '?q=a%20b', '?q=a%20b&project=all&iteration=backlog'],
  [{ project: 5, iteration: 'backlog' }, '?b=2&a=1&project=1&c=3', '?b=2&a=1&project=5&c=3&iteration=backlog'],

  // Existing values are replaced.
  [{ project: 'all', iteration: 'backlog' }, '?project=7&iteration=3', '?project=all&iteration=backlog'],
  [{ project: 9, iteration: 4 }, '?project=all&iteration=backlog', '?project=9&iteration=4'],

  // Search given without a leading '?'.
  [{ project: 1, iteration: 1 }, 'tab=a', '?tab=a&project=1&iteration=1'],

  // Bare '?' adds nothing.
  [{ project: 2, iteration: 'backlog' }, '?', '?project=2&iteration=backlog'],
];

const roundTripCases: ReadonlyArray<readonly [scope: Scope, search: string]> = [
  [{ project: 1, iteration: 'backlog' }, '?tab=a'],
  [{ project: 'all', iteration: 7 }, ''],
  [{ project: 42, iteration: 1 }, '?project=9&x=y'],
  [{ project: 'all', iteration: 'backlog' }, ''],
  [{ project: 8, iteration: 'backlog' }, '?iteration=3&tab=b'],
  [{ project: 6, iteration: 6 }, '?q=a%20b&project=all'],
];

// The file as a whole holds at least 30 cases.
describe('scope codec check file', () => {
  it('has at least 30 cases', () => {
    const total = parseCases.length + formatCases.length + roundTripCases.length;
    assert.ok(total >= 30, `expected at least 30 cases, found ${total}`);
  });
});

describe('parseScope check table', () => {
  for (const [search, expected] of parseCases) {
    it(`parses ${JSON.stringify(search)} to ${JSON.stringify(expected)}`, () => {
      assert.deepStrictEqual(
        parseScope(search),
        expected,
        `parseScope(${JSON.stringify(search)}) must return ${JSON.stringify(expected)}`,
      );
    });
  }
});

describe('formatScope check table', () => {
  for (const [scope, search, expected] of formatCases) {
    it(`formats ${JSON.stringify(scope)} onto ${JSON.stringify(search)} as ${JSON.stringify(expected)}`, () => {
      assert.deepStrictEqual(
        formatScope(scope, search),
        expected,
        `formatScope(${JSON.stringify(scope)}, ${JSON.stringify(search)}) must return ${JSON.stringify(expected)}`,
      );
    });
  }

  for (const [scope, search] of roundTripCases) {
    it(`round-trips ${JSON.stringify(scope)} through ${JSON.stringify(search)}`, () => {
      assert.deepStrictEqual(
        parseScope(formatScope(scope, search)),
        scope,
        `parseScope(formatScope(${JSON.stringify(scope)}, ${JSON.stringify(search)})) must equal the scope`,
      );
    });
  }
});
