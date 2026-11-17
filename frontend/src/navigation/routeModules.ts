import { matchPath } from 'react-router-dom';
import { getDestination, type DestinationId } from './destinations';
import { mapLegacyPath } from './legacyPaths';

export const routeModuleLoaders = {
    landing: () => import('../pages/LandingPage'),
    overview: () => import('../pages/OverviewPage'),
    plan: () => import('../pages/PlanPage'),
    planShare: () => import('../pages/PlanSharePage'),
    team: () => import('../pages/TeamPage'),
    tasks: () => import('../pages/TasksPage'),
    myWork: () => import('../pages/MyWorkPage'),
    nativeConnection: () => import('../pages/NativeConnectionPage'),
    triage: () => import('../pages/TriagePage'),
    projects: () => import('../pages/ProjectsPage'),
    projectDetail: () => import('../pages/ProjectDetailPage'),
    projectReleaseDetail: () => import('../pages/ProjectReleaseDetailPage'),
    gantt: () => import('../pages/GanttPage'),
    analytics: () => import('../pages/AnalyticsPage'),
    settings: () => import('../pages/SettingsPage'),
    notFound: () => import('../pages/NotFoundPage'),
} as const;

export type RouteModuleKey = keyof typeof routeModuleLoaders;

type RouteMetadata = {
    key: RouteModuleKey;
    path: string;
    titleKey: string;
};

// A destination's own page takes its title from the registry, so the document title and the
// sidebar label are the same vocabulary name.
const destinationTitle = (id: DestinationId) => getDestination(id).labelKey;

export const routeMetadata: RouteMetadata[] = [
    { key: 'landing', path: '/welcome', titleKey: 'documentTitles.landing' },
    { key: 'overview', path: '/', titleKey: destinationTitle('overview') },
    { key: 'planShare', path: '/plan/share/:publicId', titleKey: 'documentTitles.planShare' },
    { key: 'plan', path: '/plan', titleKey: destinationTitle('plan') },
    { key: 'team', path: '/team', titleKey: destinationTitle('team') },
    { key: 'myWork', path: '/my-work', titleKey: destinationTitle('my_work') },
    { key: 'nativeConnection', path: '/mobile/connect', titleKey: 'teamwork.connectRoute' },
    { key: 'tasks', path: '/tasks', titleKey: destinationTitle('tasks') },
    { key: 'triage', path: '/triage', titleKey: destinationTitle('triage') },
    { key: 'projectReleaseDetail', path: '/projects/:projectId/releases/:releaseId', titleKey: 'documentTitles.projectReleaseDetail' },
    { key: 'projectDetail', path: '/projects/:projectId', titleKey: 'documentTitles.projectDetail' },
    { key: 'projects', path: '/projects', titleKey: destinationTitle('projects') },
    { key: 'gantt', path: '/gantt', titleKey: destinationTitle('gantt') },
    { key: 'analytics', path: '/analytics', titleKey: destinationTitle('analytics') },
    { key: 'settings', path: '/settings', titleKey: destinationTitle('settings') },
];

export const metadataForPath = (pathname: string): RouteMetadata => {
    const legacyTarget = mapLegacyPath(pathname, '');
    const currentPath = legacyTarget?.split('?')[0] ?? pathname;
    return routeMetadata.find(route => matchPath({ path: route.path, end: true }, currentPath))
    ?? { key: 'notFound', path: '*', titleKey: 'documentTitles.notFound' }
};

export const warmRouteModule = async (pathname: string) => {
    await routeModuleLoaders[metadataForPath(pathname).key]();
};
