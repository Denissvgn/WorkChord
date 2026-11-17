import i18n, { ensureLanguageResources } from '../i18n/i18n';
import { SETTINGS_FIELD_LABEL_KEYS } from '../components/settings/settingsFieldLabels';
import type { SettingsSectionId } from '../components/settings/settingsFieldLabels';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { render, screen, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClientProvider } from '@tanstack/react-query';
import { createMemoryRouter, RouterProvider } from 'react-router-dom';
import { computeAccessibleName } from 'dom-accessibility-api';
import { createTestQueryClient, renderWithProviders } from '../test/renderWithProviders';
import { ToastProvider } from '../components/feedback/ToastProvider';
import { IdentityContext } from '../features/identity/identityContext';
import { identityService, type WorkspaceIdentity } from '../features/identity/identityService';
import type { WorkTemplate } from '../types/template';
import type { LabelGroup } from '../types/label';
import type { SchedulingRulesResponse } from '../types/schedulingRules';
import type { OutboundWebhookTarget } from '../types/outboundWebhook';
import type { GitHubStatusAutomationRule } from '../types/github';
import type { SystemSettings } from '../types/systemSettings';
import SettingsPage from './SettingsPage';

const adminAccessMock = vi.hoisted(() => ({ hasAdminKey: true }));
vi.mock('../hooks/useAdminAccess', () => ({
    useAdminAccess: () => ({ hasAdminKey: adminAccessMock.hasAdminKey, hasAdminAccess: adminAccessMock.hasAdminKey }),
    useCanReadSettings: () => true,
    useKeylessReader: () => ({ settings: true, workViews: true }),
}));
const emailMock = vi.hoisted(() => ({ getSettings: vi.fn(), updateSettings: vi.fn(), testConnection: vi.fn() }));
vi.mock('../services/emailSettingsService', () => ({ emailSettingsService: emailMock }));
const healthMock = vi.hoisted(() => ({ check: vi.fn() }));
vi.mock('../services/healthService', () => ({ healthService: healthMock }));
const calendarServiceMock = vi.hoisted(() => ({ getAll: vi.fn(), create: vi.fn(), update: vi.fn(), delete: vi.fn() }));
const planningMock = vi.hoisted(() => ({ readInitial: vi.fn() }));
vi.mock('../services/calendarService', () => ({ calendarService: calendarServiceMock }));
vi.mock('../services/planningInputService', () => ({ planningInputService: planningMock }));

// The real panels run here; only the services they call are replaced.
const templateServiceMock = vi.hoisted(() => ({ getAll: vi.fn(), getById: vi.fn(), create: vi.fn(), update: vi.fn() }));
const labelServiceMock = vi.hoisted(() => ({
    getGroups: vi.fn(), getLabels: vi.fn(), createGroup: vi.fn(), updateGroup: vi.fn(), createLabel: vi.fn(), updateLabel: vi.fn(),
}));
const rulesServiceMock = vi.hoisted(() => ({ getRules: vi.fn(), updateRules: vi.fn(), resetRules: vi.fn() }));
const webhookServiceMock = vi.hoisted(() => ({
    getTargets: vi.fn(), createTarget: vi.fn(), updateTarget: vi.fn(), deleteTarget: vi.fn(),
    testTarget: vi.fn(), getDeliveries: vi.fn(), retryDelivery: vi.fn(),
}));
vi.mock('../services/templateService', () => ({ templateService: templateServiceMock }));
vi.mock('../services/labelService', () => ({ labelService: labelServiceMock }));
vi.mock('../services/schedulingRulesService', () => ({ schedulingRulesService: rulesServiceMock }));
vi.mock('../services/outboundWebhookService', () => ({ outboundWebhookService: webhookServiceMock }));
const githubServiceMock = vi.hoisted(() => ({
    getStatusAutomationRules: vi.fn(), createStatusAutomationRule: vi.fn(), updateStatusAutomationRule: vi.fn(), deleteStatusAutomationRule: vi.fn(),
}));
const systemSettingsServiceMock = vi.hoisted(() => ({
    getSettings: vi.fn(), updateApp: vi.fn(), updateLLM: vi.fn(), updateGitHub: vi.fn(), updateWebIntake: vi.fn(),
}));
vi.mock('../services/githubService', () => ({ githubService: githubServiceMock }));
vi.mock('../services/systemSettingsService', () => ({ systemSettingsService: systemSettingsServiceMock }));

const template = (id: number, name: string, type: WorkTemplate['template_type']): WorkTemplate => ({
    id, name, description: null, seed_key: null, template_type: type, default_title: null, default_description: null,
    default_priority: null, default_effort_days: null, default_labels: [], default_checklist: [], default_payload: {},
    is_active: true, sort_order: id * 10, created_at: '2026-07-01T10:00:00Z', updated_at: '2026-07-01T10:00:00Z',
});

const labelGroup: LabelGroup = {
    id: 1, key: 'workflow', name: 'Workflow', description: null, color: '#2563eb', is_active: true, sort_order: 10, seed_key: null,
    labels: [{
        id: 101, slug: 'planning', name: 'Planning', group_id: 1, description: null, color: '#2563eb', is_active: true,
        sort_order: 10, seed_key: null, created_at: '2026-07-01T10:00:00Z', updated_at: '2026-07-01T10:00:00Z',
    }],
    created_at: '2026-07-01T10:00:00Z', updated_at: '2026-07-01T10:00:00Z',
};

const rules: SchedulingRulesResponse = {
    source: 'database',
    rules: {
        schema_version: '1.0',
        effort_modifiers: [{ id: 'professionalism', enabled: true, formula: 'effort', fallback: 'effort', min_value: 0 }],
        scheduling_passes: [{ id: 'critical_deadline', description: 'Nearest deadline first', enabled: true, filter: { all: ['task.priority >= 9'] }, sort: [{ field: 'max_finish_date', order: 'asc' }] }],
        constraints: {
            sequential_per_assignee: true, respect_dependencies: true, min_start_date: true, max_finish_date: true,
            prefer_uninterrupted: true, balance_workload: { enabled: true, max_overload_percent: 10 },
        },
    },
};

const webhookTarget: OutboundWebhookTarget = {
    id: 1, name: 'Ops hook', description: null, url: 'https://hooks.example.com/1', enabled: true,
    subscribed_events_json: ['task.*'], has_secret: true, headers_json: {},
    created_at: '2026-07-01T12:00:00Z', updated_at: '2026-07-02T12:00:00Z',
};

const githubRule: GitHubStatusAutomationRule = {
    id: 7, name: 'Merged PR resolves', description: 'Resolve the task when its PR merges', enabled: true,
    github_event_type: 'github_pr_merged', from_status: 'active', target_status: 'resolved',
    reason_template: 'Resolved by {repo} PR #{pr_number} after merge', sort_order: 20,
    created_at: '2026-07-01T12:00:00Z', updated_at: '2026-07-02T12:00:00Z',
};

const systemSettings: SystemSettings = {
    app: { ui_language: 'en', ai_language_mode: 'auto', field_sources: {} },
    llm: {
        provider: 'openai', api_url: 'https://api.openai.com/v1', model: 'gpt-5', temperature: 0.2,
        max_output_tokens: 3000, has_api_key: true, field_sources: {},
    },
    github: {
        api_url: 'https://github.example.com/api/v3', request_timeout_seconds: 15,
        webhook_create_triage_for_unmatched: true, has_token: true, has_webhook_secret: true, field_sources: {},
    },
    web_intake: { rate_limit_per_minute: 30, has_token: true, field_sources: {} },
    restart_required: [],
};

// Admin access is mocked separately so the real editable panels can open their forms.
const localIdentity: WorkspaceIdentity = {
    mode: 'trusted_local', authenticated: false, configured: false, principal: null, profile: null,
    workspace_role: null, projects: {}, csrf_token: null,
};

const renderSettings = (tab: string, useDataRouter = false) => {
    const page = (
        <IdentityContext.Provider value={{ identity: localIdentity, refresh: vi.fn(), signOut: async () => undefined }}>
            <SettingsPage />
        </IdentityContext.Provider>
    );
    const initialEntries = [`/settings?tab=${tab}`];
    if (!useDataRouter) return renderWithProviders(page, { initialEntries });
    const queryClient = createTestQueryClient();
    const router = createMemoryRouter([{ path: '/settings', element: page }], { initialEntries });
    return {
        user: userEvent.setup(),
        queryClient,
        ...render(<QueryClientProvider client={queryClient}><ToastProvider><RouterProvider router={router} /></ToastProvider></QueryClientProvider>),
    };
};


const sections: SettingsSectionId[] = ['theme', 'shortcuts', 'language', 'work_calendar', 'scheduling', 'templates_labels', 'notifications', 'github', 'webhooks', 'web_intake', 'ai_provider', 'access', 'runtime', 'about'];

const checkLabels = (section: SettingsSectionId, root: ParentNode, fixtureHeadings: Element[] = []) => {
    const indexed = SETTINGS_FIELD_LABEL_KEYS[section].flatMap(key => [1, 2].map(index => i18n.t(key, { index, name: 'Merged PR resolves', id: 'professionalism' })));
    if (SETTINGS_FIELD_LABEL_KEYS[section].includes('settingsScheduling.aria.enablePass')) {
        for (const id of ['critical_deadline', 'pass_1735689600000']) {
            indexed.push(i18n.t('settingsScheduling.aria.enablePass', { id }));
        }
    }
    if (section === 'webhooks' && SETTINGS_FIELD_LABEL_KEYS.webhooks.includes('actions.edit')) indexed.push(`${i18n.t('actions.edit')}: Ops hook`);
    if (section === 'webhooks' && SETTINGS_FIELD_LABEL_KEYS.webhooks.includes('settingsWebhooks.view')) indexed.push(`${i18n.t('settingsWebhooks.view')}: Ops hook`);
    if (section === 'webhooks' && SETTINGS_FIELD_LABEL_KEYS.webhooks.includes('settingsWebhooks.enabled')) indexed.push(`Ops hook: ${i18n.t('settingsWebhooks.enabled')}`);
    // Only these fixture rows and explicitly supplied drawer titles contain user data.
    const fixtureRows = section === 'templates_labels'
        ? [...root.querySelectorAll('#work-template-1-heading, #label-group-1-heading')]
        : [];
    const excludedHeadings = new Set([...fixtureRows, ...fixtureHeadings]);
    const labels = [...root.querySelectorAll('label, legend, h1, h2, h3, h4, h5, h6, [role=heading]')].filter(node => node.id !== 'settings-destination-title' && !excludedHeadings.has(node)).map(node => {
        const copy = node.cloneNode(true) as Element;
        copy.querySelectorAll('select, input, textarea, .field-required').forEach(control => control.remove());
        const text = copy.textContent?.trim().replace(/\s*\*\s*$/, '') ?? '';
        return text;
    }).filter(Boolean);
    // Some real field names are available only through their accessible label.
    root.querySelectorAll('input[aria-label], select[aria-label], textarea[aria-label], [role=radiogroup], [role=radio], [role=switch], [role=checkbox]').forEach(field => {
        const name = computeAccessibleName(field);
        if (name) labels.push(name);
    });
    if (section === 'about') {
        // Health renders a status indicator, with no additional field labels or headings.
        expect(root.querySelector('[data-health-state=healthy]')).not.toBeNull();
    } else {
        expect(labels.length, `${section}: no labels or headings rendered`).toBeGreaterThan(0);
    }
    expect(labels.filter(label => !indexed.includes(label)), `${section}: missing rendered labels`).toEqual([]);
};

describe('Settings search rendered labels', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        adminAccessMock.hasAdminKey = true;
        vi.spyOn(identityService, 'sessions').mockResolvedValue([]);
        window.localStorage.clear();
        window.sessionStorage.clear();
        templateServiceMock.getAll.mockResolvedValue([template(1, 'Bug report', 'task')]);
        labelServiceMock.getGroups.mockResolvedValue([labelGroup]);
        rulesServiceMock.getRules.mockResolvedValue(rules);
        webhookServiceMock.getTargets.mockResolvedValue([webhookTarget]);
        webhookServiceMock.getDeliveries.mockResolvedValue([]);
        githubServiceMock.getStatusAutomationRules.mockResolvedValue([githubRule]);
        systemSettingsServiceMock.getSettings.mockResolvedValue(systemSettings);
        emailMock.getSettings.mockResolvedValue({ enabled: true, smtp_host: 'smtp.example.com', smtp_port: 587, smtp_user: 'mailer@example.com', smtp_from_email: 'notifications@example.com', smtp_use_tls: true, has_password: true, field_sources: {} });
        healthMock.check.mockResolvedValue({ state: 'healthy', statusCode: 200 });
        const calendar = { id: 1, name: 'Workspace', year: 2026, holidays: ['2026-01-01'], short_days: ['2026-01-02'], weekend_days: [5, 6] };
        const calendars = [calendar, { ...calendar, id: 2, name: 'Other workspace' }];
        calendarServiceMock.getAll.mockResolvedValue(calendars);
        planningMock.readInitial.mockImplementation(async (_kind, id) => ({ resource: calendars.find(item => item.id === id), resource_id: id, expected_revisions: {}, complete: true }));
    });

    afterEach(async () => {
        vi.restoreAllMocks();
        await i18n.changeLanguage('en');
    });

    it('rejects product headings that share fixture names', async () => {
        const view = renderSettings('templates_labels');
        await screen.findByRole('heading', { name: 'Bug report' });
        const content = view.container.querySelector('.settings-content')!;
        checkLabels('templates_labels', content);
        for (const name of ['Workflow', 'Planning', 'Bug report', 'Ops hook', 'Merged PR resolves', 'professionalism', 'critical_deadline', 'pass_1735689600000']) {
            const heading = document.createElement('h3');
            heading.textContent = name;
            content.append(heading);
            expect(() => checkLabels('templates_labels', content), name).toThrow('missing rendered labels');
            heading.remove();
        }
        view.unmount();
    });

    it.each(['en', 'ru'].flatMap(language => sections.map(section => ({ language, section }))))('indexes rendered labels in $section ($language)', async ({ language, section }) => {
        await ensureLanguageResources(language);
        await i18n.changeLanguage(language);
        const view = renderSettings(section);
        const content = view.container.querySelector('.settings-content')!;
        const ready: Partial<Record<SettingsSectionId, string>> = {
            language: 'settings.aiLanguageMode', scheduling: 'settingsScheduling.sections.constraints.title',
            notifications: 'surfaces.emailSettings.smtpHost', github: 'settings.githubApiUrl',
            web_intake: 'settings.rateLimitPerMinute', ai_provider: 'settings.model',
            access: 'agentAccess.title', runtime: 'settings.restartRequired',
        };
        if (ready[section]) await screen.findAllByText(i18n.t(ready[section]!));
        if (section === 'templates_labels') await screen.findByText('Bug report');
        if (section === 'webhooks') await screen.findAllByText('Ops hook');
        if (section === 'github') await screen.findByText('Merged PR resolves');
        if (section === 'access') await screen.findByText(i18n.t('teamwork.readersEmpty'));
        if (section === 'work_calendar') {
            await screen.findByRole('heading', { name: i18n.t('calendar.companyNonWorkingDays') });
            await vi.waitFor(() => expect(content.querySelector('fieldset')).toBeEnabled());
        }
        if (section === 'about') await vi.waitFor(() => expect(content.querySelector('[data-health-state=healthy]')).not.toBeNull());
        checkLabels(section, content);
        if (section === 'work_calendar') {
            await view.user.click(screen.getByRole('button', { name: i18n.t('calendar.listView') }));
            checkLabels(section, content);
            await view.user.click(screen.getByRole('button', { name: i18n.t('actions.moreActions') }));
            await view.user.click(screen.getByRole('menuitem', { name: i18n.t('calendar.newCalendar') }));
            checkLabels(section, screen.getByRole('dialog'));
            await view.user.click(within(screen.getByRole('dialog')).getByRole('button', { name: i18n.t('actions.close') }));
            await view.user.click(screen.getByRole('button', { name: i18n.t('calendar.calendarView') }));
            const day = content.querySelector('button[aria-label*="2026"]');
            expect(day).not.toBeNull();
            await view.user.click(day!);
            checkLabels(section, content);
        }
        if (section === 'scheduling') {
            await view.user.click(screen.getByRole('button', { name: 'professionalism' }));
            const drawer = screen.getByRole('dialog');
            const modifierHeading = within(drawer).getByRole('heading', { name: 'professionalism', level: 2 });
            checkLabels(section, drawer, [modifierHeading]);
            for (const value of ['divide_by_field', 'inverse_percentage', 'multiply', 'divide_constant', 'add_buffer', 'custom', '_operation_']) {
                await view.user.selectOptions(within(drawer).getByLabelText(i18n.t('settingsScheduling.fields.type')), value);
                checkLabels(section, drawer, [modifierHeading]);
            }
            await view.user.click(within(drawer).getByRole('button', { name: i18n.t('actions.close') }));
            await view.user.click(screen.getByRole('button', { name: 'critical_deadline Nearest deadline first' }));
            const passDrawer = screen.getByRole('dialog');
            const passHeading = within(passDrawer).getByRole('heading', { name: 'critical_deadline', level: 2 });
            checkLabels(section, passDrawer, [passHeading]);
            const addButtons = within(passDrawer).getAllByRole('button', { name: i18n.t('settingsScheduling.actions.add') });
            await view.user.click(addButtons[0]);
            await view.user.click(addButtons[1]);
            expect(within(passDrawer).getByRole('combobox', { name: i18n.t('settingsScheduling.aria.conditionField', { index: 2 }) })).toBeInTheDocument();
            expect(within(passDrawer).getByRole('combobox', { name: i18n.t('settingsScheduling.aria.sortField', { index: 2 }) })).toBeInTheDocument();
            checkLabels(section, passDrawer, [passHeading]);
            await view.user.click(within(passDrawer).getByRole('button', { name: i18n.t('actions.close') }));
            const now = vi.spyOn(Date, 'now').mockReturnValue(1735689600000);
            await view.user.click(screen.getByRole('button', { name: i18n.t('settingsScheduling.sections.passes.add') }));
            now.mockRestore();
            await view.user.click(screen.getByRole('button', { name: `pass_1735689600000 ${i18n.t('settingsScheduling.newPassDescription')}` }));
            const newPassDrawer = screen.getByRole('dialog');
            checkLabels(section, newPassDrawer, [within(newPassDrawer).getByRole('heading', { name: 'pass_1735689600000', level: 2 })]);
            await view.user.click(within(screen.getByRole('dialog')).getByRole('button', { name: i18n.t('actions.close') }));
            const balance = screen.getByRole('checkbox', { name: i18n.t('settingsScheduling.constraints.balance_workload.label') });
            await view.user.click(balance);
            expect(screen.queryByRole('spinbutton', { name: i18n.t('settingsScheduling.fields.maxAllowableOverload') })).not.toBeInTheDocument();
            checkLabels(section, content);
            await view.user.click(balance);
            expect(screen.getByRole('spinbutton', { name: i18n.t('settingsScheduling.fields.maxAllowableOverload') })).toBeInTheDocument();
            checkLabels(section, content);
        }
        if (section === 'webhooks') {
            await view.user.click(screen.getByRole('button', { name: i18n.t('settingsWebhooks.newTarget') }));
            checkLabels(section, screen.getByRole('dialog'));
            await view.user.click(within(screen.getByRole('dialog')).getByRole('button', { name: i18n.t('actions.cancel') }));
            await view.user.click(screen.getByRole('button', { name: `${i18n.t('actions.edit')}: Ops hook` }));
            checkLabels(section, screen.getByRole('dialog'));
        }
        if (section === 'github') {
            await screen.findByText('Merged PR resolves');
            await view.user.click(screen.getByRole('button', { name: i18n.t('settingsGithubAutomation.newRule') }));
            checkLabels(section, screen.getByRole('dialog'));
            await view.user.click(within(screen.getByRole('dialog')).getByRole('button', { name: i18n.t('actions.cancel') }));
            await view.user.click(screen.getByRole('button', { name: i18n.t('settingsGithubAutomation.editRule', { name: 'Merged PR resolves' }) }));
            checkLabels(section, screen.getByRole('dialog'));
        }
        if (section === 'templates_labels') {
            await view.user.click(screen.getByRole('button', { name: i18n.t('surfaces.templateLabels.newTemplate') }));
            checkLabels(section, screen.getByRole('dialog'));
            await view.user.click(within(screen.getByRole('dialog')).getByRole('button', { name: i18n.t('surfaces.templateLabels.closeTemplateForm') }));
            await view.user.click(screen.getByRole('button', { name: `${i18n.t('surfaces.templateLabels.editTemplate')}: Bug report` }));
            checkLabels(section, screen.getByRole('dialog'));
            await view.user.click(within(screen.getByRole('dialog')).getByRole('button', { name: i18n.t('surfaces.templateLabels.closeTemplateForm') }));
            await view.user.click(screen.getByRole('tab', { name: i18n.t('surfaces.templateLabels.labels') }));
            await screen.findByRole('heading', { name: 'Workflow' });
            checkLabels(section, content);
            for (const [button, action, close] of [
                [i18n.t('surfaces.templateLabels.newGroup'), '', 'closeGroupForm'],
                [i18n.t('surfaces.templateLabels.rowActions', { name: 'Workflow' }), 'editGroup', 'closeGroupForm'],
                [i18n.t('surfaces.templateLabels.addLabel'), '', 'closeLabelForm'],
                [i18n.t('surfaces.templateLabels.rowActions', { name: 'Planning' }), 'editLabel', 'closeLabelForm'],
            ]) {
                await view.user.click(screen.getByRole('button', { name: button }));
                if (action) await view.user.click(screen.getByRole('menuitem', { name: i18n.t(`surfaces.templateLabels.${action}`) }));
                checkLabels(section, screen.getByRole('dialog'));
                await view.user.click(within(screen.getByRole('dialog')).getByRole('button', { name: i18n.t(`surfaces.templateLabels.${close}`) }));
            }
        }
        view.unmount();
    });

    it.each(['en', 'ru'].flatMap(language => (['scheduling', 'github', 'webhooks', 'work_calendar'] as const).map(section => ({ language, section }))))('indexes confirmation headings in $section ($language)', async ({ language, section }) => {
        await ensureLanguageResources(language);
        await i18n.changeLanguage(language);
        const view = renderSettings(section, section === 'work_calendar');
        const cancelConfirmation = async (title: string, cancel = 'actions.cancel') => {
            const dialog = await screen.findByRole('dialog', { name: i18n.t(title) });
            checkLabels(section, dialog);
            await view.user.click(within(dialog).getByRole('button', { name: i18n.t(cancel) }));
        };
        if (section === 'scheduling') {
            const reset = await screen.findByRole('button', { name: i18n.t('settingsScheduling.actions.resetToDefaults') });
            await view.user.click(reset);
            await cancelConfirmation('settingsScheduling.actions.resetToDefaults');
            expect(rulesServiceMock.resetRules).not.toHaveBeenCalled();
        }
        if (section === 'github' || section === 'webhooks') {
            const github = section === 'github';
            const prefix = github ? 'settingsGithubAutomation' : 'settingsWebhooks';
            if (github) await screen.findByText('Merged PR resolves');
            else await screen.findAllByText('Ops hook');
            await view.user.click(screen.getByRole('button', { name: i18n.t(`${prefix}.${github ? 'newRule' : 'newTarget'}`) }));
            const drawer = screen.getByRole('dialog');
            const name = within(drawer).getAllByRole('textbox')[0];
            await view.user.type(name, 'Draft');
            await view.user.click(within(drawer).getByRole('button', { name: i18n.t('actions.close') }));
            await cancelConfirmation(`${prefix}.discardDraftTitle`);
            await view.user.clear(name);
            await view.user.click(within(drawer).getByRole('button', { name: i18n.t('actions.close') }));
            await view.user.click(screen.getByRole('button', { name: github
                ? i18n.t('settingsGithubAutomation.deleteRule', { name: 'Merged PR resolves' })
                : `${i18n.t('actions.delete')}: Ops hook` }));
            await cancelConfirmation('actions.delete');
            expect(githubServiceMock.createStatusAutomationRule).not.toHaveBeenCalled();
            expect(githubServiceMock.deleteStatusAutomationRule).not.toHaveBeenCalled();
            expect(webhookServiceMock.createTarget).not.toHaveBeenCalled();
            expect(webhookServiceMock.deleteTarget).not.toHaveBeenCalled();
        }
        if (section === 'work_calendar') {
            await screen.findByRole('heading', { name: i18n.t('calendar.companyNonWorkingDays') });
            const calendar = screen.getByRole('combobox', { name: i18n.t('calendar.selectCalendar') });
            await vi.waitFor(() => expect(calendar).toBeEnabled());
            await view.user.click(screen.getByRole('button', { name: i18n.t('actions.moreActions') }));
            await view.user.click(screen.getByRole('menuitem', { name: i18n.t('calendar.deleteCalendar') }));
            await cancelConfirmation('calendar.deleteCalendar');
            const day = view.container.querySelector('button[aria-label*="2026"]');
            expect(day).not.toBeNull();
            await view.user.click(day!);
            expect(screen.getByRole('button', { name: i18n.t('calendar.saveSettings') })).toBeEnabled();
            await view.user.selectOptions(calendar, '2');
            await cancelConfirmation('calendar.unsavedSwitchTitle', 'calendar.keepEditing');
            const themeLink = view.container.querySelector('a[href="/settings?tab=theme"]');
            expect(themeLink).not.toBeNull();
            await view.user.click(themeLink!);
            await cancelConfirmation('calendar.unsavedLeaveTitle', 'calendar.keepEditing');
            expect(calendarServiceMock.delete).not.toHaveBeenCalled();
            expect(calendarServiceMock.update).not.toHaveBeenCalled();
        }
        view.unmount();
    });

    it.each(['en', 'ru'])('indexes empty calendar labels (%s)', async language => {
        await ensureLanguageResources(language);
        await i18n.changeLanguage(language);
        calendarServiceMock.getAll.mockResolvedValue([]);
        const view = renderSettings('work_calendar');
        await screen.findByRole('heading', { name: i18n.t('calendar.unavailable') });
        checkLabels('work_calendar', view.container.querySelector('.settings-content')!);
        await view.user.click(screen.getByRole('button', { name: i18n.t('calendar.newCalendar') }));
        checkLabels('work_calendar', screen.getByRole('dialog'));
        await view.user.click(within(screen.getByRole('dialog')).getByRole('button', { name: i18n.t('actions.cancel') }));
        expect(calendarServiceMock.create).not.toHaveBeenCalled();
        view.unmount();
    });

    it.each(['en', 'ru'].flatMap(language => (['templates_labels', 'github', 'webhooks'] as const).map(section => ({ language, section }))))('indexes readonly drawer labels in $section ($language)', async ({ language, section }) => {
        await ensureLanguageResources(language);
        await i18n.changeLanguage(language);
        adminAccessMock.hasAdminKey = false;
        const view = renderSettings(section);
        const content = view.container.querySelector('.settings-content')!;
        const checkDrawer = () => {
            const drawer = screen.getByRole('dialog');
            expect(drawer.querySelector('fieldset')).toBeDisabled();
            checkLabels(section, drawer);
        };

        if (section === 'templates_labels') {
            await screen.findByText('Bug report');
            checkLabels(section, content);
            await view.user.click(screen.getByRole('button', { name: `${i18n.t('surfaces.templateLabels.viewTemplate')}: Bug report` }));
            checkDrawer();
            await view.user.click(within(screen.getByRole('dialog')).getByRole('button', { name: i18n.t('surfaces.templateLabels.closeTemplateForm') }));
            await view.user.click(screen.getByRole('tab', { name: i18n.t('surfaces.templateLabels.labels') }));
            await screen.findByRole('heading', { name: 'Workflow' });
            checkLabels(section, content);
            for (const [name, action, close] of [
                ['Workflow', 'viewGroup', 'closeGroupForm'],
                ['Planning', 'viewLabel', 'closeLabelForm'],
            ]) {
                await view.user.click(screen.getByRole('button', { name: i18n.t('surfaces.templateLabels.rowActions', { name }) }));
                await view.user.click(screen.getByRole('menuitem', { name: i18n.t(`surfaces.templateLabels.${action}`) }));
                checkDrawer();
                await view.user.click(within(screen.getByRole('dialog')).getByRole('button', { name: i18n.t(`surfaces.templateLabels.${close}`) }));
            }
        }
        if (section === 'github') {
            await screen.findByText('Merged PR resolves');
            await screen.findByText(i18n.t('settings.githubApiUrl'));
            checkLabels(section, content);
            await view.user.click(screen.getByRole('button', { name: i18n.t('settingsGithubAutomation.viewRule', { name: 'Merged PR resolves' }) }));
            checkDrawer();
        }
        if (section === 'webhooks') {
            await screen.findAllByText('Ops hook');
            checkLabels(section, content);
            await view.user.click(screen.getByRole('button', { name: `${i18n.t('settingsWebhooks.view')}: Ops hook` }));
            checkDrawer();
        }
        view.unmount();
    });
});
