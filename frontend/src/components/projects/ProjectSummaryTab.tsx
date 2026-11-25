import clsx from 'clsx';
import {
    Activity,
    AlertTriangle,
    MessageSquare,
    Send
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import i18n from '../../i18n/i18n';
import type { Project } from '../../types/project';

import { MetricCount } from '../tasks/MetricCount';
import {
    InlineEmptyState,
    Pill,
    SectionCard,
    StickyRail
} from '../ui';
import type {
    ProjectUpdateEntry
} from '../../types/project';
import { formatDate, formatDateTime } from '../../utils/formatDate';
import { formatEffortDays } from '../../utils/workNumbers';

import type { ComponentProps } from 'react';
import { MilestonesSection } from './MilestonesSection';
import { formatNumber, formatUpdateAge, healthDotClass, healthLabelKeys, healthToTone, riskLabelKeys, riskTone, updateDetailFields, updateFreshnessMessage, updateFreshnessLabelKeys } from './projectDetailShared';
export const ProjectSummaryTab = ({ project, summary, updates: projectUpdates, milestones, onPostUpdate }: {
    project: Project; summary?: import('../../types/project').ProjectSummary; updates: ProjectUpdateEntry[];
    milestones: ComponentProps<typeof MilestonesSection>; onPostUpdate: () => void;
}) => {
    const { t } = useTranslation();
    const metricScope = { project_id: project.id };
    const latestUpdate = summary?.latest_update ?? projectUpdates[0] ?? null;
    const latestUpdateAge = summary?.latest_update
        ? formatUpdateAge(summary.days_since_latest_update)
        : null;
    const freshnessWarning = summary
        ? updateFreshnessMessage(
            summary.update_freshness,
            summary.days_since_latest_update,
            summary.stale_update_threshold_days,
        )
        : null;

    const completionPercent = Math.min(100, Math.max(0, summary?.completion_percent ?? 0));

    return (<div className="space-y-5">
        <div>
            <p className="mb-1.5 text-sm text-content-secondary">
                {/* Each count opens the tasks it counts. */}
                <MetricCount metric="implemented" scope={metricScope} title={t('metricList.implemented')} className="font-semibold text-content-primary">
                    {t('surfaces.projectDetail.summaryImplemented', { done: summary?.implemented_tasks ?? 0, total: summary?.total_tasks ?? 0 })}
                </MetricCount>
                {' · '}<MetricCount metric="accepted" scope={metricScope} title={t('metricList.accepted')}>{t('surfaces.projectDetail.summaryAccepted', { count: summary?.accepted_tasks ?? 0 })}</MetricCount>
                {' · '}<MetricCount metric="active" scope={metricScope} title={t('metricList.active')}>{t('surfaces.projectDetail.summaryActive', { count: summary?.active_tasks ?? 0 })}</MetricCount>
                {(summary?.blocked_tasks ?? 0) > 0 && <>{' · '}<MetricCount metric="blocked" scope={metricScope} title={t('metricList.blocked')} className="text-feedback-warning-foreground">{t('surfaces.projectDetail.summaryBlocked', { count: summary?.blocked_tasks })}</MetricCount></>}
                {(summary?.overdue_tasks ?? 0) > 0 && <>{' · '}<MetricCount metric="overdue" scope={metricScope} title={t('metricList.overdue')} className="text-feedback-danger-foreground">{t('surfaces.projectDetail.summaryOverdue', { count: summary?.overdue_tasks })}</MetricCount></>}
            </p>
            <div style={{ height: 6, background: 'var(--panel-3)', borderRadius: 999, overflow: 'hidden' }} aria-hidden="true">
                <div style={{ height: '100%', width: `${completionPercent}%`, background: 'var(--done)', borderRadius: 999 }} />
            </div>
        </div>

        {/* ── Two-column workspace: main content + sticky right rail ─── */}
        <div className="grid items-start gap-5 xl:grid-cols-[minmax(0,1fr)_300px]">
            <div className="wc-panel-stack">
                {project.description && <p className="max-w-prose whitespace-pre-wrap text-sm text-content-secondary">{project.description}</p>}
                <SectionCard
                    icon={<MessageSquare className="h-4 w-4 text-action" />}
                    title={t('surfaces.projectDetail.latestUpdate')}
                    actions={<span className="text-xs tabular-nums text-content-secondary">
                        {summary && t(updateFreshnessLabelKeys[summary.update_freshness])}
                        {latestUpdate && ` · ${formatDateTime(latestUpdate.created_at)}`}
                    </span>}
                >
                    {freshnessWarning && (
                        <div className="mb-3 flex gap-2 rounded-md bg-feedback-warning-muted p-3 text-sm text-feedback-warning-foreground">
                            <AlertTriangle className="mt-0.5 h-4 w-4 shrink-0" />
                            <span>{freshnessWarning}</span>
                        </div>
                    )}

                    {latestUpdate ? (
                        <div className="border-l-2 border-border pl-4">
                            <div className="mb-2 flex flex-wrap items-center gap-2">
                                <Pill tone={healthToTone(latestUpdate.health)} icon={<span className={clsx('h-1.5 w-1.5 rounded-full', healthDotClass(latestUpdate.health))} />}>
                                    {t(healthLabelKeys[latestUpdate.health])}
                                </Pill>
                                {latestUpdateAge && <span className="text-xs text-content-secondary">{latestUpdateAge}</span>}
                            </div>
                            <p className="text-sm font-medium text-content-primary">{latestUpdate.summary}</p>
                            {updateDetailFields(latestUpdate).length > 0 && (
                                <div className="mt-3 grid grid-cols-1 gap-3 text-xs md:grid-cols-4">
                                    {updateDetailFields(latestUpdate).map(field => (
                                        <div key={field.label}>
                                            <p className="text-wc-micro font-semibold uppercase tracking-wide text-content-tertiary">{field.label}</p>
                                            <p className="mt-0.5 text-content-primary">{field.value}</p>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
                    ) : (
                        <InlineEmptyState
                            title={t('surfaces.projectDetail.noProjectUpdatesYet')}
                            actions={(
                                <Button size="sm" variant="secondary" onClick={onPostUpdate}>
                                    <Send className="mr-1.5 h-3.5 w-3.5" />
                                    {t('surfaces.projectDetail.postFirstUpdate')}
                                </Button>
                            )}
                        />
                    )}
                </SectionCard>

                {/* Milestones */}
                <MilestonesSection {...milestones} />

            </div>

            {/* ── Sticky right rail: facts at a glance ─────────────────── */}
            <StickyRail label={t('surfaces.projectDetail.factsLabel')}>
                {/* Date risk */}
                <div className="rounded-xl border border-border bg-surface-card p-5 shadow-xs">
                    <div className="mb-3 flex items-center gap-2">
                        <AlertTriangle className="h-4 w-4 text-content-secondary" />
                        <h2 className="text-sm font-semibold tracking-tight text-content-primary">{t('surfaces.projectDetail.targetDateRisk')}</h2>
                        <div className="flex-1" />
                        <Pill tone={riskTone(summary?.target_date_risk)}>{t(riskLabelKeys[summary?.target_date_risk || 'unknown'])}</Pill>
                    </div>
                    <div className="space-y-2 text-sm">
                        <div className="flex items-baseline justify-between">
                            <span className="text-content-secondary">{t('surfaces.projectDetail.daysUntilTarget')}</span>
                            <span className="font-semibold tabular-nums text-content-primary">{summary?.days_until_target ?? '—'}</span>
                        </div>
                        <div className="flex items-baseline justify-between">
                            <span className="text-content-secondary">{t('surfaces.projectDetail.slip')}</span>
                            <span className="font-semibold tabular-nums text-content-primary">{summary?.target_date_slip_days ?? 0}d</span>
                        </div>
                        <div className="flex items-baseline justify-between">
                            <span className="text-content-secondary">{t('surfaces.projectDetail.taskRange')}</span>
                            <span className="font-medium tabular-nums text-content-primary">
                                {formatDate(summary?.task_start_date)} – {formatDate(summary?.task_end_date)}
                            </span>
                        </div>
                    </div>
                    {summary?.target_date_risk_reason && (
                        <p className="mt-3 rounded-md bg-surface-muted p-3 text-xs text-content-secondary">
                            {summary.target_date_risk_reason}
                        </p>
                    )}
                </div>

                {/* Effort */}
                <div className="rounded-xl border border-border bg-surface-card p-5 shadow-xs">
                    <div className="mb-3 flex items-center gap-2">
                        <Activity className="h-4 w-4 text-content-secondary" />
                        <h2 className="text-sm font-semibold tracking-tight text-content-primary">{t('surfaces.projectDetail.effort')}</h2>
                    </div>
                    <div className="space-y-3">
                        <div>
                            <div className="mb-1 flex justify-between text-sm">
                                <span className="text-content-secondary">{t('surfaces.projectDetail.effortDone', {
                                    done: formatNumber(Math.max(0, (summary?.total_effort_days ?? 0) - (summary?.remaining_effort_days ?? 0))),
                                    total: formatNumber(summary?.total_effort_days),
                                })}</span>
                                <span className="font-semibold tabular-nums text-content-primary">{t('surfaces.projectDetail.effortRemaining', { days: formatNumber(summary?.remaining_effort_days) })}</span>
                            </div>
                            <div className="h-1.5 overflow-hidden rounded-full bg-surface-subtle" aria-hidden="true">
                                {/* The bar fills with done work, like the completion bar above. */}
                                <div
                                    className="h-full rounded-full bg-feedback-success"
                                    style={{
                                        width: `${summary?.total_effort_days
                                            ? Math.min(100, Math.max(0, ((summary.total_effort_days - summary.remaining_effort_days) / summary.total_effort_days) * 100))
                                            : 0}%`,
                                    }}
                                />
                            </div>
                        </div>
                        <div className="flex justify-between text-sm">
                            <span className="text-content-secondary">{t('surfaces.projectDetail.total')}</span>
                            <span className="font-medium tabular-nums text-content-primary">{formatEffortDays(summary?.total_effort_days, i18n.language) ?? t('common.unknown')}</span>
                        </div>
                    </div>
                </div>

            </StickyRail>
        </div>

    </div>);
};
