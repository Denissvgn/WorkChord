import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import type { ReactElement } from 'react';
import type { AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import type { Project } from '../types/project';
import api from '../services/api';
import i18n from '../i18n/i18n';
import { mapLegacyPath } from '../navigation/legacyPaths';
import { clearAdminApiKey, setAdminApiKey } from '../utils/adminAccess';
import { clearAgentApiKey, setAgentApiKey } from '../utils/agentAccess';
import { useGetStartedVisibility } from '../features/firstRun/getStartedVisibility';
import { useScopeStore } from '../features/scope/scopeStore';
import { IdentityContext } from '../features/identity/identityContext';
import type { WorkspaceIdentity } from '../features/identity/identityService';
import { renderWithProviders } from '../test/renderWithProviders';
import OverviewPage from './OverviewPage';
import MyWorkPage from './MyWorkPage';
import TriagePage from './TriagePage';
import ProjectsPage from './ProjectsPage';
import PlanPage from './PlanPage';
import GanttPage from './GanttPage';
import TasksPage from './TasksPage';
import AnalyticsPage from './AnalyticsPage';
import TeamPage from './TeamPage';

/**
 * Every destination and view, rendered with the real pages and an empty service layer: each must show its
 * empty state with one sentence and one button, a filtered list with no results must offer Clear filters and no
 * create action, and no empty state may link to a path that redirects.
 */

type Scenario = {
    /** A profile is chosen in this workspace, so the first setup step is past it. */
    profile?: boolean;
    iterations?: unknown[];
    projects?: unknown[];
    triage?: unknown[];
    tasks?: unknown[];
    pipeline?: Record<string, unknown[]>;
    /** The admin-key view of Team models: a key that may administer, and the two lists it shows. */
    models?: { catalog: unknown[]; bindings: unknown[] };
};

const MODEL = { id: 1, key: 'atlas-model', provider: 'acme', configured_model_alias: 'atlas', reasoning_tier: 'standard',
    context_tier: 'standard', modality_tags: [], cost_tier: 'standard', latency_tier: 'standard', enabled: true, revision: 1,
    last_verified_at: null, created_at: '2026-08-01T00:00:00Z', updated_at: '2026-08-01T00:00:00Z' };

const BINDING = { id: 1, actor_id: 1, model_catalog_id: 1, is_default: true, enabled: true, tool_tags: [], data_policy_tags: [],
    revision: 1, model_catalog_key: 'atlas-model', selectable: true, model_catalog: MODEL, live_assignment_count: 0,
    historical_assignment_count: 0, run_reference_count: 0, created_at: '2026-08-01T00:00:00Z', updated_at: '2026-08-01T00:00:00Z' };

const ITERATION = { id: 1, name: 'August plan', calendar_id: 1, project: null, project_id: 1,
    start_date: '2026-08-03', end_date: '2026-08-14', working_days: 10 };

const TRIAGE = { id: 1, title: 'Export the weekly report', description: null, source: 'email', status: 'new',
    labels: [], metadata_json: {}, request_count: 0, created_at: '2026-08-01T00:00:00Z', updated_at: '2026-08-01T00:00:00Z' };

const task = (id: number) => ({
    id,
    iteration_id: 1,
    project_id: null,
    milestone_id: null,
    parent_id: null,
    title: `Task ${id}`,
    description: '',
    priority: id,
    effort_days: 1,
    effort_hours: 8,
    project: null,
    milestone: null,
    assignee: null,
    status: 'planned',
    start_date: null,
    end_date: null,
    actual_start_date: null,
    actual_end_date: null,
    min_start_date: null,
    max_end_date: null,
    is_overdue: false,
    is_delayed: false,
    is_composite: false,
    is_optional: false,
    is_deferred: false,
    tags: [],
    sort_order: id,
    external_links: [],
    request_count: 0,
    agent_readiness: {
        is_ready: true,
        blockers: [],
        warnings: [],
        criteria: [],
    },
    version: 1,
    children: [],
    dependencies: [],
});

const PROJECT = {
    id: 1,
    name: 'Atlas',
    description: null,
    status: 'active',
    health: 'on_track',
    owner_id: null,
    owner: null,
    owner_profile_id: null,
    owner_profile: null,
    initiative_id: null,
    initiative: null,
    start_date: '2026-08-01',
    target_date: '2026-09-01',
    completed_at: null,
    sort_order: 1,
    created_at: '2026-08-01T00:00:00Z',
    updated_at: '2026-08-01T00:00:00Z',
} as unknown as Project;

const PAGE = { has_more: false, next_after_id: null, upper_id: 0, limit: 100 };
const GUEST = { id: 1, public_id: 'guest0001', display_name: 'Guest', authenticated: false, principal_id: null,
    created_at: '2026-08-01T00:00:00Z', last_seen_at: '2026-08-01T00:00:00Z' };

let scenario: Scenario = {};

const respond = (fullUrl: string) => {
    const [url, query = ''] = fullUrl.split('?');
    if (url === '/session/whoami') return GUEST;
    if (url === '/iterations/page') return { ...PAGE, items: scenario.iterations ?? [] };
    if (url === '/projects/page') return { ...PAGE, items: scenario.projects ?? [] };
    if (url === '/projects/portfolio-summaries/page') return { ...PAGE, items: [] };
    // Triage search runs on the server: a search that matches nothing returns no rows.
    if (url === '/triage') return new URLSearchParams(query).get('q') ? [] : (scenario.triage ?? []);
    if (/^\/iterations\/\d+\/tasks$/.test(url)) return scenario.tasks ?? [];
    if (url === '/tasks/lookup') return { ...PAGE, items: [] };
    if (url === '/agent/pipeline') {
        return { needs_definition: [], ready_to_assign: [], assigned_waiting: [], start_ready: [], executing: [],
            verification_required: [], recovery_required: [], ...scenario.pipeline };
    }
    if (scenario.models && url === '/agent/capabilities') return { scopes: ['admin'] };
    if (scenario.models && url === '/agent/model-catalog') return scenario.models.catalog;
    if (scenario.models && url === '/agent/model-bindings') return scenario.models.bindings;
    if (url === '/tasks/my-work') return { state: 'ready', queues: {}, has_more: false, next_after_id: null };
    if (url === '/tasks/review-queue' || url === '/notifications') return { ...PAGE, items: [] };
    return [];
};

const originalAdapter = api.defaults.adapter;
beforeEach(() => {
    scenario = {};
    // Module-level stores outlive a render; each case starts with the first-run and scope state of a new browser.
    useGetStartedVisibility.setState({ dismissed: false, requested: false });
    useScopeStore.setState({ project: null, iteration: null });
    api.defaults.adapter = (async (config: InternalAxiosRequestConfig) => ({
        data: respond(String(config.url ?? '')),
        status: 200,
        statusText: 'OK',
        headers: {},
        config,
        request: {},
    }) as AxiosResponse) as unknown as typeof api.defaults.adapter;
});
afterEach(() => {
    api.defaults.adapter = originalAdapter;
    clearAdminApiKey();
    clearAgentApiKey();
});

type Case = {
    name: string;
    path: string;
    page: () => ReactElement;
    scenario?: Scenario;
    /** The copy key the page's (first) empty state must show. */
    copy?: string;
    /** Text typed into the page's search box before the empty state is read. */
    typeSearch?: string;
    /** A list that filters hide: it must offer Clear filters. */
    filtered?: boolean;
    adminKey?: boolean;
    /** The agent key the Models tab needs before it reads anything. */
    agentKey?: boolean;
    /** Copy keys of controls that must not appear on the page: competing actions of an empty workspace. */
    absent?: string[];
    /** Rendered with the shell's identity, so the first-run step decides the page's one next step. */
    setup?: boolean;
};

/** The text a node shows itself, without its children's text, so a button's icon does not hide its label. */
const ownText = (element: Element) => Array.from(element.childNodes)
    .filter(node => node.nodeType === Node.TEXT_NODE)
    .map(node => node.textContent ?? '')
    .join('')
    .trim();

const CASES: Case[] = [
    { name: 'Overview without an iteration', path: '/', page: () => <OverviewPage />, copy: 'emptyStates.overview.iterationBody' },
    { name: 'Overview with an iteration and no work', path: '/', page: () => <OverviewPage />, scenario: { iterations: [ITERATION] } },
    { name: 'My Work', path: '/my-work', page: () => <MyWorkPage /> },
    {
        name: 'Triage',
        path: '/triage',
        page: () => <TriagePage />,
        setup: true,
        copy: 'emptyStates.triage.emptyBody',
        // Empty workspace: no iteration notice and no second call to action.
        absent: ['surfaces.triagePage.createIteration', 'surfaces.triagePage.conversionRequiresAnIteration'],
    },
    { name: 'Triage filtered', path: '/triage', page: () => <TriagePage />, scenario: { triage: [TRIAGE] }, typeSearch: 'no-such-request', filtered: true },
    { name: 'Projects', path: '/projects', page: () => <ProjectsPage />, copy: 'emptyStates.projects.body' },
    { name: 'Projects filtered', path: '/projects?q=no-such-project', page: () => <ProjectsPage />, scenario: { projects: [PROJECT] }, filtered: true },
    { name: 'Roadmap', path: '/projects?view=roadmap', page: () => <ProjectsPage />, copy: 'emptyStates.projects.body' },
    { name: 'Roadmap filtered', path: '/projects?view=roadmap&q=no-such-project', page: () => <ProjectsPage />, scenario: { projects: [PROJECT] }, filtered: true },
    {
        name: 'Plan',
        path: '/plan',
        page: () => <PlanPage />,
        setup: true,
        copy: 'emptyStates.plan.body',
        // Empty workspace: the checkpoint actions wait until the setup step before them is done.
        absent: ['iterations.newIteration', 'iterations.allIterations'],
    },
    { name: 'Gantt', path: '/gantt', page: () => <GanttPage />, copy: 'emptyStates.gantt.body' },
    {
        name: 'Tasks backlog',
        path: '/tasks',
        page: () => <TasksPage />,
        setup: true,
        copy: 'emptyStates.tasks.backlogBody',
        // Empty workspace: no capture control and no iteration action beside the one setup step.
        absent: ['teamwork.captureTask', 'firstRun.steps.iteration.title'],
    },
    { name: 'Tasks list', path: '/tasks?iteration=1', page: () => <TasksPage />, scenario: { iterations: [ITERATION] }, copy: 'emptyStates.tasks.body' },
    { name: 'Tasks list filtered', path: '/tasks?iteration=1&q=no-such-task', page: () => <TasksPage />, scenario: { iterations: [ITERATION], tasks: [task(1)] }, filtered: true },
    { name: 'Tasks board', path: '/tasks?iteration=1&layout=board', page: () => <TasksPage />, scenario: { iterations: [ITERATION] }, copy: 'emptyStates.tasks.body' },
    { name: 'Tasks board filtered', path: '/tasks?iteration=1&layout=board&q=no-such-task', page: () => <TasksPage />, scenario: { iterations: [ITERATION], tasks: [task(1)] }, filtered: true },
    { name: 'Tasks pipeline', path: '/tasks?layout=pipeline', page: () => <TasksPage />, adminKey: true, copy: 'emptyStates.pipeline.body' },
    { name: 'Tasks pipeline filtered', path: '/tasks?layout=pipeline&q=no-such-task', page: () => <TasksPage />, adminKey: true, scenario: { pipeline: { executing: [task(1)] } }, filtered: true },
    { name: 'Analytics', path: '/analytics', page: () => <AnalyticsPage />, copy: 'emptyStates.analytics.body' },
    { name: 'Team members', path: '/team', page: () => <TeamPage />, copy: 'emptyStates.team.membersBody' },
    { name: 'Team models without the admin key', path: '/team?tab=models', page: () => <TeamPage />, copy: 'emptyStates.team.modelsBody' },
    { name: 'Team models with an empty catalog and no bindings', path: '/team?tab=models', page: () => <TeamPage />, agentKey: true,
        scenario: { models: { catalog: [], bindings: [] } }, copy: 'emptyStates.team.catalogBody' },
    // One list empty and the other filled: each empty state is checked on its own.
    { name: 'Team models with an empty model catalog', path: '/team?tab=models', page: () => <TeamPage />, agentKey: true,
        scenario: { models: { catalog: [], bindings: [BINDING] } }, copy: 'emptyStates.team.catalogBody' },
    { name: 'Team models with an empty bindings list', path: '/team?tab=models', page: () => <TeamPage />, agentKey: true,
        scenario: { models: { catalog: [MODEL], bindings: [] } }, copy: 'emptyStates.team.bindingsBody' },
    { name: 'Team connect without the admin key', path: '/team?tab=connect', page: () => <TeamPage />, copy: 'emptyStates.team.connectBody' },
];

const LANGUAGES = ['en', 'ru'] as const;
type Language = (typeof LANGUAGES)[number];

/** Terminal punctuation that ends a sentence: a full stop, question or exclamation mark followed by a space or the end. */
const sentenceCount = (text: string) => (text.match(/[.!?](?=\s|$)/g) ?? []).length;

/** The shell provides the identity to every page; a workspace starts with no profile chosen. */
const localIdentity = (profile: WorkspaceIdentity['profile']): WorkspaceIdentity => ({
    mode: 'trusted_local',
    authenticated: true,
    configured: true,
    principal: null,
    profile,
    workspace_role: 'owner',
    projects: {},
    csrf_token: null,
    access: 'full',
});

const withIdentity = (page: ReactElement) => (
    <IdentityContext.Provider value={{
        identity: localIdentity(scenario.profile ? { id: 1, display_name: 'Ada Lovelace' } : null),
        refresh: () => {},
        signOut: async () => {},
    }}>
        {page}
    </IdentityContext.Provider>
);

/** Renders a case in one language and returns its empty states once they have appeared. */
const renderCase = async (testCase: Case, language: Language) => {
    await i18n.changeLanguage(language);
    scenario = testCase.scenario ?? {};
    if (testCase.adminKey) setAdminApiKey('operator-key');
    if (testCase.agentKey) setAgentApiKey('operator-key');
    const page = testCase.setup ? withIdentity(testCase.page()) : testCase.page();
    const view = renderWithProviders(page, { initialEntries: [testCase.path] });
    if (testCase.typeSearch) {
        await view.user.type(await screen.findByPlaceholderText(i18n.t('surfaces.triagePage.searchTitleDescriptionSourceKey')), testCase.typeSearch);
    }
    await waitFor(() => {
        expect(view.container.querySelectorAll('.inline-empty').length).toBeGreaterThan(0);
    }, { timeout: 8000 });
    return Array.from(view.container.querySelectorAll<HTMLElement>('.inline-empty'));
};

const actionsOf = (state: HTMLElement) => Array.from(state.querySelectorAll<HTMLElement>('.inline-empty-actions > *'));

/** Whether any element on the rendered page shows this text itself. */
const shownText = (text: string) => Array.from(document.body.querySelectorAll('*')).some(element => ownText(element) === text);

describe('destination and view empty states', () => {
    it.each(
        CASES.flatMap(testCase => LANGUAGES.map(language => ({ testCase, language })))
            .map(({ testCase, language }) => ({ name: testCase.name, language, testCase })),
    )('$name shows one sentence and one next step ($language)', async ({ testCase, language }) => {
        const states = await renderCase(testCase, language);
        expect(states.length).toBeGreaterThan(0);
        for (const state of states) {
            const copy = state.querySelectorAll('.inline-empty-copy');
            expect(copy, 'one sentence').toHaveLength(1);
            expect(sentenceCount(copy[0].textContent ?? ''), copy[0].textContent ?? '').toBe(1);
            expect(actionsOf(state), 'one button').toHaveLength(1);
        }
        if (testCase.copy) {
            expect(states[0].querySelector('.inline-empty-copy')?.textContent).toBe(i18n.t(testCase.copy, { lng: language }));
        }
        for (const key of testCase.absent ?? []) {
            // The setup progress that decides these controls arrives after the first render: wait for it to settle.
            await waitFor(() => {
                expect(shownText(i18n.t(key, { lng: language })), `${key} must not be shown beside the empty state`).toBe(false);
            }, { timeout: 8000 });
        }
    }, 30000);

    it.each(CASES.filter(testCase => testCase.filtered).flatMap(testCase => LANGUAGES.map(language => ({
        name: testCase.name, language, testCase,
    }))))('$name offers Clear filters and no create action ($language)', async ({ testCase, language }) => {
        const states = await renderCase(testCase, language);
        expect(states.length).toBeGreaterThan(0);
        const [action] = actionsOf(states[0]);
        expect(actionsOf(states[0])).toHaveLength(1);
        expect(action.textContent).toBe(i18n.t('emptyStates.filtered.clear', { lng: language }));
        expect(states[0].querySelector('.inline-empty-title')?.textContent).toBe(i18n.t('emptyStates.filtered.title', { lng: language }));
    }, 30000);

    it.each(LANGUAGES.map(language => ({ language })))(
        'Overview with work elsewhere shows no next-step button in an empty Work now list ($language)',
        async ({ language }) => {
            await i18n.changeLanguage(language);
            scenario = { iterations: [ITERATION], tasks: [{ ...task(1), status: 'closed' }] };
            const view = renderWithProviders(<OverviewPage />, { initialEntries: ['/'] });
            const note = i18n.t('overview.noWorkNow', { lng: language });
            await waitFor(() => { expect(view.container.querySelector('.overview-work-now')?.textContent ?? '').toContain(note); }, { timeout: 8000 });
            const section = view.container.querySelector('.overview-work-now') as HTMLElement;
            expect(section.querySelectorAll('.inline-empty')).toHaveLength(0);
            expect(section.querySelectorAll('.inline-empty-actions')).toHaveLength(0);
        },
        30000,
    );

    it.each(LANGUAGES.map(language => ({ language })))(
        'Plan with a project and no iteration leaves New iteration as the one next step ($language)',
        async ({ language }) => {
            await i18n.changeLanguage(language);
            scenario = { profile: true, projects: [PROJECT] };
            renderWithProviders(withIdentity(<PlanPage />), { initialEntries: ['/plan'] });
            // The Iteration checkpoint owns the step: no separate empty state, and no All iterations with nothing to list.
            await waitFor(() => {
                expect(document.querySelectorAll('.inline-empty')).toHaveLength(0);
                expect(shownText(i18n.t('iterations.allIterations', { lng: language }))).toBe(false);
                expect(shownText(i18n.t('iterations.newIteration', { lng: language }))).toBe(true);
            }, { timeout: 8000 });
        },
        30000,
    );

    it.each(CASES.map(testCase => ({ name: testCase.name, testCase })))('$name links to no redirecting path', async ({ testCase }) => {
        const states = await renderCase(testCase, 'en');
        const links = states.flatMap(state => Array.from(state.querySelectorAll<HTMLAnchorElement>('.inline-empty-actions a')));
        for (const link of links) {
            const href = link.getAttribute('href') ?? '';
            const url = new URL(href, 'http://workchord.local');
            expect(mapLegacyPath(url.pathname, url.search), href).toBeNull();
        }
    }, 30000);
});
