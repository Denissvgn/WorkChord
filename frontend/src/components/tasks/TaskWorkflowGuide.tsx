import { useState } from 'react';
import {
    Bot,
    CalendarRange,
    CheckCircle2,
    ChevronRight,
    CircleHelp,
    UserRoundCheck,
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { Button } from '../common/Button';
import { SlideOverDrawer } from '../ui/SlideOverDrawer';

export const TaskWorkflowGuide = () => {
    const { t } = useTranslation();
    const [open, setOpen] = useState(false);

    return (
        <>
            <Button
                type="button"
                variant="ghost"
                size="sm"
                className="gap-1.5"
                aria-expanded={open}
                aria-haspopup="dialog"
                onClick={() => setOpen(true)}
            >
                <CircleHelp aria-hidden="true" className="h-4 w-4" />
                {t('tasks.guide.trigger')}
            </Button>
            <SlideOverDrawer
                open={open}
                title={t('tasks.guide.title')}
                subtitle={t('tasks.guide.summary')}
                icon={<CircleHelp aria-hidden="true" className="h-4 w-4" />}
                onClose={() => setOpen(false)}
            >
                <div className="task-workflow-help">
                    <section className="task-workflow-required">
                        <h4>{t('tasks.guide.requiredTitle')}</h4>
                        <p>{t('tasks.guide.description')}</p>
                        <ol>
                            <li>
                                <span className="task-workflow-guide-step" aria-hidden="true">1</span>
                                <UserRoundCheck aria-hidden="true" className="h-4 w-4" />
                                <span>
                                    <strong>{t('tasks.guide.defineTitle')}</strong>
                                    <span>{t('tasks.guide.defineBody')}</span>
                                </span>
                            </li>
                            <li>
                                <span className="task-workflow-guide-step" aria-hidden="true">2</span>
                                <CheckCircle2 aria-hidden="true" className="h-4 w-4" />
                                <span>
                                    <strong>{t('tasks.guide.readyTitle')}</strong>
                                    <span>{t('tasks.guide.readyBody')}</span>
                                </span>
                            </li>
                            <li>
                                <span className="task-workflow-guide-step" aria-hidden="true">3</span>
                                <CalendarRange aria-hidden="true" className="h-4 w-4" />
                                <span>
                                    <strong>{t('tasks.guide.scheduleTitle')}</strong>
                                    <span>{t('tasks.guide.scheduleBody')}</span>
                                </span>
                            </li>
                        </ol>
                    </section>
                    <section className="task-workflow-agent-branch">
                        <Bot aria-hidden="true" className="h-4 w-4" />
                        <div>
                            <h4>{t('tasks.guide.optionalAgentTitle')}</h4>
                            <p>{t('tasks.guide.optionalAgentBody')}</p>
                        </div>
                    </section>
                    <Link
                        to="/plan/master"
                        className="btn secondary sm"
                        onClick={() => setOpen(false)}
                    >
                        {t('tasks.guide.openPlanWork')}
                        <ChevronRight aria-hidden="true" className="h-3.5 w-3.5" />
                    </Link>
                </div>
            </SlideOverDrawer>
        </>
    );
};
