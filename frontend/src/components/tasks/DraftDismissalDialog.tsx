import { useContext, useEffect, useRef } from 'react';
import { UNSAFE_DataRouterContext, useBlocker } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ConfirmDialog } from '../common/ConfirmDialog';
import { useDraftDismissal } from './useDraftDismissal';
import { leaveGuardsBypassed } from '../common/leaveGuardBypass';

type DraftGuard = ReturnType<typeof useDraftDismissal>;

const DraftRouteBlocker = ({ guard }: { guard: DraftGuard }) => {
    const blocker = useBlocker(() => !leaveGuardsBypassed() && (guard.status.current.dirty || guard.status.current.pending));
    // The router accepts one answer per blocked navigation; a second one is an invalid transition.
    const answered = useRef(false);
    useEffect(() => {
        if (blocker.state !== 'blocked') { answered.current = false; return; }
        if (answered.current) return;
        answered.current = true;
        if (guard.status.current.pending) blocker.reset();
        else guard.request(() => blocker.proceed(), () => blocker.reset());
    }, [blocker, guard]);
    return null;
};

export const DraftDismissalDialog = ({ guard }: { guard: DraftGuard }) => {
    const { t } = useTranslation();
    const dataRouter = useContext(UNSAFE_DataRouterContext);
    return <>
        {dataRouter && <DraftRouteBlocker guard={guard} />}
        <ConfirmDialog open={guard.promptOpen} title={t('taskEditor.unsavedTitle')}
            description={t('taskEditor.unsavedBody')} confirmLabel={t('taskEditor.discard')}
            cancelLabel={t('taskEditor.keepEditing')} closeLabel={t('actions.close')} tone="warning"
            pending={guard.pending} onCancel={guard.cancel} onConfirm={guard.discard} />
    </>;
};
