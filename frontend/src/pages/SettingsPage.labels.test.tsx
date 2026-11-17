import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../test/renderWithProviders';
import { IdentityContext } from '../features/identity/identityContext';
import type { WorkspaceIdentity } from '../features/identity/identityService';
import type { WorkTemplate } from '../types/template';
import type { LabelGroup } from '../types/label';
import type { SchedulingRulesResponse } from '../types/schedulingRules';
import type { OutboundWebhookTarget } from '../types/outboundWebhook';
import type { GitHubStatusAutomationRule } from '../types/github';
import type { SystemSettings } from '../types/systemSettings';
import SettingsPage from './SettingsPage';

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
        scheduling_passes: [{ id: 'critical_deadline', description: 'Nearest deadline first', enabled: true, filter: { all: [] }, sort: [] }],
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

/** A trusted-local browser: may read settings without the admin key, but not change them. */
const reader: WorkspaceIdentity = {
    mode: 'trusted_local', authenticated: false, configured: false, principal: null, profile: null,
    workspace_role: null, projects: {}, csrf_token: null,
};

const renderSettings = (tab: string) => renderWithProviders(
    <IdentityContext.Provider value={{ identity: reader, refresh: vi.fn(), signOut: async () => undefined }}>
        <SettingsPage />
    </IdentityContext.Provider>,
    { initialEntries: [`/settings?tab=${tab}`] },
);

import i18n, { ensureLanguageResources } from '../i18n/i18n';
import { SETTINGS_FIELD_LABEL_KEYS } from '../components/settings/settingsFieldLabels';
import type { SettingsSectionId } from '../components/settings/settingsFieldLabels';

const sections: SettingsSectionId[] = ['theme', 'shortcuts', 'language', 'work_calendar', 'scheduling', 'templates_labels', 'notifications', 'github', 'webhooks', 'web_intake', 'ai_provider', 'access', 'runtime', 'about'];

const checkLabels = (section: SettingsSectionId, root: ParentNode) => {
    const indexed = SETTINGS_FIELD_LABEL_KEYS[section].map(key => i18n.t(key));
    const labels = [...root.querySelectorAll('label, legend')].map(node => node.textContent?.trim().replace(/\s*\*\s*$/, '') ?? '').filter(Boolean);
    expect(labels.filter(label => !indexed.includes(label)), `${section}: missing rendered labels`).toEqual([]);
};

describe('Settings search rendered labels', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        window.localStorage.clear();
        window.sessionStorage.clear();
        templateServiceMock.getAll.mockResolvedValue([template(1, 'Bug report', 'task')]);
        labelServiceMock.getGroups.mockResolvedValue([labelGroup]);
        rulesServiceMock.getRules.mockResolvedValue(rules);
        webhookServiceMock.getTargets.mockResolvedValue([webhookTarget]);
        webhookServiceMock.getDeliveries.mockResolvedValue([]);
        githubServiceMock.getStatusAutomationRules.mockResolvedValue([githubRule]);
        systemSettingsServiceMock.getSettings.mockResolvedValue(systemSettings);
    });

    it.each(['en', 'ru'])('indexes rendered field labels in every section (%s)', async language => {
        await ensureLanguageResources(language);
        await i18n.changeLanguage(language);
        try {
            for (const section of sections) {
                const view = renderSettings(section);
                await vi.waitFor(() => {
                    if (['language', 'github', 'web_intake', 'ai_provider', 'runtime'].includes(section)) expect(systemSettingsServiceMock.getSettings).toHaveBeenCalled();
                    if (section === 'scheduling') expect(screen.getByText('professionalism')).toBeVisible();
                    if (section === 'templates_labels') expect(screen.getByText('Bug report')).toBeVisible();
                    if (section === 'webhooks') expect(screen.getAllByText('Ops hook').length).toBeGreaterThan(0);
                });
                const content = view.container.querySelector('.settings-content')!;
                checkLabels(section, content);
                if (['webhooks', 'access'].includes(section)) {
                    const headings = [...content.querySelectorAll('h2:not(#settings-destination-title), h3, h4')].map(node => node.textContent?.trim());
                    expect(headings.length).toBeGreaterThan(0);
                    const indexed = SETTINGS_FIELD_LABEL_KEYS[section].map(key => i18n.t(key));
                    expect(headings.filter(heading => heading && !indexed.includes(heading)), `${section}: missing rendered headings`).toEqual([]);
                }
                view.unmount();
            }
        } finally {
            await i18n.changeLanguage('en');
        }
    });
});
