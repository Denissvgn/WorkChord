import { useEffect, useState } from 'react';
import type { KeyboardEvent } from 'react';
import {
    Activity,
    ArrowRight,
    Bell,
    Bot,
    CalendarClock,
    Check,
    CircleHelp,
    Github,
    KeyRound,
    Palette,
    ServerCog,
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
import { PageHeader, PageLayout, SlideOverDrawer } from '../components/ui';

type SettingsTab = 'appearance' | 'scheduling' | 'templates_labels' | 'models_agents' | 'github' | 'webhooks' | 'notifications' | 'admin_access' | 'runtime' | 'about';
type SettingsGroupId = 'personal' | 'planning' | 'agents' | 'integrations' | 'system';

interface SettingsDestination {
    id: SettingsTab;
    labelKey: string;
    descriptionKey: string;
    icon: LucideIcon;
}

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

const isSettingsTab = (value: string | null): value is SettingsTab => (
    SETTINGS_DESTINATIONS.some(destination => destination.id === value)
);

const parseSettingsTab = (value: string | null): SettingsTab => (
    isSettingsTab(value) ? value : 'appearance'
);

const SettingsPage = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const [goalGuideOpen, setGoalGuideOpen] = useState(false);
    const rawTab = searchParams.get('tab');
    const activeTab = parseSettingsTab(rawTab);
    const activeDestination = SETTINGS_DESTINATIONS.find(destination => destination.id === activeTab) ?? SETTINGS_DESTINATIONS[0];
    const ActiveIcon = activeDestination.icon;
    const { theme, setTheme } = useThemeStore();
    const { t } = useTranslation();

    useEffect(() => {
        if (rawTab === null || isSettingsTab(rawTab)) return;
        const nextParams = new URLSearchParams(searchParams);
        nextParams.delete('tab');
        setSearchParams(nextParams, { replace: true });
    }, [rawTab, searchParams, setSearchParams]);

    const settingsHref = (tab: SettingsTab) => {
        const nextParams = new URLSearchParams(searchParams);
        if (tab === 'appearance') nextParams.delete('tab');
        else nextParams.set('tab', tab);
        const query = nextParams.toString();
        return query ? `/settings?${query}` : '/settings';
    };

    const activateTab = (tab: SettingsTab) => {
        const nextParams = new URLSearchParams(searchParams);
        if (tab === 'appearance') nextParams.delete('tab');
        else nextParams.set('tab', tab);
        setSearchParams(nextParams);
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
                actions={(
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
                )}
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
                        {SETTINGS_GROUPS.map(group => (
                            <section key={group.id} className="settings-nav-group" aria-labelledby={`settings-group-${group.id}`}>
                                <h2 id={`settings-group-${group.id}`}>{t(group.labelKey)}</h2>
                                <ul>
                                    {group.items.map(destination => {
                                        const Icon = destination.icon;
                                        const active = destination.id === activeTab;
                                        return (
                                            <li key={destination.id}>
                                                <Link
                                                    to={settingsHref(destination.id)}
                                                    className="settings-nav-item"
                                                    aria-current={active ? 'page' : undefined}
                                                >
                                                    <Icon aria-hidden="true" className="h-4 w-4 shrink-0" />
                                                    <span>{t(destination.labelKey)}</span>
                                                </Link>
                                            </li>
                                        );
                                    })}
                                </ul>
                            </section>
                        ))}
                    </nav>
                </aside>

                <label className="settings-mobile-nav">
                    <span>{t('settingsPage.sectionLabel')}</span>
                    <select
                        className="input"
                        value={activeTab}
                        onChange={event => activateTab(event.target.value as SettingsTab)}
                    >
                        {SETTINGS_GROUPS.map(group => (
                            <optgroup key={group.id} label={t(group.labelKey)}>
                                {group.items.map(destination => (
                                    <option key={destination.id} value={destination.id}>
                                        {t(destination.labelKey)}
                                    </option>
                                ))}
                            </optgroup>
                        ))}
                    </select>
                </label>

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
