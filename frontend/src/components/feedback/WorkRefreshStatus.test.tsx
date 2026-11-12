import { useQuery } from '@tanstack/react-query';
import { useState } from 'react';
import { fireEvent, screen } from '@testing-library/react';
import { afterEach, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import { WorkRefreshStatus } from './WorkRefreshStatus';

const Reader = () => {
    const { data } = useQuery({ queryKey: ['tasks', 'refresh-status'], queryFn: async () => 'loaded' });
    return <p>{data ?? 'loading'}</p>;
};

const Page = () => {
    const [open, setOpen] = useState(false);
    return <><WorkRefreshStatus /><button type="button" onClick={() => setOpen(true)}>Open</button>{open && <Reader />}</>;
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
