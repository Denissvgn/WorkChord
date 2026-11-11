import { planningInputService, type ObservedRevisions } from '../../services/planningInputService';
import { useState } from 'react';
import { useQueries, useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { ChevronDown, ChevronUp, Loader2, Trash2, User, Plane, Calendar } from 'lucide-react';
import { teamService } from '../../services/teamService';
import { Button } from '../common/Button';
import { useConfirmDialog } from '../common/useConfirmDialog';
import { VacationManager } from './VacationManager';
import type { MemberCapacity, MemberWorkload, TeamMember } from '../../types/team';
import { QueryErrorState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';
import { getApiErrorMessage } from '../../utils/apiError';
import { feedbackMessage } from '../../features/mutationFeedback';
import type { MutationFeedbackMeta } from '../../features/mutationFeedback';
import { formatDecimal } from '../../utils/workNumbers';

interface TeamListProps {
    iterationId: number;
    onEdit: (member: TeamMember) => void;
}

export const TeamList = ({ iterationId, onEdit }: TeamListProps) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const toast = useToast();
    const [managingVacationsForId, setManagingVacationsForId] = useState<number | null>(null);
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();

    const { data: members, isLoading, error, refetch } = useQuery({
        queryKey: ['team', iterationId],
        queryFn: () => teamService.getByIteration(iterationId),
    });

    const deleteMutation = useMutation({
        mutationFn: ({ id, revisions }: { id: number; revisions: ObservedRevisions }) => teamService.delete(id, revisions),
        meta: { success: (_data, variables) => feedbackMessage(t, 'deleted', 'teamMember', members?.find(member => member.id === (variables as { id: number }).id)?.name) } satisfies MutationFeedbackMeta,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['team', iterationId] });
        },
        onError: error => {
            toast.error(getApiErrorMessage(error, t('teamCapacity.deleteFailed')));
        },
    });

    const confirmMemberDelete = async (member: TeamMember) => {
        try {
            const observed = await planningInputService.readInitial<TeamMember>('member', member.id);
            requestConfirmation({ title: t('actions.delete'), description: observed.resource.name,
                confirmLabel: t('actions.delete'), cancelLabel: t('actions.cancel'), closeLabel: t('actions.close'),
                onConfirm: () => deleteMutation.mutateAsync({ id: member.id, revisions: observed.expected_revisions }) });
        } catch (cause) { toast.error(getApiErrorMessage(cause, t('teamCapacity.deleteFailed'))); }
    };

    // feedback-policy: query loading,error,retry,empty - each row shows its own workload error and retry; the total counts loaded rows only.
    const workloads = useQueries({
        queries: (members ?? []).map(member => ({
            queryKey: ['workload', member.id],
            queryFn: () => teamService.getWorkload(member.id),
            staleTime: 5 * 60 * 1000,
        })),
    });
    const loaded = workloads.map(query => query.data).filter((workload): workload is MemberWorkload => Boolean(workload));
    // One shared scale, so bars can be compared across people.
    const scale = Math.max(1, ...loaded.map(workload => Math.max(workload.capacity_hours ?? 0, workload.allocated_hours ?? 0)));

    // Find the current member from fresh data for the vacation manager
    const managingVacationsFor = managingVacationsForId
        ? members?.find(m => m.id === managingVacationsForId) || null
        : null;

    if (isLoading) return <div>{t('teamCapacity.loading')}</div>;
    if (error) return <QueryErrorState error={error} onRetry={() => void refetch()} />;

    return (
        <div className="grid grid-cols-1 gap-4">
            {members && members.length > 0 && <CapacityTotals workloads={loaded} expected={members.length} />}
            {members?.map((member) => (
                <TeamMemberCard
                    key={member.id}
                    scale={scale}
                    member={member}
                    onEdit={onEdit}
                    onDelete={() => void confirmMemberDelete(member)}
                    onManageVacations={() => setManagingVacationsForId(member.id)}
                />
            ))}
            {members?.length === 0 && (
                <div className="text-center py-12 text-content-tertiary bg-surface-muted rounded-lg border border-dashed border-border">
                    {t('teamCapacity.noAssignments')}
                </div>
            )}

            {managingVacationsFor && (
                <VacationManager
                    member={managingVacationsFor}
                    onClose={() => setManagingVacationsForId(null)}
                />
            )}
            {confirmationDialog}
        </div>
    );
};

/** The team's total, who is over capacity, and the hour conversion, said once. */
const CapacityTotals = ({ workloads, expected }: { workloads: MemberWorkload[]; expected: number }) => {
    const { t, i18n } = useTranslation();
    const locale = i18n.resolvedLanguage ?? i18n.language;
    const hours = (value: number) => formatDecimal(value, locale) ?? '0';
    const capacity = workloads.reduce((sum, workload) => sum + (workload.capacity_hours ?? 0), 0);
    const planned = workloads.reduce((sum, workload) => sum + (workload.allocated_hours ?? 0), 0);
    // A row whose capacity is unknown is not "over"; its bar says the capacity is unknown.
    const over = workloads.filter(workload => (workload.capacity_hours ?? 0) > 0 && (workload.allocated_hours ?? 0) > (workload.capacity_hours ?? 0)).length;
    const dayLengths = [...new Set(workloads.map(workload => workload.nominal_day_hours).filter((value): value is number => Boolean(value)))];
    return (
        <section className="card card-pad space-y-1" aria-labelledby="capacity-totals-title">
            <h3 id="capacity-totals-title" className="text-base font-semibold">{t('teamCapacity.totalTitle')}</h3>
            <p className="text-sm">
                <strong>{t('teamCapacity.hoursOf', { planned: hours(planned), capacity: hours(capacity) })}</strong>
                {' · '}{planned <= capacity ? t('teamCapacity.hoursFree', { hours: hours(capacity - planned) }) : t('teamCapacity.hoursOver', { hours: hours(planned - capacity) })}
                {over > 0 && <>{' · '}<span className="text-feedback-danger-foreground">{t('teamCapacity.overCount', { count: over })}</span></>}
                {workloads.length < expected && <>{' · '}<span className="text-content-secondary">{t('teamCapacity.partialTotal', { loaded: workloads.length, total: expected })}</span></>}
            </p>
            <p className="text-xs text-content-secondary">
                {dayLengths.length === 1 ? t('teamCapacity.conversion', { hours: hours(dayLengths[0]) }) : t('teamCapacity.conversionMixed')}
            </p>
        </section>
    );
};

/** Planned hours against capacity on the team's shared scale, labelled at the end. */
const CapacityBar = ({ workload, scale }: { workload: MemberWorkload; scale: number }) => {
    const { t, i18n } = useTranslation();
    const locale = i18n.resolvedLanguage ?? i18n.language;
    const hours = (value: number) => formatDecimal(value, locale) ?? '0';
    const capacity = workload.capacity_hours ?? 0;
    const planned = workload.allocated_hours ?? 0;
    const width = (value: number) => `${Math.min(100, value / scale * 100)}%`;
    if (capacity <= 0) {
        return <p className="w-64 text-sm text-feedback-warning-foreground">{t('teamCapacity.capacityUnknown')} · {t('teamCapacity.plannedOnly', { planned: hours(planned) })}</p>;
    }
    const over = planned > capacity;
    return (
        <div className="w-64 space-y-1">
            <div className="relative h-3 rounded-full bg-surface-subtle" aria-hidden="true">
                <span className="absolute inset-y-0 left-0 rounded-full border border-feedback-success-border bg-feedback-success-muted" style={{ width: width(capacity) }} />
                <span className="absolute inset-y-0 left-0 rounded-full bg-action" style={{ width: width(Math.min(planned, capacity)) }} />
                {over && <span className="absolute inset-y-0 rounded-r-full bg-feedback-danger" style={{ left: width(capacity), width: `${Math.min(100, (planned - capacity) / scale * 100)}%` }} />}
            </div>
            <p className={`text-sm tabular-nums ${over ? 'text-feedback-danger-foreground' : 'text-content-primary'}`}>
                {t('teamCapacity.hoursOf', { planned: hours(planned), capacity: hours(capacity) })}
                {' · '}{over ? t('teamCapacity.hoursOver', { hours: hours(planned - capacity) }) : t('teamCapacity.hoursFree', { hours: hours(capacity - planned) })}
            </p>
        </div>
    );
};

const TeamMemberCard = ({
    member,
    scale,
    onDelete,
    onEdit,
    onManageVacations
}: {
    member: TeamMember,
    scale: number,
    onDelete: () => void,
    onEdit: (m: TeamMember) => void,
    onManageVacations: () => void
}) => {
    const { t } = useTranslation();
    const [showCapacity, setShowCapacity] = useState(false);
    // Fetch workload data individually for now (ideal: batch or included in list response)
    const { data: workload, error: workloadError, refetch: refetchWorkload } = useQuery<MemberWorkload>({
        queryKey: ['workload', member.id],
        queryFn: () => teamService.getWorkload(member.id),
        staleTime: 5 * 60 * 1000,
    });

    // Detailed breakdown loads lazily, only when the row is expanded
    const {
        data: capacity,
        isLoading: isLoadingCapacity,
        error: capacityError,
        refetch: refetchCapacity,
    } = useQuery<MemberCapacity>({
        queryKey: ['capacity', member.id],
        queryFn: () => teamService.getCapacity(member.id),
        enabled: showCapacity,
        staleTime: 5 * 60 * 1000,
    });

    return (
        <div className="card flex flex-col p-4">
        <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
                <div className="p-3 bg-surface-subtle rounded-full">
                    <User className="w-6 h-6 text-content-secondary" />
                </div>
                <div>
                    <h3 className="font-semibold text-lg flex items-center gap-2">
                        {member.name}
                        <span className="text-xs font-normal px-2 py-0.5 rounded-full bg-action-muted text-action border border-action">
                            {member.position}
                        </span>
                    </h3>
                    <div className="text-sm text-content-secondary mt-1 flex items-center gap-4">
                        <span title={t('teamCapacity.availabilityHelp')}>{t('teamCapacity.availabilityShort')} {member.availability_percent}%</span>
                        <span title={t('teamCapacity.utilizationHelp')}>{t('teamCapacity.utilizationShort')} {member.operational_utilization}%</span>
                        <span title={t('teamCapacity.coefficientHelp')}>{t('teamCapacity.coefficientShort')} ×{member.professionalism_coefficient}</span>
                        {member.vacations.length > 0 && (
                            <span className="flex items-center text-feedback-purple-foreground">
                                <Plane className="w-3 h-3 mr-1" />
                                {t('teamCapacity.vacationsCount', { count: member.vacations.length })}
                            </span>
                        )}
                    </div>
                    <div className="mt-2 flex flex-wrap gap-1">
                        {member.profile?.skills.slice(0, 5).map(skill => (
                            <span
                                key={skill.id}
                                className={`rounded-full px-2 py-0.5 text-xs ${skill.is_weakness ? 'bg-feedback-warning-muted text-feedback-warning-foreground' : 'bg-surface-subtle text-content-primary'}`}
                            >
                                {skill.skill_name}{skill.is_weakness ? ` ${t('teamProfiles.weak')}` : ''}
                            </span>
                        ))}
                        {member.profile && member.profile.skills.length === 0 && (
                            <span className="text-xs text-content-tertiary">{t('teamCapacity.profileLinkedNoSkills')}</span>
                        )}
                        {!member.profile && (
                            <span className="text-xs text-content-tertiary">{t('teamCapacity.noCapabilityProfile')}</span>
                        )}
                    </div>
                </div>
            </div>

            <div className="flex items-center gap-6">
                {workloadError && <QueryErrorState className="max-w-xs" error={workloadError} onRetry={() => void refetchWorkload()} />}
                {workload && <CapacityBar workload={workload} scale={scale} />}

                <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => setShowCapacity(prev => !prev)}
                    aria-expanded={showCapacity}
                    aria-label={t('teamCapacity.capacityBreakdown')}
                    title={t('teamCapacity.capacityBreakdown')}
                >
                    {showCapacity ? <ChevronUp className="w-4 h-4" /> : <ChevronDown className="w-4 h-4" />}
                </Button>
                <Button
                    variant="ghost"
                    size="sm"
                    onClick={onManageVacations}
                    className="text-feedback-purple-foreground hover:bg-feedback-purple-muted"
                    title={t('teamVacations.title')}
                    aria-label={t('teamVacations.title')}
                >
                    <Calendar className="w-4 h-4" />
                </Button>
                <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => onEdit(member)}
                    className="text-action hover:text-action hover:bg-action-muted"
                >
                    {t('actions.edit')}
                </Button>
                <Button
                    variant="ghost"
                    size="sm"
                    onClick={onDelete}
                    aria-label={t('actions.delete')}
                    className="text-feedback-danger-foreground hover:bg-feedback-danger-muted"
                >
                    <Trash2 className="w-4 h-4" />
                </Button>
            </div>
        </div>

        {showCapacity && (
            <div className="mt-4 border-t border-border pt-3">
                <h4 className="mb-2 text-xs font-semibold uppercase tracking-wide text-content-secondary">
                    {t('teamCapacity.capacityBreakdown')}
                </h4>
                {isLoadingCapacity && (
                    <div className="flex items-center gap-2 text-sm text-content-secondary">
                        <Loader2 className="h-4 w-4 animate-spin" />
                        {t('teamCapacity.loading')}
                    </div>
                )}
                {capacityError != null && (
                    <QueryErrorState error={capacityError} onRetry={() => void refetchCapacity()} />
                )}
                {capacity && (
                    <div className="grid grid-cols-2 gap-2 text-sm sm:grid-cols-3 lg:grid-cols-6">
                        {[
                            [t('teamCapacity.workingDays'), String(capacity.working_days)],
                            [t('teamCapacity.vacationDays'), String(capacity.vacation_days)],
                            [t('teamCapacity.availableDays'), String(capacity.available_days)],
                            [t('teamCapacity.effectiveDays'), String(capacity.effective_days)],
                            [t('teamCapacity.adjustedDays'), String(capacity.adjusted_days)],
                            [t('teamCapacity.capacityHours'), String(capacity.hours)],
                        ].map(([label, value]) => (
                            <div key={label} className="rounded-md border border-border bg-surface-muted p-2">
                                <p className="text-xs text-content-secondary">{label}</p>
                                <p className="mt-0.5 font-medium text-content-primary">{value}</p>
                            </div>
                        ))}
                    </div>
                )}
            </div>
        )}
        </div>
    );
}
