import WorkCalendarSettings from '../components/settings/WorkCalendarSettings';
import { useEffect, useId, useMemo, useState } from 'react';
import type { KeyboardEvent, ReactNode } from 'react';
import {
    Activity,
    ArrowRight,
    Building2,
    CalendarClock,
    CalendarDays,
    Check,
    Github,
    Globe2,
    Inbox,
    KeyRound,
    Keyboard,
    LockKeyhole,
    Mail,
    Monitor,
    Palette,
    Search,
    ServerCog,
    Sparkles,
    Tags,
    Webhook,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Link, Navigate, useSearchParams } from 'react-router-dom';
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
import { AccessKeysSummary } from '../components/settings/AccessKeysSummary';
import { ConnectedReadersPanel } from '../components/settings/ConnectedReadersPanel';
import { SystemHealthPanel } from '../components/settings/SystemHealthPanel';
import { SharedUnlockContext } from '../components/settings/sharedUnlock';
import { ReadOnlyFieldset } from '../components/settings/ReadOnlyFieldset';
import { SETTINGS_FIELD_LABEL_KEYS } from '../components/settings/settingsFieldLabels';
import type { SettingsSectionId } from '../components/settings/settingsFieldLabels';
import { Button } from '../components/common/Button';
import { Checkbox } from '../components/common/Checkbox';
import { PageHeader, PageLayout } from '../components/ui';
import { useAdminAccess, useKeylessReader } from '../hooks/useAdminAccess';
import { useSingleKeyShortcutPreference } from '../hooks/useSingleKeyShortcutPreference';

type SettingsGroupId = 'myPreferences' | 'workspace' | 'connections' | 'accessSystem';
/** Where a section's values are kept: in this browser only, or on the server for everyone. */
type SavedIn = 'browser' | 'workspace';
/** One part of a section whose parts are kept in different places. */
interface SavedInPart {
    /** Key under `settingsPage.savedInParts` naming the part. */
    part: string;
    savedIn: SavedIn;
}

interface SettingsSection {
    id: SettingsSectionId;
    labelKey: string;
    descriptionKey: string;
    /** Other words people search for in this section; its field labels come from `SETTINGS_FIELD_LABEL_KEYS`. */
    keywordsKey: string;
    icon: LucideIcon;
    savedIn: SavedIn | readonly SavedInPart[];
    /** Changes need the admin key; without it the section is read-only. */
    protected: boolean;
}

interface SettingsGroup {
    id: SettingsGroupId;
    labelKey: string;
    items: SettingsSection[];
}

const section = (
    id: SettingsSectionId,
    key: string,
    icon: LucideIcon,
    savedIn: SettingsSection['savedIn'],
    isProtected: boolean,
): SettingsSection => ({
    id,
    labelKey: `settingsPage.sections.${key}`,
    descriptionKey: `settingsPage.descriptions.${key}`,
    keywordsKey: `settingsPage.keywords.${key}`,
    icon,
    savedIn,
    protected: isProtected,
});

const SETTINGS_GROUPS: SettingsGroup[] = [
    {
        id: 'myPreferences',
        labelKey: 'settingsPage.groups.myPreferences',
        items: [
            section('theme', 'theme', Palette, 'browser', false),
            section('shortcuts', 'shortcuts', Keyboard, 'browser', false),
        ],
    },
    {
        id: 'workspace',
        labelKey: 'settingsPage.groups.workspace',
        items: [
            section('language', 'language', Globe2, 'workspace', true),
            section('work_calendar', 'workCalendar', CalendarDays, 'workspace', false),
            section('scheduling', 'scheduling', CalendarClock, 'workspace', true),
            section('templates_labels', 'templatesLabels', Tags, 'workspace', true),
            section('notifications', 'notifications', Mail, 'workspace', true),
        ],
    },
    {
        id: 'connections',
        labelKey: 'settingsPage.groups.connections',
        items: [
            section('github', 'github', Github, 'workspace', true),
            section('webhooks', 'webhooks', Webhook, 'workspace', true),
            section('web_intake', 'webIntake', Inbox, 'workspace', true),
            section('ai_provider', 'aiProvider', Sparkles, 'workspace', true),
        ],
    },
    {
        id: 'accessSystem',
        labelKey: 'settingsPage.groups.accessSystem',
        items: [
            // The keys stay in this browser tab; revoking a connected reader ends its session on the server.
            section('access', 'access', KeyRound, [
                { part: 'accessKeys', savedIn: 'browser' },
                { part: 'connectedReaders', savedIn: 'workspace' },
            ], false),
            section('runtime', 'runtime', ServerCog, 'workspace', true),
            section('about', 'about', Activity, 'workspace', false),
        ],
    },
];

const SETTINGS_SECTIONS = SETTINGS_GROUPS.flatMap(group => group.items);
const SEARCH_GROUPS = SETTINGS_GROUPS;
const DEFAULT_SECTION: SettingsSectionId = 'theme';
const LAST_SECTION_STORAGE_KEY = 'workchord.settings.lastSection';

/** Earlier `?tab=` values whose settings now live in a section with another id. */
const RENAMED_TABS: Readonly<Record<string, SettingsSectionId>> = {
    appearance: 'theme',
    admin_access: 'access',
    calendar: 'work_calendar',
};

const isSectionId = (value: string | null): value is SettingsSectionId => (
    SETTINGS_SECTIONS.some(item => item.id === value)
);

const resolveTab = (value: string | null): SettingsSectionId | null => {
    if (value === null) return null;
    if (isSectionId(value)) return value;
    return RENAMED_TABS[value] ?? null;
};

const readLastSection = (): SettingsSectionId | null => {
    try {
        const stored = window.localStorage.getItem(LAST_SECTION_STORAGE_KEY);
        return isSectionId(stored) ? stored : null;
    } catch {
        return null;
    }
};

const rememberSection = (id: SettingsSectionId) => {
    try {
        window.localStorage.setItem(LAST_SECTION_STORAGE_KEY, id);
    } catch {
        // Without storage Settings opens on the default section next time.
    }
};

const SavedInNote = ({ savedIn }: { savedIn: SettingsSection['savedIn'] }) => {
    const { t } = useTranslation();
    const icon = (where: SavedIn) => {
        const Icon = where === 'browser' ? Monitor : Building2;
        return <Icon aria-hidden="true" className="h-3.5 w-3.5" />;
    };
    if (typeof savedIn === 'string') {
        return (
            <p className="settings-saved-in" data-saved-in={savedIn}>
                {icon(savedIn)}
                {t(`settingsPage.savedIn.${savedIn}`)}
            </p>
        );
    }
    return (
        <ul className="settings-saved-in-parts">
            {savedIn.map(({ part, savedIn: where }) => (
                <li key={part} className="settings-saved-in" data-saved-in={where}>
                    {icon(where)}
                    {t(`settingsPage.savedInPart.${where}`, { part: t(`settingsPage.savedInParts.${part}`) })}
                </li>
            ))}
        </ul>
    );
};

const SettingsPage = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const [destinationSearch, setDestinationSearch] = useState('');
    const [unlockOpen, setUnlockOpen] = useState(false);
    const [initialSection] = useState(() => readLastSection() ?? DEFAULT_SECTION);
    const lockNoteId = useId();
    const rawTab = searchParams.get('tab');
    const activeId = resolveTab(rawTab) ?? initialSection;
    const activeSection = SETTINGS_SECTIONS.find(item => item.id === activeId) ?? SETTINGS_SECTIONS[0];
    const ActiveIcon = activeSection.icon;
    const { theme, setTheme } = useThemeStore();
    const { hasAdminKey } = useAdminAccess();
    const reader = useKeylessReader();
    const {
        enabled: singleKeyShortcutsEnabled,
        setEnabled: setSingleKeyShortcutsEnabled,
    } = useSingleKeyShortcutPreference();
    const { t } = useTranslation();
    const normalizedSearch = destinationSearch.trim().toLocaleLowerCase();
    const filteredGroups = useMemo(() => {
        const searchable = (group: SettingsGroup, item: SettingsSection) => [
            t(item.labelKey), t(item.descriptionKey), t(item.keywordsKey), t(group.labelKey),
            ...SETTINGS_FIELD_LABEL_KEYS[item.id].map(key => t(key)),
        ].join(' ').toLocaleLowerCase();
        const words = normalizedSearch.split(/\s+/).filter(Boolean);
        // Whole words first, so "key" finds Access rather than "keyboard" or "single-key"; any substring otherwise.
        const wholeWords = (text: string) => {
            const present = new Set(text.split(/[^\p{L}\p{N}:-]+/u));
            return words.every(word => present.has(word));
        };
        const filterBy = (matches: (text: string) => boolean) => SEARCH_GROUPS
            .map(group => ({ ...group, items: group.items.filter(item => matches(searchable(group, item))) }))
            .filter(group => group.items.length > 0);
        const exact = filterBy(wholeWords);
        return exact.length > 0 ? exact : filterBy(text => text.includes(normalizedSearch));
    }, [normalizedSearch, t]);
    const filteredSectionCount = filteredGroups.reduce(
        (count, group) => count + group.items.length,
        0,
    );

    // An earlier tab value is rewritten to the section that now holds its settings; an unknown one is dropped.
    useEffect(() => {
        if (rawTab === null || isSectionId(rawTab) || rawTab === 'models' || rawTab === 'models_agents') return;
        const nextParams = new URLSearchParams(searchParams);
        const renamed = RENAMED_TABS[rawTab];
        if (renamed) nextParams.set('tab', renamed);
        else nextParams.delete('tab');
        setSearchParams(nextParams, { replace: true });
    }, [rawTab, searchParams, setSearchParams]);

    useEffect(() => {
        rememberSection(activeSection.id);
    }, [activeSection.id]);

    const settingsHref = (id: SettingsSectionId) => {
        const nextParams = new URLSearchParams(searchParams);
        nextParams.set('tab', id);
        return `/settings?${nextParams.toString()}`;
    };

    const renderSectionLink = (item: SettingsSection) => {
        const Icon = item.icon;
        const active = item.id === activeSection.id;
        return (
            <Link
                key={item.id}
                to={settingsHref(item.id)}
                className="settings-nav-item"
                aria-current={active ? 'page' : undefined}
            >
                <Icon aria-hidden="true" className="h-4 w-4 shrink-0" />
                <span>{t(item.labelKey)}</span>
            </Link>
        );
    };

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

    const locked = !hasAdminKey;
    // One control in the page header unlocks every protected section at once.
    const editLock = activeSection.protected && locked ? (
        <div className="settings-edit-lock">
            <span id={lockNoteId} className="settings-edit-lock-state">
                <LockKeyhole aria-hidden="true" className="h-3.5 w-3.5" />
                {reader.settings ? t('settings.readOnlyTitle') : t('settings.lockedTitle')}
                <span className="sr-only">. {t('settings.readOnlyBody')}</span>
            </span>
            <span aria-hidden="true">·</span>
            <Button
                size="sm"
                variant="secondary"
                aria-expanded={unlockOpen}
                aria-controls="settings-unlock-panel"
                onClick={() => setUnlockOpen(open => !open)}
            >
                {t('settings.unlockEditing')}
            </Button>
        </div>
    ) : !locked && unlockOpen ? (
        <div className="settings-edit-lock">
            <span className="settings-edit-lock-state" role="status">
                <Check aria-hidden="true" className="h-3.5 w-3.5" />
                {t('settings.editingUnlocked')}
            </span>
            <Button size="sm" variant="secondary" onClick={() => setUnlockOpen(false)}>
                {t('actions.close')}
            </Button>
        </div>
    ) : null;

    /** `managesReadOnly`: the panel locks only its editing controls, so its tabs and filters still work. */
    const gated = (content: ReactNode, { managesReadOnly = false } = {}) => (
        <AdminAccessGate showPanel={false} readable managesReadOnly={managesReadOnly}>{content}</AdminAccessGate>
    );

    const sectionLink = (id: SettingsSectionId) => {
        const target = SETTINGS_SECTIONS.find(item => item.id === id)!;
        return <Link key={id} to={settingsHref(id)}>{t(target.labelKey)}</Link>;
    };

    const renderSection = (): ReactNode => {
        switch (activeSection.id) {
            case 'theme':
                return (
                    <section className="card settings-panel-narrow">
                        <div className="card-pad">
                            <p className="muted settings-theme-help">{t('settingsPage.chooseTheme')}</p>
                            <div className="settings-theme-grid" role="radiogroup" aria-label={t('settingsPage.chooseTheme')}>
                                {themes.map((themeOption, index) => {
                                    const active = theme === themeOption.id;
                                    return (
                                        <Button
                                            key={themeOption.id}
                                            type="button"
                                            role="radio"
                                            data-page-chrome-control="button"
                                            aria-checked={active}
                                            tabIndex={active ? 0 : -1}
                                            onClick={() => setTheme(themeOption.id)}
                                            onKeyDown={event => handleThemeKeyDown(event, index)}
                                            className="settings-theme-option"
                                         variant="secondary">
                                            <span aria-hidden="true" data-theme={themeOption.id} className="settings-theme-preview">
                                                <span />
                                                <span />
                                            </span>
                                            <strong>{themeOption.name}</strong>
                                            {active && <Check aria-hidden="true" className="h-4 w-4 text-action" />}
                                        </Button>
                                    );
                                })}
                            </div>
                        </div>
                    </section>
                );
            case 'shortcuts':
                return (
                    <section className="card settings-shortcut-card settings-panel-narrow">
                        <div className="card-pad">
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
                );
            case 'language':
                return gated(
                    <div className="wc-panel-stack max-w-3xl">
                        <InterfaceLanguageSettings />
                        <RuntimeConfigSettings parts={['aiLanguage']} />
                    </div>,
                );
            case 'work_calendar':
                return <WorkCalendarSettings />;
            case 'scheduling':
                return gated(<SchedulingRulesSettings />, { managesReadOnly: true });
            case 'templates_labels':
                return gated(<TemplateLabelSettings />, { managesReadOnly: true });
            case 'notifications':
                return gated(<EmailSettingsPanel />);
            case 'github':
                // The automation rules lock only their changes, so each rule still opens through View.
                return gated(
                    <div className="space-y-5">
                        <ReadOnlyFieldset>
                            <RuntimeConfigSettings parts={['github']} />
                        </ReadOnlyFieldset>
                        <GitHubSettingsPanel />
                    </div>,
                    { managesReadOnly: true },
                );
            case 'webhooks':
                return gated(<OutboundWebhooksPanel />, { managesReadOnly: true });
            case 'web_intake':
                return gated(<RuntimeConfigSettings parts={['webIntake']} />);
            case 'ai_provider':
                return (
                    <div className="space-y-5">
                        {gated(<RuntimeConfigSettings parts={['llm']} />)}
                        <p className="settings-related-note">
                            {t('settingsPage.aiProviderModelsNote')}{' '}
                            <Link to="/team?tab=models">
                                {t('teamPage.tabs.models')}
                                <ArrowRight aria-hidden="true" className="h-3.5 w-3.5" />
                            </Link>
                        </p>
                    </div>
                );
            case 'access':
                return (
                    <div className="space-y-5">
                        <AccessKeysSummary />
                        <ConnectedReadersPanel />
                        <AdminAccessPanel />
                        <AgentAccessPanel />
                    </div>
                );
            case 'runtime':
                return (
                    <div className="space-y-5">
                        <p className="settings-related-note">
                            {t('settingsPage.runtimeMovedNote')}{' '}
                            {(['language', 'github', 'web_intake', 'ai_provider'] as const).map((id, index, all) => (
                                <span key={id}>
                                    {sectionLink(id)}
                                    {index < all.length - 1 ? ', ' : '.'}
                                </span>
                            ))}
                        </p>
                        {gated(<RuntimeConfigSettings parts={['restart']} />)}
                    </div>
                );
            case 'about':
                return (
                    <div className="settings-panel-narrow">
                        <SystemHealthPanel />
                    </div>
                );
        }
    };

    if (['models', 'models_agents'].includes(searchParams.get('tab') ?? '')) {
        const params = new URLSearchParams(searchParams);
        params.set('tab', 'models');
        return <Navigate to={`/team?${params.toString()}`} replace />;
    }

    return (
        <PageLayout>
            <PageHeader
                title={t('settingsPage.title')}
                purpose={t('settingsPage.description')}
                secondaryActions={editLock}
            />

            {unlockOpen && (
                <div id="settings-unlock-panel">
                    <AdminAccessPanel headingLevel={2} />
                </div>
            )}

            <div className="settings-shell">
                <aside className="settings-local-nav">
                    <nav aria-label={t('settingsPage.navigationLabel')}>
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
                                    {t('settingsPage.catalog.results', { count: filteredSectionCount })}
                                </p>
                                {filteredSectionCount === 0 ? (
                                    <p className="settings-nav-empty">{t('settingsPage.catalog.noResults')}</p>
                                ) : filteredGroups.map(group => (
                                    <section
                                        key={group.id}
                                        className="settings-nav-group"
                                        aria-labelledby={`settings-search-group-${group.id}`}
                                    >
                                        <h2 id={`settings-search-group-${group.id}`}>{t(group.labelKey)}</h2>
                                        <div className="settings-nav-list">
                                            {group.items.map(renderSectionLink)}
                                        </div>
                                    </section>
                                ))}
                            </div>
                        ) : (
                            <div className="settings-catalog-groups">
                                {SETTINGS_GROUPS.map(group => (
                                    <section
                                        key={group.id}
                                        className="settings-nav-group"
                                        aria-labelledby={`settings-group-${group.id}`}
                                    >
                                        <h2 id={`settings-group-${group.id}`}>{t(group.labelKey)}</h2>
                                        <div className="settings-nav-list">
                                            {group.items.map(renderSectionLink)}
                                        </div>
                                    </section>
                                ))}
                            </div>
                        )}
                    </nav>
                </aside>

                <section className="settings-content" aria-labelledby="settings-destination-title">
                    <header className="settings-destination-header">
                        <span className="settings-destination-icon" aria-hidden="true">
                            <ActiveIcon className="h-5 w-5" />
                        </span>
                        <div>
                            <h2 id="settings-destination-title">{t(activeSection.labelKey)}</h2>
                            <p>{t(activeSection.descriptionKey)}</p>
                            <SavedInNote savedIn={activeSection.savedIn} />
                        </div>
                    </header>

                    <div className="settings-panel-body">
                        <SharedUnlockContext.Provider value={{ noteId: lockNoteId }}>
                            {renderSection()}
                        </SharedUnlockContext.Provider>
                    </div>
                </section>
            </div>
        </PageLayout>
    );
};

export default SettingsPage;
