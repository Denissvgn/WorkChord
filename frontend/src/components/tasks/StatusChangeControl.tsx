import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { ArrowRight, AlertTriangle, Check } from 'lucide-react';
import { Button } from '../common/Button';
import { Modal } from '../common/Modal';
import { QueryErrorState } from '../feedback/QueryState';
import { taskService } from '../../services/taskService';
import type { Task, TaskStatus, CascadeUpdateInfo } from '../../types/task';
import { pillToneClassName, STATUS_TONE } from '../ui/tone';
import { formatDate } from '../../utils/formatDate';

interface StatusChangeControlProps {
    task: Task;
    iterationId: number;
    onStatusChanged?: () => void;
}

// Valid transitions map
const VALID_TRANSITIONS: Record<TaskStatus, TaskStatus[]> = {
    'planned': ['active'],
    'active': ['resolved'],
    'resolved': ['active', 'closed'],
    'closed': []
};

export const StatusChangeControl = ({ task, iterationId, onStatusChanged }: StatusChangeControlProps) => {
    const queryClient = useQueryClient();
    const { t } = useTranslation();
    const [reason, setReason] = useState('');
    const [cascadeInfo, setCascadeInfo] = useState<CascadeUpdateInfo[] | null>(null);
    const [showConfirm, setShowConfirm] = useState<TaskStatus | null>(null);

    const mutation = useMutation({
        mutationFn: (newStatus: TaskStatus) => taskService.changeStatus(
            task.id,
            newStatus,
            reason || undefined,
            task.version,
        ),
        onSuccess: (data) => {
            queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] });
            queryClient.invalidateQueries({ queryKey: ['gantt'] });

            if (data.cascade_updates?.length > 0) {
                setCascadeInfo(data.cascade_updates);
            }

            setShowConfirm(null);
            setReason('');
            onStatusChanged?.();
        }
    });

    const availableTransitions = VALID_TRANSITIONS[task.status] || [];
    const statusLabel = (status: TaskStatus) => t(`statuses.${status}`);

    const handleStatusChange = (newStatus: TaskStatus) => {
        if (mutation.isPending) return;
        mutation.reset();
        // If it's a significant transition (to closed or might cascade), show confirmation
        if (newStatus === 'closed' || task.is_delayed) {
            setShowConfirm(newStatus);
        } else {
            mutation.mutate(newStatus);
        }
    };

    const confirmChange = () => {
        if (showConfirm && !mutation.isPending) {
            mutation.mutate(showConfirm);
        }
    };

    return (
        <div className="space-y-3">
            {/* Current status badge */}
            <div className="flex items-center gap-2">
                <span className="text-sm text-content-secondary">{t('statusChange.currentStatus')}</span>
                <span className={`px-2 py-1 rounded-full text-sm font-medium ${pillToneClassName[STATUS_TONE[task.status]]}`}>
                    {statusLabel(task.status)}
                </span>
                {task.is_delayed && (
                    <span className="flex items-center gap-1 text-feedback-purple-foreground text-sm">
                        <AlertTriangle className="w-4 h-4" />
                        {t('statusChange.delayedStart')}
                    </span>
                )}
            </div>

            {/* Transition buttons */}
            {availableTransitions.length > 0 && (
                <div className="flex flex-wrap gap-2">
                    {availableTransitions.map((newStatus) => (
                        <Button
                            key={newStatus}
                            variant="secondary"
                            size="sm"
                            onClick={() => handleStatusChange(newStatus)}
                            disabled={mutation.isPending}
                        >
                            <ArrowRight className="w-3 h-3 mr-1" />
                            {statusLabel(newStatus)}
                        </Button>
                    ))}
                </div>
            )}

            {mutation.isError && (
                <QueryErrorState
                    error={mutation.error}
                    fallback={t('statusChange.updateFailed')}
                    onRetry={() => {
                        if (mutation.variables) mutation.mutate(mutation.variables);
                    }}
                />
            )}

            <Modal
                open={showConfirm !== null}
                title={showConfirm ? t('statusChange.confirmTransition', { status: statusLabel(showConfirm) }) : t('actions.confirm')}
                closeLabel={t('actions.close')}
                closeDisabled={mutation.isPending}
                onClose={() => setShowConfirm(null)}
                className="max-w-md"
                footer={<div className="flex justify-end gap-2"><Button variant="secondary" onClick={() => setShowConfirm(null)} disabled={mutation.isPending}>{t('actions.cancel')}</Button><Button onClick={confirmChange} isLoading={mutation.isPending}><Check className="mr-1 h-3 w-3" />{t('actions.confirm')}</Button></div>}
            >
                {showConfirm && (
                    <input
                        type="text"
                        placeholder={t('statusChange.reasonPlaceholder')}
                        value={reason}
                        onChange={(e) => setReason(e.target.value)}
                        className="w-full px-2 py-1 text-sm border rounded"
                    />
                )}
            </Modal>

            {/* Cascade updates display */}
            {cascadeInfo && cascadeInfo.length > 0 && (
                <div className="border border-action bg-action-muted rounded-md p-3">
                    <p className="text-sm font-medium text-action mb-2">
                        {t('statusChange.cascadeUpdated', { count: cascadeInfo.length })}
                    </p>
                    <ul className="text-xs text-action space-y-1">
                        {cascadeInfo.slice(0, 5).map((u) => (
                            <li key={u.task_id}>
                                {u.task_title}: {formatDate(u.old_start_date)} → {formatDate(u.new_start_date)}
                            </li>
                        ))}
                        {cascadeInfo.length > 5 && (
                            <li>{t('statusChange.andMore', { count: cascadeInfo.length - 5 })}</li>
                        )}
                    </ul>
                    <Button
                        size="sm"
                        variant="ghost"
                        className="mt-2"
                        onClick={() => setCascadeInfo(null)}
                    >
                        {t('actions.close')}
                    </Button>
                </div>
            )}
        </div>
    );
};
