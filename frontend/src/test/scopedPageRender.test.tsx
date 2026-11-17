import { act, screen, waitFor, within } from '@testing-library/react';
import { Route, Routes, Outlet } from 'react-router-dom';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { ScopeBar } from '../components/layout/ScopeBar';
import { useScopeStore } from '../features/scope/scopeStore';
import { useWorkScope } from '../features/scope/useWorkScope';
import i18n from '../i18n/i18n';
import { routeModuleLoaders } from '../navigation/routeModules';
import { expectPageChrome } from './pageChrome';
import { renderWithProviders } from './renderWithProviders';
import { installWorkspaceApi } from './workspaceApi';

/** Stands in for the app shell: it holds the scope for every page and shows the scope bar, as the top bar does. */
const Shell = () => {
    const { isReady } = useWorkScope();
    return <><output data-testid="ready">{String(isReady)}</output><ScopeBar /><Outlet /></>;
};

const SCOPED_PAGES = [
    { key: 'overview', path: '/' },
    { key: 'plan', path: '/plan' },
    { key: 'gantt', path: '/gantt' },
    { key: 'tasks', path: '/tasks' },
    { key: 'analytics', path: '/analytics' },
] as const;

// Today is 2026-11-16, inside iteration 12 of project 1.
const SCOPES = [
    { label: 'All projects', search: '?project=all', project: 'All projects' },
    { label: 'a project', search: '?project=1&iteration=12', project: 'Alpha', iteration: 'Iteration 12' },
    { label: 'Backlog', search: '?project=1&iteration=backlog', project: 'Alpha', iteration: 'Backlog' },
] as const;

describe('scoped pages', () => {
    let errors: ReturnType<typeof vi.spyOn>;
    beforeEach(() => {
        vi.useFakeTimers({ toFake: ['Date'] });
        vi.setSystemTime(new Date('2026-11-16T12:00:00Z'));
        useScopeStore.setState({ project: null, iteration: null });
        errors = vi.spyOn(console, 'error').mockImplementation(() => {});
    });
    afterEach(() => {
        vi.useRealTimers();
        vi.restoreAllMocks();
    });

    describe.each(SCOPED_PAGES)('$key', ({ key, path }) => {
        it.each(SCOPES)(`renders with $label in scope`, async ({ search, project, ...scope }) => {
            const { unplanned } = installWorkspaceApi();
            const Page = (await routeModuleLoaders[key]()).default;
            const { container } = renderWithProviders(
                <Routes><Route element={<Shell />}><Route path={path} element={<Page />} /></Route></Routes>,
                { initialEntries: [`${path}${search}`] },
            );
            await waitFor(() => expect(screen.getByTestId('ready')).toHaveTextContent('true'));
            const bar = within(screen.getByTestId('scope-bar'));
            await waitFor(() => expect(bar.getByRole('combobox', { name: i18n.t('scopeBar.project') })).toHaveValue(project));
            if ('iteration' in scope) {
                await waitFor(() => expect(bar.getByRole('combobox', { name: i18n.t('scopeBar.iteration') })).toHaveValue(scope.iteration));
            }
            // Let the page's own requests finish before looking for an error.
            await act(() => new Promise(resolve => setTimeout(resolve, 200)));

            expect(unplanned).toEqual([]);
            expectPageChrome(container);
            expect(screen.queryAllByRole('alert')).toEqual([]);
            expect(errors).not.toHaveBeenCalled();
        }, 20_000);
    });
});
