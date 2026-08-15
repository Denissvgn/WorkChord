import {
    getWorkspaceForPath,
    PRIMARY_NAV_ITEMS,
} from './workspaces';
import {
    metadataForPath,
    type RouteModuleKey,
} from './routeModules';

export type HelpContentProvider = 'plan' | 'gantt' | 'tasks' | 'settings' | 'workspace';

export type HelpRelatedLink = {
    to: string;
    labelKey: string;
    defaultLabel: string;
    descriptionKey?: string;
};

const CONTENT_PROVIDER_BY_ROUTE: Partial<Record<RouteModuleKey, HelpContentProvider>> = {
    plan: 'plan',
    planMaster: 'plan',
    planShare: 'plan',
    gantt: 'gantt',
    tasks: 'tasks',
    settings: 'settings',
};

const RELATED_PATHS_BY_ROUTE: Partial<Record<RouteModuleKey, readonly string[]>> = {
    overview: ['/tasks', '/triage'],
    tasks: ['/plan', '/triage'],
    triage: ['/tasks', '/projects'],
    projects: ['/tasks', '/roadmap'],
    projectDetail: ['/tasks', '/roadmap'],
    projectReleaseDetail: ['/tasks', '/roadmap'],
    agentPipeline: ['/agent-team/setup', '/tasks'],
    plan: ['/plan/master', '/gantt'],
    planMaster: ['/tasks', '/gantt'],
    planShare: ['/plan', '/gantt'],
    gantt: ['/plan', '/iterations', '/settings?tab=scheduling'],
    roadmap: ['/projects', '/plan'],
    iterations: ['/calendar', '/team', '/plan'],
    calendar: ['/iterations', '/team'],
    team: ['/calendar', '/settings'],
    analytics: ['/team', '/tasks'],
    settings: ['/team', '/agent-team/setup'],
    agentTeamSetup: ['/agent-pipeline', '/settings?tab=models_agents'],
    notFound: ['/'],
};

const SPECIAL_RELATED_LINKS: Record<string, Omit<HelpRelatedLink, 'to'>> = {
    '/plan/master': {
        labelKey: 'documentTitles.planMaster',
        defaultLabel: 'Planning workspace',
    },
    '/settings?tab=scheduling': {
        labelKey: 'settingsPage.scheduling',
        defaultLabel: 'Scheduling',
        descriptionKey: 'settingsPage.descriptions.scheduling',
    },
    '/settings?tab=github': {
        labelKey: 'settingsPage.github',
        defaultLabel: 'GitHub',
        descriptionKey: 'settingsPage.descriptions.github',
    },
    '/settings?tab=models_agents': {
        labelKey: 'settingsPage.modelsAgents',
        defaultLabel: 'Models & agents',
        descriptionKey: 'settingsPage.descriptions.modelsAgents',
    },
};

const relatedLinkForPath = (to: string): HelpRelatedLink => {
    const special = SPECIAL_RELATED_LINKS[to];
    if (special) return { to, ...special };

    const pathname = to.split('?')[0] ?? to;
    const navItem = PRIMARY_NAV_ITEMS.find(item => item.to === pathname);
    if (navItem) {
        return {
            to,
            labelKey: navItem.labelKey,
            defaultLabel: navItem.defaultLabel,
        };
    }

    return {
        to,
        labelKey: 'nav.overview',
        defaultLabel: 'Overview',
    };
};

const routeContainsItem = (pathname: string, itemPath: string) => (
    itemPath === '/'
        ? pathname === '/'
        : pathname === itemPath || pathname.startsWith(`${itemPath}/`)
);

export const getHelpContext = (pathname: string) => {
    const route = metadataForPath(pathname);
    const workspace = getWorkspaceForPath(pathname);
    const configuredPaths = RELATED_PATHS_BY_ROUTE[route.key];
    const fallbackPaths = workspace.items
        .filter(item => !routeContainsItem(pathname, item.to))
        .slice(0, 3)
        .map(item => item.to);

    return {
        routeKey: route.key,
        pageTitleKey: route.titleKey,
        workspace,
        provider: CONTENT_PROVIDER_BY_ROUTE[route.key] ?? 'workspace',
        relatedLinks: (configuredPaths ?? fallbackPaths).map(relatedLinkForPath),
    };
};
