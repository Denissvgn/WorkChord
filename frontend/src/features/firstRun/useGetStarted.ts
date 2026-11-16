import { useGetStartedVisibility } from './getStartedVisibility';
import { useFirstRunProgress } from './useFirstRunProgress';

/**
 * Whether Overview shows the Get started panel: once every step's state is known, while setup
 * is incomplete and the panel is not dismissed in this browser, or when Help reopened it.
 */
export const useGetStarted = () => {
    const progress = useFirstRunProgress();
    const { dismissed, requested } = useGetStartedVisibility();
    const visible = progress.applies && progress.known && (requested || (!dismissed && !progress.complete));
    return { visible, progress };
};
