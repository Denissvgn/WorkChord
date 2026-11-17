import { useEffect } from 'react';
import { useGetStartedVisibility } from './getStartedVisibility';
import { useFirstRunProgress } from './useFirstRunProgress';

/**
 * Whether Overview shows the Get started panel: once every step's state is known, while setup
 * is incomplete and the panel is not dismissed in this browser, or when Help reopened it. A
 * reopening of incomplete setup ends when setup completes, so the panel still hides itself.
 */
export const useGetStarted = () => {
    const progress = useFirstRunProgress();
    const { dismissed, requested, settleRequest } = useGetStartedVisibility();
    const { known, complete } = progress;
    useEffect(() => {
        if (known && requested) settleRequest(complete);
    }, [complete, known, requested, settleRequest]);
    const shownOnRequest = requested === 'pending'
        || requested === 'complete'
        || (requested === 'incomplete' && !complete);
    const visible = progress.applies && known && (shownOnRequest || (!dismissed && !complete));
    return { visible, progress };
};
