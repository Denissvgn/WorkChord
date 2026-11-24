import { vi } from 'vitest';
import api from '../services/api';
import type { Task, TaskStatus } from '../types/task';

/**
 * A small workspace behind the HTTP client, for tests that open whole pages.
 * Every request a page makes is answered from these records; a request nobody
 * planned for fails with its own URL in the message, so a page that starts
 * asking for more shows up as a test failure instead of a silent empty state.
 */

const iteration = (id: number, project_id: number, start_date: string, end_date: string) => ({
    id, name: `Iteration ${id}`, calendar_id: 1, project_id, start_date, end_date, working_days: 10,
});

export const WORKSPACE_ITERATIONS = [
    iteration(11, 1, '2026-10-01', '2026-10-31'),
    iteration(12, 1, '2026-11-01', '2026-11-30'),
    iteration(21, 2, '2026-09-01', '2026-09-30'),
];

export const WORKSPACE_PROJECTS = [
    {
        id: 1, name: 'Alpha', description: 'First project', status: 'active', health: 'on_track', owner_id: null, owner: null,
        owner_profile_id: null, owner_profile: null, initiative_id: null, initiative: null, start_date: '2026-09-01',
        target_date: '2026-12-31', completed_at: null, sort_order: 1, created_at: '2026-09-01T00:00:00Z', updated_at: '2026-09-01T00:00:00Z',
    },
    {
        id: 2, name: 'Beta', description: null, status: 'active', health: 'on_track', owner_id: null, owner: null,
        owner_profile_id: null, owner_profile: null, initiative_id: null, initiative: null, start_date: null,
        target_date: null, completed_at: null, sort_order: 2, created_at: '2026-09-01T00:00:00Z', updated_at: '2026-09-01T00:00:00Z',
    },
];

const task = (id: number, iteration_id: number | null, status: TaskStatus): Task => ({
    id, title: `Task ${id}`, status, priority: 5, project_id: 1, iteration_id, effort_days: 1, effort_hours: 8,
    is_overdue: false, is_delayed: false, is_composite: false, is_optional: false, is_deferred: false, tags: [], sort_order: id,
    external_links: [], request_count: 0, version: 1, children: [], dependencies: [],
    agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] },
});

export const WORKSPACE_TASKS = [task(1, 12, 'planned'), task(2, 12, 'active'), task(3, null, 'planned')];

const page = <T,>(items: T[]) => ({ items, has_more: false, next_after_id: null, upper_id: items.length });

const durations = { unit: 'elapsed_seconds', sample_count: 0, mean: null, median: null, censored_count: 0, unknown_count: 0 };

const summary = (id: number) => ({
    ...WORKSPACE_ITERATIONS.find(item => item.id === id)!,
    total_tasks: 2, completed_tasks: 0, total_effort_days: 2, team_capacity_days: 10, overdue_tasks_count: 0,
    status_counts: { planned: 1, active: 1 }, blocked_tasks: 0, remaining_effort_days: 2, unknown_estimate_tasks: 0,
});

const gantt = (id: number) => ({
    iteration: WORKSPACE_ITERATIONS.find(item => item.id === id),
    tasks: [{ ...WORKSPACE_TASKS[0], start_date: '2026-11-02', end_date: '2026-11-03' }],
    overdue_task_ids: [], holidays: [], weekends: [], member_vacations: {}, schedule_result: null,
});

const readiness = (id: number) => ({
    iteration_id: id, team_member_count: 0, team_capacity_hours: 0, planned_hours: 16, assigned_hours: 0,
    team_members_no_capacity: 0, task_count: 2, tasks_without_assignee: 2, tasks_without_effort: 0, has_schedule: false, risk_count: 0,
    checkpoints: ['iteration', 'team', 'work', 'blockers', 'schedule', 'review'].map((id, index) => ({
        id, state: index === 0 ? 'done' : 'todo', reason_codes: [], counts: {},
    })),
    checkpoints_done: 1, checkpoints_total: 6,
});

const ROUTES: Array<[RegExp, (match: RegExpMatchArray) => unknown]> = [
    [/^\/projects\/page$/, () => page(WORKSPACE_PROJECTS)],
    [/^\/iterations\/page$/, () => page(WORKSPACE_ITERATIONS)],
    [/^\/iterations\/(\d+)\/gantt$/, match => gantt(Number(match[1]))],
    [/^\/iterations\/(\d+)\/summary$/, match => summary(Number(match[1]))],
    [/^\/iterations\/\d+\/tasks$/, () => WORKSPACE_TASKS.filter(item => item.iteration_id === 12)],
    [/^\/iterations\/\d+\/team$/, () => []],
    [/^\/iterations\/(\d+)\/planning-readiness$/, match => readiness(Number(match[1]))],
    [/^\/tasks\/lookup$/, () => ({ items: WORKSPACE_TASKS.filter(item => item.iteration_id === null), has_more: false, next_after_id: null })],
    [/^\/label-groups$/, () => []],
    [/^\/roadmap\/milestones$/, () => ({ items: [], next_cursor: null })],
    [/^\/saved-views$/, () => []],
    [/^\/session\/whoami$/, () => ({ id: 1, principal_id: null })],
    [/^\/tasks\/delivery-metrics$/, () => ({
        contract_version: 1, window_start: '2026-10-17T00:00:00Z', window_end: '2026-11-16T00:00:00Z', scope_basis: 'iteration',
        accepted_leaf_tasks: 0, acceptance_events: 0, rejection_events: 0, canceled_leaf_tasks: 0, reopened_events: 0,
        lead_time: durations, cycle_time: durations, review_delay: durations, coverage: {}, review_queue: [], recovery_queue: [],
        queues_truncated: false,
    })],
    [/^\/tasks\/execution-usage$/, () => ({
        window_start: '2026-10-17T00:00:00Z', window_end: '2026-11-16T00:00:00Z', window_basis: 'completed', expected_runs: 0,
        reported_runs: 0, unreported_runs: 0, partial_reports: 0, unavailable_reports: 0, simulated_reports: 0,
        measured_report_count: 0, provider_reported_cost: {}, estimated_cost: {}, known_cost_reports: {}, unknown_cost_reports: 0,
        accepted_task_identities: 0, reports_linked_to_accepted_tasks: 0, reported_human_effort_minutes: null,
        human_effort_reports: 0, reported_units: {}, unit_report_counts: {}, simulated_reported_cost: {},
        simulated_estimated_cost: {}, simulated_units: {}, independently_reconciled: false, advisory_budget: null,
    })],
];

/** Records of one concrete project, release and shared plan, for pages opened by id. */
export const WORKSPACE_RELEASE = {
    id: 5, project_id: 1, name: 'Release 1', description: 'First release', status: 'planned', target_date: '2026-12-01',
    shipped_at: null, version: '1.0', environment: null, task_ids: [], tasks: [], created_at: '2026-10-01T00:00:00Z',
    updated_at: '2026-10-01T00:00:00Z',
};

export const WORKSPACE_SHARE = {
    id: 3, public_id: 'shared-plan', iteration_id: 12, iteration_name: 'Iteration 12', created_by_display: 'Alex',
    created_at: '2026-11-01T00:00:00Z', revoked_at: null,
    snapshot_data: {
        iteration: { id: 12, name: 'Iteration 12', start_date: '2026-11-01', end_date: '2026-11-30' },
        tasks: [], team_members: [], snapshot_info: { created_at: '2026-11-01T00:00:00Z', reason: 'share' },
    },
};

const DETAIL_ROUTES: Array<[RegExp, (match: RegExpMatchArray) => unknown]> = [
    [/^\/projects\/(\d+)$/, match => WORKSPACE_PROJECTS.find(project => project.id === Number(match[1]))],
    [/^\/projects\/\d+\/(tasks|milestones|updates|iterations|releases)$/, () => []],
    [/^\/projects\/\d+\/summary$/, () => ({})],
    [/^\/releases\/(\d+)$/, () => WORKSPACE_RELEASE],
    [/^\/plan-shares\/[^/]+$/, () => WORKSPACE_SHARE],
];

/**
 * Answers every GET from the workspace above, with the unplanned ones failing by URL. `pending` lists the
 * GETs still waiting for an answer, so a page stuck on a read shows which one. Restored by `vi.restoreAllMocks`.
 */
export const installWorkspaceApi = (extra: Array<[RegExp, (match: RegExpMatchArray) => unknown]> = []) => {
    const unplanned: string[] = [];
    const pending: string[] = [];
    vi.spyOn(api, 'get').mockImplementation(async (url: string) => {
        const path = url.split('?')[0];
        pending.push(url);
        try {
            for (const [pattern, answer] of [...extra, ...ROUTES, ...DETAIL_ROUTES]) {
                const match = path.match(pattern);
                if (match) return { data: await answer(match) } as never;
            }
            unplanned.push(path);
            throw new Error(`Request nobody planned for: GET ${path}`);
        } finally {
            pending.splice(pending.indexOf(url), 1);
        }
    });
    return { unplanned, pending };
};
