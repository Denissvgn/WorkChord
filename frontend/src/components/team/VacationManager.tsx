import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Plane, Trash2, Plus, Calendar, Upload } from 'lucide-react';
import { teamService } from '../../services/teamService';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { Modal } from '../common/Modal';
import { useConfirmDialog } from '../common/useConfirmDialog';
import type { Vacation, TeamMember } from '../../types/team';
import { getApiErrorMessage } from '../../utils/apiError';
import { formatDate } from '../../utils/formatDate';

interface VacationManagerProps {
    member: TeamMember;
    onClose: () => void;
}

const apiErrorMessage = (error: unknown, fallback: string) => {
    if (typeof error === 'object' && error !== null && 'response' in error) {
        const response = (error as { response?: { data?: { detail?: string } } }).response;
        return response?.data?.detail || fallback;
    }
    return fallback;
};

export const VacationManager = ({ member, onClose }: VacationManagerProps) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const [startDate, setStartDate] = useState('');
    const [endDate, setEndDate] = useState('');
    const [importSummary, setImportSummary] = useState('');
    const [importError, setImportError] = useState('');
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();

    const addMutation = useMutation({
        mutationFn: (data: { start_date: string; end_date: string }) =>
            teamService.addVacation(member.id, data),
        onSuccess: () => {
            // Invalidate all team queries to refresh member data with new vacations
            queryClient.invalidateQueries({ queryKey: ['team'] });
            queryClient.invalidateQueries({ queryKey: ['workload', member.id] });
            setStartDate('');
            setEndDate('');
        },
    });

    const deleteMutation = useMutation({
        mutationFn: teamService.deleteVacation,
        onSuccess: () => {
            // Invalidate all team queries to refresh member data
            queryClient.invalidateQueries({ queryKey: ['team'] });
            queryClient.invalidateQueries({ queryKey: ['workload', member.id] });
        },
    });

    const importMutation = useMutation({
        mutationFn: (csvText: string) => teamService.importVacationsCsv(member.iteration_id, csvText),
        onSuccess: (data) => {
            queryClient.invalidateQueries({ queryKey: ['team'] });
            queryClient.invalidateQueries({ queryKey: ['workload', member.id] });
            setImportSummary(t('teamVacations.importSummary', {
                imported: data.imported_count,
                skipped: data.skipped_count,
            }));
            setImportError(data.errors.length ? data.errors.map(err => `${err.row}: ${err.message}`).join('; ') : '');
        },
        onError: (error: unknown) => {
            setImportSummary('');
            setImportError(apiErrorMessage(error, t('teamVacations.importFailed')));
        },
    });

    const handleAdd = () => {
        if (startDate && endDate && startDate <= endDate) {
            addMutation.mutate({ start_date: startDate, end_date: endDate });
        }
    };

    const handleCsvFile = async (file: File | null) => {
        if (!file) return;
        importMutation.mutate(await file.text());
    };

    return (
        <Modal
            open
            title={t('teamVacations.title')}
            description={member.name}
            closeLabel={t('teamVacations.close')}
            onClose={onClose}
            className="max-w-lg"
            footer={<div className="flex justify-end"><Button variant="ghost" onClick={onClose}>{t('teamVacations.close')}</Button></div>}
        >
                <div className="mb-6">
                    <div className="flex items-center gap-3">
                        <div className="p-2 bg-feedback-purple-muted rounded-lg">
                            <Plane className="w-5 h-5 text-feedback-purple-foreground" />
                        </div>
                        <span className="text-sm text-content-secondary">{member.name}</span>
                    </div>
                </div>

                {(addMutation.isError || deleteMutation.isError) && (
                    <div role="alert" className="mb-4 rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                        {getApiErrorMessage(addMutation.error ?? deleteMutation.error, t('queryFeedback.fallback'))}
                    </div>
                )}

                {/* Add new vacation */}
                <div className="bg-surface-muted rounded-lg p-4 mb-4">
                    <div className="mb-3 flex items-center justify-between gap-3">
                        <h3 className="text-sm font-medium text-content-secondary">{t('teamVacations.addPeriod')}</h3>
                        <label className="btn btn-secondary cursor-pointer px-2 py-1 text-sm">
                            <Upload className="w-4 h-4 mr-2" />
                            {t('teamVacations.importCsv')}
                            <input
                                type="file"
                                accept=".csv,text/csv"
                                className="hidden"
                                onChange={(event) => {
                                    handleCsvFile(event.target.files?.[0] || null);
                                    event.currentTarget.value = '';
                                }}
                            />
                        </label>
                    </div>
                    {(importSummary || importError) && (
                        <div className={`mb-3 rounded-md border px-3 py-2 text-sm ${importError ? 'border-feedback-warning-border bg-feedback-warning-muted text-feedback-warning-foreground' : 'border-feedback-success-border bg-feedback-success-muted text-feedback-success-foreground'}`}>
                            {importSummary}
                            {importError && <div>{importError}</div>}
                        </div>
                    )}
                    <div className="grid grid-cols-2 gap-3">
                        <Input
                            type="date"
                            label={t('teamVacations.startDate')}
                            value={startDate}
                            onChange={(e) => setStartDate(e.target.value)}
                        />
                        <Input
                            type="date"
                            label={t('teamVacations.endDate')}
                            value={endDate}
                            onChange={(e) => setEndDate(e.target.value)}
                            min={startDate}
                        />
                    </div>
                    <Button
                        onClick={handleAdd}
                        disabled={!startDate || !endDate || startDate > endDate || addMutation.isPending}
                        isLoading={addMutation.isPending}
                        className="w-full mt-3"
                    >
                        <Plus className="w-4 h-4 mr-2" />
                        {t('teamVacations.addVacation')}
                    </Button>
                </div>

                {/* Existing vacations */}
                <div>
                    <h3 className="text-sm font-medium text-content-primary mb-3">
                        {t('teamVacations.current', { count: member.vacations?.length || 0 })}
                    </h3>
                    <div className="space-y-2 max-h-48 overflow-y-auto">
                        {member.vacations && member.vacations.length > 0 ? (
                            member.vacations.map((vacation: Vacation) => (
                                <div
                                    key={vacation.id}
                                    className="flex items-center justify-between p-3 bg-surface-card border rounded-lg"
                                >
                                    <div className="flex items-center gap-3">
                                        <Calendar className="w-4 h-4 text-content-tertiary" />
                                        <span className="text-sm">
                                            {formatDate(vacation.start_date)}
                                            {' → '}
                                            {formatDate(vacation.end_date)}
                                        </span>
                                    </div>
                                    <Button
                                        variant="ghost"
                                        size="sm"
                                        onClick={() => requestConfirmation({
                                            title: t('actions.delete'),
                                            description: t('teamVacations.deleteConfirm'),
                                            confirmLabel: t('actions.delete'),
                                            cancelLabel: t('actions.cancel'),
                                            closeLabel: t('actions.close'),
                                            onConfirm: () => deleteMutation.mutateAsync(vacation.id),
                                        })}
                                        aria-label={t('actions.delete')}
                                        className="text-feedback-danger hover:text-feedback-danger-foreground"
                                        isLoading={deleteMutation.isPending}
                                    >
                                        <Trash2 className="w-4 h-4" />
                                    </Button>
                                </div>
                            ))
                        ) : (
                            <div className="text-center py-6 text-content-tertiary bg-surface-muted rounded-lg border border-dashed">
                                {t('teamVacations.empty')}
                            </div>
                        )}
                    </div>
                </div>

                {confirmationDialog}
        </Modal>
    );
};
