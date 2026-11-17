import { useRef, useState } from 'react';
import clsx from 'clsx';
import { Link, useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Plus } from 'lucide-react';
import { Button } from '../components/common/Button';
import { PageHeader, PageLayout } from '../components/ui';
import { PlanReturnBar } from '../components/planning/PlanReturnBar';
import { AgentModelAdministration } from '../components/team/AgentModelAdministration';
import { TeamDirectory, type DrawerTarget } from '../components/team/TeamDirectory';
import { ConnectAgentSteps } from '../components/team/ConnectAgentSteps';

const TEAM_TABS = ['members', 'models', 'connect'] as const;
type TeamTab = (typeof TEAM_TABS)[number];

const parseTab = (value: string | null): TeamTab => (
    TEAM_TABS.find(tab => tab === value) ?? 'members'
);

const TeamPage = () => {
    const { t } = useTranslation();
    const [searchParams, setSearchParams] = useSearchParams();
    const [drawer, setDrawer] = useState<DrawerTarget>(null);
    // An empty members list offers Add person itself, so the header does not repeat it.
    const [membersEmpty, setMembersEmpty] = useState(false);
    // That header button can disappear while the drawer it opened is still open, so the drawer falls back to Members.
    const membersTabRef = useRef<HTMLAnchorElement>(null);
    const activeTab = parseTab(searchParams.get('tab'));

    const tabParams = (tab: TeamTab) => {
        const next = new URLSearchParams(searchParams);
        if (tab === 'members') next.delete('tab');
        else next.set('tab', tab);
        return next;
    };
    const openTab = (tab: TeamTab) => setSearchParams(tabParams(tab));

    return (
        <PageLayout>
            <PageHeader
                title={t('teamPage.title')}
                purpose={t('teamPage.purpose')}
                primaryAction={activeTab !== 'connect' && !(activeTab === 'members' && membersEmpty) && (
                    <Button type="button" onClick={() => { openTab('members'); setDrawer({ mode: 'add' }); }}>
                        <Plus className="h-4 w-4" aria-hidden="true" />
                        {t('teamPage.addPerson')}
                    </Button>
                )}
                secondaryActions={activeTab !== 'connect' && (
                    <Button type="button" variant="secondary" onClick={() => { setDrawer(null); openTab('connect'); }}>
                        {t('teamPage.connectAgent')}
                    </Button>
                )}
            />
            <PlanReturnBar />
            <div
                role="tablist"
                tabIndex={-1}
                aria-label={t('teamPage.tabsLabel')}
                className="flex flex-wrap gap-1 border-b border-border"
                onKeyDown={event => {
                    const offset = event.key === 'ArrowRight' ? 1 : event.key === 'ArrowLeft' ? -1 : 0;
                    if (!offset && event.key !== 'Home' && event.key !== 'End') return;
                    event.preventDefault();
                    const index = event.key === 'Home' ? 0 : event.key === 'End' ? TEAM_TABS.length - 1
                        : (TEAM_TABS.indexOf(activeTab) + offset + TEAM_TABS.length) % TEAM_TABS.length;
                    openTab(TEAM_TABS[index]);
                    document.getElementById(`team-tab-${TEAM_TABS[index]}`)?.focus();
                }}
            >
                {TEAM_TABS.map(tab => (
                    <Link
                        key={tab}
                        ref={tab === 'members' ? membersTabRef : undefined}
                        id={`team-tab-${tab}`}
                        role="tab"
                        aria-selected={activeTab === tab}
                        aria-controls={`team-panel-${tab}`}
                        tabIndex={activeTab === tab ? 0 : -1}
                        to={{ search: tabParams(tab).toString() }}
                        onClick={() => setDrawer(null)}
                        className={clsx(
                            'border-b-2 px-4 py-3 text-sm font-medium focus-visible:outline focus-visible:outline-2 focus-visible:outline-action',
                            activeTab === tab ? 'border-action text-action' : 'border-transparent text-content-secondary hover:bg-surface-muted',
                        )}
                    >
                        {t(`teamPage.tabs.${tab}`)}
                    </Link>
                ))}
            </div>
            <div role="tabpanel" id={`team-panel-${activeTab}`} aria-labelledby={`team-tab-${activeTab}`} className="space-y-3">
                {activeTab === 'members' && (
                    <>
                        <p className="text-sm text-content-secondary">{t('teamPage.capacityNote')}</p>
                        <TeamDirectory drawer={drawer} onDrawerChange={setDrawer} onEmptyChange={setMembersEmpty} drawerFallbackFocusRef={membersTabRef} />
                    </>
                )}
                {activeTab === 'models' && (
                    <AgentModelAdministration />
                )}
                {activeTab === 'connect' && (
                    <ConnectAgentSteps />
                )}
            </div>
        </PageLayout>
    );
};

export default TeamPage;
