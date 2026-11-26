import { useId, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { taskService } from '../../services/taskService';
import type { Task } from '../../types/task';
import { getApiErrorMessage } from '../../utils/apiError';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { useIdentity } from '../../features/identity/identityContext';
import type { MutationFeedbackMeta } from '../../features/mutationFeedback';

/** The code the server gives Accept while the project needs a verified agent publisher to review. */
export const VERIFIED_PUBLISHER_CODE = 'verified_publisher_review_required';

/**
 * Accepting resolved work as an owner while the different-publisher policy stays on. Only a signed-in
 * workspace owner or operator is offered the form; everyone else, including a trusted-local browser
 * with no signed-in person, is told why it is unavailable and what to do.
 */
export const TaskOwnerAcceptance = ({ task, disabled, onPending, onUpdated }: {
    task: Task; disabled: boolean; onPending: (pending: boolean) => void; onUpdated: (task: Task) => void;
}) => {
    const { t } = useTranslation();
    const id = useId();
    const identity = useIdentity()?.identity;
    const [reason, setReason] = useState('');
    // feedback-policy: mutation pending,inline
    const accept = useMutation({
        meta: { success: t('feedback.ownerAccepted', { name: task.title }) } satisfies MutationFeedbackMeta,
        mutationFn: () => taskService.ownerAccept(task.id, { expected_version: task.version,
            brief_revision: task.brief_revision ?? 0, artifact_revision: task.artifact_revision ?? 0, reason: reason.trim() }),
        onSuccess: latest => { setReason(''); onUpdated(latest); },
        onSettled: () => onPending(false),
        // feedback-policy: mutation pending,inline
    });
    const signedInHuman = identity?.principal?.kind === 'human' && identity.access !== 'observe';
    const mayOverride = signedInHuman && (identity?.workspace_role === 'owner' || identity?.workspace_role === 'operator');
    const trustedLocalBrowser = identity?.mode === 'trusted_local' && !identity.principal;
    const unavailable = !identity ? null : trustedLocalBrowser ? t('domain.ownerAcceptTrustedLocal')
        : identity.access === 'observe' ? t('domain.ownerAcceptObserver')
            : mayOverride ? null : t('domain.ownerAcceptNoAuthority');
    return <section className="space-y-3 border-t border-border pt-3" aria-labelledby={`${id}-heading`}>
        <h4 id={`${id}-heading`} className="font-medium text-content-primary">{t('domain.ownerAccept')}</h4>
        <p className="text-sm text-content-secondary">{t('domain.ownerAcceptHelp')}</p>
        {unavailable && <p role="status" className="text-sm text-content-secondary">{unavailable}</p>}
        {mayOverride && <div className="space-y-3">
            <Input label={t('domain.ownerAcceptReason')} required value={reason} maxLength={2000} disabled={disabled || accept.isPending}
                onChange={event => setReason(event.target.value)} />
            {accept.isError && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(accept.error, t('domain.ownerAcceptFailed'))}</p>}
            <div className="flex flex-wrap items-center gap-2">
                <Button type="button" isLoading={accept.isPending} aria-describedby={!reason.trim() ? `${id}-needs-reason` : undefined}
                    disabled={disabled || !reason.trim()} onClick={() => { onPending(true); accept.mutate(); }}>{t('domain.ownerAccept')}</Button>
                {!reason.trim() && <p id={`${id}-needs-reason`} className="text-sm text-content-secondary">{t('domain.ownerAcceptNeedsReason')}</p>}
            </div>
        </div>}
    </section>;
};
