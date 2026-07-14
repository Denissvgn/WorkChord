import { useRef, useState } from 'react';
import type { KeyboardEvent } from 'react';
import { useTranslation } from 'react-i18next';
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
import { SystemHealthPanel } from '../components/settings/SystemHealthPanel';
import { PageHeader, PageLayout } from '../components/ui';

type SettingsTab = 'appearance' | 'scheduling' | 'templates_labels' | 'runtime' | 'github' | 'webhooks' | 'notifications' | 'about';

const TABS: { id: SettingsTab; labelKey: string }[] = [
    { id: 'appearance',       labelKey: 'settingsPage.appearance' },
    { id: 'scheduling',       labelKey: 'settingsPage.scheduling' },
    { id: 'templates_labels', labelKey: 'settingsPage.templatesLabels' },
    { id: 'runtime',          labelKey: 'settingsPage.runtimeConfig' },
    { id: 'github',           labelKey: 'settingsPage.github' },
    { id: 'webhooks',         labelKey: 'settingsPage.webhooks' },
    { id: 'notifications',    labelKey: 'settingsPage.notifications' },
    { id: 'about',            labelKey: 'settingsPage.about' },
];

const SettingsPage = () => {
    const [activeTab, setActiveTab] = useState<SettingsTab>('appearance');
    const { theme, setTheme } = useThemeStore();
    const { t } = useTranslation();
    const tabRefs = useRef<Partial<Record<SettingsTab, HTMLButtonElement | null>>>({});

    const themes = [
        { id: 'light', name: t('settingsPage.themes.light') },
        { id: 'dark',  name: t('settingsPage.themes.dark') },
        { id: 'blue',  name: t('settingsPage.themes.blue') },
        { id: 'green', name: t('settingsPage.themes.green') },
    ];

    const handleTabKeyDown = (event: KeyboardEvent<HTMLButtonElement>, index: number) => {
        let nextIndex: number | null = null;
        if (event.key === 'ArrowRight') nextIndex = (index + 1) % TABS.length;
        if (event.key === 'ArrowLeft') nextIndex = (index - 1 + TABS.length) % TABS.length;
        if (event.key === 'Home') nextIndex = 0;
        if (event.key === 'End') nextIndex = TABS.length - 1;
        if (nextIndex === null) return;
        event.preventDefault();
        const nextTab = TABS[nextIndex].id;
        setActiveTab(nextTab);
        tabRefs.current[nextTab]?.focus();
    };

    return (
        <PageLayout>
            <PageHeader
                title={t('settingsPage.title')}
                subtitle={t('settingsPage.aboutVersion')}
            />

            <AdminAccessPanel/>

            {/* Tab navigation using .seg pattern */}
            <div className="seg" role="tablist" aria-label={t('settingsPage.tabsLabel')} style={{display:'flex', flexWrap:'wrap', width:'100%', marginTop:4}}>
                {TABS.map((tab, index) => (
                    <button key={tab.id}
                        type="button"
                        role="tab"
                        id={`settings-tab-${tab.id}`}
                        aria-selected={activeTab === tab.id}
                        aria-controls={`settings-panel-${tab.id}`}
                        tabIndex={activeTab === tab.id ? 0 : -1}
                        ref={node => { tabRefs.current[tab.id] = node; }}
                        onKeyDown={event => handleTabKeyDown(event, index)}
                        onClick={() => setActiveTab(tab.id)}
                        style={{borderRadius:'var(--r)', padding:'5px 12px'}}>
                        {t(tab.labelKey)}
                    </button>
                ))}
            </div>

            <div
                id={`settings-panel-${activeTab}`}
                role="tabpanel"
                aria-labelledby={`settings-tab-${activeTab}`}
                tabIndex={0}
                style={{marginTop:16}}
            >
                {activeTab === 'appearance' && (
                    <div style={{maxWidth:480, display:'flex', flexDirection:'column', gap:16}}>
                        <AdminAccessGate showPanel={false}>
                            <InterfaceLanguageSettings/>
                        </AdminAccessGate>
                        <div className="card">
                            <div className="card-head"><h3>{t('settingsPage.appearance')}</h3></div>
                            <div className="card-pad">
                                <p className="muted" style={{marginBottom:12}}>{t('settingsPage.chooseTheme')}</p>
                                <div style={{display:'grid', gridTemplateColumns:'1fr 1fr', gap:10}}>
                                    {themes.map(th => (
                                        <button key={th.id}
                                            type="button"
                                            onClick={() => setTheme(th.id as 'light' | 'dark' | 'blue' | 'green')}
                                            className={`btn${theme === th.id ? ' primary' : ''}`}
                                            style={{justifyContent:'flex-start', gap:10}}>
                                            <span
                                                aria-hidden="true"
                                                data-theme={th.id}
                                                className="inline-block h-3.5 w-3.5 shrink-0 rounded-full border-[1.5px] border-content-primary bg-surface-canvas opacity-85"
                                            />
                                            {th.name}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>
                )}
                {activeTab === 'scheduling'       && (
                    <AdminAccessGate showPanel={false}>
                        <SchedulingRulesSettings/>
                    </AdminAccessGate>
                )}
                {activeTab === 'templates_labels' && <TemplateLabelSettings/>}
                {activeTab === 'runtime'          && (
                    <AdminAccessGate showPanel={false}>
                        <RuntimeConfigSettings/>
                    </AdminAccessGate>
                )}
                {activeTab === 'github'           && <GitHubSettingsPanel/>}
                {activeTab === 'webhooks'         && (
                    <AdminAccessGate showPanel={false}>
                        <OutboundWebhooksPanel/>
                    </AdminAccessGate>
                )}
                {activeTab === 'notifications'    && (
                    <AdminAccessGate showPanel={false}>
                        <EmailSettingsPanel/>
                    </AdminAccessGate>
                )}
                {activeTab === 'about' && (
                    <div style={{maxWidth:480}}>
                        <SystemHealthPanel />
                    </div>
                )}
            </div>
        </PageLayout>
    );
};

export default SettingsPage;
