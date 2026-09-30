import { useContext, useEffect } from 'react';
import { UNSAFE_DataRouterContext, useBlocker } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ConfirmDialog } from '../common/ConfirmDialog';
import { useDraftDismissal } from './useDraftDismissal';

type DraftGuard = ReturnType<typeof useDraftDismissal>;

const DraftRouteBlocker = ({ guard }: { guard: DraftGuard }) => {
    const blocker = useBlocker(() => guard.status.current.dirty || guard.status.current.pending);
    useEffect(() => {
        if (blocker.state !== 'blocked') return;
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
