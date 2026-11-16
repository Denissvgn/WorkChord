import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { renderWithProviders } from '../test/renderWithProviders';
import { IdentityContext } from '../features/identity/identityContext';
import type { WorkspaceIdentity } from '../features/identity/identityService';
import type { WorkTemplate } from '../types/template';
import type { LabelGroup } from '../types/label';
import type { SchedulingRulesResponse } from '../types/schedulingRules';
import type { OutboundWebhookTarget } from '../types/outboundWebhook';
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
        webhookServiceMock.getTargets.mockResolvedValue([webhookTarget]);
        webhookServiceMock.getDeliveries.mockResolvedValue([]);
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
        expect(screen.getByRole('heading', { name: 'Group details' })).toBeVisible();
        expect(screen.getByRole('textbox', { name: /Key/ })).toHaveValue('workflow');
        expect(screen.getByRole('textbox', { name: /Key/ })).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Save group' })).toBeDisabled();
        expect(templateServiceMock.update).not.toHaveBeenCalled();
        expect(labelServiceMock.updateGroup).not.toHaveBeenCalled();

        // The one control in the Settings header unlocks the same panel.
        await unlock(user);
        expect(screen.getByRole('button', { name: 'New group' })).toBeEnabled();
        expect(screen.getByRole('button', { name: 'Add label' })).toBeEnabled();
        expect(screen.getByRole('textbox', { name: /Key/ })).toBeEnabled();
        await user.click(screen.getByRole('button', { name: 'Actions for Workflow' }));
        expect(menuItem('Edit group')).not.toHaveAttribute('aria-disabled');
        expect(menuItem('Archive group')).not.toHaveAttribute('aria-disabled');
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

        // One rule opens to show its details, which cannot be changed.
        expect(screen.getByRole('checkbox', { name: 'Enable professionalism modifier' })).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Remove modifier' })).toBeDisabled();
        const rule = screen.getByRole('button', { name: /^professionalism/i });
        expect(rule).toBeEnabled();
        await user.click(rule);
        expect(rule).toHaveAttribute('aria-expanded', 'true');
        const ruleId = screen.getByDisplayValue('professionalism');
        expect(ruleId).toBeDisabled();

        await unlock(user);
        // Saving the key reloads the rules, so the rule is opened again.
        const reloadedRule = screen.getByRole('button', { name: /^professionalism/i });
        if (reloadedRule.getAttribute('aria-expanded') !== 'true') await user.click(reloadedRule);
        expect(screen.getByDisplayValue('professionalism')).toBeEnabled();
        expect(screen.getByRole('checkbox', { name: 'Enable professionalism modifier' })).toBeEnabled();
        expect(screen.getByRole('button', { name: 'Add modifier' })).toBeEnabled();
        expect(screen.getByRole('button', { name: 'Reset to defaults' })).toBeEnabled();
    });

    it('lets readers filter webhook deliveries, with every change disabled until Unlock editing', async () => {
        const { user } = renderSettings('webhooks');

        const testDelivery = await screen.findByRole('button', { name: 'Send test delivery: Ops hook' });
        expect(testDelivery).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Edit: Ops hook' })).toBeDisabled();
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
});
