import type { ReactNode } from 'react';
import { describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { AppShell } from './AppShell';

vi.mock('./AppTopNav', () => ({ AppTopNav: () => <header>Top navigation</header> }));
vi.mock('./AppSidebar', () => ({ AppSidebar: () => <aside>Context navigation</aside> }));
vi.mock('./DocumentMetadata', () => ({ DocumentMetadata: () => null }));
vi.mock('./CommandMenu', () => ({ CommandMenu: () => null }));
vi.mock('./RouteErrorBoundary', () => ({
    RouteErrorBoundary: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

describe('AppShell', () => {
    it('offers a keyboard shortcut to a focusable workspace main region', () => {
        renderWithProviders(
            <AppShell>
                <div>Workspace content</div>
            </AppShell>,
            { initialEntries: ['/overview'] },
        );

        expect(screen.getByRole('link', { name: 'Skip to workspace content' }))
            .toHaveAttribute('href', '#workspace-main');

        const main = screen.getByRole('main');
        expect(main).toHaveAttribute('id', 'workspace-main');
        expect(main).toHaveAttribute('tabindex', '-1');
        expect(main).toHaveTextContent('Workspace content');
    });
});
