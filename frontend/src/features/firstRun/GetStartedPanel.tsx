import { useState } from 'react';
import type { ReactNode } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { ArrowRight, Check, ChevronDown, X } from 'lucide-react';
import clsx from 'clsx';
import { Button } from '../../components/common/Button';
import { useIdentity } from '../identity/identityContext';
import { LocalProfilePicker } from '../identity/LocalProfilePicker';
import { useScopeLink } from '../scope/useScopeLink';
import { useSetWorkScope } from '../scope/useWorkScope';
import { SampleProjectAction } from './SampleProjectAction';
import { CreateProjectModal } from './CreateProjectModal';
import { FIRST_RUN_PLAN_CHECKPOINT, firstRunPlanHref, type FirstRunStep, type FirstRunStepId } from './firstRunSteps';
import { useGetStartedVisibility } from './getStartedVisibility';
import type { FirstRunProgress } from './useFirstRunProgress';

const TITLE_ID = 'get-started-title';

const StepResult = ({ step, progress }: { step: FirstRunStep; progress: FirstRunProgress }) => {
    const { t } = useTranslation();
    const identity = useIdentity()?.identity;
    const { facts } = progress;
    switch (step.id) {
        case 'profile':
            return <>{t('firstRun.steps.profile.result', { name: identity?.profile?.display_name ?? '' })}</>;
        case 'project':
            return <>{t('firstRun.steps.project.result', { count: facts.projectCount, name: progress.projectName ?? '' })}</>;
        case 'iteration':
            return <>{t('firstRun.steps.iteration.result', { count: facts.iterationCount })}</>;
        case 'capacity':
            return <>{t('firstRun.steps.capacity.result', { count: facts.capacityRows })}</>;
        case 'tasks':
            return <>{t('firstRun.steps.tasks.result', { count: facts.taskCount })}</>;
        case 'schedule':
            return <>{t('firstRun.steps.schedule.result')}</>;
    }
};

const StepBody = ({ step, isNext }: { step: FirstRunStep; isNext: boolean }) => {
    const { t } = useTranslation();
    const scopeLink = useScopeLink();
    const identityContext = useIdentity();
    const identity = identityContext?.identity;
    const { setProject } = useSetWorkScope();
    const [creatingProject, setCreatingProject] = useState(false);
    // One primary action per page: only the next step's own action is primary.
    const primary = isNext && !step.done;

    if (step.id === 'profile') {
        const local = identity?.mode === 'trusted_local' && !identity.principal;
        // The picker explains the choice itself; a managed account is linked by an operator.
        return local
            ? <div className="get-started-picker"><LocalProfilePicker current={identity?.profile ?? null} onChosen={() => identityContext?.refresh()} /></div>
            : <p className="plan-section-waiting">{step.done
                ? t('firstRun.steps.profile.result', { name: identity?.profile?.display_name ?? '' })
                : t('firstRun.steps.profile.managed')}</p>;
    }
    if (step.id === 'project') {
        return (
            <>
                <p className="plan-section-waiting">{t('firstRun.steps.project.body')}</p>
                <div className="plan-section-owner">
                    <Button variant={primary ? 'primary' : 'secondary'} onClick={() => setCreatingProject(true)}>
                        {t('firstRun.steps.project.action')}
                    </Button>
                </div>
                {creatingProject && (
                    <CreateProjectModal
                        onClose={() => setCreatingProject(false)}
                        onCreated={project => {
                            setCreatingProject(false);
                            // The new project becomes the scope, so its first iteration is created in it.
                            setProject(project.id);
                        }}
                    />
                )}
            </>
        );
    }
    const checkpoint = FIRST_RUN_PLAN_CHECKPOINT[step.id]!;
    return (
        <>
            <p className="plan-section-waiting">{t(`firstRun.steps.${step.id}.body`)}</p>
            <div className="plan-section-owner">
                <Link className={clsx('btn', primary ? 'primary' : 'secondary')} to={scopeLink(firstRunPlanHref(checkpoint))}>
                    {t('firstRun.openPlan')}
                    <ArrowRight aria-hidden="true" size={14} />
                </Link>
            </div>
        </>
    );
};

const StepRow = ({ step, open, isNext, onToggle, progress }: {
    step: FirstRunStep;
    open: boolean;
    isNext: boolean;
    onToggle: () => void;
    progress: FirstRunProgress;
}) => {
    const { t } = useTranslation();
    const headingId = `get-started-${step.id}-title`;
    const bodyId = `get-started-${step.id}-body`;
    const statusId = `get-started-${step.id}-status`;
    return (
        <li
            className={clsx('plan-section', step.done ? 'is-done' : isNext && 'is-next', open && 'is-open')}
            data-testid={`get-started-step-${step.id}`}
            data-done={step.done ? 'true' : 'false'}
        >
            <div className="plan-section-head">
                <span className="plan-section-number" aria-hidden="true">
                    {step.done ? <Check size={13} strokeWidth={3} /> : step.number}
                </span>
                <h3 id={headingId} className="plan-section-title">
                    <Button variant="ghost" className="plan-section-toggle" aria-expanded={open} aria-controls={bodyId}
                        aria-describedby={statusId} onClick={onToggle}>
                        <span className="sr-only">{t('firstRun.stepNumber', { number: step.number })}: </span>
                        {t(`firstRun.steps.${step.id}.title`)}
                        <ChevronDown aria-hidden="true" size={15} className="plan-section-chevron" />
                    </Button>
                </h3>
                <p id={statusId} className="plan-section-status">
                    {step.done ? (
                        <>
                            <span className="pill resolved"><span className="pdot" />{t('firstRun.done')}</span>
                            <span className="plan-section-result"><StepResult step={step} progress={progress} /></span>
                        </>
                    ) : isNext ? (
                        <span className="pill accent"><span className="pdot" />{t('firstRun.next')}</span>
                    ) : (
                        <span className="plan-section-result">{t('firstRun.notDone')}</span>
                    )}
                </p>
            </div>
            {open && (
                <div id={bodyId} className="plan-section-body" role="region" aria-labelledby={headingId}>
                    <StepBody step={step} isNext={isNext} />
                </div>
            )}
        </li>
    );
};

/**
 * The Get started panel: six steps from an empty workspace to its first applied schedule.
 * Each step is done exactly while its data exists, and the first one not done is open.
 * `secondaryAction` is the place for another way in, such as a sample project.
 */
export const GetStartedPanel = ({ progress, secondaryAction }: { progress: FirstRunProgress; secondaryAction?: ReactNode }) => {
    const { t } = useTranslation();
    const dismiss = useGetStartedVisibility(state => state.dismiss);
    const { steps, nextId, complete } = progress;
    // Opening a step by hand holds until the next step changes; then the new next step opens.
    const [override, setOverride] = useState<{ nextId: FirstRunStepId | null; open: FirstRunStepId | null } | null>(null);
    const openId = override && override.nextId === nextId ? override.open : nextId;

    return (
        <section className="get-started" aria-labelledby={TITLE_ID} data-testid="get-started-panel">
            <header className="get-started-head">
                <div className="get-started-copy">
                    <h2 id={TITLE_ID}>{t('firstRun.title')}</h2>
                    <p>{complete ? t('firstRun.allDone') : t('firstRun.purpose')}</p>
                </div>
                <Button variant="ghost" size="sm" onClick={dismiss} aria-label={t('firstRun.dismissLabel')}
                    aria-describedby="get-started-reopen-hint">
                    <X aria-hidden="true" className="h-4 w-4" />
                    {t('firstRun.dismiss')}
                </Button>
            </header>
            <ol className="plan-sections get-started-steps" aria-label={t('firstRun.stepsLabel')}>
                {steps.map(step => (
                    <StepRow
                        key={step.id}
                        step={step}
                        open={openId === step.id}
                        isNext={nextId === step.id}
                        progress={progress}
                        onToggle={() => setOverride({ nextId, open: openId === step.id ? null : step.id })}
                    />
                ))}
            </ol>
            <footer className="get-started-foot">
                <p id="get-started-reopen-hint">{t('firstRun.reopenHint')}</p>
                <div className="get-started-secondary" data-testid="get-started-secondary-slot">{secondaryAction ?? <SampleProjectAction />}</div>
            </footer>
        </section>
    );
};
