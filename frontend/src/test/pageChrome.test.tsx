import { describe, expect, it } from 'vitest';
import { Button } from '../components/common/Button';
import { Select } from '../components/common/Select';
import { FilterBar, PageHeader, PageToolbar, ViewSwitch } from '../components/ui';
import { routeMetadata, routeModuleLoaders } from '../navigation/routeModules';
import { expectPageChrome } from './pageChrome';
import { renderWithProviders } from './renderWithProviders';
import { routeRegistry } from './routeRegistry';

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
    it.each(routeRegistry.filter(route => route.status === 'migrated'))('checks migrated route $path', async ({ key, path, status }) => {
        const Page = (await routeModuleLoaders[key]()).default;
        const { container } = renderWithProviders(<Page />, { initialEntries: [path === '*' ? '/missing' : path] });
        expectPageChrome(container, { status });
    });
});
