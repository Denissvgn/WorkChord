import { act, renderHook } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { useDraftDismissal } from './useDraftDismissal';

it('declines dirty dismissal and blocks pending dismissal, including sign-out', () => {
    const close = vi.fn();
    const discard = vi.fn();
    const signOut = vi.fn();
    const { result } = renderHook(() => useDraftDismissal(close));
    act(() => { result.current.setDirty(true); result.current.onDiscardReady(discard); result.current.requestClose(); });
    expect(result.current.promptOpen).toBe(true);
    act(() => result.current.cancel());
    expect(close).not.toHaveBeenCalled();
    expect(discard).not.toHaveBeenCalled();
    act(() => result.current.setPending(true));
    act(() => result.current.requestClose());
    const event = new CustomEvent('workchord-before-signout', { cancelable: true, detail: signOut });
    act(() => { window.dispatchEvent(event); });
    expect(event.defaultPrevented).toBe(true);
    expect(result.current.promptOpen).toBe(false);
    expect(signOut).not.toHaveBeenCalled();
    act(() => { result.current.setPending(false); result.current.requestClose(); result.current.discard(); });
    expect(close).toHaveBeenCalledOnce();
    expect(discard).toHaveBeenCalledOnce();
});

describe('clean forms', () => {
    it('closes without a discard prompt and removes the unload listener on unmount', () => {
        const close = vi.fn();
        const { result, unmount } = renderHook(() => useDraftDismissal(close));
        act(() => result.current.requestClose());
        expect(close).toHaveBeenCalledOnce();
        expect(result.current.promptOpen).toBe(false);
        act(() => result.current.setDirty(true));
        const first = new Event('beforeunload', { cancelable: true });
        window.dispatchEvent(first);
        expect(first.defaultPrevented).toBe(true);
        unmount();
        const second = new Event('beforeunload', { cancelable: true });
        window.dispatchEvent(second);
        expect(second.defaultPrevented).toBe(false);
    });
});
