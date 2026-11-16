import { beforeEach, describe, expect, it } from 'vitest';
import type { ReactNode } from 'react';
import { renderHook } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { useScopeStore } from './scopeStore';
import { scopeLinkNow, useScopeLink } from './useScopeLink';

const builderAt = (entry: string) => renderHook(() => useScopeLink(), {
    wrapper: ({ children }: { children: ReactNode }) => <MemoryRouter initialEntries={[entry]}>{children}</MemoryRouter>,
}).result.current;

describe('useScopeLink', () => {
    beforeEach(() => {
        useScopeStore.setState({ project: null, iteration: null });
    });

    it('adds the scope of the URL to links to scoped pages', () => {
        useScopeStore.setState({ project: 1, iteration: 12 });
        const scopeLink = builderAt('/my-work?project=2&iteration=21');

        expect(scopeLink('/tasks?task=5')).toBe('/tasks?task=5&project=2&iteration=21');
        expect(scopeLink('/')).toBe('/?project=2&iteration=21');
        expect(scopeLink('/plan#checkpoints')).toBe('/plan?project=2&iteration=21#checkpoints');
    });

    it('falls back to the remembered scope', () => {
        useScopeStore.setState({ project: 'all', iteration: 'backlog' });

        expect(builderAt('/team')('/gantt')).toBe('/gantt?project=all&iteration=backlog');
    });

    it('leaves links to other pages and links without a known scope unchanged', () => {
        useScopeStore.setState({ project: 1, iteration: 12 });
        expect(builderAt('/team')('/triage?view=3')).toBe('/triage?view=3');
        expect(builderAt('/team')('/plan/share/abc')).toBe('/plan/share/abc');
        expect(builderAt('/team')('/plan/master?step=schedule')).toBe('/plan/master?step=schedule&project=1&iteration=12');

        useScopeStore.setState({ project: null, iteration: null });
        expect(builderAt('/team')('/tasks')).toBe('/tasks');
    });

    it('lets a link replace part of the scope', () => {
        useScopeStore.setState({ project: 2, iteration: 21 });
        const scopeLink = builderAt('/tasks');

        expect(scopeLink('/tasks', { iteration: 'backlog' })).toBe('/tasks?project=2&iteration=backlog');
        expect(scopeLink('/tasks', { project: 1, iteration: 12 })).toBe('/tasks?project=1&iteration=12');
    });

    it('builds the same link outside React from the remembered scope', () => {
        useScopeStore.setState({ project: 3, iteration: 31 });

        expect(scopeLinkNow('/')).toBe('/?project=3&iteration=31');
        expect(scopeLinkNow('/settings')).toBe('/settings');
    });
});
