import { afterEach, describe, expect, it, vi } from 'vitest';
import { act, render, screen } from '@testing-library/react';
import { ToastProvider } from './ToastProvider';
import { useToast } from './toast';

const Trigger = ({ kind }: { kind: 'success' | 'error' }) => {
    const toast = useToast();
    return <button type="button" onClick={() => toast[kind](kind === 'error' ? 'The project could not be saved.' : 'Project saved.')}>show</button>;
};

describe('one feedback rule for toasts', () => {
    afterEach(() => vi.useRealTimers());

    it('keeps an error toast until it is dismissed and announces it assertively', () => {
        vi.useFakeTimers();
        render(<ToastProvider><Trigger kind="error" /></ToastProvider>);
        act(() => screen.getByRole('button', { name: 'show' }).click());
        act(() => { vi.advanceTimersByTime(60_000); });
        expect(screen.getByRole('alert')).toHaveTextContent('The project could not be saved.');
    });

    it('lets a success toast time out', () => {
        vi.useFakeTimers();
        render(<ToastProvider><Trigger kind="success" /></ToastProvider>);
        act(() => screen.getByRole('button', { name: 'show' }).click());
        expect(screen.getByText('Project saved.')).toBeInTheDocument();
        act(() => { vi.advanceTimersByTime(6_000); });
        expect(screen.queryByText('Project saved.')).not.toBeInTheDocument();
    });
});
