import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import {
    CalendarDays,
    CheckCircle2,
    Copy,
    ExternalLink,
    ListChecks,
    Users,
} from 'lucide-react';
import { Link, useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Button } from '../components/common/Button';
import { QueryErrorState, QueryLoadingState } from '../components/feedback/QueryState';
import { useToast } from '../components/feedback/toast';
import { PageHeader, PageLayout } from '../components/ui';
import { planShareService } from '../services/planShareService';
import type { PlanShareTask } from '../services/planShareService';
import { copyText } from '../utils/copyText';
import { formatDate, formatDateTime } from '../utils/formatDate';

const flattenTasks = (tasks: PlanShareTask[]): PlanShareTask[] => (
    tasks.flatMap(task => [task, ...flattenTasks(task.children ?? [])])
);

const PlanSharePage = () => {
    const { publicId = '' } = useParams();
    const { t, i18n } = useTranslation();
    const toast = useToast();
    // feedback-policy: query loading,error,retry,empty - the token page renders a full loading or revocation-safe recovery state.
    const shareQuery = useQuery({
        queryKey: ['plan-share', publicId],
        queryFn: () => planShareService.getByPublicId(publicId),
        enabled: Boolean(publicId),
        retry: false,
    });
    const share = shareQuery.data;
    const tasks = useMemo(
        () => flattenTasks(share?.snapshot_data.tasks ?? []),
        [share?.snapshot_data.tasks],
    );
    const scheduledCount = tasks.filter(task => task.start_date && task.end_date).length;
    const unassignedCount = tasks.filter(task => !task.assignee_name).length;
    const shareUrl = typeof window === 'undefined' ? '' : window.location.href;

    const handleCopy = async () => {
        if (await copyText(shareUrl)) {
            toast.success(t('plan.master.shareLinkCopied'), {
                dedupeKey: `plan-share-copy-${publicId}`,
            });
            return;
        }
        toast.error(t('plan.master.shareLinkCopyFailed'), {
            dedupeKey: `plan-share-copy-failed-${publicId}`,
        });
    };

    if (shareQuery.isLoading) {
        return <QueryLoadingState message={t('plan.master.loadingSharedPlan')} />;
    }

    if (shareQuery.isError || !share) {
        return (
            <PageLayout>
                <QueryErrorState
                    error={shareQuery.error}
                    title={t('plan.master.sharedPlanUnavailable')}
                    fallback={t('plan.master.sharedPlanUnavailableBody')}
                    onRetry={() => { void shareQuery.refetch(); }}
                />
            </PageLayout>
        );
    }

    const iteration = share.snapshot_data.iteration;
    const teamMembers = share.snapshot_data.team_members;

    return (
        <PageLayout>
            <PageHeader
                title={share.iteration_name}
                subtitle={t('plan.master.sharedPlanSubtitle', {
                    date: formatDateTime(share.created_at, i18n.language),
                    owner: share.created_by_display,
                })}
                actions={(
                    <Button onClick={() => { void handleCopy(); }}>
                        <Copy aria-hidden="true" className="h-4 w-4" />
                        {t('plan.master.copyShareLink')}
                    </Button>
                )}
            />

            <div className="flex flex-wrap items-center gap-2 border-y border-border py-3 text-sm">
                <span className="pill done">
                    <CheckCircle2 aria-hidden="true" className="h-3.5 w-3.5" />
                    {t('plan.master.readOnlySnapshot')}
                </span>
                <span className="text-content-secondary">
                    {t('plan.master.sharedPlanSnapshotNotice')}
                </span>
            </div>

            <dl className="grid gap-4 border-b border-border pb-5 sm:grid-cols-2 xl:grid-cols-4">
                <div>
                    <dt className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-content-tertiary">
                        <CalendarDays aria-hidden="true" className="h-4 w-4" />
                        {t('plan.master.planningPeriod')}
                    </dt>
                    <dd className="mt-1 font-medium text-content-primary">
                        {formatDate(iteration.start_date, i18n.language)} – {formatDate(iteration.end_date, i18n.language)}
                    </dd>
                </div>
                <div>
                    <dt className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-content-tertiary">
                        <ListChecks aria-hidden="true" className="h-4 w-4" />
                        {t('plan.master.tasks')}
                    </dt>
                    <dd className="mt-1 font-medium tabular-nums text-content-primary">{tasks.length}</dd>
                </div>
                <div>
                    <dt className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-content-tertiary">
                        <ExternalLink aria-hidden="true" className="h-4 w-4" />
                        {t('plan.master.scheduledTasks')}
                    </dt>
                    <dd className="mt-1 font-medium tabular-nums text-content-primary">
                        {t('plan.master.scheduledTaskCount', { scheduled: scheduledCount, total: tasks.length })}
                    </dd>
                </div>
                <div>
                    <dt className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wide text-content-tertiary">
                        <Users aria-hidden="true" className="h-4 w-4" />
                        {t('plan.master.team')}
                    </dt>
                    <dd className="mt-1 font-medium tabular-nums text-content-primary">{teamMembers.length}</dd>
                </div>
            </dl>

            <div className="grid min-w-0 gap-6 2xl:grid-cols-[minmax(0,1fr)_320px]">
                <section className="min-w-0" aria-labelledby="shared-plan-tasks">
                    <div className="mb-3 flex flex-wrap items-baseline justify-between gap-2">
                        <h2 id="shared-plan-tasks" className="text-lg font-semibold text-content-primary">
                            {t('plan.master.sharedWork')}
                        </h2>
                        {unassignedCount > 0 && (
                            <span className="text-sm text-feedback-warning-foreground">
                                {t('plan.master.unassignedTaskCount', { count: unassignedCount })}
                            </span>
                        )}
                    </div>
                    {tasks.length === 0 ? (
                        <div className="empty">
                            <h3>{t('plan.master.noSharedTasks')}</h3>
                            <p>{t('plan.master.noSharedTasksBody')}</p>
                        </div>
                    ) : (
                        <div className="overflow-x-auto rounded-lg border border-border">
                            <table className="w-full min-w-[720px] border-collapse text-sm">
                                <thead className="bg-surface-subtle text-left text-xs uppercase tracking-wide text-content-tertiary">
                                    <tr>
                                        <th className="px-4 py-3 font-semibold">{t('plan.master.task')}</th>
                                        <th className="px-4 py-3 font-semibold">{t('plan.master.assignee')}</th>
                                        <th className="px-4 py-3 font-semibold">{t('plan.master.status')}</th>
                                        <th className="px-4 py-3 font-semibold">{t('plan.master.effort')}</th>
                                        <th className="px-4 py-3 font-semibold">{t('plan.master.schedule')}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {tasks.map(task => (
                                        <tr key={task.id} className="border-t border-border-subtle">
                                            <td className="max-w-[360px] px-4 py-3">
                                                <div className="font-medium text-content-primary">{task.title}</div>
                                                <div className="mt-0.5 text-xs text-content-tertiary">P{task.priority}</div>
                                            </td>
                                            <td className="px-4 py-3 text-content-secondary">
                                                {task.assignee_name ?? t('plan.master.unassigned')}
                                            </td>
                                            <td className="px-4 py-3 capitalize text-content-secondary">
                                                {t(`statuses.${task.status}`, { defaultValue: task.status })}
                                            </td>
                                            <td className="px-4 py-3 tabular-nums text-content-secondary">
                                                {t('units.daysCompact', { count: task.effort_days })}
                                            </td>
                                            <td className="px-4 py-3 tabular-nums text-content-secondary">
                                                {task.start_date && task.end_date
                                                    ? `${formatDate(task.start_date, i18n.language)} – ${formatDate(task.end_date, i18n.language)}`
                                                    : t('plan.master.notScheduled')}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </section>

                <aside aria-labelledby="shared-plan-team">
                    <h2 id="shared-plan-team" className="mb-3 text-lg font-semibold text-content-primary">
                        {t('plan.master.team')}
                    </h2>
                    <div className="divide-y divide-border-subtle border-y border-border">
                        {teamMembers.map(member => (
                            <div key={`${member.name}-${member.position}`} className="py-3">
                                <div className="font-medium text-content-primary">{member.name}</div>
                                <div className="text-sm text-content-secondary">{member.position}</div>
                                <div className="mt-1 text-xs text-content-tertiary">
                                    {t('plan.master.availabilityPercent', { count: member.availability_percent })}
                                </div>
                            </div>
                        ))}
                        {teamMembers.length === 0 && (
                            <p className="py-3 text-sm text-content-secondary">{t('plan.master.noSharedTeam')}</p>
                        )}
                    </div>
                    <Link to="/plan/master" className="btn mt-4 w-full">
                        {t('plan.master.openPlanMaster')}
                    </Link>
                </aside>
            </div>
        </PageLayout>
    );
};

export default PlanSharePage;
