import { useLayoutEffect, useRef } from 'react';
import type { ReactNode } from 'react';
import { describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { useLocation, useNavigate } from 'react-router-dom';
import { renderWithProviders } from '../../test/renderWithProviders';
import { AppShell } from './AppShell';

vi.mock('./AppTopNav', () => ({ AppTopNav: () => <header>Top navigation</header> }));
vi.mock('./AppSidebar', () => ({ AppSidebar: () => <aside>Context navigation</aside> }));
vi.mock('./DocumentMetadata', () => ({ DocumentMetadata: () => null }));
vi.mock('./CommandMenu', () => ({ CommandMenu: () => null }));
vi.mock('./RouteErrorBoundary', () => ({
    RouteErrorBoundary: ({ children }: { children: ReactNode }) => <>{children}</>,
}));

const NavigationControls = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const initialFocusRef = useRef<HTMLButtonElement>(null);

    useLayoutEffect(() => {
        initialFocusRef.current?.focus();
    }, []);

    return (
        <>
            <button ref={initialFocusRef} type="button">
                Initial focus
            </button>
            <button
                type="button"
                onClick={() => navigate({ search: '?view=compact' })}
            >
                Change query
            </button>
            <button
                type="button"
                onClick={() => navigate({ hash: '#details' })}
            >
                Change hash
            </button>
            <button
                type="button"
                onClick={() => navigate('/tasks?panel=filters#work-now')}
            >
                Change workspace path
            </button>
            <output aria-label="Current location">
                {`${location.pathname}${location.search}${location.hash}`}
            </output>
        </>
    );
};

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
        expect(screen.getAllByRole('main')).toHaveLength(1);
    });

    it('preserves focus on initial mount and query or hash-only navigation', async () => {
        const { user } = renderWithProviders(
            <AppShell>
                <NavigationControls />
            </AppShell>,
            { initialEntries: ['/overview'] },
        );

        expect(screen.getByRole('button', { name: 'Initial focus' })).toHaveFocus();

        const queryControl = screen.getByRole('button', { name: 'Change query' });
        await user.click(queryControl);
        expect(queryControl).toHaveFocus();
        expect(screen.getByRole('status', { name: 'Current location' }))
            .toHaveTextContent('/overview?view=compact');

        const hashControl = screen.getByRole('button', { name: 'Change hash' });
        await user.click(hashControl);
        expect(hashControl).toHaveFocus();
        expect(screen.getByRole('status', { name: 'Current location' }))
            .toHaveTextContent('/overview#details');
    });

    it('focuses the single workspace main after pathname navigation', async () => {
        const { user } = renderWithProviders(
            <AppShell>
                <NavigationControls />
            </AppShell>,
            { initialEntries: ['/overview?view=compact#details'] },
        );

        await user.click(screen.getByRole('button', { name: 'Change workspace path' }));

        const main = screen.getByRole('main');
        expect(main).toHaveFocus();
        expect(screen.getAllByRole('main')).toHaveLength(1);
        expect(screen.getByRole('status', { name: 'Current location' }))
            .toHaveTextContent('/tasks?panel=filters#work-now');
    });
});
