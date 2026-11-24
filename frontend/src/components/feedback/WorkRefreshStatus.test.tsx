import { useQuery } from '@tanstack/react-query';
import { lazy, Suspense, useState } from 'react';
import { fireEvent, screen } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import { WorkRefreshStatus } from './WorkRefreshStatus';

import { Button } from '../../components/common/Button';
const Reader = () => {
    const { data } = useQuery({ queryKey: ['tasks', 'refresh-status'], queryFn: async () => 'loaded' });
    return <p>{data ?? 'loading'}</p>;
};

const Page = () => {
    const [open, setOpen] = useState(false);
    return <><WorkRefreshStatus /><Button type="button" onClick={() => setOpen(true)} variant="secondary">Open</Button>{open && <Reader />}</>;
};

afterEach(() => vi.restoreAllMocks());

it('does not update while another component renders its query', async () => {
    const consoleError = vi.spyOn(console, 'error').mockImplementation(() => undefined);
    renderWithProviders(<Page />);
    // A query that starts after the status has subscribed, as when a page opens.
    fireEvent.click(screen.getByRole('button', { name: 'Open' }));
    expect(await screen.findByText('loaded')).toBeInTheDocument();
    expect(consoleError.mock.calls.filter(call => String(call[0]).includes('while rendering a different component'))).toEqual([]);
});

/** Keeps the thread busy for a few milliseconds, like rendering a large part of a page. */
const renderWork = (milliseconds: number) => {
    const until = performance.now() + milliseconds;
    while (performance.now() < until) { /* busy */ }
};

/** A part of a page that takes a few milliseconds to render and reads its own query, as a busy page does. */
const SlowReader = ({ index }: { index: number }) => {
    const { data } = useQuery({ queryKey: ['tasks', 'slow-reader', index], queryFn: async () => index });
    renderWork(3);
    return <li>{data ?? index}</li>;
};

const SlowPage = () => (
    <>
        <h1>Slow page</h1>
        <ul>{Array.from({ length: 8 }, (_, index) => <SlowReader key={index} index={index} />)}</ul>
    </>
);

it('lets a page that needs several time slices to render appear while its queries start', async () => {
    // The page arrives later, as a lazy route does, so React renders it in time slices it may interrupt.
    const LazyPage = lazy(async () => ({ default: SlowPage }));
    renderWithProviders(<><WorkRefreshStatus /><Suspense fallback={<p>Loading view</p>}><LazyPage /></Suspense></>);

    expect(await screen.findByRole('heading', { name: 'Slow page' }, { timeout: 3000 })).toBeInTheDocument();
});
