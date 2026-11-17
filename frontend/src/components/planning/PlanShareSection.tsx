import { useEffect, useRef, useState } from 'react';
import type { ReactNode } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Copy, ExternalLink, RefreshCw, Share2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { buttonClassName } from '../common/buttonStyles';
import { useConfirmDialog } from '../common/useConfirmDialog';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';
import { planShareService } from '../../services/planShareService';
import type { PlanShare } from '../../services/planShareService';
import { copyText } from '../../utils/copyText';
import { formatDateTime } from '../../utils/formatDate';

type FocusTarget = 'ready' | 'shared' | 'retry' | null;

/** The read-only share link of an iteration's plan, made from the Review checkpoint. */
export const PlanShareSection = ({ iterationId }: { iterationId: number }) => {
    const { t, i18n } = useTranslation();
    const queryClient = useQueryClient();
    const toast = useToast();
    const { requestConfirmation, confirmationDialog, confirmationOpen } = useConfirmDialog();
    const [focusTarget, setFocusTarget] = useState<FocusTarget>(null);
    const readyHeadingRef = useRef<HTMLHeadingElement>(null);
    const sharedHeadingRef = useRef<HTMLHeadingElement>(null);
    const retryButtonRef = useRef<HTMLButtonElement>(null);

    // feedback-policy: query loading,error,retry,empty - no share link yet is the empty state.
    const shareQuery = useQuery({
        queryKey: ['plan-share', iterationId],
        queryFn: () => planShareService.getCurrent(iterationId),
        retry: false,
    });
    // feedback-policy: mutation pending,toast,inline
    const createShare = useMutation<PlanShare, unknown, 'create' | 'refresh'>({
        mutationFn: () => planShareService.create(iterationId),
        onSuccess: (share, command) => {
            queryClient.setQueryData(['plan-share', share.iteration_id], share);
            toast.success(t(command === 'refresh' ? 'plan.master.shareLinkRefreshed' : 'plan.master.shareLinkCreated'), {
                dedupeKey: `plan-share-${command}-${share.id}`,
            });
            if (command === 'create') setFocusTarget('shared');
        },
        onError: () => setFocusTarget('retry'),
    });
    // feedback-policy: mutation pending,toast,inline
    const revokeShare = useMutation({
        mutationFn: (shareId: number) => planShareService.revoke(shareId),
        onSuccess: () => {
            queryClient.setQueryData(['plan-share', iterationId], null);
            toast.success(t('plan.master.shareLinkRevoked'), { dedupeKey: 'plan-share-revoked' });
            setFocusTarget('ready');
        },
        onError: () => setFocusTarget('retry'),
    });

    const share = shareQuery.data ?? null;
    const pending = createShare.isPending || revokeShare.isPending;
    const error = shareQuery.error ?? createShare.error ?? revokeShare.error;

    useEffect(() => {
        if (!focusTarget || confirmationOpen) return;
        const target = focusTarget === 'ready'
            ? readyHeadingRef.current
            : focusTarget === 'shared' ? sharedHeadingRef.current : retryButtonRef.current;
        if (!target) return;
        target.focus();
        setFocusTarget(null);
    }, [confirmationOpen, focusTarget, share, error]);

    const retry = async () => {
        const result = await shareQuery.refetch();
        if (result.isError) {
            setFocusTarget('retry');
            return;
        }
        createShare.reset();
        revokeShare.reset();
        setFocusTarget(result.data ? 'shared' : 'ready');
    };

    const renderContent = (): ReactNode => {
        if (shareQuery.isLoading) return <QueryLoadingState message={t('plan.master.loadingShareLink')} />;
        if (error) {
            return (
                <QueryErrorState
                    error={error}
                    title={t('plan.master.shareLinkUnavailable')}
                    fallback={t('plan.master.shareLinkUnavailableBody')}
                    headingLevel={3}
                    isRetrying={shareQuery.isFetching}
                    onRetry={() => { void retry(); }}
                    retryButtonRef={retryButtonRef}
                />
            );
        }
        if (!share) {
            return (
                <section className="plan-checkpoint-share" aria-labelledby="plan-share-heading">
                    <div>
                        <h3 id="plan-share-heading" ref={readyHeadingRef} tabIndex={-1}>
                            {t('plan.master.readyToShareTitle')}
                        </h3>
                        <p>{t('plan.master.readyToShareBody')}</p>
                    </div>
                    <Button variant="secondary" disabled={pending} onClick={() => createShare.mutate('create')}>
                        <Share2 aria-hidden="true" size={14} />
                        {createShare.isPending ? t('plan.master.creatingShareLink') : t('plan.master.createShareLink')}
                    </Button>
                </section>
            );
        }

        const shareUrl = `${window.location.origin}/plan/share/${share.public_id}`;
        const copy = async () => {
            if (await copyText(shareUrl)) {
                toast.success(t('plan.master.shareLinkCopied'), { dedupeKey: `plan-share-copy-${share.id}` });
                return;
            }
            toast.error(t('plan.master.shareLinkCopyFailed'), { dedupeKey: `plan-share-copy-failed-${share.id}` });
        };
        const requestRevoke = () => requestConfirmation({
            title: t('plan.master.revokeShareTitle'),
            description: t('plan.master.revokeShareBody'),
            confirmLabel: t('plan.master.revokeShareLink'),
            cancelLabel: t('actions.cancel'),
            closeLabel: t('actions.close'),
            tone: 'danger',
            onConfirm: () => revokeShare.mutateAsync(share.id),
        });

        return (
            <section className="plan-checkpoint-share active" aria-labelledby="plan-share-heading">
                <div className="plan-checkpoint-share-copy">
                    <h3 id="plan-share-heading" ref={sharedHeadingRef} tabIndex={-1}>
                        {t('plan.master.planSharedTitle')}
                    </h3>
                    <p>{t('plan.master.planSharedBody', { date: formatDateTime(share.created_at, i18n.language) })}</p>
                    <label className="plan-share-link-field">
                        {t('plan.master.shareLinkLabel')}
                        <input value={shareUrl} readOnly />
                    </label>
                </div>
                <div className="plan-checkpoint-share-actions">
                    <Button variant="secondary" disabled={pending} onClick={() => { void copy(); }}>
                        <Copy aria-hidden="true" size={14} />
                        {t('plan.master.copyShareLink')}
                    </Button>
                    <a className={buttonClassName('ghost')} href={shareUrl} target="_blank" rel="noreferrer">
                        <ExternalLink aria-hidden="true" size={14} />
                        {t('plan.master.openSharedPlan')}
                    </a>
                    <Button variant="ghost" disabled={pending} onClick={() => createShare.mutate('refresh')}>
                        <RefreshCw aria-hidden="true" size={14} />
                        {t('plan.master.refreshShareSnapshot')}
                    </Button>
                    <Button variant="ghost" disabled={pending} onClick={requestRevoke}>
                        {t('plan.master.revokeShareLink')}
                    </Button>
                </div>
            </section>
        );
    };

    // The confirmation stays mounted in every state: a failed revocation keeps it open, so the
    // person can try again or cancel, while the section behind it shows the error panel.
    return (
        <>
            {renderContent()}
            {confirmationDialog}
        </>
    );
};
