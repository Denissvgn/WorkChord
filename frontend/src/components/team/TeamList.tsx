import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Trash2, User, Plane, Calendar } from 'lucide-react';
import { teamService } from '../../services/teamService';
import { Button } from '../common/Button';
import { useConfirmDialog } from '../common/useConfirmDialog';
import { VacationManager } from './VacationManager';
import type { MemberWorkload, TeamMember } from '../../types/team';
import { QueryErrorState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';
import { getApiErrorMessage } from '../../utils/apiError';

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
        mutationFn: teamService.delete,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['team', iterationId] });
        },
        onError: error => {
            toast.error(getApiErrorMessage(error, t('teamCapacity.deleteFailed')));
        },
    });

    // Find the current member from fresh data for the vacation manager
    const managingVacationsFor = managingVacationsForId
        ? members?.find(m => m.id === managingVacationsForId) || null
        : null;

    if (isLoading) return <div>{t('teamCapacity.loading')}</div>;
    if (error) return <QueryErrorState error={error} onRetry={() => void refetch()} />;

    return (
        <div className="grid grid-cols-1 gap-4">
            {members?.map((member) => (
                <TeamMemberCard
                    key={member.id}
                    member={member}
                    onEdit={onEdit}
                    onDelete={() => requestConfirmation({
                        title: t('actions.delete'),
                        description: t('teamCapacity.deleteAssignmentConfirm'),
                        confirmLabel: t('actions.delete'),
                        cancelLabel: t('actions.cancel'),
                        closeLabel: t('actions.close'),
                        onConfirm: () => deleteMutation.mutateAsync(member.id),
                    })}
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

const TeamMemberCard = ({
    member,
    onDelete,
    onEdit,
    onManageVacations
}: {
    member: TeamMember,
    onDelete: () => void,
    onEdit: (m: TeamMember) => void,
    onManageVacations: () => void
}) => {
    const { t } = useTranslation();
    // Fetch workload data individually for now (ideal: batch or included in list response)
    const { data: workload, error: workloadError, refetch: refetchWorkload } = useQuery<MemberWorkload>({
        queryKey: ['workload', member.id],
        queryFn: () => teamService.getWorkload(member.id),
        staleTime: 5 * 60 * 1000,
    });

    const getStatusColor = (status: string) => {
        switch (status) {
            case 'green': return 'bg-feedback-success-muted text-feedback-success-foreground border-feedback-success-border';
            case 'yellow': return 'bg-feedback-warning-muted text-feedback-warning-foreground border-feedback-warning-border';
            case 'red': return 'bg-feedback-danger-muted text-feedback-danger-foreground border-feedback-danger-border';
            default: return 'bg-surface-subtle text-content-primary';
        }
    };

    return (
        <div className="card flex items-center justify-between p-4">
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
                        <span>{t('teamCapacity.availabilityShort')} {member.availability_percent}%</span>
                        <span>{t('teamCapacity.coefficientShort')} {member.professionalism_coefficient}</span>
                        <span>{t('teamCapacity.utilizationShort')} {member.operational_utilization}%</span>
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
                {workload && (
                    <div className={`px-4 py-2 rounded-md border text-sm font-medium ${getStatusColor(workload.workload_status)}`}>
                        <div className="flex flex-col items-end">
                            <span>{t('teamCapacity.allocatedDays', { allocated: workload.allocated_days, capacity: workload.capacity_days })}</span>
                            <span className="text-xs">
                                {workload.free_days >= 0
                                    ? t('teamCapacity.freeDays', { count: workload.free_days })
                                    : t('teamCapacity.overloadedBy', { count: Math.abs(workload.free_days) })
                                }
                            </span>
                        </div>
                    </div>
                )}

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
    );
}
