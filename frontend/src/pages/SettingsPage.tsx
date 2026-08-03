import { useEffect, useMemo, useState } from 'react';
import type { KeyboardEvent } from 'react';
import {
    Activity,
    AlertTriangle,
    ArrowRight,
    Bell,
    Bot,
    CalendarClock,
    Check,
    ChevronDown,
    CircleHelp,
    Github,
    KeyRound,
    Keyboard,
    Palette,
    Search,
    ServerCog,
    Settings2,
    Tags,
    Webhook,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Link, useSearchParams } from 'react-router-dom';
import { useThemeStore } from '../store/themeStore';
import { SchedulingRulesSettings } from '../components/settings/SchedulingRulesSettings';
import { EmailSettingsPanel } from '../components/settings/EmailSettingsPanel';
import { TemplateLabelSettings } from '../components/settings/TemplateLabelSettings';
import { GitHubSettingsPanel } from '../components/settings/GitHubSettingsPanel';
import { OutboundWebhooksPanel } from '../components/settings/OutboundWebhooksPanel';
import { RuntimeConfigSettings } from '../components/settings/RuntimeConfigSettings';
import { InterfaceLanguageSettings } from '../components/settings/InterfaceLanguageSettings';
import { AdminAccessPanel } from '../components/settings/AdminAccessPanel';
import { AdminAccessGate } from '../components/settings/AdminAccessGate';
import { AgentAccessPanel } from '../components/settings/AgentAccessPanel';
import { AgentModelAdministration } from '../components/settings/AgentModelAdministration';
import { SystemHealthPanel } from '../components/settings/SystemHealthPanel';
import { Button } from '../components/common/Button';
import { Checkbox } from '../components/common/Checkbox';
import { PageHeader, PageLayout, SlideOverDrawer } from '../components/ui';
import { useAdminAccess } from '../hooks/useAdminAccess';
import { useSingleKeyShortcutPreference } from '../hooks/useSingleKeyShortcutPreference';

type SettingsTab = 'appearance' | 'scheduling' | 'templates_labels' | 'models_agents' | 'github' | 'webhooks' | 'notifications' | 'admin_access' | 'runtime' | 'about';
type SettingsPageTab = 'overview' | SettingsTab;
type SettingsGroupId = 'personal' | 'planning' | 'agents' | 'integrations' | 'system';

interface SettingsDestination {
    id: SettingsTab;
    labelKey: string;
    descriptionKey: string;
    icon: LucideIcon;
}

type SettingsDestinationHeader = Pick<
    SettingsDestination,
    'labelKey' | 'descriptionKey' | 'icon'
>;

interface SettingsGroup {
    id: SettingsGroupId;
    labelKey: string;
    items: SettingsDestination[];
}

const SETTINGS_GROUPS: SettingsGroup[] = [
    {
        id: 'personal',
        labelKey: 'settingsPage.groups.personal',
        items: [
            {
                id: 'appearance',
                labelKey: 'settingsPage.appearance',
                descriptionKey: 'settingsPage.descriptions.appearance',
                icon: Palette,
            },
        ],
    },
    {
        id: 'planning',
        labelKey: 'settingsPage.groups.planning',
        items: [
            {
                id: 'scheduling',
                labelKey: 'settingsPage.scheduling',
                descriptionKey: 'settingsPage.descriptions.scheduling',
                icon: CalendarClock,
            },
            {
                id: 'templates_labels',
                labelKey: 'settingsPage.templatesLabels',
                descriptionKey: 'settingsPage.descriptions.templatesLabels',
                icon: Tags,
            },
        ],
    },
    {
        id: 'agents',
        labelKey: 'settingsPage.groups.agents',
        items: [
            {
                id: 'models_agents',
                labelKey: 'settingsPage.modelsAgents',
                descriptionKey: 'settingsPage.descriptions.modelsAgents',
                icon: Bot,
            },
        ],
    },
    {
        id: 'integrations',
        labelKey: 'settingsPage.groups.integrations',
        items: [
            {
                id: 'github',
                labelKey: 'settingsPage.github',
                descriptionKey: 'settingsPage.descriptions.github',
                icon: Github,
            },
            {
                id: 'webhooks',
                labelKey: 'settingsPage.webhooks',
                descriptionKey: 'settingsPage.descriptions.webhooks',
                icon: Webhook,
            },
            {
                id: 'notifications',
                labelKey: 'settingsPage.notifications',
                descriptionKey: 'settingsPage.descriptions.notifications',
                icon: Bell,
            },
        ],
    },
    {
        id: 'system',
        labelKey: 'settingsPage.groups.system',
        items: [
            {
                id: 'admin_access',
                labelKey: 'settingsPage.adminAccess',
                descriptionKey: 'settingsPage.descriptions.adminAccess',
                icon: KeyRound,
            },
            {
                id: 'runtime',
                labelKey: 'settingsPage.runtimeConfig',
                descriptionKey: 'settingsPage.descriptions.runtime',
                icon: ServerCog,
            },
            {
                id: 'about',
                labelKey: 'settingsPage.about',
                descriptionKey: 'settingsPage.descriptions.about',
                icon: Activity,
            },
        ],
    },
];

const SETTINGS_DESTINATIONS = SETTINGS_GROUPS.flatMap(group => group.items);
const MAX_RECENT_SETTINGS = 3;
export const RECENT_SETTINGS_STORAGE_KEY = 'workchord.settings.recent';

const readRecentSettings = (): SettingsTab[] => {
    if (typeof window === 'undefined') return [];
    try {
        const parsed = JSON.parse(window.localStorage.getItem(RECENT_SETTINGS_STORAGE_KEY) ?? '[]');
        if (!Array.isArray(parsed)) return [];
        const valid = parsed.filter((value): value is SettingsTab => (
            typeof value === 'string' && SETTINGS_DESTINATIONS.some(destination => destination.id === value)
        ));
        return [...new Set(valid)].slice(0, MAX_RECENT_SETTINGS);
    } catch {
        return [];
    }
};

const writeRecentSettings = (tabs: SettingsTab[]) => {
    if (typeof window === 'undefined') return;
    try {
        window.localStorage.setItem(RECENT_SETTINGS_STORAGE_KEY, JSON.stringify(tabs));
    } catch {
        // Recents are an enhancement; Settings remains fully usable if storage is unavailable.
    }
};

const isSettingsTab = (value: string | null): value is SettingsTab => (
    SETTINGS_DESTINATIONS.some(destination => destination.id === value)
);

const parseSettingsTab = (value: string | null): SettingsPageTab => (
    isSettingsTab(value) ? value : 'overview'
);

const SettingsPage = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const [goalGuideOpen, setGoalGuideOpen] = useState(false);
    const [destinationSearch, setDestinationSearch] = useState('');
    const rawTab = searchParams.get('tab');
    const activeTab = parseSettingsTab(rawTab);
    const activeDestination: SettingsDestinationHeader = activeTab === 'overview'
        ? {
            labelKey: 'settingsPage.overview',
            descriptionKey: 'settingsPage.overviewDescription',
            icon: Settings2,
        }
        : SETTINGS_DESTINATIONS.find(destination => destination.id === activeTab) ?? SETTINGS_DESTINATIONS[0];
    const ActiveIcon = activeDestination.icon;
    const { theme, setTheme } = useThemeStore();
    const { hasAdminKey } = useAdminAccess();
    const {
        enabled: singleKeyShortcutsEnabled,
        setEnabled: setSingleKeyShortcutsEnabled,
    } = useSingleKeyShortcutPreference();
    const { t } = useTranslation();
    const recentTabs = useMemo(() => {
        const storedTabs = readRecentSettings();
        if (activeTab === 'overview') return storedTabs;
        return [activeTab, ...storedTabs.filter(tab => tab !== activeTab)]
            .slice(0, MAX_RECENT_SETTINGS);
    }, [activeTab]);
    const normalizedSearch = destinationSearch.trim().toLocaleLowerCase();
    const filteredGroups = useMemo(() => SETTINGS_GROUPS
        .map(group => ({
            ...group,
            items: group.items.filter(destination => (
                [
                    t(destination.labelKey),
                    t(destination.descriptionKey),
                    t(group.labelKey),
                ].some(value => value.toLocaleLowerCase().includes(normalizedSearch))
            )),
        }))
        .filter(group => group.items.length > 0), [normalizedSearch, t]);
    const filteredDestinationCount = filteredGroups.reduce(
        (count, group) => count + group.items.length,
        0,
    );
    const recentDestinations = recentTabs
        .map(tab => SETTINGS_DESTINATIONS.find(destination => destination.id === tab))
        .filter((destination): destination is SettingsDestination => Boolean(destination));

    useEffect(() => {
        if (rawTab === null || isSettingsTab(rawTab)) return;
        const nextParams = new URLSearchParams(searchParams);
        nextParams.delete('tab');
        setSearchParams(nextParams, { replace: true });
    }, [rawTab, searchParams, setSearchParams]);

    useEffect(() => {
        if (activeTab === 'overview') return;
        writeRecentSettings(recentTabs);
    }, [activeTab, recentTabs]);

    const settingsHref = (tab: SettingsPageTab) => {
        const nextParams = new URLSearchParams(searchParams);
        if (tab === 'overview') nextParams.delete('tab');
        else nextParams.set('tab', tab);
        const query = nextParams.toString();
        return query ? `/settings?${query}` : '/settings';
    };

    const renderDestinationLink = (destination: SettingsDestination) => {
        const Icon = destination.icon;
        const active = destination.id === activeTab;
        return (
            <Link
                key={destination.id}
                to={settingsHref(destination.id)}
                className="settings-nav-item"
                aria-current={active ? 'page' : undefined}
            >
                <Icon aria-hidden="true" className="h-4 w-4 shrink-0" />
                <span>{t(destination.labelKey)}</span>
            </Link>
        );
    };

    const adminRecovery = (
        <Link to={settingsHref('admin_access')} className="btn secondary sm">
            <KeyRound aria-hidden="true" className="h-3.5 w-3.5" />
            {t('settingsPage.openAdminAccess')}
        </Link>
    );

    const themes = [
        { id: 'light', name: t('settingsPage.themes.light') },
        { id: 'dark',  name: t('settingsPage.themes.dark') },
        { id: 'blue',  name: t('settingsPage.themes.blue') },
        { id: 'green', name: t('settingsPage.themes.green') },
    ] as const;

    const handleThemeKeyDown = (event: KeyboardEvent<HTMLButtonElement>, index: number) => {
        let nextIndex: number | null = null;
        if (event.key === 'ArrowRight' || event.key === 'ArrowDown') nextIndex = (index + 1) % themes.length;
        if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') nextIndex = (index - 1 + themes.length) % themes.length;
        if (event.key === 'Home') nextIndex = 0;
        if (event.key === 'End') nextIndex = themes.length - 1;
        if (nextIndex === null) return;

        event.preventDefault();
        setTheme(themes[nextIndex].id);
        const radios = event.currentTarget
            .closest('[role="radiogroup"]')
            ?.querySelectorAll<HTMLButtonElement>('[role="radio"]');
        radios?.[nextIndex]?.focus();
    };

    return (
        <PageLayout>
            <PageHeader
                title={t('settingsPage.title')}
                subtitle={t('settingsPage.description')}
                actions={activeTab !== 'overview' ? (
                    <Button
                        type="button"
                        variant="ghost"
                        size="sm"
                        className="gap-1.5"
                        aria-expanded={goalGuideOpen}
                        aria-haspopup="dialog"
                        onClick={() => setGoalGuideOpen(true)}
                    >
                        <CircleHelp aria-hidden="true" className="h-4 w-4" />
                        {t('settingsPage.goalGuide.trigger')}
                    </Button>
                ) : undefined}
            />

            <SlideOverDrawer
                open={goalGuideOpen}
                title={t('settingsPage.goalGuide.title')}
                subtitle={t('settingsPage.goalGuide.description')}
                icon={<CircleHelp aria-hidden="true" className="h-4 w-4" />}
                onClose={() => setGoalGuideOpen(false)}
            >
                <nav className="settings-goal-help" aria-label={t('settingsPage.goalGuide.navigationLabel')}>
                    <Link to={settingsHref('scheduling')} onClick={() => setGoalGuideOpen(false)}>
                        <span>
                            <strong>{t('settingsPage.goalGuide.scheduleTitle')}</strong>
                            <span>{t('settingsPage.goalGuide.scheduleBody')}</span>
                        </span>
                        <ArrowRight aria-hidden="true" className="h-4 w-4" />
                    </Link>
                    <Link to={settingsHref('github')} onClick={() => setGoalGuideOpen(false)}>
                        <span>
                            <strong>{t('settingsPage.goalGuide.githubTitle')}</strong>
                            <span>{t('settingsPage.goalGuide.githubBody')}</span>
                        </span>
                        <ArrowRight aria-hidden="true" className="h-4 w-4" />
                    </Link>
                    <Link to={settingsHref('models_agents')} onClick={() => setGoalGuideOpen(false)}>
                        <span>
                            <strong>{t('settingsPage.goalGuide.agentsTitle')}</strong>
                            <span>{t('settingsPage.goalGuide.agentsBody')}</span>
                        </span>
                        <ArrowRight aria-hidden="true" className="h-4 w-4" />
                    </Link>
                </nav>
            </SlideOverDrawer>

            <div className="settings-shell">
                <aside className="settings-local-nav">
                    <nav aria-label={t('settingsPage.navigationLabel')}>
                        <Link
                            to={settingsHref('overview')}
                            className="settings-nav-item settings-overview-link"
                            aria-current={activeTab === 'overview' ? 'page' : undefined}
                        >
                            <Settings2 aria-hidden="true" className="h-4 w-4 shrink-0" />
                            <span>{t('settingsPage.overview')}</span>
                        </Link>

                        <label className="settings-nav-search">
                            <span className="sr-only">{t('settingsPage.catalog.searchLabel')}</span>
                            <Search aria-hidden="true" className="h-4 w-4" />
                            <input
                                type="search"
                                value={destinationSearch}
                                onChange={event => setDestinationSearch(event.target.value)}
                                placeholder={t('settingsPage.catalog.searchPlaceholder')}
                                aria-label={t('settingsPage.catalog.searchLabel')}
                            />
                        </label>

                        {normalizedSearch ? (
                            <div className="settings-search-results">
                                <p className="settings-nav-status" role="status">
                                    {t('settingsPage.catalog.results', { count: filteredDestinationCount })}
                                </p>
                                {filteredDestinationCount === 0 ? (
                                    <p className="settings-nav-empty">{t('settingsPage.catalog.noResults')}</p>
                                ) : filteredGroups.map(group => (
                                    <section
                                        key={group.id}
                                        className="settings-nav-group"
                                        aria-labelledby={`settings-search-group-${group.id}`}
                                    >
                                        <h2 id={`settings-search-group-${group.id}`}>{t(group.labelKey)}</h2>
                                        <div className="settings-nav-list">
                                            {group.items.map(renderDestinationLink)}
                                        </div>
                                    </section>
                                ))}
                            </div>
                        ) : (
                            <>
                                <section className="settings-nav-group" aria-labelledby="settings-recent-title">
                                    <h2 id="settings-recent-title">{t('settingsPage.catalog.recent')}</h2>
                                    {recentDestinations.length > 0 ? (
                                        <div className="settings-nav-list">
                                            {recentDestinations.map(renderDestinationLink)}
                                        </div>
                                    ) : (
                                        <p className="settings-nav-empty">{t('settingsPage.catalog.recentEmpty')}</p>
                                    )}
                                </section>
                                <details className="settings-catalog">
                                    <summary>
                                        <span>{t('settingsPage.catalog.browseAll')}</span>
                                        <ChevronDown aria-hidden="true" className="h-4 w-4" />
                                    </summary>
                                    <div className="settings-catalog-groups">
                                        {SETTINGS_GROUPS.map(group => (
                                            <section
                                                key={group.id}
                                                className="settings-nav-group"
                                                aria-labelledby={`settings-group-${group.id}`}
                                            >
                                                <h2 id={`settings-group-${group.id}`}>{t(group.labelKey)}</h2>
                                                <div className="settings-nav-list">
                                                    {group.items.map(renderDestinationLink)}
                                                </div>
                                            </section>
                                        ))}
                                    </div>
                                </details>
                            </>
                        )}
                    </nav>
                </aside>

                <section className="settings-content" aria-labelledby="settings-destination-title">
                    <header className="settings-destination-header">
                        <span className="settings-destination-icon" aria-hidden="true">
                            <ActiveIcon className="h-5 w-5" />
                        </span>
                        <div>
                            <h2 id="settings-destination-title">{t(activeDestination.labelKey)}</h2>
                            <p>{t(activeDestination.descriptionKey)}</p>
                        </div>
                    </header>

                    <div className="settings-panel-body">
                        {activeTab === 'overview' && (
                            <div className="settings-overview">
                                {!hasAdminKey && (
                                    <section
                                        className="settings-overview-section"
                                        aria-labelledby="settings-current-warnings-title"
                                    >
                                        <header>
                                            <h3 id="settings-current-warnings-title">
                                                {t('settingsPage.overviewContent.currentWarnings')}
                                            </h3>
                                            <p>{t('settingsPage.overviewContent.currentWarningsDescription')}</p>
                                        </header>
                                        <div className="settings-overview-status warning" role="status">
                                            <AlertTriangle aria-hidden="true" className="h-5 w-5" />
                                            <div>
                                                <strong>{t('settingsPage.overviewContent.adminLockedTitle')}</strong>
                                                <span>{t('settingsPage.overviewContent.adminLockedBody')}</span>
                                                <Link to={settingsHref('admin_access')}>
                                                    {t('settingsPage.openAdminAccess')}
                                                    <ArrowRight aria-hidden="true" className="h-3.5 w-3.5" />
                                                </Link>
                                            </div>
                                        </div>
                                    </section>
                                )}

                                <section
                                    className="settings-overview-section"
                                    aria-labelledby="settings-common-jobs-title"
                                >
                                    <header>
                                        <h3 id="settings-common-jobs-title">
                                            {t('settingsPage.overviewContent.commonJobs')}
                                        </h3>
                                        <p>{t('settingsPage.overviewContent.commonJobsDescription')}</p>
                                    </header>
                                    <nav
                                        className="settings-common-jobs"
                                        aria-label={t('settingsPage.overviewContent.commonJobs')}
                                    >
                                        {(['appearance', 'scheduling', 'github'] as const).map(tab => {
                                            const destination = SETTINGS_DESTINATIONS.find(item => item.id === tab)!;
                                            const Icon = destination.icon;
                                            return (
                                                <Link key={tab} to={settingsHref(tab)}>
                                                    <Icon aria-hidden="true" className="h-4 w-4" />
                                                    <span>
                                                        <strong>{t(`settingsPage.overviewContent.${tab}Title`)}</strong>
                                                        <span>{t(`settingsPage.overviewContent.${tab}Body`)}</span>
                                                    </span>
                                                    <ArrowRight aria-hidden="true" className="h-4 w-4" />
                                                </Link>
                                            );
                                        })}
                                    </nav>
                                </section>
                            </div>
                        )}
                        {activeTab === 'appearance' && (
                            <div className="settings-panel-narrow wc-panel-stack">
                                <AdminAccessGate showPanel={false} recovery={adminRecovery}>
                                    <InterfaceLanguageSettings/>
                                </AdminAccessGate>
                                <section className="card">
                                    <div className="card-pad">
                                        <p className="muted settings-theme-help">{t('settingsPage.chooseTheme')}</p>
                                        <div className="settings-theme-grid" role="radiogroup" aria-label={t('settingsPage.chooseTheme')}>
                                            {themes.map((themeOption, index) => {
                                                const active = theme === themeOption.id;
                                                return (
                                                    <button
                                                        key={themeOption.id}
                                                        type="button"
                                                        role="radio"
                                                        aria-checked={active}
                                                        tabIndex={active ? 0 : -1}
                                                        onClick={() => setTheme(themeOption.id)}
                                                        onKeyDown={event => handleThemeKeyDown(event, index)}
                                                        className="settings-theme-option"
                                                    >
                                                        <span aria-hidden="true" data-theme={themeOption.id} className="settings-theme-preview">
                                                            <span />
                                                            <span />
                                                        </span>
                                                        <strong>{themeOption.name}</strong>
                                                        {active && <Check aria-hidden="true" className="h-4 w-4 text-action" />}
                                                    </button>
                                                );
                                            })}
                                        </div>
                                    </div>
                                </section>
                                <section className="card settings-shortcut-card" aria-labelledby="settings-keyboard-shortcuts-title">
                                    <div className="card-pad">
                                        <header>
                                            <span className="settings-shortcut-icon" aria-hidden="true">
                                                <Keyboard className="h-4 w-4" />
                                            </span>
                                            <div>
                                                <h3 id="settings-keyboard-shortcuts-title">
                                                    {t('settingsPage.keyboardShortcuts.title')}
                                                </h3>
                                                <p>{t('settingsPage.keyboardShortcuts.intro')}</p>
                                            </div>
                                        </header>
                                        <Checkbox
                                            checked={singleKeyShortcutsEnabled}
                                            onChange={setSingleKeyShortcutsEnabled}
                                            label={t('commandMenu.singleKeyShortcuts.label')}
                                            aria-describedby="settings-single-key-shortcuts-description"
                                        />
                                        <p id="settings-single-key-shortcuts-description" className="settings-shortcut-description">
                                            {t('commandMenu.singleKeyShortcuts.description')}
                                        </p>
                                    </div>
                                </section>
                            </div>
                        )}
                        {activeTab === 'scheduling' && (
                            <AdminAccessGate showPanel={false} recovery={adminRecovery}>
                                <SchedulingRulesSettings/>
                            </AdminAccessGate>
                        )}
                        {activeTab === 'templates_labels' && <TemplateLabelSettings/>}
                        {activeTab === 'models_agents' && (
                            <div className="space-y-5">
                                <AgentAccessPanel />
                                <AgentModelAdministration />
                            </div>
                        )}
                        {activeTab === 'github' && <GitHubSettingsPanel/>}
                        {activeTab === 'webhooks' && (
                            <AdminAccessGate showPanel={false} recovery={adminRecovery}>
                                <OutboundWebhooksPanel/>
                            </AdminAccessGate>
                        )}
                        {activeTab === 'notifications' && (
                            <AdminAccessGate showPanel={false} recovery={adminRecovery}>
                                <EmailSettingsPanel/>
                            </AdminAccessGate>
                        )}
                        {activeTab === 'admin_access' && <AdminAccessPanel/>}
                        {activeTab === 'runtime' && (
                            <AdminAccessGate showPanel={false} recovery={adminRecovery}>
                                <RuntimeConfigSettings/>
                            </AdminAccessGate>
                        )}
                        {activeTab === 'about' && (
                            <div className="settings-panel-narrow">
                                <SystemHealthPanel />
                            </div>
                        )}
                    </div>
                </section>
            </div>
        </PageLayout>
    );
};

export default SettingsPage;
