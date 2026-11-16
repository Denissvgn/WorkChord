import { compareAsc, parseISO } from 'date-fns';
import type { Initiative, Project, ProjectHealth, ProjectStatus } from '../../types/project';

/** The two views of the portfolio. */
export type PortfolioView = 'list' | 'roadmap';

/**
 * Everything that narrows the portfolio, as it is kept in the address bar.
 * Both views read the same values, so switching views keeps them.
 */
export type PortfolioFilters = {
    search: string;
    status: ProjectStatus | '';
    health: ProjectHealth | '';
    /** `profile:<id>`, `member:<id>` or `none`. */
    owner: string;
    /** An initiative id or `none`. */
    initiative: string;
    /** Set by the at-risk count: at risk or off track. */
    attention: 'at_risk' | '';
};

export const PORTFOLIO_PARAMS = {
    view: 'view',
    search: 'q',
    status: 'status',
    health: 'health',
    owner: 'owner',
    initiative: 'initiative',
    attention: 'attention',
    from: 'from',
    to: 'to',
} as const;

/** Value of the owner and initiative filters for projects that have none. */
export const NONE_VALUE = 'none';

export const PROJECT_STATUSES: readonly ProjectStatus[] = ['proposed', 'planned', 'active', 'paused', 'completed', 'canceled'];
export const PROJECT_HEALTHS: readonly ProjectHealth[] = ['unknown', 'on_track', 'at_risk', 'off_track'];

const isoDate = /^\d{4}-\d{2}-\d{2}$/;

/** The view named in the address; a saved-view id or anything else shows the list. */
export const readPortfolioView = (params: URLSearchParams): PortfolioView => (
    params.get(PORTFOLIO_PARAMS.view) === 'roadmap' ? 'roadmap' : 'list'
);

/** A numeric `view` value opens a saved view, as links from the command menu do. */
export const readSavedViewId = (params: URLSearchParams): number | null => {
    const value = params.get(PORTFOLIO_PARAMS.view);
    return value && /^[1-9][0-9]*$/.test(value) ? Number(value) : null;
};

export const readPortfolioFilters = (params: URLSearchParams): PortfolioFilters => {
    const status = params.get(PORTFOLIO_PARAMS.status) ?? '';
    const health = params.get(PORTFOLIO_PARAMS.health) ?? '';
    return {
        search: params.get(PORTFOLIO_PARAMS.search) ?? '',
        status: (PROJECT_STATUSES as readonly string[]).includes(status) ? status as ProjectStatus : '',
        health: (PROJECT_HEALTHS as readonly string[]).includes(health) ? health as ProjectHealth : '',
        owner: params.get(PORTFOLIO_PARAMS.owner) ?? '',
        initiative: params.get(PORTFOLIO_PARAMS.initiative) ?? '',
        attention: params.get(PORTFOLIO_PARAMS.attention) === 'at_risk' ? 'at_risk' : '',
    };
};

/** The timeline window set by a preset; empty when the timeline fits its projects. */
export const readTimelineWindow = (params: URLSearchParams) => {
    const from = params.get(PORTFOLIO_PARAMS.from) ?? '';
    const to = params.get(PORTFOLIO_PARAMS.to) ?? '';
    return { from: isoDate.test(from) ? from : '', to: isoDate.test(to) ? to : '' };
};

export const hasActiveFilters = (filters: PortfolioFilters) => Boolean(
    filters.search.trim() || filters.status || filters.health || filters.owner || filters.initiative || filters.attention,
);

export const ownerKeyForProject = (project: Pick<Project, 'owner_profile_id' | 'owner_id'>) => {
    if (project.owner_profile_id) return `profile:${project.owner_profile_id}`;
    if (project.owner_id) return `member:${project.owner_id}`;
    return null;
};

export const matchesPortfolioFilters = (project: Project, filters: PortfolioFilters) => {
    const search = filters.search.trim().toLowerCase();
    if (search && !project.name.toLowerCase().includes(search)) return false;
    if (filters.status && project.status !== filters.status) return false;
    if (filters.health && project.health !== filters.health) return false;
    if (filters.attention === 'at_risk' && !['at_risk', 'off_track'].includes(project.health)) return false;
    if (filters.owner) {
        const ownerKey = ownerKeyForProject(project);
        if (filters.owner === NONE_VALUE ? ownerKey !== null : ownerKey !== filters.owner) return false;
    }
    if (filters.initiative) {
        if (filters.initiative === NONE_VALUE ? project.initiative_id : project.initiative_id !== Number(filters.initiative)) return false;
    }
    return true;
};

export type InitiativeGroupInfo = Pick<
    Initiative,
    'id' | 'name' | 'owner_id' | 'owner' | 'owner_profile_id' | 'owner_profile' | 'health' | 'target_date'
> & Partial<Pick<Initiative, 'description'>>;

export type InitiativeGroup<T> = {
    key: string;
    /** Null for the projects that belong to no initiative. */
    initiative: InitiativeGroupInfo | null;
    items: T[];
};

const parseDate = (value?: string | null) => {
    if (!value) return null;
    const parsed = parseISO(value);
    return Number.isNaN(parsed.getTime()) ? null : parsed;
};

/** Earliest target date first, undated initiatives after, then by name. */
export const compareInitiatives = (a: InitiativeGroupInfo, b: InitiativeGroupInfo) => {
    const aTarget = parseDate(a.target_date);
    const bTarget = parseDate(b.target_date);
    if (aTarget && bTarget) {
        const delta = compareAsc(aTarget, bTarget);
        if (delta !== 0) return delta;
    }
    if (aTarget && !bTarget) return -1;
    if (!aTarget && bTarget) return 1;
    return a.name.localeCompare(b.name) || a.id - b.id;
};

/**
 * Puts each item under its project's initiative, keeping the items' order inside
 * a group. Initiatives come in target-date order and "No initiative" comes last.
 * With `includeEmpty`, initiatives without matching projects still get a group,
 * so they can be seen and edited.
 */
export const groupByInitiative = <T,>(
    items: T[],
    projectOf: (item: T) => Project,
    initiatives: Initiative[],
    includeEmpty: boolean,
): InitiativeGroup<T>[] => {
    const initiativesById = new Map(initiatives.map(initiative => [initiative.id, initiative]));
    const groups = new Map<string, InitiativeGroup<T>>();
    if (includeEmpty) {
        initiatives.forEach(initiative => {
            groups.set(`initiative-${initiative.id}`, { key: `initiative-${initiative.id}`, initiative, items: [] });
        });
    }
    const unassignedItems: T[] = [];
    items.forEach(item => {
        const project = projectOf(item);
        const initiativeId = project.initiative_id;
        if (!initiativeId) {
            unassignedItems.push(item);
            return;
        }
        const key = `initiative-${initiativeId}`;
        if (!groups.has(key)) {
            const initiative: InitiativeGroupInfo = initiativesById.get(initiativeId) ?? project.initiative ?? {
                id: initiativeId,
                name: `#${initiativeId}`,
                owner_id: null,
                owner: null,
                owner_profile_id: null,
                owner_profile: null,
                health: 'unknown',
                target_date: null,
            };
            groups.set(key, { key, initiative, items: [] });
        }
        groups.get(key)!.items.push(item);
    });
    const sorted = Array.from(groups.values()).sort((a, b) => compareInitiatives(a.initiative!, b.initiative!));
    return unassignedItems.length > 0
        ? [...sorted, { key: 'unassigned', initiative: null, items: unassignedItems }]
        : sorted;
};
