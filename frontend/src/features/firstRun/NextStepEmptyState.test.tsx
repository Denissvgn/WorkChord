import { afterEach, describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import i18n from '../../i18n/i18n';
import { mapLegacyPath } from '../../navigation/legacyPaths';
import { renderWithProviders } from '../../test/renderWithProviders';
import { FIRST_RUN_STEP_IDS, type FirstRunStepId } from './firstRunSteps';
import { NextStepEmptyState } from './NextStepEmptyState';

const progress = vi.hoisted(() => ({
    value: { known: true, nextId: null as FirstRunStepId | null },
}));

vi.mock('./useFirstRunProgress', () => ({
    useFirstRunProgress: () => ({
        known: progress.value.known,
        applies: true,
        steps: [],
        nextId: progress.value.nextId,
        complete: progress.value.nextId === null,
        facts: {},
        projectName: null,
    }),
}));

const setNextStep = (nextId: FirstRunStepId | null, known = true) => {
    progress.value = { known, nextId };
};

/** The buttons and links an empty state offers, in document order. */
const actionsIn = (container: HTMLElement) => Array.from(
    container.querySelectorAll<HTMLElement>('.inline-empty-actions a, .inline-empty-actions button'),
);

afterEach(async () => {
    setNextStep(null);
    await i18n.changeLanguage('en');
});

describe('NextStepEmptyState', () => {
    it.each(['iteration', 'capacity', 'tasks', 'schedule'] as const)(
        'offers one link to the first-run step %s in English',
        nextId => {
            setNextStep(nextId);
            const { container } = renderWithProviders(
                <NextStepEmptyState title="Nothing yet" description="What appears here." fallback={{ label: 'Fallback', to: '/tasks' }} />,
            );
            expect(screen.getByText('Nothing yet')).toBeInTheDocument();
            expect(screen.getByText('What appears here.')).toBeInTheDocument();
            const actions = actionsIn(container);
            expect(actions).toHaveLength(1);
            expect(actions[0].tagName).toBe('A');
            expect(actions[0]).toHaveTextContent(i18n.t(`firstRun.steps.${nextId}.title`, { lng: 'en' }));
        },
    );

    it('offers the same one-step button in Russian', async () => {
        await i18n.changeLanguage('ru');
        setNextStep('iteration');
        const { container } = renderWithProviders(
            <NextStepEmptyState title="Пусто" description="Здесь появится итерация." fallback={{ label: 'Запасной', to: '/tasks' }} />,
        );
        const actions = actionsIn(container);
        expect(actions).toHaveLength(1);
        expect(actions[0]).toHaveTextContent(i18n.t('firstRun.steps.iteration.title', { lng: 'ru' }));
        expect(actions[0]).not.toHaveTextContent('Fallback');
    });

    it('offers the page fallback once setup has no step left', () => {
        setNextStep(null);
        const { container } = renderWithProviders(
            <NextStepEmptyState description="Nothing yet." fallback={{ label: 'New task', to: '/tasks' }} />,
        );
        const actions = actionsIn(container);
        expect(actions).toHaveLength(1);
        expect(actions[0]).toHaveTextContent('New task');
    });

    it('offers the page fallback while setup progress is still unknown', () => {
        setNextStep('iteration', false);
        const { container } = renderWithProviders(
            <NextStepEmptyState description="Nothing yet." fallback={{ label: 'Open Tasks', to: '/tasks' }} />,
        );
        expect(actionsIn(container)).toHaveLength(1);
        expect(actionsIn(container)[0]).toHaveTextContent('Open Tasks');
    });

    it('runs the page action in place for the project step when the page can create one', async () => {
        const user = userEvent.setup();
        const onCreateProject = vi.fn();
        setNextStep('project');
        const { container } = renderWithProviders(
            <NextStepEmptyState description="Projects group work." fallback={{ label: 'New project', onClick: vi.fn() }} onCreateProject={onCreateProject} />,
        );
        const [action] = actionsIn(container);
        expect(action.tagName).toBe('BUTTON');
        await user.click(action);
        expect(onCreateProject).toHaveBeenCalledTimes(1);
    });

    it('never links to a path that redirects (AC3)', () => {
        const hrefs: string[] = [];
        for (const nextId of [null, 'profile', ...FIRST_RUN_STEP_IDS.filter(id => id !== 'profile')] as const) {
            setNextStep(nextId);
            const { container, unmount } = renderWithProviders(
                <NextStepEmptyState description="Nothing yet." fallback={{ label: 'Open Tasks', to: '/tasks' }} />,
            );
            hrefs.push(...actionsIn(container).map(action => action.getAttribute('href') ?? ''));
            unmount();
        }
        hrefs.push('/settings?tab=access');
        expect(hrefs.length).toBeGreaterThan(0);
        for (const href of hrefs) {
            const url = new URL(href, 'http://workchord.local');
            expect(mapLegacyPath(url.pathname, url.search), href).toBeNull();
        }
    });
});
