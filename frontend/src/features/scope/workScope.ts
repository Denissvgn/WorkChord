import { matchPath } from 'react-router-dom';
import { DESTINATIONS, type DestinationId } from '../../navigation/destinations';
import { formatScope, parseScope } from '../../navigation/scopeParams';

/** One project or every project. */
export type ScopeProject = number | 'all';
/** One iteration, or work that has no iteration. */
export type ScopeIteration = number | 'backlog';

export interface WorkScope {
    project: ScopeProject;
    iteration: ScopeIteration;
}

/** A scope that may be incomplete: read from the URL, remembered, or just chosen. */
export interface PartialWorkScope {
    project?: ScopeProject | null;
    iteration?: ScopeIteration | null;
}

export interface ScopeIterationRecord {
    id: number;
    project_id?: number | null;
    start_date: string;
    end_date: string;
}

/** Pages that show and set the scope; on every other page the scope is read-only. */
export const SCOPED_DESTINATIONS: readonly DestinationId[] = ['overview', 'plan', 'gantt', 'tasks', 'analytics'];

/** Pages inside a scoped destination that show the same scope as the page it opens. */
const SCOPED_SUBPATHS: readonly string[] = ['/plan/master'];

const SCOPED_PATHS: readonly string[] = [
    ...DESTINATIONS.filter(destination => SCOPED_DESTINATIONS.includes(destination.id)).map(destination => destination.path),
    ...SCOPED_SUBPATHS,
];

/**
 * True for the page a scoped destination opens, and for the planning page inside Plan.
 * Paths are matched the way the router matches its routes, so variants such as a
 * trailing slash or different letter case count as the same page.
 */
export const isScopedPath = (pathname: string): boolean => (
    SCOPED_PATHS.some(path => matchPath({ path, caseSensitive: false, end: true }, pathname) !== null)
);

export const sameScope = (a: PartialWorkScope | undefined, b: PartialWorkScope | undefined): boolean => (
    (a?.project ?? null) === (b?.project ?? null) && (a?.iteration ?? null) === (b?.iteration ?? null)
);

export const isCompleteScope = (scope: PartialWorkScope): scope is WorkScope => (
    scope.project != null && scope.iteration != null
);

type DatedIteration = { id: number; start_date: string; end_date: string };

/**
 * The one rule every page uses when no valid iteration is selected: the
 * iteration that covers today, else the next upcoming one, else the most
 * recent. Dates are ISO calendar dates, so string comparison orders them.
 */
export const pickDefaultIteration = <T extends DatedIteration>(
    iterations: readonly T[],
    today: string = new Date().toISOString().slice(0, 10),
): T | undefined => {
    if (iterations.length === 0) return undefined;
    const current = iterations.find(item => item.start_date.slice(0, 10) <= today && today <= item.end_date.slice(0, 10));
    if (current) return current;
    const upcoming = iterations
        .filter(item => item.start_date.slice(0, 10) > today)
        .sort((a, b) => a.start_date.localeCompare(b.start_date))[0];
    if (upcoming) return upcoming;
    return [...iterations].sort((a, b) => b.end_date.localeCompare(a.end_date))[0];
};

/** An iteration without a project is only part of All projects. */
const projectOfIteration = (iteration: ScopeIterationRecord): ScopeProject => iteration.project_id ?? 'all';

const iterationsOfProject = <T extends ScopeIterationRecord>(iterations: readonly T[], project: ScopeProject): T[] => (
    project === 'all' ? [...iterations] : iterations.filter(iteration => iteration.project_id === project)
);

/**
 * The iteration a project opens on: the one that contains today, else the next one,
 * else the latest. A project without iterations opens on its Backlog.
 */
export const defaultIterationForProject = (
    iterations: readonly ScopeIterationRecord[],
    project: ScopeProject,
    today?: string,
): ScopeIteration => pickDefaultIteration(iterationsOfProject(iterations, project), today)?.id ?? 'backlog';

/**
 * Resolves the scope to show. Values in `primary` win over `fallback`; an iteration that
 * does not exist or is not part of the chosen project is replaced by the project's default.
 * With no project anywhere, the project is the one of the most recently used iteration,
 * else the one of the iteration the default rule picks across all projects.
 */
export const resolveWorkScope = (
    primary: PartialWorkScope,
    fallback: PartialWorkScope,
    iterations: readonly ScopeIterationRecord[],
    today?: string,
): WorkScope => {
    const byId = new Map(iterations.map(iteration => [iteration.id, iteration]));
    const knownIteration = (value: ScopeIteration | null | undefined) => (
        typeof value === 'number' ? byId.get(value) : undefined
    );

    const primaryIteration = knownIteration(primary.iteration);
    const fallbackIteration = knownIteration(fallback.iteration);
    const anyDefault = pickDefaultIteration(iterations, today);

    const project: ScopeProject = primary.project
        ?? (primaryIteration ? projectOfIteration(primaryIteration) : undefined)
        ?? fallback.project
        ?? (fallbackIteration ? projectOfIteration(fallbackIteration) : undefined)
        ?? (anyDefault ? projectOfIteration(anyDefault) : 'all');

    const fits = (value: ScopeIteration | null | undefined): value is ScopeIteration => {
        if (value === 'backlog') return true;
        const iteration = knownIteration(value);
        return iteration !== undefined && (project === 'all' || iteration.project_id === project);
    };

    const iteration = [primary.iteration, fallback.iteration].find(fits)
        ?? defaultIterationForProject(iterations, project, today);

    return { project, iteration };
};

/** The search string for a path with the scope written into it; other parameters are kept. */
export const withScopeSearch = (search: string, scope: WorkScope): string => formatScope(scope, search);

export const hasScopeParams = (search: string): boolean => {
    const parsed = parseScope(search);
    return parsed.project !== undefined || parsed.iteration !== undefined;
};

/**
 * Adds the scope to a link when it opens a scoped page. Other links, and links built
 * before any scope is known, are returned unchanged.
 */
export const scopedLink = (to: string, scope: WorkScope | undefined): string => {
    if (!scope) return to;
    const hashIndex = to.indexOf('#');
    const withoutHash = hashIndex === -1 ? to : to.slice(0, hashIndex);
    const hash = hashIndex === -1 ? '' : to.slice(hashIndex);
    const queryIndex = withoutHash.indexOf('?');
    const pathname = queryIndex === -1 ? withoutHash : withoutHash.slice(0, queryIndex);
    if (!isScopedPath(pathname)) return to;
    const search = queryIndex === -1 ? '' : withoutHash.slice(queryIndex);
    return `${pathname}${withScopeSearch(search, scope)}${hash}`;
};
