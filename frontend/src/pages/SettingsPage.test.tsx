import type { ReactNode } from 'react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { renderWithProviders } from '../test/renderWithProviders';
import SettingsPage from './SettingsPage';
import { CommandMenu } from '../components/layout/CommandMenu';
import { SINGLE_KEY_SHORTCUTS_STORAGE_KEY } from '../utils/singleKeyShortcutPreference';
import { ADMIN_API_KEY_STORAGE_KEY } from '../utils/adminAccess';

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

vi.mock('../components/settings/InterfaceLanguageSettings', () => ({
    InterfaceLanguageSettings: () => <div>Language settings</div>,
}));

describe('SettingsPage', () => {
    beforeEach(() => {
        window.localStorage.clear();
        window.sessionStorage.clear();
        themeStoreMock.setTheme.mockReset();
    });

    it('starts with a warning-focused overview and always lists every destination', () => {
        renderWithProviders(<SettingsPage />, {
            initialEntries: ['/settings'],
        });

        const navigation = screen.getByRole('navigation', { name: 'Settings navigation' });
        expect(screen.getByRole('heading', { name: 'Overview' })).toBeVisible();
        expect(within(navigation).getByRole('link', { name: 'Overview' }))
            .toHaveAttribute('aria-current', 'page');
        expect(screen.getByText('Changing settings needs the admin key')).toBeVisible();
        expect(screen.getByRole('link', { name: 'Open Access' }))
            .toHaveAttribute('href', '/settings?tab=admin_access');
        expect(screen.getByRole('navigation', { name: 'Common settings jobs' }))
            .toBeVisible();
        expect(screen.queryByRole('button', { name: 'Setup help' })).not.toBeInTheDocument();
        expect(within(navigation).queryByText('Browse all settings')).not.toBeInTheDocument();
        expect(within(navigation).getByRole('heading', { name: 'Personal' })).toBeVisible();
        expect(within(navigation).getByRole('heading', { name: 'Planning' })).toBeVisible();
        expect(within(navigation).getByRole('heading', { name: 'Integrations' })).toBeVisible();
        // Ten destinations plus Overview, always listed.
        expect(within(navigation).getAllByRole('link')).toHaveLength(11);
    });

    it('searches field labels and keywords, so "key" finds Access and not Appearance', async () => {
        const { user } = renderWithProviders(<SettingsPage />, {
            initialEntries: ['/settings?tab=appearance'],
        });

        const navigation = screen.getByRole('navigation', { name: 'Settings navigation' });
        const search = within(navigation).getByRole('searchbox', { name: 'Search settings' });
        await user.type(search, 'repository');
        expect(within(navigation).getByRole('link', { name: 'GitHub' })).toBeVisible();
        expect(within(navigation).queryByRole('link', { name: 'Scheduling' })).not.toBeInTheDocument();

        await user.clear(search);
        await user.type(search, 'key');
        expect(within(navigation).getByRole('link', { name: 'Access' })).toBeVisible();
        expect(within(navigation).queryByRole('link', { name: 'Appearance' })).not.toBeInTheDocument();

        await user.clear(search);
        await user.type(search, 'SMTP');
        expect(within(navigation).getByRole('link', { name: 'Notifications' })).toBeVisible();
    });

    it('omits the setup warning when protected settings access is available', () => {
        window.sessionStorage.setItem(ADMIN_API_KEY_STORAGE_KEY, 'test-admin-key');

        renderWithProviders(<SettingsPage />, {
            initialEntries: ['/settings'],
        });

        expect(screen.queryByRole('heading', { name: 'Current setup warning' }))
            .not.toBeInTheDocument();
        expect(screen.getByRole('navigation', { name: 'Common settings jobs' }))
            .toBeVisible();
    });

    it('groups destinations and gives the theme radiogroup complete keyboard behavior', async () => {
        const { user } = renderWithProviders(<SettingsPage />, {
            initialEntries: ['/settings?tab=appearance'],
        });

        expect(screen.queryByText('Start with a setup goal')).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Setup help' })).not.toBeInTheDocument();

        const lightTheme = screen.getByRole('radio', { name: 'Light' });
        const darkTheme = screen.getByRole('radio', { name: 'Dark' });
        expect(lightTheme).toHaveAttribute('tabindex', '0');
        expect(darkTheme).toHaveAttribute('tabindex', '-1');

        lightTheme.focus();
        await user.keyboard('{ArrowDown}');

        expect(themeStoreMock.setTheme).toHaveBeenCalledWith('dark');
        expect(darkTheme).toHaveFocus();
    });

    it('exposes an off-by-default shortcut preference and synchronizes Commands immediately', async () => {
        const { user } = renderWithProviders(
            <>
                <SettingsPage />
                <CommandMenu />
            </>,
            { initialEntries: ['/settings?tab=appearance'] },
        );

        const settingsToggle = screen.getByRole('checkbox', {
            name: 'Enable single-key task shortcuts',
        });
        expect(settingsToggle).not.toBeChecked();

        await user.click(settingsToggle);
        expect(window.localStorage.getItem(SINGLE_KEY_SHORTCUTS_STORAGE_KEY)).toBe('true');

        await user.keyboard('{Control>}k{/Control}');
        const commandDialog = screen.getByRole('dialog', { name: 'Command menu' });
        expect(within(commandDialog).getByRole('checkbox', {
            name: 'Enable single-key task shortcuts',
        })).toBeChecked();
    });
});
