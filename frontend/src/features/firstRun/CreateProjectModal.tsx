import { useRef, useState } from 'react';
import type { FormEvent } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { Modal } from '../../components/common/Modal';
import { projectService } from '../../services/projectService';
import type { Project } from '../../types/project';
import { getApiErrorMessage } from '../../utils/apiError';
import { feedbackMessage } from '../mutationFeedback';
import type { MutationFeedbackMeta } from '../mutationFeedback';

/** The short way to a first project: a name and, optionally, its start and target dates. */
export const CreateProjectModal = ({ onClose, onCreated }: { onClose: () => void; onCreated: (project: Project) => void }) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const nameRef = useRef<HTMLInputElement>(null);
    const [name, setName] = useState('');
    const [startDate, setStartDate] = useState('');
    const [targetDate, setTargetDate] = useState('');
    const datesInvalid = Boolean(startDate && targetDate && targetDate < startDate);
    // feedback-policy: mutation pending,inline - the modal keeps the draft and shows the error in place.
    const create = useMutation({
        mutationFn: () => projectService.create({
            name: name.trim(),
            status: 'planned',
            health: 'unknown',
            start_date: startDate || null,
            target_date: targetDate || null,
            sort_order: 0,
        }),
        meta: { success: data => feedbackMessage(t, 'created', 'project', (data as Project).name) } satisfies MutationFeedbackMeta,
        onSuccess: async project => {
            await queryClient.invalidateQueries({ queryKey: ['projects'] });
            onCreated(project);
        },
    });
    const close = () => { if (!create.isPending) onClose(); };
    const submit = (event: FormEvent) => {
        event.preventDefault();
        if (!name.trim() || datesInvalid || create.isPending) return;
        create.mutate();
    };
    const formId = 'get-started-project-form';

    return (
        <Modal
            open
            title={t('firstRun.createProject.title')}
            description={t('firstRun.createProject.description')}
            onClose={close}
            closeLabel={t('actions.close')}
            closeDisabled={create.isPending}
            initialFocusRef={nameRef}
            footer={(
                <div className="flex justify-end gap-2">
                    <Button variant="secondary" onClick={close} disabled={create.isPending}>{t('surfaces.projectForm.cancel')}</Button>
                    <Button type="submit" form={formId} isLoading={create.isPending}
                        disabled={!name.trim() || datesInvalid || create.isPending}>
                        {t('surfaces.projectForm.createProject')}
                    </Button>
                </div>
            )}
        >
            <form id={formId} className="space-y-4" onSubmit={submit} noValidate>
                <Input
                    ref={nameRef}
                    label={t('surfaces.projectForm.projectName')}
                    value={name}
                    onChange={event => setName(event.target.value)}
                    maxLength={255}
                    required
                />
                <div className="grid gap-4 sm:grid-cols-2">
                    <Input
                        type="date"
                        label={t('surfaces.projectForm.startDate')}
                        value={startDate}
                        onChange={event => setStartDate(event.target.value)}
                    />
                    <Input
                        type="date"
                        label={t('surfaces.projectForm.targetDate')}
                        value={targetDate}
                        min={startDate || undefined}
                        onChange={event => setTargetDate(event.target.value)}
                        error={datesInvalid ? t('firstRun.createProject.datesInvalid') : undefined}
                    />
                </div>
                {create.isError && (
                    <p role="alert" className="text-sm text-feedback-danger-foreground">
                        {getApiErrorMessage(create.error, t('surfaces.projectForm.createFailed'))}
                    </p>
                )}
            </form>
        </Modal>
    );
};
