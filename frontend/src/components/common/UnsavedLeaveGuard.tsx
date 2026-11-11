import { useContext, useEffect } from 'react';
import { UNSAFE_DataRouterContext, useBlocker } from 'react-router-dom';
import { ConfirmDialog } from './ConfirmDialog';

interface UnsavedLeaveGuardProps {
    when: boolean;
    title: string;
    description: string;
    leaveLabel: string;
    stayLabel: string;
    closeLabel: string;
}

const BlockingGuard = ({ when, title, description, leaveLabel, stayLabel, closeLabel }: UnsavedLeaveGuardProps) => {
    const blocker = useBlocker(({ currentLocation, nextLocation }) => when && currentLocation.pathname !== nextLocation.pathname);
    return <ConfirmDialog
        open={blocker.state === 'blocked'}
        title={title}
        description={description}
        confirmLabel={leaveLabel}
        cancelLabel={stayLabel}
        closeLabel={closeLabel}
        tone="danger"
        onConfirm={() => blocker.proceed?.()}
        onCancel={() => blocker.reset?.()}
    />;
};

/** Asks before leaving a page with unsaved changes, in the app and on reload or close. */
export const UnsavedLeaveGuard = (props: UnsavedLeaveGuardProps) => {
    const dataRouter = useContext(UNSAFE_DataRouterContext);
    const { when } = props;
    useEffect(() => {
        if (!when) return undefined;
        const beforeUnload = (event: BeforeUnloadEvent) => {
            event.preventDefault();
            event.returnValue = '';
        };
        window.addEventListener('beforeunload', beforeUnload);
        return () => window.removeEventListener('beforeunload', beforeUnload);
    }, [when]);
    // In-app navigation can only be intercepted inside the app's data router.
    return dataRouter ? <BlockingGuard {...props} /> : null;
};
