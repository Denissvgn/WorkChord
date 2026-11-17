import { useEffect } from 'react';
import { ArrowLeft, Waypoints } from 'lucide-react';
import { useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ButtonLink } from '../../components/common/ButtonLink';
import { useScopeLink } from '../scope/useScopeLink';
import { FIRST_RUN_SETUP_PARAM } from './firstRunSteps';
import { useSetupReturn } from './setupReturn';

/**
 * On a page opened from the Get started panel: the way back, where the next step is open. The
 * panel's link starts the step; the way back then stays while the step moves the page on.
 */
export const SetupReturnBar = () => {
    const { t } = useTranslation();
    const [searchParams] = useSearchParams();
    const scopeLink = useScopeLink();
    const fromPanel = searchParams.get(FIRST_RUN_SETUP_PARAM) === '1';
    const active = useSetupReturn(state => state.active);
    const start = useSetupReturn(state => state.start);
    useEffect(() => {
        if (fromPanel) start();
    }, [fromPanel, start]);
    if (!fromPanel && !active) return null;
    return (
        <aside className="plan-return-bar" aria-label={t('firstRun.returnTitle')}>
            <Waypoints aria-hidden="true" className="plan-return-bar-icon" />
            <div className="plan-return-bar-copy">
                <strong>{t('firstRun.returnTitle')}</strong>
                <span>{t('firstRun.returnBody')}</span>
            </div>
            <ButtonLink variant="primary" size="sm" to={scopeLink('/')}>
                <ArrowLeft aria-hidden="true" size={13} />
                {t('firstRun.backToSetup')}
            </ButtonLink>
        </aside>
    );
};
