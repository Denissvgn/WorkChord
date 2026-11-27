import type { ReactNode } from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import { renderWithProviders } from '../test/renderWithProviders';
import SettingsPage from './SettingsPage';
import { CommandMenu } from '../components/layout/CommandMenu';
import i18n, { ensureLanguageResources } from '../i18n/i18n';
import { SINGLE_KEY_SHORTCUTS_STORAGE_KEY } from '../utils/singleKeyShortcutPreference';

const themeStoreMock = vi.hoisted(() => ({
    setTheme: vi.fn(),
}));

vi.mock('../store/themeStore', () => ({
    useThemeStore: () => ({
        theme: 'light',
        setTheme: themeStoreMock.setTheme,
    }),
}));

vi.mock('../components/settings/AdminAccessGate', () => ({
    AdminAccessGate: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

// Each panel is replaced by a line naming it, so a test can tell which settings a section holds.
vi.mock('../components/settings/InterfaceLanguageSettings', () => ({ InterfaceLanguageSettings: () => <p>Interface language panel</p> }));
vi.mock('../components/settings/SchedulingRulesSettings', () => ({ SchedulingRulesSettings: () => <p>Scheduling rules panel</p> }));
vi.mock('../components/settings/TemplateLabelSettings', () => ({ TemplateLabelSettings: () => <p>Templates and labels panel</p> }));
vi.mock('../components/settings/EmailSettingsPanel', () => ({ EmailSettingsPanel: () => <p>Email panel</p> }));
vi.mock('../components/settings/GitHubSettingsPanel', () => ({ GitHubSettingsPanel: () => <p>GitHub automation panel</p> }));
vi.mock('../components/settings/OutboundWebhooksPanel', () => ({ OutboundWebhooksPanel: () => <p>Webhooks panel</p> }));
vi.mock('../components/settings/RuntimeConfigSettings', () => ({
    RuntimeConfigSettings: ({ parts }: { parts: string[] }) => <p>Server settings: {parts.join(', ')}</p>,
}));
vi.mock('../components/settings/AdminAccessPanel', () => ({ AdminAccessPanel: () => <p>Admin key panel</p> }));
vi.mock('../components/settings/AgentAccessPanel', () => ({ AgentAccessPanel: () => <p>Agent key panel</p> }));
vi.mock('../components/settings/ConnectedReadersPanel', () => ({ ConnectedReadersPanel: () => <p>Connected readers panel</p> }));
vi.mock('../components/settings/SystemHealthPanel', () => ({ SystemHealthPanel: () => <p>System health panel</p> }));

const LocationProbe = () => {
    const location = useLocation();
    return <output data-testid="location">{`${location.pathname}${location.search}`}</output>;
};

const renderSettings = (path: string, extra?: ReactNode) => renderWithProviders(
    <>
        <SettingsPage />
        <LocationProbe />
        {extra}
    </>,
    { initialEntries: [path] },
);

const sectionHeader = () => document.querySelector<HTMLElement>('.settings-content')!;
const sectionTitle = () => document.getElementById('settings-destination-title')?.textContent;

const GROUPS = [
    { name: 'My preferences', sections: ['Theme', 'Keyboard shortcuts'] },
    { name: 'Workspace', sections: ['Language', 'Work calendar', 'Scheduling', 'Templates and labels', 'Email notifications'] },
    { name: 'Connections', sections: ['GitHub', 'Webhooks', 'Web intake', 'AI provider', 'Qualification keys'] },
    { name: 'Access and system', sections: ['Access', 'Runtime', 'About'] },
];

describe('SettingsPage', () => {
    beforeEach(() => {
        window.localStorage.clear();
        window.sessionStorage.clear();
        themeStoreMock.setTheme.mockReset();
    });

    it('lists four groups with their sections and no Overview', () => {
        renderSettings('/settings');

        const navigation = screen.getByRole('navigation', { name: 'Settings navigation' });
        const groupHeadings = within(navigation).getAllByRole('heading', { level: 2 });
        expect(groupHeadings.map(heading => heading.textContent)).toEqual(GROUPS.map(group => group.name));
        for (const group of GROUPS) {
            const region = within(navigation).getByRole('region', { name: group.name });
            expect(within(region).getAllByRole('link').map(link => link.textContent)).toEqual(group.sections);
        }
        expect(within(navigation).queryByRole('link', { name: 'Overview' })).toBeNull();
        expect(screen.queryByText(/common settings jobs/i)).toBeNull();
    });

    it('opens on Theme the first time and on the last section used afterwards', async () => {
        const first = renderSettings('/settings');
        expect(sectionTitle()).toBe('Theme');
        expect(screen.getByRole('radiogroup', { name: 'Choose your preferred theme:' })).toBeVisible();

        await first.user.click(screen.getByRole('link', { name: 'Webhooks' }));
        expect(sectionTitle()).toBe('Webhooks');
        first.unmount();

        renderSettings('/settings');
        expect(sectionTitle()).toBe('Webhooks');
        expect(screen.getByText('Webhooks panel')).toBeVisible();
    });

    it('says in every section header where the setting is saved, and keeps workspace-wide settings out of My preferences', async () => {
        const { user } = renderSettings('/settings?tab=theme');
        const navigation = screen.getByRole('navigation', { name: 'Settings navigation' });

        for (const group of GROUPS) {
            for (const name of group.sections) {
                await user.click(within(navigation).getByRole('link', { name }));
                expect(sectionTitle()).toBe(name);
                const header = sectionHeader().querySelector('header')!;
                if (name === 'Access') {
                    // The keys stay in this browser tab; revoking a connected reader changes the server.
                    expect(within(header).getAllByRole('listitem').map(item => item.textContent)).toEqual([
                        'Admin and agent keys: saved in this browser',
                        'Connected readers: saved for the whole workspace',
                    ]);
                    expect(within(header).queryByText(/^Saved /)).toBeNull();
                    continue;
                }
                const saved = within(header).getByText(/^Saved (in this browser|for the whole workspace)$/);
                if (group.name === 'My preferences') {
                    expect(saved).toHaveTextContent('Saved in this browser');
                }
                if (group.name === 'Workspace' || group.name === 'Connections') {
                    expect(saved).toHaveTextContent('Saved for the whole workspace');
                }
            }
        }

        // The interface language changes the workspace for everyone, so it is not a preference.
        const preferences = within(navigation).getByRole('region', { name: 'My preferences' });
        expect(within(preferences).queryByRole('link', { name: /language/i })).toBeNull();
        await user.click(within(navigation).getByRole('link', { name: 'Language' }));
        expect(screen.getByText('Interface language panel')).toBeVisible();
        expect(screen.getByText('Server settings: aiLanguage')).toBeVisible();
    });

    it.each([
        ['appearance', 'Theme', 'theme', null],
        ['scheduling', 'Scheduling', 'scheduling', 'Scheduling rules panel'],
        ['templates_labels', 'Templates and labels', 'templates_labels', 'Templates and labels panel'],
        ['github', 'GitHub', 'github', 'GitHub automation panel'],
        ['webhooks', 'Webhooks', 'webhooks', 'Webhooks panel'],
        ['notifications', 'Email notifications', 'notifications', 'Email panel'],
        ['admin_access', 'Access', 'access', 'Admin key panel'],
        ['runtime', 'Runtime', 'runtime', 'Server settings: restart'],
        ['about', 'About', 'about', 'System health panel'],
        ['calendar', 'Work calendar', 'work_calendar', null],
    ])('opens the section that now holds the settings of the old tab %s', (oldTab, title, newTab, panel) => {
        renderSettings(`/settings?tab=${oldTab}&project=7`);

        expect(sectionTitle()).toBe(title);
        if (panel) expect(screen.getByText(panel)).toBeVisible();
        const location = screen.getByTestId('location').textContent!;
        const params = new URLSearchParams(location.split('?')[1]);
        expect(params.get('tab')).toBe(newTab);
        expect(params.get('project')).toBe('7');
    });

    it('puts the settings of the old Runtime config into their own sections and links them from Runtime', async () => {
        const { user } = renderSettings('/settings?tab=runtime');
        const runtime = sectionHeader();
        for (const [link, parts] of [
            ['Language', 'Server settings: aiLanguage'],
            ['GitHub', 'Server settings: github'],
            ['Web intake', 'Server settings: webIntake'],
            ['AI provider', 'Server settings: llm'],
        ] as const) {
            await user.click(within(runtime).getByRole('link', { name: link }));
            expect(sectionTitle()).toBe(link);
            expect(screen.getByText(parts)).toBeVisible();
            await user.click(screen.getByRole('link', { name: 'Runtime' }));
        }
        expect(screen.getByText('Server settings: restart')).toBeVisible();
    });

    it('keeps GitHub connection fields and automation rules together', () => {
        renderSettings('/settings?tab=github');
        expect(screen.getByText('Server settings: github')).toBeVisible();
        expect(screen.getByText('GitHub automation panel')).toBeVisible();
    });

    it('links model administration from AI provider to Team', () => {
        renderSettings('/settings?tab=ai_provider');
        expect(within(sectionHeader()).getByRole('link', { name: 'Models' })).toHaveAttribute('href', '/team?tab=models');
    });

    it.each(['models', 'models_agents'])('redirects the old %s address to Team and preserves scope', async tab => {
        renderSettings(`/settings?tab=${tab}&project=7`);
        expect(await screen.findByTestId('location')).toHaveTextContent('/team?tab=models&project=7');
    });

    it('drops an unknown tab and opens the default section', () => {
        renderSettings('/settings?tab=overview');
        expect(sectionTitle()).toBe('Theme');
        expect(screen.getByTestId('location')).toHaveTextContent(/^\/settings$/);
    });

    it('searches section and field names, so "key" finds Access and not Keyboard shortcuts', async () => {
        const { user } = renderSettings('/settings?tab=theme');

        const navigation = screen.getByRole('navigation', { name: 'Settings navigation' });
        const search = within(navigation).getByRole('searchbox', { name: 'Search settings' });
        await user.type(search, 'repository');
        expect(within(navigation).getByRole('link', { name: 'GitHub' })).toBeVisible();
        expect(within(navigation).queryByRole('link', { name: 'Scheduling' })).not.toBeInTheDocument();

        await user.clear(search);
        await user.type(search, 'key');
        expect(within(navigation).getByRole('link', { name: 'Access' })).toBeVisible();
        expect(within(navigation).queryByRole('link', { name: 'Keyboard shortcuts' })).not.toBeInTheDocument();

        await user.clear(search);
        await user.type(search, 'SMTP');
        expect(within(navigation).getByRole('link', { name: 'Email notifications' })).toBeVisible();

        await user.clear(search);
        await user.type(search, 'temperature');
        expect(within(navigation).getByRole('link', { name: 'AI provider' })).toBeVisible();

        await user.clear(search);
        await user.type(search, 'rate limit');
        expect(within(navigation).getByRole('link', { name: 'Web intake' })).toBeVisible();
    });

    it.each([
        { field: 'Max output tokens', section: 'AI provider', group: 'Connections' },
        { field: 'Replace intake token', section: 'Web intake', group: 'Connections' },
        { field: 'Reason template', section: 'GitHub', group: 'Connections' },
        { field: 'Port', section: 'Email notifications', group: 'Workspace' },
        { field: 'Test recipient', section: 'Email notifications', group: 'Workspace' },
        { field: 'Default payload JSON', section: 'Templates and labels', group: 'Workspace' },
        { field: 'Max allowable overload', section: 'Scheduling', group: 'Workspace' },
        { field: 'Single-key task shortcuts', section: 'Keyboard shortcuts', group: 'My preferences' },
        { field: 'Agent key', section: 'Access', group: 'Access and system' },
    ])('finds the field "$field" under $group › $section', async ({ field, section, group }) => {
        const { user } = renderSettings('/settings?tab=theme');

        const navigation = screen.getByRole('navigation', { name: 'Settings navigation' });
        await user.type(within(navigation).getByRole('searchbox', { name: 'Search settings' }), field);
        const groupRegion = within(navigation).getByRole('region', { name: group });
        expect(within(groupRegion).getByRole('link', { name: section })).toBeVisible();
        expect(within(navigation).queryByText('No settings match this search.')).not.toBeInTheDocument();
    });

    it.each([
        ['en', 'Divisor', 'Scheduling', 'Workspace'],
        ['en', 'Multiplier', 'Scheduling', 'Workspace'],
        ['en', 'Filter conditions', 'Scheduling', 'Workspace'],
        ['en', 'Sort criteria', 'Scheduling', 'Workspace'],
        ['ru', 'Делитель', 'Планирование', 'Рабочее пространство'],
        ['ru', 'Множитель', 'Планирование', 'Рабочее пространство'],
        ['ru', 'Условия фильтра', 'Планирование', 'Рабочее пространство'],
        ['ru', 'Критерии сортировки', 'Планирование', 'Рабочее пространство'],
    ])('finds Scheduling by %s label %s', async (language, field, section, group) => {
        await ensureLanguageResources(language);
        await i18n.changeLanguage(language);
        try {
            const { user } = renderSettings('/settings?tab=theme');
            const navigation = screen.getByRole('navigation');
            await user.type(within(navigation).getByRole('searchbox'), field);
            expect(within(within(navigation).getByRole('region', { name: group })).getByRole('link', { name: section })).toBeVisible();
        } finally {
            await i18n.changeLanguage('en');
        }
    });

    it('gives the theme radiogroup complete keyboard behavior', async () => {
        const { user } = renderSettings('/settings?tab=theme');

        const lightTheme = screen.getByRole('radio', { name: 'Light' });
        const darkTheme = screen.getByRole('radio', { name: 'Dark' });
        expect(lightTheme).toHaveAttribute('tabindex', '0');
        expect(darkTheme).toHaveAttribute('tabindex', '-1');

        lightTheme.focus();
        await user.keyboard('{ArrowDown}');

        expect(themeStoreMock.setTheme).toHaveBeenCalledWith('dark');
        expect(darkTheme).toHaveFocus();
    });

    it('exposes an on-by-default shortcut preference and synchronizes Commands immediately', async () => {
        const { user } = renderSettings('/settings?tab=shortcuts', <CommandMenu />);

        const settingsToggle = screen.getByRole('checkbox', {
            name: 'Single-key task shortcuts',
        });
        expect(settingsToggle).toBeChecked();

        await user.click(settingsToggle);
        expect(window.localStorage.getItem(SINGLE_KEY_SHORTCUTS_STORAGE_KEY)).toBe('false');

        await user.keyboard('{Control>}k{/Control}');
        const commandDialog = screen.getByRole('dialog', { name: 'Command menu' });
        expect(within(commandDialog).getByRole('checkbox', {
            name: 'Single-key task shortcuts',
        })).not.toBeChecked();
    });
});
