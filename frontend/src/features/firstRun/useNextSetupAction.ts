import { useTranslation } from 'react-i18next';
import { useScopeLink } from '../scope/useScopeLink';
import { useFirstRunProgress } from './useFirstRunProgress';
import { FIRST_RUN_PLAN_CHECKPOINT, firstRunPlanHref } from './firstRunSteps';

export type NextAction = { label: string; to: string } | { label: string; onClick: () => void };

/**
 * The one button an empty page offers: the first setup step not yet done, in the order Get
 * started lists them. Until setup progress is known, or once every step is done, the page's
 * own fallback action is used instead.
 */
export const useNextSetupAction = ({ fallback, onCreateProject }: {
    fallback: NextAction;
    /** Opens the project form in place, when the page can. Otherwise the project step opens Projects. */
    onCreateProject?: () => void;
}): NextAction => {
    const { t } = useTranslation();
    const scopeLink = useScopeLink();
    const { known, nextId } = useFirstRunProgress();
    if (!known || nextId === null) return fallback;
    if (nextId === 'profile') return { label: t('firstRun.steps.profile.title'), to: scopeLink('/') };
    if (nextId === 'project') {
        const label = t('firstRun.steps.project.action');
        return onCreateProject ? { label, onClick: onCreateProject } : { label, to: scopeLink('/projects') };
    }
    const checkpoint = FIRST_RUN_PLAN_CHECKPOINT[nextId];
    return {
        label: t(`firstRun.steps.${nextId}.title`),
        to: scopeLink(checkpoint ? firstRunPlanHref(checkpoint) : '/plan'),
    };
};
