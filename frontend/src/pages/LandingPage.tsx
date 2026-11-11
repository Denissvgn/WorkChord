import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import '../styles/landing.css';

// Copy lives in the landing catalog (EN and RU); the numbering stays in code.
const STAGES = [
    { number: '1.0', key: 'capture' },
    { number: '2.0', key: 'shape' },
    { number: '3.0', key: 'coordinate' },
    { number: '4.0', key: 'review' },
] as const;

const BENEFITS = ['source', 'constraints', 'agent', 'evidence'] as const;

const WorkflowMap = () => {
    const { t } = useTranslation();
    return (
    <figure className="landing-map" aria-labelledby="landing-map-caption">
        <figcaption id="landing-map-caption">{t('landing.map.caption')}</figcaption>
        <svg className="landing-map__diagram" viewBox="0 0 720 330" aria-hidden="true">
            <path className="landing-map__path" d="M 140 96 C 205 96 205 96 270 96" />
            <path className="landing-map__path" d="M 450 96 C 515 96 515 96 580 96" />
            <path className="landing-map__path landing-map__path--return" d="M 620 142 C 620 258 100 258 100 142" />
            <circle className="landing-map__signal" cx="205" cy="96" r="5" />
            <circle className="landing-map__signal" cx="515" cy="96" r="5" />

            <g className="landing-map__node">
                <rect x="20" y="50" width="120" height="92" rx="6" />
                <text className="landing-map__index" x="38" y="78">1.0</text>
                <text className="landing-map__label" x="38" y="108">{t('landing.map.capture')}</text>
                <text className="landing-map__detail" x="80" y="126" textAnchor="middle">{t('landing.map.captureDetail')}</text>
            </g>
            <g className="landing-map__node landing-map__node--active">
                <rect x="270" y="38" width="180" height="116" rx="6" />
                <text className="landing-map__index" x="292" y="70">2.0 + 3.0</text>
                <text className="landing-map__label" x="292" y="103">{t('landing.map.plan')}</text>
                <text className="landing-map__detail" x="360" y="125" textAnchor="middle">{t('landing.map.planDetail')}</text>
            </g>
            <g className="landing-map__node">
                <rect x="580" y="50" width="120" height="92" rx="6" />
                <text className="landing-map__index" x="598" y="78">4.0</text>
                <text className="landing-map__label" x="598" y="108">{t('landing.map.review')}</text>
                <text className="landing-map__detail" x="640" y="126" textAnchor="middle">{t('landing.map.reviewDetail')}</text>
            </g>

            <text className="landing-map__loop-label" x="360" y="280" textAnchor="middle">{t('landing.map.loop')}</text>
        </svg>
        <ol className="landing-map__mobile" aria-label={t('landing.map.flow')}>
            <li><span>1.0</span> {t('landing.map.steps.capture')}</li>
            <li><span>2.0</span> {t('landing.map.steps.shape')}</li>
            <li><span>3.0</span> {t('landing.map.steps.coordinate')}</li>
            <li><span>4.0</span> {t('landing.map.steps.review')}</li>
        </ol>
    </figure>
    );
};

const LandingPage = () => {
    const { t } = useTranslation();
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
                <Link className="landing-nav__action landing-action" to="/">{t('landing.openWorkspace')} <span aria-hidden="true">↗</span></Link>
            </header>

            <main id="landing-main" tabIndex={-1}>
                <section className="landing-hero" aria-labelledby="landing-title">
                    <div className="landing-hero__copy">
                        <p className="landing-hero__context">{t('landing.heroContext')}</p>
                        <h1 id="landing-title">{t('landing.heroTitle')}</h1>
                        <p className="landing-hero__lede">{t('landing.heroLede')}</p>
                        <a className="landing-text-link landing-action" href="#workflow">
                            {t('landing.followWorkflow')} <span aria-hidden="true">↓</span>
                        </a>
                    </div>
                    <WorkflowMap />
                </section>

                <section id="workflow" className="landing-workflow" aria-labelledby="workflow-title">
                    <div className="landing-workflow__intro">
                        <h2 id="workflow-title">{t('landing.workflowTitle')}</h2>
                        <p>{t('landing.workflowIntro')}</p>
                    </div>

                    <ol className="landing-stages">
                        {STAGES.map(({ number, key }) => {
                            const verb = t(`landing.stages.${key}.verb`);
                            const surfaces = t(`landing.stages.${key}.surfaces`, { returnObjects: true }) as string[];
                            return (
                                <li className="landing-stage" key={number}>
                                    <div className="landing-stage__heading">
                                        <span className="landing-stage__number">{number} · {verb}</span>
                                        <h3>{t(`landing.stages.${key}.title`)}</h3>
                                    </div>
                                    <div className="landing-stage__body">
                                        <p>{t(`landing.stages.${key}.description`)}</p>
                                        <p className="landing-stage__result">{t('landing.result', { result: t(`landing.stages.${key}.result`) })}</p>
                                    </div>
                                    <ul className="landing-stage__surfaces" aria-label={t('landing.stageSurfaces', { verb })}>
                                        {surfaces.map(surface => <li key={surface}>{surface}</li>)}
                                    </ul>
                                </li>
                            );
                        })}
                    </ol>
                </section>

                <section className="landing-operating" aria-labelledby="operating-title">
                    <div className="landing-operating__intro">
                        <h2 id="operating-title">{t('landing.operatingTitle')}</h2>
                        <p>{t('landing.operatingIntro')}</p>
                    </div>
                    <dl className="landing-benefits">
                        {BENEFITS.map(key => (
                            <div className="landing-benefit" key={key}>
                                <dt>{t(`landing.benefits.${key}.term`)}</dt>
                                <dd>{t(`landing.benefits.${key}.detail`)}</dd>
                            </div>
                        ))}
                    </dl>
                </section>

                <section className="landing-close" aria-labelledby="landing-close-title">
                    <div>
                        <h2 id="landing-close-title">{t('landing.closeTitle')}</h2>
                        <p>{t('landing.closeBody')}</p>
                    </div>
                    <Link className="landing-text-link landing-action" to="/">
                        {t('landing.openTheWorkspace')} <span aria-hidden="true">→</span>
                    </Link>
                </section>
            </main>

            <footer className="landing-footer">
                <p className="landing-footer__statement">{t('landing.footerStatement')}</p>
                <div className="landing-footer__meta">
                    <span>WorkChord</span>
                    <span>{t('landing.footerMeta')}</span>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
