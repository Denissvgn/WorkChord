import { useRef, useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { Modal } from '../common/Modal';
import { projectService } from '../../services/projectService';
import type { Project, ProjectMilestone } from '../../types/project';
import { feedbackMessage, type MutationFeedbackMeta } from '../../features/mutationFeedback';
import { getApiErrorMessage } from '../../utils/apiError';

/** A short form for a milestone on the page that shows the project: its name and target date. */
export const AddMilestoneModal = ({ project, onClose }: { project: Project; onClose: () => void }) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const nameRef = useRef<HTMLInputElement>(null);
    const [name, setName] = useState('');
    const [targetDate, setTargetDate] = useState('');

    // feedback-policy: mutation pending,inline - the form is disabled while saving and a failure stays in the modal.
    const create = useMutation({
        mutationFn: () => projectService.createMilestone(project.id, {
            name: name.trim(),
            target_date: targetDate,
            status: 'planned',
        }),
        meta: {
            success: data => feedbackMessage(t, 'created', 'milestone', (data as ProjectMilestone).name),
            undo: data => ({ run: () => projectService.deleteMilestone(project.id, (data as ProjectMilestone).id) }),
        } satisfies MutationFeedbackMeta,
        onSuccess: () => {
            for (const queryKey of [['projectMilestones'], ['projects'], ['project', project.id], ['gantt']]) {
                void queryClient.invalidateQueries({ queryKey });
            }
            onClose();
        },
    });

    const formId = `add-milestone-${project.id}`;

    return (
        <Modal
            open
            title={t('surfaces.projectsPage.addMilestone')}
            description={project.name}
            closeLabel={t('actions.close')}
            onClose={onClose}
            initialFocusRef={nameRef}
            closeDisabled={create.isPending}
            className="max-w-md"
            footer={(
                <div className="flex justify-end gap-2">
                    <Button type="button" variant="ghost" onClick={onClose} disabled={create.isPending}>{t('actions.cancel')}</Button>
                    <Button type="submit" form={formId} isLoading={create.isPending}>{t('surfaces.projectsPage.addMilestone')}</Button>
                </div>
            )}
        >
            <form
                id={formId}
                className="space-y-4"
                onSubmit={event => {
                    event.preventDefault();
                    if (!create.isPending && name.trim() && targetDate) create.mutate();
                }}
            >
                <fieldset disabled={create.isPending} className="m-0 space-y-4 border-0 p-0">
                    <Input
                        ref={nameRef}
                        label={t('surfaces.projectsPage.milestoneName')}
                        value={name}
                        onChange={event => setName(event.target.value)}
                        maxLength={255}
                        required
                    />
                    <Input
                        type="date"
                        label={t('surfaces.projectsPage.milestoneTargetDate')}
                        value={targetDate}
                        onChange={event => setTargetDate(event.target.value)}
                        required
                    />
                </fieldset>
                {create.error && (
                    <p role="alert" className="text-sm text-feedback-danger-foreground">
                        {getApiErrorMessage(create.error, t('surfaces.projectsPage.milestoneCreateFailed'))}
                    </p>
                )}
            </form>
        </Modal>
    );
};
