import { describe, it } from 'node:test';
import assert from 'node:assert';
import { mapLegacyPath } from './legacyPaths.ts';

// Specification for mapLegacyPath(pathname, search).
// - search may be given with or without a leading '?'. The result adds '?' only when the query is non-empty.
// - The query is built from the caller's pairs, kept in their original order and raw text (no re-encoding),
//   followed by each mapped pair whose key the caller does not already set. The caller's value wins.
// - Matching is exact on the path, ignoring one trailing slash. Deeper paths and unknown paths return null.
// - A current path returns null, with or without a query.
type Case = readonly [pathname: string, search: string, expected: string | null];

const cases: readonly Case[] = [
  // Redirects named in the navigation rule, no extra query.
  ['/plan/master', '', '/plan'],
  ['/iterations', '', '/plan?panel=iterations'],
  ['/roadmap', '', '/projects?view=roadmap'],
  ['/agent-pipeline', '', '/tasks?layout=pipeline'],
  ['/agent-team/setup', '', '/team?tab=connect'],
  ['/calendar', '', '/settings?tab=calendar'],

  // Redirects with existing query parameters, which must survive.
  ['/plan/master', '?project=3&iteration=backlog', '/plan?project=3&iteration=backlog'],
  ['/iterations', '?project=3', '/plan?project=3&panel=iterations'],
  ['/roadmap', '?project=3&zoom=2', '/projects?project=3&zoom=2&view=roadmap'],
  ['/agent-pipeline', '?project=3&iteration=2', '/tasks?project=3&iteration=2&layout=pipeline'],
  ['/agent-team/setup', '?return=%2Fteam', '/team?return=%2Fteam&tab=connect'],
  ['/calendar', '?year=2026', '/settings?year=2026&tab=calendar'],

  // The mapping sets a parameter, and the caller's value wins.
  ['/iterations', '?panel=backlog', '/plan?panel=backlog'],
  ['/agent-team/setup', '?tab=models', '/team?tab=models'],
  ['/calendar', '?tab=holidays', '/settings?tab=holidays'],
  ['/roadmap', '?view=board', '/projects?view=board'],
  ['/iterations', '?panel=a&panel=b', '/plan?panel=a&panel=b'],

  // Caller's pairs keep their order; mapped pairs are appended after them.
  ['/iterations', '?zeta=1&project=3', '/plan?zeta=1&project=3&panel=iterations'],
  ['/roadmap', '?x=1', '/projects?x=1&view=roadmap'],

  // Raw query text is kept as it was given.
  ['/iterations', '?label=a%20b', '/plan?label=a%20b&panel=iterations'],
  ['/plan/master', '?q=a+b', '/plan?q=a+b'],

  // Search given without a leading '?'.
  ['/roadmap', 'view=board', '/projects?view=board'],
  ['/iterations', 'project=3', '/plan?project=3&panel=iterations'],

  // Trailing slashes.
  ['/plan/master/', '', '/plan'],
  ['/iterations/', '?project=3', '/plan?project=3&panel=iterations'],
  ['/agent-pipeline/', '', '/tasks?layout=pipeline'],

  // An empty query marker adds nothing.
  ['/plan/master', '?', '/plan'],

  // Current paths return null.
  ['/', '', null],
  ['/plan', '', null],
  ['/plan', '?project=3', null],
  ['/plan/', '', null],
  ['/projects', '?view=roadmap', null],
  ['/tasks', '?layout=pipeline', null],
  ['/team', '?tab=connect', null],
  ['/settings', '?tab=calendar', null],
  ['/settings/', '', null],

  // Nested paths are not redirected.
  ['/plan/master/extra', '', null],
  ['/iterations/2', '', null],
  ['/agent-team/setup/extra', '', null],
  ['/agent-team', '', null],
  ['/roadmap/board', '', null],

  // Unknown paths, including prefixes of known ones.
  ['/missing', '', null],
  ['/planner', '', null],
  ['/plan-master', '', null],
  ['/calendar.ics', '', null],
  ['/agent-pipelines', '', null],
];

describe('mapLegacyPath check table', () => {
  it(`has at least 30 cases`, () => {
    assert.ok(cases.length >= 30, `expected at least 30 cases, found ${cases.length}`);
  });

  for (const [pathname, search, expected] of cases) {
    it(`maps ${pathname} with search ${JSON.stringify(search)} to ${expected ?? 'null'}`, () => {
      assert.deepStrictEqual(
        mapLegacyPath(pathname, search),
        expected,
        `mapLegacyPath(${JSON.stringify(pathname)}, ${JSON.stringify(search)}) must return ${JSON.stringify(expected)}`,
      );
    });
  }
});
