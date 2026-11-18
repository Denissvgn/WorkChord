import { useWorkScope } from '../../features/scope/useWorkScope';
import type { AnalyticsScope } from '../../types/analyticsScope';

export const useAnalyticsScope = (days: number): AnalyticsScope | undefined => {
    const { project, iteration, isReady } = useWorkScope();
    if (!isReady) return undefined;
    if (project === 'all') return { all_projects: true, all_projects_backlog: true, lookback_days: days };
    if (typeof iteration === 'number') return { iteration_id: iteration, lookback_days: days };
    if (typeof project === 'number') return { project_id: project, backlog: true, lookback_days: days };
    return undefined;
};
