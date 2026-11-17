import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { renderWithProviders } from '../test/renderWithProviders';
import { IdentityContext } from '../features/identity/identityContext';
import type { WorkspaceIdentity } from '../features/identity/identityService';
import SettingsPage from './SettingsPage';
import { ADMIN_API_KEY_STORAGE_KEY } from '../utils/adminAccess';

const verifyKey = vi.hoisted(() => vi.fn());
vi.mock('../services/adminAccessService', () => ({ verifyAdminApiKey: verifyKey }));

// Each protected panel is replaced by one field, so the test can tell whether it can be edited.
// Panels that lock only their own editing controls wrap that field the way the real panels do;
// SettingsPage.readOnlyPanels.test.tsx runs those real panels.
const { field, selfLockingField } = vi.hoisted(() => {
    const field = (label: string) => () => <label>{label} <input defaultValue="value" /></label>;
    const selfLockingField = async (label: string) => {
        const { ReadOnlyFieldset } = await import('../components/settings/ReadOnlyFieldset');
        const Field = field(label);
        return () => <ReadOnlyFieldset><Field /></ReadOnlyFieldset>;
    };
    return { field, selfLockingField };
});
vi.mock('../components/settings/InterfaceLanguageSettings', () => ({ InterfaceLanguageSettings: field('Interface language') }));
vi.mock('../components/settings/SchedulingRulesSettings', async () => ({ SchedulingRulesSettings: await selfLockingField('Working hours') }));
vi.mock('../components/settings/TemplateLabelSettings', async () => ({ TemplateLabelSettings: await selfLockingField('Template name') }));
vi.mock('../components/settings/EmailSettingsPanel', () => ({ EmailSettingsPanel: field('Mail server') }));
vi.mock('../components/settings/GitHubSettingsPanel', async () => ({ GitHubSettingsPanel: await selfLockingField('Automation rule') }));
vi.mock('../components/settings/OutboundWebhooksPanel', async () => ({ OutboundWebhooksPanel: await selfLockingField('Webhook target') }));
vi.mock('../components/settings/RuntimeConfigSettings', () => ({
    RuntimeConfigSettings: ({ parts }: { parts: string[] }) => <label>{`Server ${parts.join(' ')}`} <input defaultValue="value" /></label>,
}));
vi.mock('../components/settings/AgentAccessPanel', () => ({ AgentAccessPanel: () => null }));
vi.mock('../components/settings/ConnectedReadersPanel', () => ({ ConnectedReadersPanel: () => null }));
vi.mock('../components/settings/SystemHealthPanel', () => ({ SystemHealthPanel: () => null }));

/** Every protected section, with the field its panel shows. */
const PROTECTED = [
    ['Language', 'Interface language'],
    ['Scheduling', 'Working hours'],
    ['Templates and labels', 'Template name'],
    ['Email notifications', 'Mail server'],
    ['GitHub', 'Automation rule'],
    ['Webhooks', 'Webhook target'],
    ['Web intake', 'Server webIntake'],
    ['AI provider', 'Server llm'],
    ['Runtime', 'Server restart'],
] as const;

const identity = (overrides: Partial<WorkspaceIdentity> = {}): WorkspaceIdentity => ({
    mode: 'trusted_local', authenticated: false, configured: false, principal: null, profile: null,
    workspace_role: null, projects: {}, csrf_token: null, ...overrides,
});

const renderSettings = (value: WorkspaceIdentity, path = '/settings?tab=scheduling') => renderWithProviders(
    <IdentityContext.Provider value={{ identity: value, refresh: vi.fn(), signOut: async () => undefined }}>
        <SettingsPage />
    </IdentityContext.Provider>,
    { initialEntries: [path] },
);

const header = () => screen.getByTestId('page-header');
const navigation = () => screen.getByRole('navigation', { name: 'Settings navigation' });
const content = () => document.querySelector<HTMLElement>('.settings-content')!;

describe('SettingsPage editing lock', () => {
    beforeEach(() => {
        window.localStorage.clear();
        window.sessionStorage.clear();
        verifyKey.mockReset().mockResolvedValue(undefined);
    });

    it('shows every protected section read-only behind one Unlock editing control, and that control unlocks them all', async () => {
        const { user } = renderSettings(identity());

        for (const [section, label] of PROTECTED) {
            await user.click(within(navigation()).getByRole('link', { name: section }));
            // Readable, not editable.
            expect(within(content()).getByRole('textbox', { name: label })).toBeDisabled();
            expect(within(header()).getByText('Read-only')).toBeVisible();
            // One control, in the Settings header, and none inside the section.
            expect(screen.getAllByRole('button', { name: 'Unlock editing' })).toHaveLength(1);
            expect(within(header()).getByRole('button', { name: 'Unlock editing' })).toBeVisible();
        }

        await user.click(within(header()).getByRole('button', { name: 'Unlock editing' }));
        await user.type(screen.getByLabelText('Admin key'), 'operator-key');
        await user.click(screen.getByRole('button', { name: 'Save key' }));
        expect(await screen.findByText('Editing unlocked')).toBeVisible();
        expect(verifyKey).toHaveBeenCalledWith('operator-key');
        expect(screen.queryByRole('button', { name: 'Unlock editing' })).toBeNull();

        for (const [section, label] of PROTECTED) {
            await user.click(within(navigation()).getByRole('link', { name: section }));
            expect(within(content()).getByRole('textbox', { name: label })).toBeEnabled();
            expect(screen.queryByText('Read-only')).toBeNull();
        }
    });

    it('shows no lock control on sections that are not protected', async () => {
        const { user } = renderSettings(identity(), '/settings?tab=theme');
        for (const section of ['Theme', 'Keyboard shortcuts', 'Work calendar', 'Access', 'About']) {
            await user.click(within(navigation()).getByRole('link', { name: section }));
            expect(screen.queryByRole('button', { name: 'Unlock editing' })).toBeNull();
        }
    });

    it('keeps protected sections closed to people who may not read them, with the same single control', () => {
        renderSettings(identity({
            mode: 'managed', authenticated: true, principal: { id: 3, kind: 'human', display_name: 'Guest' },
        }));
        expect(screen.queryByRole('textbox', { name: 'Working hours' })).toBeNull();
        expect(within(content()).getByRole('heading', { name: 'Admin key required' })).toBeVisible();
        expect(within(header()).getByText('Locked')).toBeVisible();
        expect(screen.getAllByRole('button', { name: 'Unlock editing' })).toHaveLength(1);
    });

    it('edits protected sections directly when the admin key is already in this browser tab', () => {
        window.sessionStorage.setItem(ADMIN_API_KEY_STORAGE_KEY, 'operator-key');
        renderSettings(identity());
        expect(screen.getByRole('textbox', { name: 'Working hours' })).toBeEnabled();
        expect(screen.queryByRole('button', { name: 'Unlock editing' })).toBeNull();
    });
});
