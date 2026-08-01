import type { ReactNode } from 'react';
import { describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { renderWithProviders } from '../test/renderWithProviders';
import SettingsPage from './SettingsPage';

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
    it('groups destinations and gives the theme radiogroup complete keyboard behavior', async () => {
        const { user } = renderWithProviders(<SettingsPage />, {
            initialEntries: ['/settings'],
        });

        const navigation = screen.getByRole('navigation', { name: 'Settings navigation' });
        expect(within(navigation).getByRole('heading', { name: 'Personal' })).toBeVisible();
        expect(within(navigation).getByRole('heading', { name: 'Planning' })).toBeVisible();
        expect(within(navigation).getByRole('heading', { name: 'Integrations' })).toBeVisible();
        expect(screen.getByRole('combobox', { name: 'Settings section' })).toHaveValue('appearance');

        const lightTheme = screen.getByRole('radio', { name: 'Light' });
        const darkTheme = screen.getByRole('radio', { name: 'Dark' });
        expect(lightTheme).toHaveAttribute('tabindex', '0');
        expect(darkTheme).toHaveAttribute('tabindex', '-1');

        lightTheme.focus();
        await user.keyboard('{ArrowDown}');

        expect(themeStoreMock.setTheme).toHaveBeenCalledWith('dark');
        expect(darkTheme).toHaveFocus();
    });
});
