type Scope = { project: number | 'all'; iteration: number | 'backlog' };
type ParsedScope = Partial<Scope>;

function parsePositiveInt(s: string): number | undefined {
  if (/^\d+$/.test(s)) {
    const n = Number(s);
    if (n > 0) return n;
  }
  return undefined;
}

export function parseScope(search: string): ParsedScope {
  const raw = search.startsWith('?') ? search.slice(1) : search;
  const result: ParsedScope = {};
  if (raw === '') return result;

  const pairs = raw.split('&');
  let projectSeen = false;
  let iterationSeen = false;

  for (const pair of pairs) {
    const eqIdx = pair.indexOf('=');
    if (eqIdx === -1) continue;
    const key = pair.slice(0, eqIdx);
    const value = pair.slice(eqIdx + 1);

    if (key === 'project' && !projectSeen) {
      projectSeen = true;
      if (value === 'all') {
        result.project = 'all';
      } else {
        const n = parsePositiveInt(value);
        if (n !== undefined) result.project = n;
      }
    } else if (key === 'iteration' && !iterationSeen) {
      iterationSeen = true;
      if (value === 'backlog') {
        result.iteration = 'backlog';
      } else {
        const n = parsePositiveInt(value);
        if (n !== undefined) result.iteration = n;
      }
    }

    if (projectSeen && iterationSeen) break;
  }

  return result;
}

export function formatScope(scope: Scope, search: string): string {
  const raw = search.startsWith('?') ? search.slice(1) : search;

  let pairs: string[];
  if (raw === '') {
    pairs = [];
  } else {
    pairs = raw.split('&');
  }

  // Find and replace existing project/iteration keys in place.
  let projectReplaced = false;
  let iterationReplaced = false;

  for (let i = 0; i < pairs.length; i++) {
    const eqIdx = pairs[i].indexOf('=');
    if (eqIdx === -1) continue;
    const key = pairs[i].slice(0, eqIdx);
    if (key === 'project' && !projectReplaced) {
      pairs[i] = `project=${scope.project}`;
      projectReplaced = true;
    } else if (key === 'iteration' && !iterationReplaced) {
      pairs[i] = `iteration=${scope.iteration}`;
      iterationReplaced = true;
    }
  }

  // Append missing keys: project before iteration.
  if (!projectReplaced) {
    pairs.push(`project=${scope.project}`);
  }
  if (!iterationReplaced) {
    pairs.push(`iteration=${scope.iteration}`);
  }

  return '?' + pairs.join('&');
}
