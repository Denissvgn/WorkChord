import {
    DESTINATIONS,
    getDestinationForPath,
    getDestinationGroup,
} from './destinations';
import { getWorkspaceForPath } from './workspaces';
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

export type GlossaryTerm = 'implemented' | 'accepted' | 'blocked' | 'overdue' | 'lateStart' | 'iterationOverflow'
    | 'unknownEstimate' | 'scheduled' | 'capacity' | 'triage' | 'agentReady';

// The terms each page shows, defined once in `contextHelp.glossary` from the server's own rules.
const DELIVERY_TERMS: readonly GlossaryTerm[] = ['implemented', 'accepted', 'blocked', 'overdue', 'lateStart', 'iterationOverflow'];
const SCHEDULE_TERMS: readonly GlossaryTerm[] = ['scheduled', 'capacity', 'lateStart', 'iterationOverflow', 'unknownEstimate'];
const GLOSSARY_BY_ROUTE: Partial<Record<RouteModuleKey, readonly GlossaryTerm[]>> = {
    overview: DELIVERY_TERMS,
    tasks: DELIVERY_TERMS,
    myWork: ['implemented', 'accepted', 'blocked'],
    projects: DELIVERY_TERMS,
    projectDetail: DELIVERY_TERMS,
    projectReleaseDetail: ['implemented', 'accepted'],
    analytics: DELIVERY_TERMS,
    triage: ['triage'],
    plan: SCHEDULE_TERMS,
    planMaster: SCHEDULE_TERMS,
    gantt: SCHEDULE_TERMS,
    roadmap: ['overdue', 'iterationOverflow'],
    iterations: ['capacity', 'scheduled'],
    calendar: ['capacity'],
    team: ['capacity', 'scheduled'],
    agentPipeline: ['agentReady', 'scheduled', 'blocked'],
    agentTeamSetup: ['agentReady'],
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
    const destination = DESTINATIONS.find(candidate => candidate.path === pathname);
    if (destination) {
        return {
            to,
            labelKey: destination.labelKey,
            defaultLabel: destination.defaultLabel,
        };
    }

    // A view or section of a destination is named by its page title; like i18next itself,
    // fall back to the key when a catalog lacks it.
    const route = metadataForPath(pathname);
    if (route.key !== 'notFound') {
        return { to, labelKey: route.titleKey, defaultLabel: route.titleKey };
    }

    return {
        to,
        labelKey: 'nav.overview',
        defaultLabel: 'Overview',
    };
};

export const getHelpContext = (pathname: string) => {
    const route = metadataForPath(pathname);
    const destination = getDestinationForPath(pathname);
    const configuredPaths = RELATED_PATHS_BY_ROUTE[route.key];
    // Without configured links, offer the other destinations of the same sidebar group.
    const fallbackPaths = destination
        ? getDestinationGroup(destination.id).destinations
            .filter(candidate => candidate.id !== destination.id)
            .slice(0, 3)
            .map(candidate => candidate.path)
        : DESTINATIONS.slice(0, 3).map(candidate => candidate.path);

    return {
        routeKey: route.key,
        pageTitleKey: route.titleKey,
        destination,
        // The current shell still frames help by its work area.
        workspace: getWorkspaceForPath(pathname),
        provider: CONTENT_PROVIDER_BY_ROUTE[route.key] ?? 'workspace',
        relatedLinks: (configuredPaths ?? fallbackPaths).map(relatedLinkForPath),
        glossary: GLOSSARY_BY_ROUTE[route.key] ?? [],
    };
};
