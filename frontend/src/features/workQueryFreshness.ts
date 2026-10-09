import type { QueryClient } from '@tanstack/react-query';

type QueryPolicy = 'live' | 'history' | 'editor' | 'reference' | 'settings' | 'identity';
const ROOTS_BY_POLICY: Record<QueryPolicy, readonly string[]> = {
    live: ['tasks', 'gantt', 'workload', 'iterations', 'iteration', 'iterationSummary', 'projects', 'project',
        'projectSummary', 'projectTasks', 'projectPortfolioSummaries', 'overview', 'releases', 'release', 'portfolio',
        'roadmap', 'savedViews', 'saved-view-dashboard', 'saved-view-dashboard-cards', 'saved-views', 'projectMilestones',
        'human-my-work', 'human-review-queue', 'personal-inbox', 'personal-deliveries', 'time-entries', 'time-report',
        'agent-pipeline', 'agent-assignments', 'agent-run-detail', 'backlog', 'calendars', 'capacity', 'profile-capacity',
        'profile-availability', 'delivery-dependencies', 'deliveryMetrics', 'discussion', 'executionUsage', 'initiatives',
        'iteration-overdue', 'projectIterations', 'projectReleases', 'projectUpdates', 'request-source-links',
        'request-sources', 'saved-view', 'snapshots', 'subscription', 'task-external-links', 'taskActions', 'taskBrowser',
        'team', 'teamMemberProfiles', 'triage', 'planning-navigation-summary', 'project-summary', 'live-window-head'],
    history: ['iteration-history', 'taskHistory', 'taskTimeline', 'task-timeline', 'comment-history', 'time-history'],
    editor: ['task', 'taskEditor', 'taskContext', 'routing-preview', 'gantt-schedule-preview', 'routing-assessment',
        'assigneeRecommendations'],
    reference: ['command-task-search', 'dependency-task-search', 'task-search', 'taskLookup', 'taskOwnerOptions',
        'mention-options', 'time-task-options', 'agent-profile-skill-catalog', 'agent-capabilities',
        'time-entry-capabilities', 'nativeConnection', 'plan-share'],
    settings: ['email-settings', 'system-settings', 'github-status-automation-rules', 'outbound-webhook-targets',
        'outbound-webhook-deliveries', 'scheduling-rules', 'labels', 'label-groups', 'templates', 'system-health',
        'agent-model-catalog', 'agent-model-bindings', 'agent-actor-roster', 'agent-team-setup'],
    identity: ['session', 'workspaceIdentity'],
};

export const WORKSPACE_QUERY_POLICIES: Readonly<Record<string, QueryPolicy>> = Object.fromEntries(
    Object.entries(ROOTS_BY_POLICY).flatMap(([policy, roots]) => roots.map(root => [root, policy as QueryPolicy])),
);

// Keep legacy roots eligible for mutation invalidation while callers adopt explicit effects.
export const WORK_QUERY_KEYS = [...ROOTS_BY_POLICY.live, ...ROOTS_BY_POLICY.history, ...ROOTS_BY_POLICY.editor,
    'project-summary'];

const MUTATION_ROOT_EFFECTS: Record<string, readonly string[]> = {
    tasks: WORK_QUERY_KEYS, planning: WORK_QUERY_KEYS, team: WORK_QUERY_KEYS,
    'time-entries': ['time-entries', 'time-report', 'time-history'],
    discussion: ['discussion', 'comment-history', 'personal-inbox', 'personal-deliveries'],
    'email-settings': [], 'outbound-webhook-settings': [], 'github-status-automation-rules': [],
};

export const installWorkFreshness = (client: QueryClient) => {
    for (const [root, policy] of Object.entries(WORKSPACE_QUERY_POLICIES)) {
        if (policy === 'identity') continue;
        client.setQueryDefaults([root], {
            retry: (count, error) => {
                const status = (error as { response?: { status?: number } })?.response?.status;
                return status !== 401 && status !== 403 && count < 1;
            },
            staleTime: policy === 'editor' ? 0 : 15000,
            refetchOnWindowFocus: policy !== 'editor' && policy !== 'history',
            refetchIntervalInBackground: false,
            refetchInterval: policy === 'live' ? query => {
                const status = (query.state.error as { response?: { status?: number } } | null)?.response?.status;
                const pages = (query.state.data as { pages?: unknown[] } | undefined)?.pages;
                if (!query.isActive() || status === 401 || status === 403 || document.visibilityState === 'hidden'
                    || pages && pages.length > 5) return false;
                return Math.min(300000, 30000 * 2 ** Math.min(query.state.fetchFailureCount, 3));
            } : false,
        });
    }
    const stopQueries = client.getQueryCache().subscribe(event => {
        if (event.type !== 'updated' || event.action.type !== 'error') return;
        const status = (event.query.state.error as { response?: { status?: number } } | null)?.response?.status;
        if (status === 401 || status === 403) event.query.setState({ data: undefined, dataUpdatedAt: 0 });
    });
    const stopMutations = client.getMutationCache().subscribe(event => {
        if (event.type !== 'updated' || event.action.type !== 'success') return;
        const explicit = event.mutation.options.meta?.workQueryRoots;
        const mapped = MUTATION_ROOT_EFFECTS[String(event.mutation.options.mutationKey?.[0])];
        const effects = Array.isArray(explicit) ? explicit.filter((value): value is string => typeof value === 'string')
            : mapped ?? WORK_QUERY_KEYS;
        if (effects.length) {
            const affected = (key: readonly unknown[]) => effects.includes(String(key[0] === 'live-window-head' ? key[1] : key[0]));
            void client.invalidateQueries({ predicate: query => affected(query.queryKey), refetchType: 'none' });
            void client.refetchQueries({ type: 'active', predicate: query => {
                const root = String(query.queryKey[0]);
                const pages = (query.state.data as { pages?: unknown[] } | undefined)?.pages;
                const status = (query.state.error as { response?: { status?: number } } | null)?.response?.status;
                return affected(query.queryKey) && WORKSPACE_QUERY_POLICIES[root] === 'live' && query.isActive()
                    && status !== 401 && status !== 403 && document.visibilityState !== 'hidden'
                    && !(pages && pages.length > 5);
            } });
        }
    });
    return () => { stopQueries(); stopMutations(); };
};
