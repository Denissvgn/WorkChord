// Pure helper – no imports, no I/O.

type Rule = {
  from: string;
  to: string;
  params: readonly (readonly [string, string])[];
};

const LEGACY_RULES: readonly Rule[] = [
  { from: '/plan/master', to: '/plan', params: [] },
  { from: '/iterations', to: '/plan', params: [['panel', 'iterations']] },
  { from: '/roadmap', to: '/projects', params: [['view', 'roadmap']] },
  { from: '/agent-pipeline', to: '/tasks', params: [['layout', 'pipeline']] },
  { from: '/agent-team/setup', to: '/team', params: [['tab', 'connect']] },
  { from: '/calendar', to: '/settings', params: [['tab', 'calendar']] },
];

const CURRENT_PATHS: ReadonlySet<string> = new Set([
  '/',
  '/plan',
  '/projects',
  '/tasks',
  '/team',
  '/settings',
]);

function stripTrailingSlash(p: string): string {
  if (p.length > 1 && p.endsWith('/')) return p.slice(0, -1);
  return p;
}

function callerKeys(search: string): Set<string> {
  const raw = search.startsWith('?') ? search.slice(1) : search;
  if (raw === '') return new Set();
  const keys = new Set<string>();
  for (const pair of raw.split('&')) {
    if (pair === '') continue;
    const eq = pair.indexOf('=');
    keys.add(eq === -1 ? pair : pair.slice(0, eq));
  }
  return keys;
}

export function mapLegacyPath(pathname: string, search: string): string | null {
  const normalized = stripTrailingSlash(pathname);

  // Current paths always return null.
  if (CURRENT_PATHS.has(normalized)) return null;

  // Find a matching legacy rule (exact match after normalization).
  let rule: Rule | undefined;
  for (const r of LEGACY_RULES) {
    if (r.from === normalized) {
      rule = r;
      break;
    }
  }
  if (!rule) return null;

  // Build the query string: caller's pairs first, then mapped pairs whose key is absent.
  const rawSearch = search.startsWith('?') ? search.slice(1) : search;
  const keys = callerKeys(search);
  const extraPairs: string[] = [];
  for (const [key, value] of rule.params) {
    if (!keys.has(key)) {
      extraPairs.push(`${key}=${value}`);
    }
  }

  // Compose final query.
  let query = rawSearch;
  if (extraPairs.length > 0) {
    // Drop a trailing separator so appending does not produce '&&'. A trailing
    // '&' carries no pair, so the caller's pairs stay unchanged. This also
    // collapses a search that is only '?' or only '&' to empty.
    while (query.endsWith('&')) query = query.slice(0, -1);
    query = query === '' ? extraPairs.join('&') : query + '&' + extraPairs.join('&');
  }

  return query === '' ? rule.to : `${rule.to}?${query}`;
}
