import { Link } from 'react-router-dom';
import '../styles/landing.css';

const workflowStages = [
    {
        number: '1.0',
        verb: 'Capture',
        title: 'Give work a clear entrance.',
        description: 'Projects, triage, and task trees keep incoming requests attached to the context that turns them into planned work.',
        result: 'Less intent is lost between intake and planning.',
        surfaces: ['Projects', 'Triage', 'Task trees'],
    },
    {
        number: '2.0',
        verb: 'Shape',
        title: 'Test the plan before commitment.',
        description: 'Iterations, dependencies, capacity, calendar, and Gantt views expose sequence and constraint decisions while they can still change.',
        result: 'Trade-offs become visible before dates become promises.',
        surfaces: ['Iterations', 'Capacity', 'Dependencies', 'Gantt'],
    },
    {
        number: '3.0',
        verb: 'Coordinate',
        title: 'Put an agent PM to work—under your control.',
        description: 'An agent PM can use portable planner roles, authenticated MCP workflows, and the agent pipeline to move qualified work through a visible queue.',
        result: 'Routine coordination can be automated while the user retains control of priorities, progress, and review.',
        surfaces: ['Agent pipeline', 'Planner role', 'Work queue', 'MCP'],
    },
    {
        number: '4.0',
        verb: 'Review',
        title: 'Follow delivery without rebuilding the story.',
        description: 'Roadmaps, release planning, analytics, and audit history keep the current plan and the record of change in the same workspace.',
        result: 'Progress and change stay explainable to the people relying on them.',
        surfaces: ['Roadmap', 'Releases', 'Analytics', 'Audit history'],
    },
] as const;

const operatingBenefits = [
    ['One source of work', 'Requests, plans, dependencies, and delivery views share the same underlying project context.'],
    ['Constraint-aware planning', 'Capacity and sequencing sit beside the work instead of in a separate spreadsheet.'],
    ['Controlled agent PM', 'Automate routine planning and coordination while the user directs priorities, watches progress, and reviews the visible work queue.'],
    ['Delivery evidence', 'Release planning, analytics, and audit history preserve what changed and why.'],
] as const;

const WorkflowMap = () => (
    <figure className="landing-map" aria-labelledby="landing-map-caption">
        <figcaption id="landing-map-caption">One planning thread, from request to review.</figcaption>
        <svg className="landing-map__diagram" viewBox="0 0 720 330" aria-hidden="true">
            <path className="landing-map__path" d="M 140 96 C 205 96 205 96 270 96" />
            <path className="landing-map__path" d="M 450 96 C 515 96 515 96 580 96" />
            <path className="landing-map__path landing-map__path--return" d="M 620 142 C 620 258 100 258 100 142" />
            <circle className="landing-map__signal" cx="205" cy="96" r="5" />
            <circle className="landing-map__signal" cx="515" cy="96" r="5" />

            <g className="landing-map__node">
                <rect x="20" y="50" width="120" height="92" rx="6" />
                <text className="landing-map__index" x="38" y="78">1.0</text>
                <text className="landing-map__label" x="38" y="108">Capture</text>
                <text className="landing-map__detail" x="80" y="126" textAnchor="middle">intake + tasks</text>
            </g>
            <g className="landing-map__node landing-map__node--active">
                <rect x="270" y="38" width="180" height="116" rx="6" />
                <text className="landing-map__index" x="292" y="70">2.0 + 3.0</text>
                <text className="landing-map__label" x="292" y="103">Plan together</text>
                <text className="landing-map__detail" x="360" y="125" textAnchor="middle">scope + capacity</text>
            </g>
            <g className="landing-map__node">
                <rect x="580" y="50" width="120" height="92" rx="6" />
                <text className="landing-map__index" x="598" y="78">4.0</text>
                <text className="landing-map__label" x="598" y="108">Review</text>
                <text className="landing-map__detail" x="640" y="126" textAnchor="middle">release record</text>
            </g>

            <text className="landing-map__loop-label" x="360" y="280" textAnchor="middle">THE RECORD RETURNS TO THE NEXT PLAN</text>
        </svg>
        <ol className="landing-map__mobile" aria-label="WorkChord planning flow">
            <li><span>1.0</span> Capture requests and work</li>
            <li><span>2.0</span> Shape scope and capacity</li>
            <li><span>3.0</span> Coordinate people and agents</li>
            <li><span>4.0</span> Review delivery and change</li>
        </ol>
    </figure>
);

const LandingPage = () => {
    return (
        <div className="landing-page">
            <a
                className="landing-skip-link landing-action"
                href="#landing-main"
                onClick={() => {
                    document.getElementById('landing-main')?.focus();
                }}
            >
                Skip to content
            </a>

            <header className="landing-nav" aria-label="Landing page navigation">
                <Link className="landing-wordmark landing-action" to="/welcome">WorkChord</Link>
                <Link className="landing-nav__action landing-action" to="/">Open workspace <span aria-hidden="true">↗</span></Link>
            </header>

            <main id="landing-main" tabIndex={-1}>
                <section className="landing-hero" aria-labelledby="landing-title">
                    <div className="landing-hero__copy">
                        <p className="landing-hero__context">SELF-HOSTED PLANNING + DELIVERY</p>
                        <h1 id="landing-title">Plan work that holds.</h1>
                        <p className="landing-hero__lede">
                            WorkChord gives product managers one place to shape work, see capacity,
                            connect dependencies, and follow delivery—across people and agents. It can
                            also give an agent PM a controlled queue for routine planning and coordination.
                        </p>
                        <a className="landing-text-link landing-action" href="#workflow">
                            Follow the workflow <span aria-hidden="true">↓</span>
                        </a>
                    </div>
                    <WorkflowMap />
                </section>

                <section id="workflow" className="landing-workflow" aria-labelledby="workflow-title">
                    <div className="landing-workflow__intro">
                        <h2 id="workflow-title">The system follows the work.</h2>
                        <p>
                            WorkChord connects planning surfaces in the order product managers use them.
                            Each stage leaves context for the next.
                        </p>
                    </div>

                    <ol className="landing-stages">
                        {workflowStages.map(stage => (
                            <li className="landing-stage" key={stage.number}>
                                <div className="landing-stage__heading">
                                    <span className="landing-stage__number">{stage.number} · {stage.verb}</span>
                                    <h3>{stage.title}</h3>
                                </div>
                                <div className="landing-stage__body">
                                    <p>{stage.description}</p>
                                    <p className="landing-stage__result">Result — {stage.result}</p>
                                </div>
                                <ul className="landing-stage__surfaces" aria-label={`${stage.verb} surfaces`}>
                                    {stage.surfaces.map(surface => <li key={surface}>{surface}</li>)}
                                </ul>
                            </li>
                        ))}
                    </ol>
                </section>

                <section className="landing-operating" aria-labelledby="operating-title">
                    <div className="landing-operating__intro">
                        <h2 id="operating-title">Fewer planning gaps.</h2>
                        <p>Not another report. A shared operating record for the work itself.</p>
                    </div>
                    <dl className="landing-benefits">
                        {operatingBenefits.map(([term, detail]) => (
                            <div className="landing-benefit" key={term}>
                                <dt>{term}</dt>
                                <dd>{detail}</dd>
                            </div>
                        ))}
                    </dl>
                </section>

                <section className="landing-close" aria-labelledby="landing-close-title">
                    <div>
                        <h2 id="landing-close-title">See the plan in its working form.</h2>
                        <p>The workspace is the product: projects, capacity, sequencing, delivery, and evidence.</p>
                    </div>
                    <Link className="landing-text-link landing-action" to="/">
                        Open the workspace <span aria-hidden="true">→</span>
                    </Link>
                </section>
            </main>

            <footer className="landing-footer">
                <p className="landing-footer__statement">A plan should survive contact with delivery.</p>
                <div className="landing-footer__meta">
                    <span>WorkChord</span>
                    <span>Self-hosted · MIT licensed</span>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
