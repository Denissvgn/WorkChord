import type { QueryClient } from '@tanstack/react-query';

export const WORK_QUERY_KEYS = ['tasks', 'task', 'gantt', 'workload', 'iterations', 'iteration', 'iterationSummary',
    'projects', 'project', 'projectSummary', 'projectTasks', 'projectPortfolioSummaries', 'taskTimeline', 'overview', 'releases', 'iteration-history', 'taskHistory', 'project-summary', 'release', 'portfolio', 'roadmap', 'savedViews', 'saved-view-dashboard', 'task-timeline', 'task-external-links', 'saved-view-dashboard-cards', 'saved-views', 'projectMilestones'];

export const installWorkFreshness = (client: QueryClient) => {
    for (const key of WORK_QUERY_KEYS) client.setQueryDefaults([key], {
        staleTime: 15000,
        refetchOnWindowFocus: true,
        refetchIntervalInBackground: false,
        refetchInterval: query => {
            const status = (query.state.error as { response?: { status?: number } } | null)?.response?.status;
            if (status === 401 || status === 403 || document.visibilityState === 'hidden') return false;
            return Math.min(300000, 30000 * 2 ** Math.min(query.state.fetchFailureCount, 3));
        },
    });
    return client.getMutationCache().subscribe(event => {
        if (event.type === 'updated' && event.action.type === 'success') {
            void client.invalidateQueries({ predicate: query => WORK_QUERY_KEYS.includes(String(query.queryKey[0])) });
        }
    });
};
