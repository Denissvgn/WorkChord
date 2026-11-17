import { ButtonLink } from '../common/ButtonLink';
import { ArrowLeft, Waypoints } from 'lucide-react';
import { useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useScopeLink } from '../../features/scope/useScopeLink';
import {
    isPlanningStepId,
    planStepHref,
    PLANNING_RETURN_STEP_PARAM,
} from '../../features/planningMasters/planningReturn';

export const PlanReturnBar = () => {
    const { t } = useTranslation();
    const [searchParams] = useSearchParams();
    const scopeLink = useScopeLink();
    const stepId = searchParams.get(PLANNING_RETURN_STEP_PARAM);

    if (!isPlanningStepId(stepId)) return null;

    return (
        <aside className="plan-return-bar" aria-label={t('plan.master.planReturnContext')}>
            <Waypoints aria-hidden="true" className="plan-return-bar-icon" />
            <div className="plan-return-bar-copy">
                <strong>{t('plan.master.workingFromCheckpoint', {
                    step: t(`plan.steps.${stepId}.title`),
                })}</strong>
                <span>{t('plan.master.returnAfterChanges')}</span>
            </div>
            <ButtonLink  to={scopeLink(planStepHref(stepId, { returned: true }))} size="sm">
                <ArrowLeft aria-hidden="true" size={13} />
                {t('plan.master.returnToCheckpoint')}
            </ButtonLink>
        </aside>
    );
};
