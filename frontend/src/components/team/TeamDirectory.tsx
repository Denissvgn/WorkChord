import { useEffect, useMemo, useState, type ReactNode, type RefObject } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Bot, User } from 'lucide-react';
import { teamService } from '../../services/teamService';
import { agentService } from '../../services/agentService';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { useAgentAccess } from '../../hooks/useAgentAccess';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { Button } from '../common/Button';
import { Pill, TableFrame } from '../ui';
import { NextStepEmptyState } from '../../features/firstRun/NextStepEmptyState';
import type { PillTone } from '../ui';
import { TeamProfileManager } from './TeamProfileManager';
import {
    actorName, buildDirectory, distinctRole, modelName,
    type AgentStatus, type ConnectionState, type DirectoryActor, type DirectoryRow, type RosterState,
} from './directoryModel';

const MAX_CHIPS = 3;
/** How often connection ages are recomputed and the roster is read again while the page is open. */
const CLOCK_TICK_MS = 30_000;
const CONNECTION_TONE: Record<ConnectionState, PillTone> = { connected: 'green', not_connected: 'gray', unknown: 'yellow' };

/** The skills worth showing first: strengths by level, weaknesses last. */
const chipSkills = (row: DirectoryRow) => [...row.skills]
    .sort((a, b) => Number(a.is_weakness) - Number(b.is_weakness) || b.level - a.level || a.skill_name.localeCompare(b.skill_name));

/** The current time, moving on every tick so values that depend on age do not freeze at mount. */
const useNow = (tickMs: number) => {
    const [now, setNow] = useState(() => Date.now());
    useEffect(() => {
        const timer = setInterval(() => setNow(Date.now()), tickMs);
        return () => clearInterval(timer);
    }, [tickMs]);
    return now;
};

const refusedStatus = (error: unknown) => {
    const status = (error as { response?: { status?: number } } | null)?.response?.status;
    return status === 401 || status === 403;
};

export type DrawerTarget = { mode: 'add' } | { mode: 'edit'; key: string } | null;

/**
 * Everyone who can do work in one table; a row opens the drawer for that person or agent.
 * `onEmptyChange` reports when the empty state, with its own Add person button, is shown.
 */
export const TeamDirectory = ({ drawer, onDrawerChange, onEmptyChange, drawerFallbackFocusRef }: {
    drawer: DrawerTarget;
    onDrawerChange: (target: DrawerTarget) => void;
    onEmptyChange?: (empty: boolean) => void;
    /** Where focus goes when the drawer closes and the control that opened it is gone. */
    drawerFallbackFocusRef?: RefObject<HTMLElement | null>;
}) => {
    const { t } = useTranslation();
    const { hasAdminAccess } = useAdminAccess();
    const { hasAgentKey } = useAgentAccess();
    const canReadRoster = hasAdminAccess || hasAgentKey;
    const tick = useNow(CLOCK_TICK_MS);

    // feedback-policy: query loading,error,retry,empty
    const profilesQuery = useQuery({
        queryKey: ['teamMemberProfiles'],
        queryFn: teamService.getProfiles,
    });
    // The roster needs the admin key; without it the page stays readable and the agent columns say Unknown.
    // The read is optional, so a rejected key shows Unknown and is not taken for an expired session.
    // feedback-policy: query loading,error,retry,empty
    const rosterQuery = useQuery({
        queryKey: ['agent-actor-roster', true],
        queryFn: () => agentService.getActorRoster(true, { optional: true }),
        enabled: canReadRoster,
        retry: false,
        // Connection is judged by when the server last saw each agent, so the roster is read again while the page is open.
        refetchInterval: query => (refusedStatus(query.state.error) ? false : CLOCK_TICK_MS),
    });
    // One clock for every connection age, in the rows and the drawer: it moves on each tick and with each roster read.
    const now = Math.max(tick, rosterQuery.dataUpdatedAt);
    // Only a successful read counts: after a failed refresh the cached roster is stale and every state is Unknown.
    const rosterState: RosterState = !canReadRoster || rosterQuery.isError ? 'unavailable'
        : rosterQuery.isSuccess ? 'loaded' : 'loading';

    const rows = useMemo(
        () => buildDirectory(profilesQuery.data ?? [], rosterQuery.data ?? [], rosterState, now),
        [profilesQuery.data, rosterQuery.data, rosterState, now],
    );
    const drawerRow = drawer?.mode === 'edit' ? rows.find(row => row.key === drawer.key) ?? null : null;
    const hasAgents = rows.some(row => row.kind === 'agent');
    const isEmpty = profilesQuery.isSuccess && rows.length === 0;
    useEffect(() => {
        onEmptyChange?.(isEmpty);
        return () => onEmptyChange?.(false);
    }, [isEmpty, onEmptyChange]);

    if (profilesQuery.isLoading) return <QueryLoadingState />;
    if (profilesQuery.isError) return <QueryErrorState error={profilesQuery.error} onRetry={() => void profilesQuery.refetch()} />;

    // A row with several actors names each one by its role, or by its own name when the role is missing or shared.
    const actorLabel = (row: DirectoryRow, entry: DirectoryActor) => {
        const role = distinctRole(row, entry);
        return role ? t(`teamPage.roles.${role}`) : actorName(entry.actor);
    };

    // Every model and connection cell is drawn from an AgentStatus, which is Unknown unless the roster was read.
    const modelText = (status: AgentStatus) => (
        status.model === undefined ? t('teamPage.unknown')
            : status.model ? modelName(status.model) : <span className="text-content-secondary">{t('teamPage.noModel')}</span>
    );
    const connectionPill = (status: AgentStatus) => (
        <Pill tone={CONNECTION_TONE[status.connection]}>{t(`teamPage.connection.${status.connection}`)}</Pill>
    );
    const statusCell = (row: DirectoryRow, render: (status: AgentStatus) => ReactNode) => (
        row.status === null ? <span className="text-content-tertiary">—</span>
            : row.rosterState === 'loading' ? <span className="text-content-secondary">{t('common.loading')}</span>
                : render(row.status)
    );

    return (
        <div className="space-y-3">
            {hasAgents && rosterState === 'unavailable' && <p className="text-sm text-content-secondary">{t('teamPage.adminKeyNote')}</p>}
            {rows.length === 0 ? (
                <NextStepEmptyState
                    title={t('teamPage.emptyTitle')}
                    description={t('emptyStates.team.membersBody')}
                    fallback={{ label: t('teamPage.addPerson'), onClick: () => onDrawerChange({ mode: 'add' }) }}
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
                                            <Button type="button" variant="ghost" size="sm" className="px-1! text-left"
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
                                        {row.actors.length > 1 && row.rosterState !== 'loading' ? (
                                            <>
                                                <td className="px-3 py-3">
                                                    <ul className="space-y-1">
                                                        {row.actors.map(entry => (
                                                            <li key={entry.actor.id} data-testid="actor-model">
                                                                <span className="text-content-secondary">{actorLabel(row, entry)} · </span>
                                                                {modelText(entry.status)}
                                                            </li>
                                                        ))}
                                                    </ul>
                                                </td>
                                                <td className="px-3 py-3">
                                                    <ul className="space-y-1">
                                                        {row.actors.map(entry => (
                                                            <li key={entry.actor.id} data-testid="actor-connection" className="flex flex-wrap items-center gap-1">
                                                                <span className="text-content-secondary">{actorLabel(row, entry)}</span>
                                                                {connectionPill(entry.status)}
                                                            </li>
                                                        ))}
                                                    </ul>
                                                </td>
                                            </>
                                        ) : (
                                            <>
                                                <td className="px-3 py-3">{statusCell(row, modelText)}</td>
                                                <td className="px-3 py-3">{statusCell(row, connectionPill)}</td>
                                            </>
                                        )}
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
                    onClose={() => onDrawerChange(null)}
                    onCreated={id => onDrawerChange({ mode: 'edit', key: `profile-${id}` })}
                    fallbackFocusRef={drawerFallbackFocusRef}
                />
            )}
        </div>
    );
};
