import { act, waitFor } from '@testing-library/react';
import { Route, Routes } from 'react-router-dom';
import { afterEach, describe, expect, it, vi } from 'vitest';
import { Button } from '../components/common/Button';
import { Select } from '../components/common/Select';
import { FilterBar, PageHeader, PageToolbar, ViewSwitch } from '../components/ui';
import { DESTINATIONS } from '../navigation/destinations';
import { LegacyRedirect } from '../navigation/LegacyRedirect';
import { mapLegacyPath } from '../navigation/legacyPaths';
import { legacySwitches } from '../navigation/legacySwitches';
import { metadataForPath, routeMetadata, routeModuleLoaders } from '../navigation/routeModules';
import { expectPageChrome } from './pageChrome';
import { renderWithProviders } from './renderWithProviders';
import { routeRegistry } from './routeRegistry';
import { installWorkspaceApi } from './workspaceApi';

// A concrete path for a route pattern, so `/projects/:projectId` is opened as `/projects/1`.
const samplePath = (pattern: string) => pattern.replace(/:[^/]+/g, match => (match === ':publicId' ? 'shared-plan' : '1'));

afterEach(() => { vi.restoreAllMocks(); });

describe('page chrome', () => {
    it('rejects multiple primary buttons, iteration selectors, and bare selects', () => {
        const { container, rerender } = renderWithProviders(<><PageHeader title="Page" purpose="Purpose." /><Button>One</Button><Button>Two</Button></>);
        expect(() => expectPageChrome(container)).toThrow('More than one primary button');
        rerender(<><PageHeader title="Page" purpose="Purpose." /><Select label="Iteration"><option>One</option></Select></>);
        expect(() => expectPageChrome(container)).toThrow('iteration selector');
        rerender(<><PageHeader title="Page" purpose="Purpose." /><select aria-label="Status"><option>Open</option></select></>);
        expect(() => expectPageChrome(container)).toThrow('Bare select');
    });
    it('accepts a page built from shared parts', () => {
        const { container } = renderWithProviders(<><PageHeader title="Page" purpose="Purpose." primaryAction={<Button>Create</Button>} />
            <PageToolbar filters={<FilterBar filters={[{ id: 'status', label: 'Status', value: '', options: [] }]} onChange={() => {}} onClear={() => {}} />}
                viewSwitch={<ViewSwitch label="View" options={[{ value: 'list', label: 'List' }]} value="list" onChange={() => {}} />} />
            <h2>Records</h2><Select label="Sort"><option>Name</option></Select></>);
        expect(() => expectPageChrome(container)).not.toThrow();
    });
    it('rejects missing headers, extra toolbars, bare buttons, and skipped headings', () => {
        const { container } = renderWithProviders(<><PageToolbar /><PageToolbar /><button>Go</button><h2>Skipped</h2></>);
        expect(() => expectPageChrome(container)).toThrow(/Expected one PageHeader.*More than one PageToolbar.*Bare button.*Heading level skips/);
    });
    it('registers every route exactly once', () => {
        const routes = [...routeMetadata.map(({ key, path }) => `${key}:${path}`), 'notFound:*'].sort();
        expect(routeRegistry.map(({ key, path }) => `${key}:${path}`).sort()).toEqual(routes);
        expect(Object.keys(routeModuleLoaders).sort()).toEqual(routeRegistry.map(({ key }) => key).sort());
    });
    it('counts ten destinations in the navigation registry and checks the page of each', () => {
        expect(DESTINATIONS).toHaveLength(10);
        const checked = new Map(routeRegistry.filter(route => route.status === 'migrated').map(route => [route.path, route.key]));
        expect(DESTINATIONS.filter(destination => !checked.has(destination.path)).map(destination => destination.path)).toEqual([]);
    });
    it('leaves no route pending', () => {
        expect(routeRegistry.filter(route => route.status === 'pending').map(route => route.path)).toEqual([]);
    });
    it.each(routeRegistry)('checks the page frame of route $path', async ({ key, path, status }) => {
        installWorkspaceApi();
        const sample = samplePath(path === '*' ? '/missing' : path);
        const Page = (await routeModuleLoaders[key]()).default;
        // An old path opens the page it redirects to, so that page is the one the frame rule applies to.
        const target = legacySwitches[path] ? mapLegacyPath(sample, '') : null;
        const Target = target ? (await routeModuleLoaders[metadataForPath(target.split('?')[0]).key]()).default : null;
        const { container } = renderWithProviders(<Routes>
            <Route path={path} element={Target ? <LegacyRedirect><Page /></LegacyRedirect> : <Page />} />
            {Target && <Route path="*" element={<Target />} />}
        </Routes>, { initialEntries: [sample] });
        // A page that reads records shows its header once they arrive.
        await waitFor(() => expectPageChrome(container, { status }), { timeout: 5000 });
        await act(() => new Promise(resolve => setTimeout(resolve, 50)));
        expectPageChrome(container, { status });
    // The first dynamic import of a page module can be slow while the whole suite runs.
    }, 20_000);
});
