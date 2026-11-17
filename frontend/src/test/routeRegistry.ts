import type { RouteModuleKey } from '../navigation/routeModules';

/**
 * `page` routes open with the shared page header. A `public` route is a page of its own outside the
 * workspace frame (the landing page): it keeps one top-level heading and the shared controls.
 */
type RouteStatus = { key: RouteModuleKey; status: 'migrated' | 'pending'; path: string; frame?: 'page' | 'public' };
export const routeRegistry: RouteStatus[] = [
    { key: 'landing', path: '/welcome', status: 'migrated', frame: 'public' },
    { key: 'overview', path: '/', status: 'migrated' },
    { key: 'planMaster', path: '/plan/master', status: 'migrated' },
    { key: 'planShare', path: '/plan/share/:publicId', status: 'migrated' },
    { key: 'plan', path: '/plan', status: 'migrated' },
    { key: 'calendar', path: '/calendar', status: 'migrated' },
    { key: 'iterations', path: '/iterations', status: 'migrated' },
    { key: 'team', path: '/team', status: 'migrated' },
    { key: 'myWork', path: '/my-work', status: 'migrated' },
    { key: 'nativeConnection', path: '/mobile/connect', status: 'migrated' },
    { key: 'tasks', path: '/tasks', status: 'migrated' },
    { key: 'triage', path: '/triage', status: 'migrated' },
    { key: 'projectReleaseDetail', path: '/projects/:projectId/releases/:releaseId', status: 'migrated' },
    { key: 'projectDetail', path: '/projects/:projectId', status: 'migrated' },
    { key: 'projects', path: '/projects', status: 'migrated' },
    { key: 'roadmap', path: '/roadmap', status: 'migrated' },
    { key: 'gantt', path: '/gantt', status: 'migrated' },
    { key: 'analytics', path: '/analytics', status: 'migrated' },
    { key: 'settings', path: '/settings', status: 'migrated' },
    { key: 'agentPipeline', path: '/agent-pipeline', status: 'migrated' },
    { key: 'agentTeamSetup', path: '/agent-team/setup', status: 'migrated' },
    { key: 'notFound', path: '*', status: 'migrated' },
];
