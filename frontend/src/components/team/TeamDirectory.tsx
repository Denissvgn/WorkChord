import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Bot, User } from 'lucide-react';
import { teamService } from '../../services/teamService';
import { agentService } from '../../services/agentService';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { useAgentAccess } from '../../hooks/useAgentAccess';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { Button } from '../common/Button';
import { InlineEmptyState, Pill, TableFrame } from '../ui';
import type { PillTone } from '../ui';
import { TeamProfileManager } from './TeamProfileManager';
import { buildDirectory, modelName, type ConnectionState, type DirectoryRow } from './directoryModel';

const MAX_CHIPS = 3;
const CONNECTION_TONE: Record<ConnectionState, PillTone> = { connected: 'green', not_connected: 'gray', unknown: 'yellow' };

/** The skills worth showing first: strengths by level, weaknesses last. */
const chipSkills = (row: DirectoryRow) => [...row.skills]
    .sort((a, b) => Number(a.is_weakness) - Number(b.is_weakness) || b.level - a.level || a.skill_name.localeCompare(b.skill_name));

export type DrawerTarget = { mode: 'add' } | { mode: 'edit'; key: string } | null;

/** Everyone who can do work in one table; a row opens the drawer for that person or agent. */
export const TeamDirectory = ({ drawer, onDrawerChange }: { drawer: DrawerTarget; onDrawerChange: (target: DrawerTarget) => void }) => {
    const { t } = useTranslation();
    const { hasAdminAccess } = useAdminAccess();
    const { hasAgentKey } = useAgentAccess();
    const canReadRoster = hasAdminAccess || hasAgentKey;
    const [now] = useState(() => Date.now());

    // feedback-policy: query loading,error,retry,empty
    const profilesQuery = useQuery({
        queryKey: ['teamMemberProfiles'],
        queryFn: teamService.getProfiles,
    });
    // The roster needs the admin key; without it the page stays readable and the agent columns say Unknown.
    // feedback-policy: query loading,error,retry,empty
    const rosterQuery = useQuery({
        queryKey: ['agent-actor-roster', true],
        queryFn: () => agentService.getActorRoster(true),
        enabled: canReadRoster,
        retry: false,
    });
    const rosterLoading = canReadRoster && rosterQuery.isLoading;
    const rosterUnavailable = !canReadRoster || rosterQuery.isError;

    const rows = useMemo(
        () => buildDirectory(profilesQuery.data ?? [], rosterQuery.data ?? [], rosterUnavailable ? 'unavailable' : 'loaded', now),
        [profilesQuery.data, rosterQuery.data, rosterUnavailable, now],
    );
    const drawerRow = drawer?.mode === 'edit' ? rows.find(row => row.key === drawer.key) ?? null : null;
    const hasAgents = rows.some(row => row.kind === 'agent');

    if (profilesQuery.isLoading) return <QueryLoadingState />;
    if (profilesQuery.isError) return <QueryErrorState error={profilesQuery.error} onRetry={() => void profilesQuery.refetch()} />;

    const cell = (row: DirectoryRow, value: string | null | undefined, empty: string) => (
        row.kind !== 'agent' ? <span className="text-content-tertiary">—</span>
            : rosterLoading ? <span className="text-content-secondary">{t('common.loading')}</span>
                : value === undefined ? t('teamPage.unknown')
                    : value ?? <span className="text-content-secondary">{empty}</span>
    );

    return (
        <div className="space-y-3">
            {hasAgents && rosterUnavailable && <p className="text-sm text-content-secondary">{t('teamPage.adminKeyNote')}</p>}
            {rows.length === 0 ? (
                <InlineEmptyState
                    title={t('teamPage.emptyTitle')}
                    description={t('teamPage.emptyBody')}
                />
            ) : (
                <TableFrame>
                    <table className="w-full text-left text-sm">
                        <caption className="sr-only">{t('teamPage.tabs.members')}</caption>
                        <thead className="text-xs text-content-secondary">
                            <tr className="border-b border-border">
                                <th scope="col" className="px-3 py-3">{t('teamPage.columns.name')}</th>
                                <th scope="col" className="px-3 py-3">{t('teamPage.columns.kind')}</th>
                                <th scope="col" className="px-3 py-3">{t('teamPage.columns.role')}</th>
                                <th scope="col" className="px-3 py-3">{t('teamPage.columns.capabilities')}</th>
                                <th scope="col" className="px-3 py-3">{t('teamPage.columns.model')}</th>
                                <th scope="col" className="px-3 py-3">{t('teamPage.columns.connection')}</th>
                            </tr>
                        </thead>
                        <tbody>
                            {rows.map(row => {
                                const chips = chipSkills(row);
                                const Icon = row.kind === 'agent' ? Bot : User;
                                return (
                                    <tr key={row.key} data-testid="team-row" className="border-b border-border align-top last:border-0">
                                        <th scope="row" className="px-3 py-3 font-medium">
                                            <Button type="button" variant="ghost" size="sm" className="!px-1 text-left"
                                                aria-label={t('teamPage.openProfile', { name: row.name })}
                                                onClick={() => onDrawerChange({ mode: 'edit', key: row.key })}>
                                                <Icon className="h-4 w-4 shrink-0 text-content-secondary" aria-hidden="true" />
                                                <span>{row.name}</span>
                                            </Button>
                                        </th>
                                        <td className="px-3 py-3">{t(`teamPage.kinds.${row.kind}`)}</td>
                                        <td className="px-3 py-3">
                                            {row.roles.length ? row.roles.map(role => t(`teamPage.roles.${role}`)).join(', ') : <span className="text-content-tertiary">—</span>}
                                        </td>
                                        <td className="px-3 py-3">
                                            {chips.length === 0 ? <span className="text-content-tertiary">{t('teamPage.noCapabilities')}</span> : (
                                                <span className="flex flex-wrap items-center gap-1">
                                                    {chips.slice(0, MAX_CHIPS).map(skill => (
                                                        <span key={skill.id} data-testid="capability-chip">
                                                            <Pill tone={skill.is_weakness ? 'yellow' : 'gray'}>{skill.skill_name}</Pill>
                                                        </span>
                                                    ))}
                                                    {chips.length > MAX_CHIPS && (
                                                        <span className="text-xs text-content-secondary" title={chips.slice(MAX_CHIPS).map(skill => skill.skill_name).join(', ')}>
                                                            {t('teamPage.moreCapabilities', { count: chips.length - MAX_CHIPS })}
                                                        </span>
                                                    )}
                                                </span>
                                            )}
                                        </td>
                                        <td className="px-3 py-3">{cell(row, row.model === undefined ? undefined : row.model ? modelName(row.model) : null, t('teamPage.noModel'))}</td>
                                        <td className="px-3 py-3">
                                            {row.kind !== 'agent' || !row.connection ? <span className="text-content-tertiary">—</span>
                                                : rosterLoading ? <span className="text-content-secondary">{t('common.loading')}</span>
                                                    : <Pill tone={CONNECTION_TONE[row.connection]}>{t(`teamPage.connection.${row.connection}`)}</Pill>}
                                        </td>
                                    </tr>
                                );
                            })}
                        </tbody>
                    </table>
                </TableFrame>
            )}
            {drawer && (drawer.mode === 'add' || drawerRow) && (
                <TeamProfileManager
                    key={drawer.mode === 'add' ? 'add' : drawer.key}
                    row={drawerRow}
                    rosterUnavailable={rosterUnavailable}
                    onClose={() => onDrawerChange(null)}
                    onCreated={id => onDrawerChange({ mode: 'edit', key: `profile-${id}` })}
                />
            )}
        </div>
    );
};
