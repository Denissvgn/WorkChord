import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import '../styles/landing.css';
import { useScopeLink } from '../features/scope/useScopeLink';
import { ButtonLink } from '../components/common/ButtonLink';
import { PageHeader } from '../components/ui';

// The four workflow stages in order. Copy lives in the landing catalog (EN and RU).
const STAGES = ['capture', 'plan', 'do', 'review'] as const;

const LandingPage = () => {
    const { t } = useTranslation();
    const scopeLink = useScopeLink();
    return (
        <div className="landing-page">
            <a
                className="landing-skip-link landing-action"
                href="#landing-main"
                onClick={() => {
                    document.getElementById('landing-main')?.focus();
                }}
            >
                {t('landing.skipToContent')}
            </a>

            <header className="landing-nav" aria-label={t('landing.navigation')}>
                <Link className="landing-wordmark landing-action" to="/welcome">WorkChord</Link>
            </header>

            <main id="landing-main" className="landing-main" tabIndex={-1}>
                <section className="landing-hero" aria-label={t('landing.heroTitle')}>
                    <PageHeader
                        title={t('landing.heroTitle')}
                        purpose={t('landing.heroLede')}
                        primaryAction={<ButtonLink variant="plain" className="landing-button" to={scopeLink('/')}>{t('landing.openTheWorkspace')}</ButtonLink>}
                    />
                    <ol className="landing-stages" aria-label={t('landing.workflowLabel')}>
                        {STAGES.map(key => (
                            <li className="landing-stage" key={key}>
                                <span className="landing-stage__term">{t(`landing.stages.${key}.term`)}</span>
                                <span className="landing-stage__sentence">{t(`landing.stages.${key}.sentence`)}</span>
                            </li>
                        ))}
                    </ol>
                </section>
            </main>
        </div>
    );
};

export default LandingPage;
