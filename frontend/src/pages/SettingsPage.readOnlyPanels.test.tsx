import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
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
const verifyKey = vi.hoisted(() => vi.fn());
vi.mock('../services/adminAccessService', () => ({ verifyAdminApiKey: verifyKey }));
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

const header = () => screen.getByTestId('page-header');

const unlock = async (user: ReturnType<typeof renderSettings>['user']) => {
    await user.click(within(header()).getByRole('button', { name: 'Unlock editing' }));
    await user.type(screen.getByLabelText('Admin key'), 'operator-key');
    await user.click(screen.getByRole('button', { name: 'Save key' }));
    expect(await screen.findByText('Editing unlocked')).toBeVisible();
    expect(verifyKey).toHaveBeenCalledWith('operator-key');
};

const menuItem = (name: string) => screen.getByRole('menuitem', { name });

describe('SettingsPage read-only panels', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        window.localStorage.clear();
        window.sessionStorage.clear();
        templateServiceMock.getAll.mockResolvedValue([template(1, 'Bug report', 'task'), template(2, 'Client launch', 'project')]);
        labelServiceMock.getGroups.mockResolvedValue([labelGroup]);
        rulesServiceMock.getRules.mockResolvedValue(rules);
        verifyKey.mockResolvedValue(undefined);
        webhookServiceMock.getTargets.mockResolvedValue([webhookTarget]);
        webhookServiceMock.getDeliveries.mockResolvedValue([]);
        githubServiceMock.getStatusAutomationRules.mockResolvedValue([githubRule]);
        systemSettingsServiceMock.getSettings.mockResolvedValue(systemSettings);
    });

    it('lets readers move through templates and labels and open each item, with every change disabled until Unlock editing', async () => {
        const { user } = renderSettings('templates_labels');

        // Template types switch while locked.
        expect(await screen.findByRole('heading', { name: 'Bug report' })).toBeVisible();
        const projectType = screen.getByRole('button', { name: 'Project' });
        expect(projectType).toBeEnabled();
        await user.click(projectType);
        expect(await screen.findByRole('heading', { name: 'Client launch' })).toBeVisible();
        expect(screen.queryByRole('heading', { name: 'Bug report' })).toBeNull();

        // Changes are disabled; a template still opens to be read.
        expect(screen.getByRole('button', { name: 'New template' })).toBeDisabled();
        expect(screen.getByRole('switch', { name: 'Active' })).toBeDisabled();
        await user.click(screen.getByRole('button', { name: 'View template: Client launch' }));
        const drawer = await screen.findByRole('dialog', { name: 'Template details' });
        expect(within(drawer).getByRole('textbox', { name: /Name/ })).toHaveValue('Client launch');
        expect(within(drawer).getByRole('textbox', { name: /Name/ })).toBeDisabled();
        expect(within(drawer).getByRole('button', { name: 'Save template' })).toBeDisabled();
        await user.click(within(drawer).getByRole('button', { name: 'Close template form' }));

        // The Labels tab and "Include archived" work while locked.
        const labelsTab = screen.getByRole('tab', { name: 'Labels' });
        expect(labelsTab).toBeEnabled();
        await user.click(labelsTab);
        expect(await screen.findByRole('heading', { name: 'Workflow' })).toBeVisible();
        const includeArchived = screen.getByRole('checkbox', { name: 'Include archived' });
        expect(includeArchived).toBeEnabled();
        await user.click(includeArchived);
        expect(labelServiceMock.getGroups).toHaveBeenLastCalledWith({ include_inactive: true });

        expect(screen.getByRole('button', { name: 'New group' })).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Add label' })).toBeDisabled();
        await user.click(screen.getByRole('button', { name: 'Actions for Workflow' }));
        expect(menuItem('Archive group')).toHaveAttribute('aria-disabled', 'true');
        expect(menuItem('Move up')).toHaveAttribute('aria-disabled', 'true');
        expect(menuItem('View group')).not.toHaveAttribute('aria-disabled');
        await user.click(menuItem('View group'));
        const groupDrawer = await screen.findByRole('dialog', { name: 'Group details' });
        expect(within(groupDrawer).getByRole('textbox', { name: /Key/ })).toHaveValue('workflow');
        expect(within(groupDrawer).getByRole('textbox', { name: /Key/ })).toBeDisabled();
        expect(within(groupDrawer).getByRole('button', { name: 'Save group' })).toBeDisabled();
        await user.click(within(groupDrawer).getByRole('button', { name: 'Close group form' }));

        // A label opens read-only in its own drawer.
        await user.click(screen.getByRole('button', { name: 'Actions for Planning' }));
        expect(menuItem('Archive label')).toHaveAttribute('aria-disabled', 'true');
        await user.click(menuItem('View label'));
        const labelDrawer = await screen.findByRole('dialog', { name: 'Label details' });
        expect(within(labelDrawer).getByRole('textbox', { name: /Slug/ })).toHaveValue('planning');
        expect(within(labelDrawer).getByRole('textbox', { name: /Slug/ })).toBeDisabled();
        expect(within(labelDrawer).getByRole('combobox', { name: 'Group' })).toBeDisabled();
        expect(within(labelDrawer).getByRole('button', { name: 'Save label' })).toBeDisabled();
        await user.click(within(labelDrawer).getByRole('button', { name: 'Close label form' }));
        expect(screen.queryByRole('dialog')).toBeNull();
        expect(templateServiceMock.update).not.toHaveBeenCalled();
        expect(labelServiceMock.updateGroup).not.toHaveBeenCalled();
        expect(labelServiceMock.updateLabel).not.toHaveBeenCalled();

        // The one control in the Settings header unlocks the same panel.
        await unlock(user);
        expect(screen.getByRole('button', { name: 'New group' })).toBeEnabled();
        expect(screen.getByRole('button', { name: 'Add label' })).toBeEnabled();
        await user.click(screen.getByRole('button', { name: 'Actions for Workflow' }));
        expect(menuItem('Archive group')).not.toHaveAttribute('aria-disabled');
        await user.click(menuItem('Edit group'));
        const editDrawer = await screen.findByRole('dialog', { name: 'Edit group' });
        expect(within(editDrawer).getByRole('textbox', { name: /Key/ })).toBeEnabled();
        expect(within(editDrawer).getByRole('button', { name: 'Save group' })).toBeEnabled();
        await user.click(within(editDrawer).getByRole('button', { name: 'Close group form' }));
        await user.click(screen.getByRole('button', { name: 'New group' }));
        expect(await screen.findByRole('dialog', { name: 'New group' })).toBeVisible();
    });

    it('lets readers collapse and expand the scheduling rules, with every change disabled until Unlock editing', async () => {
        const { user } = renderSettings('scheduling');

        const modifiers = await screen.findByRole('button', { name: /Effort modifiers/ });
        expect(modifiers).toBeEnabled();
        expect(screen.getByRole('button', { name: 'Add modifier' })).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Reset to defaults' })).toBeDisabled();
        await user.click(modifiers);
        expect(modifiers).toHaveAttribute('aria-expanded', 'false');
        expect(screen.queryByRole('button', { name: 'Add modifier' })).toBeNull();
        await user.click(modifiers);
        expect(modifiers).toHaveAttribute('aria-expanded', 'true');

        // One rule opens in the drawer to show its details, which cannot be changed.
        expect(screen.getByRole('checkbox', { name: 'Enable professionalism modifier' })).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Remove modifier' })).toBeDisabled();
        const rule = screen.getByRole('button', { name: /^professionalism/i });
        expect(rule).toBeEnabled();
        await user.click(rule);
        expect(rule).toHaveAttribute('aria-expanded', 'true');
        const drawer = screen.getByRole('dialog');
        const ruleId = within(drawer).getByDisplayValue('professionalism');
        expect(ruleId).toBeDisabled();
        expect(within(drawer).getByLabelText('Fallback')).toBeDisabled();
        await user.click(within(drawer).getByRole('button', { name: 'Close' }));
        expect(screen.queryByRole('dialog')).toBeNull();

        await unlock(user);
        await user.click(screen.getByRole('button', { name: /^professionalism/i }));
        expect(within(screen.getByRole('dialog')).getByDisplayValue('professionalism')).toBeEnabled();
        await user.click(within(screen.getByRole('dialog')).getByRole('button', { name: 'Close' }));
        expect(screen.getByRole('checkbox', { name: 'Enable professionalism modifier' })).toBeEnabled();
        expect(screen.getByRole('button', { name: 'Add modifier' })).toBeEnabled();
        expect(screen.getByRole('button', { name: 'Reset to defaults' })).toBeEnabled();
    });

    it('lets readers filter webhook deliveries, with every change disabled until Unlock editing', async () => {
        const { user } = renderSettings('webhooks');

        const testDelivery = await screen.findByRole('button', { name: 'Send test delivery: Ops hook' });
        expect(testDelivery).toBeDisabled();
        expect(screen.getByRole('button', { name: 'View: Ops hook' })).toBeEnabled();
        expect(screen.getByRole('button', { name: 'Delete: Ops hook' })).toBeDisabled();
        expect(screen.getByRole('button', { name: 'New target' })).toBeDisabled();

        const status = screen.getByRole('combobox', { name: 'Status' });
        expect(status).toBeEnabled();
        await user.selectOptions(status, 'failed');
        expect(webhookServiceMock.getDeliveries).toHaveBeenLastCalledWith(expect.objectContaining({ status: 'failed' }));

        await unlock(user);
        expect(screen.getByRole('button', { name: 'Edit: Ops hook' })).toBeEnabled();
        expect(screen.getByRole('button', { name: 'New target' })).toBeEnabled();
    });

    it('opens a GitHub rule read-only through View, so its reason template can be read before Unlock editing', async () => {
        const { user } = renderSettings('github');

        // The connection fields show their saved values, disabled.
        expect(await screen.findByDisplayValue('https://github.example.com/api/v3')).toBeDisabled();
        expect(screen.getByRole('checkbox', { name: /Create Triage items for unmatched/i })).toBeChecked();

        // Until a rule is chosen there is no blank new-rule form to mistake for saved values.
        expect(await screen.findByText('Merged PR resolves')).toBeVisible();
        expect(screen.getByText('Choose View on a rule to see all of its details.')).toBeVisible();
        expect(screen.queryByRole('textbox', { name: 'Reason template' })).toBeNull();
        expect(screen.getByRole('button', { name: 'New rule' })).toBeDisabled();
        expect(screen.getByRole('checkbox', { name: 'Disable Merged PR resolves' })).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Delete Merged PR resolves' })).toBeDisabled();
        expect(screen.queryByRole('button', { name: 'Edit Merged PR resolves' })).toBeNull();

        await user.click(screen.getByRole('button', { name: 'View Merged PR resolves' }));
        const drawer = await screen.findByRole('dialog', { name: 'View Merged PR resolves' });
        const reason = within(drawer).getByRole('textbox', { name: 'Reason template' });
        expect(reason).toHaveValue('Resolved by {repo} PR #{pr_number} after merge');
        expect(reason).toBeDisabled();
        expect(within(drawer).getByRole('textbox', { name: /^Name/ })).toHaveValue('Merged PR resolves');
        expect(within(drawer).getByRole('textbox', { name: 'Description' })).toHaveValue('Resolve the task when its PR merges');
        expect(within(drawer).getByRole('combobox', { name: 'Event' })).toHaveValue('github_pr_merged');
        expect(within(drawer).getByRole('combobox', { name: 'From status' })).toHaveValue('active');
        expect(within(drawer).getByRole('combobox', { name: 'Target status' })).toHaveValue('resolved');
        expect(within(drawer).getByRole('spinbutton', { name: 'Order' })).toHaveValue(20);
        expect(within(drawer).getByRole('checkbox', { name: 'Enabled' })).toBeDisabled();
        expect(within(drawer).getByRole('combobox', { name: 'Event' })).toBeDisabled();
        expect(within(drawer).queryByRole('button', { name: 'Save rule' })).toBeNull();

        await user.click(within(drawer).getByRole('button', { name: 'Close' }));
        expect(screen.queryByRole('dialog')).toBeNull();
        expect(githubServiceMock.createStatusAutomationRule).not.toHaveBeenCalled();
        expect(githubServiceMock.updateStatusAutomationRule).not.toHaveBeenCalled();
        expect(githubServiceMock.deleteStatusAutomationRule).not.toHaveBeenCalled();
        expect(systemSettingsServiceMock.updateGitHub).not.toHaveBeenCalled();

        await unlock(user);
        expect(screen.getByRole('button', { name: 'New rule' })).toBeEnabled();
        expect(screen.getByDisplayValue('https://github.example.com/api/v3')).toBeEnabled();
        await user.click(screen.getByRole('button', { name: 'Edit Merged PR resolves' }));
        const editDrawer = await screen.findByRole('dialog', { name: 'Edit Merged PR resolves' });
        expect(within(editDrawer).getByRole('textbox', { name: 'Reason template' })).toBeEnabled();
        expect(within(editDrawer).getByRole('button', { name: 'Save rule' })).toBeEnabled();
    });

    it('opens a webhook target read-only through View, with its headers and subscriptions, before Unlock editing', async () => {
        webhookServiceMock.getTargets.mockResolvedValue([{
            ...webhookTarget, description: 'Routes ops events', headers_json: { 'X-Route': 'ops-desk' },
            subscribed_events_json: ['task.*', 'github.pr_merged'],
        }]);
        const { user } = renderSettings('webhooks');

        expect(await screen.findByText('Choose View on a target to see all of its details.')).toBeVisible();
        await user.click(screen.getByRole('button', { name: 'View: Ops hook' }));
        const drawer = await screen.findByRole('dialog', { name: 'View: Ops hook' });
        expect(within(drawer).getByRole('textbox', { name: /^Name/ })).toHaveValue('Ops hook');
        expect(within(drawer).getByRole('textbox', { name: /^Name/ })).toBeDisabled();
        expect(within(drawer).getByRole('textbox', { name: /^URL/ })).toHaveValue('https://hooks.example.com/1');
        expect(within(drawer).getByRole('textbox', { name: 'Description' })).toHaveValue('Routes ops events');
        const headers = within(drawer).getByRole('textbox', { name: 'Headers JSON' });
        expect(headers).toHaveValue(JSON.stringify({ 'X-Route': 'ops-desk' }, null, 2));
        expect(headers).toBeDisabled();
        expect(within(drawer).getByRole('checkbox', { name: 'GitHub PR merged' })).toBeChecked();
        expect(within(drawer).getByRole('checkbox', { name: 'GitHub PR merged' })).toBeDisabled();
        // The secret itself stays hidden; only whether one is stored is shown.
        expect(within(drawer).getByLabelText('Secret')).toHaveValue('');
        expect(within(drawer).getByLabelText('Secret')).toHaveAttribute('placeholder', 'Signed');
        expect(within(drawer).queryByRole('checkbox', { name: 'Clear stored secret on save' })).toBeNull();
        expect(within(drawer).queryByRole('button', { name: 'Save target' })).toBeNull();

        await user.click(within(drawer).getByRole('button', { name: 'Close' }));
        expect(screen.queryByRole('dialog')).toBeNull();
        expect(webhookServiceMock.updateTarget).not.toHaveBeenCalled();
        expect(webhookServiceMock.createTarget).not.toHaveBeenCalled();
    });
});
