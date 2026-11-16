import { ArrowLeft, Waypoints } from 'lucide-react';
import { Link, useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { useScopeLink } from '../scope/useScopeLink';
import { FIRST_RUN_SETUP_PARAM } from './firstRunSteps';

/** On a page opened from the Get started panel: the way back, where the next step is open. */
export const SetupReturnBar = () => {
    const { t } = useTranslation();
    const [searchParams] = useSearchParams();
    const scopeLink = useScopeLink();
    if (searchParams.get(FIRST_RUN_SETUP_PARAM) !== '1') return null;
    return (
        <aside className="plan-return-bar" aria-label={t('firstRun.returnTitle')}>
            <Waypoints aria-hidden="true" className="plan-return-bar-icon" />
            <div className="plan-return-bar-copy">
                <strong>{t('firstRun.returnTitle')}</strong>
                <span>{t('firstRun.returnBody')}</span>
            </div>
            <Link className="btn sm" to={scopeLink('/')}>
                <ArrowLeft aria-hidden="true" size={13} />
                {t('firstRun.backToSetup')}
            </Link>
        </aside>
    );
};
