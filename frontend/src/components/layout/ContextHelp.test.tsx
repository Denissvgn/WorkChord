import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import i18n from '../../i18n/i18n';
import { renderWithProviders } from '../../test/renderWithProviders';
import { SINGLE_KEY_SHORTCUTS_STORAGE_KEY } from '../../utils/singleKeyShortcutPreference';
import { ContextHelp } from './ContextHelp';
import { OPEN_SETUP_GUIDE_EVENT } from './setupGuideEvents';

const LocationProbe = () => {
    const location = useLocation();
    return <output data-testid="help-location">{`${location.pathname}${location.search}`}</output>;
};

describe('ContextHelp', () => {
    beforeEach(() => {
        window.localStorage.clear();
    });

    it('shows the current Gantt workflow before shortcuts and related work', async () => {
        const { user } = renderWithProviders(
            <>
                <ContextHelp />
                <main id="workspace-main" tabIndex={-1}>Workspace</main>
                <LocationProbe />
            </>,
            { initialEntries: ['/gantt'] },
        );

        await user.click(screen.getByRole('button', {
            name: i18n.t('contextHelp.openForPage', {
                page: i18n.t('documentTitles.gantt'),
            }),
        }));

        const drawer = screen.getByRole('dialog', { name: i18n.t('contextHelp.title') });
        const sectionHeadings = within(drawer).getAllByRole('heading', { level: 4 });
        expect(sectionHeadings.map(heading => heading.textContent)).toEqual([
            i18n.t('nav.gantt'),
            i18n.t('contextHelp.glossaryTitle'),
            i18n.t('contextHelp.setupGuide.title'),
            i18n.t('contextHelp.shortcuts.title'),
            i18n.t('contextHelp.related.title'),
        ]);
        expect(within(drawer).getByText(i18n.t('contextHelp.destinations.gantt.summary'))).toBeVisible();
        expect(within(drawer).getByText(i18n.t('gantt.help.sandboxBody'))).toBeVisible();
        // The page's own terms, defined from the vocabulary.
        expect(within(drawer).getByText(i18n.t('contextHelp.glossary.waits_for.definition'))).toBeVisible();
        expect(within(drawer).getByText(i18n.t('contextHelp.shortcuts.globalDescription')))
            .toBeVisible();
        expect(within(drawer).queryByText(i18n.t('contextHelp.shortcuts.taskKeys')))
            .not.toBeInTheDocument();
        expect(within(drawer).queryByRole('checkbox', {
            name: i18n.t('commandMenu.singleKeyShortcuts.label'),
        })).not.toBeInTheDocument();

        await user.click(within(drawer).getByRole('link', {
            name: i18n.t('contextHelp.related.openDestination', {
                destination: i18n.t('nav.planWork'),
            }),
        }));

        expect(screen.getByTestId('help-location')).toHaveTextContent('/plan');
        expect(screen.queryByRole('dialog', { name: i18n.t('contextHelp.title') }))
            .not.toBeInTheDocument();
    });

    it('presents only wired task keys, on by default and easy to turn off', async () => {
        const { user } = renderWithProviders(<ContextHelp />, {
            initialEntries: ['/tasks'],
        });

        await user.click(screen.getByRole('button', {
            name: i18n.t('contextHelp.openForPage', {
                page: i18n.t('documentTitles.tasks'),
            }),
        }));

        const drawer = screen.getByRole('dialog', { name: i18n.t('contextHelp.title') });
        expect(within(drawer).getByText(i18n.t('tasks.guide.readyBody'))).toBeVisible();
        expect(within(drawer).getByText(i18n.t('contextHelp.shortcuts.enabled'))).toBeVisible();
        expect(within(drawer).getAllByText(/^[NFRBM]$/).map(node => node.textContent))
            .toEqual(['N', 'F', 'R', 'B', 'M']);

        const shortcutToggle = within(drawer).getByRole('checkbox', {
            name: i18n.t('commandMenu.singleKeyShortcuts.label'),
        });
        expect(shortcutToggle).toBeChecked();

        await user.click(shortcutToggle);

        expect(shortcutToggle).not.toBeChecked();
        expect(within(drawer).getByText(i18n.t('contextHelp.shortcuts.disabled'))).toBeVisible();
        expect(window.localStorage.getItem(SINGLE_KEY_SHORTCUTS_STORAGE_KEY)).toBe('false');
    });

    it('reuses setup goals on Settings and gives Plan-area views their destination help', async () => {
        const settingsRender = renderWithProviders(<ContextHelp />, {
            initialEntries: ['/settings?tab=about'],
        });

        await settingsRender.user.click(screen.getByRole('button', {
            name: i18n.t('contextHelp.openForPage', {
                page: i18n.t('documentTitles.settings'),
            }),
        }));

        let drawer = screen.getByRole('dialog', { name: i18n.t('contextHelp.title') });
        expect(within(drawer).getByRole('link', {
            name: new RegExp(i18n.t('settingsPage.goalGuide.scheduleTitle')),
        })).toHaveAttribute('href', '/settings?tab=scheduling');
        expect(within(drawer).queryByText(i18n.t('contextHelp.shortcuts.taskKeys')))
            .not.toBeInTheDocument();

        settingsRender.unmount();
        const roadmapRender = renderWithProviders(<ContextHelp />, {
            initialEntries: ['/roadmap'],
        });
        await roadmapRender.user.click(screen.getByRole('button', {
            name: i18n.t('contextHelp.openForPage', {
                page: i18n.t('documentTitles.roadmap'),
            }),
        }));

        drawer = screen.getByRole('dialog', { name: i18n.t('contextHelp.title') });
        expect(within(drawer).getByRole('heading', {
            name: i18n.t('nav.projects'),
        })).toBeVisible();
        expect(within(drawer).getByText(i18n.t('contextHelp.destinations.projects.summary')))
            .toBeVisible();
        expect(within(drawer).queryByText(i18n.t('contextHelp.shortcuts.taskKeys')))
            .not.toBeInTheDocument();
        expect(within(drawer).getByRole('link', {
            name: i18n.t('contextHelp.related.openDestination', {
                destination: i18n.t('nav.planWork'),
            }),
        })).toHaveAttribute('href', '/plan');
    });

    it('opens the setup guide through the event the first-run panel will listen for', async () => {
        const listener = vi.fn();
        window.addEventListener(OPEN_SETUP_GUIDE_EVENT, listener);
        try {
            const { user } = renderWithProviders(<ContextHelp />, {
                initialEntries: ['/team'],
            });

            await user.click(screen.getByRole('button', {
                name: i18n.t('contextHelp.openForPage', {
                    page: i18n.t('documentTitles.team'),
                }),
            }));

            const drawer = screen.getByRole('dialog', { name: i18n.t('contextHelp.title') });
            await user.click(within(drawer).getByRole('button', {
                name: i18n.t('contextHelp.setupGuide.open'),
            }));

            expect(listener).toHaveBeenCalledTimes(1);
        } finally {
            window.removeEventListener(OPEN_SETUP_GUIDE_EVENT, listener);
        }
    });
});
