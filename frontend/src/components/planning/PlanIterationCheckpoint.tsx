import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { useIterationPanels } from '../../features/planningMasters/useIterationPanels';
import { calendarService } from '../../services/calendarService';
import { iterationService } from '../../services/iterationService';
import type { Iteration } from '../../types/iteration';
import { formatDate } from '../../utils/formatDate';

/**
 * The body of the Iteration checkpoint: what the iteration in scope is, and the actions that manage
 * iterations without leaving Plan. The checkpoint's state comes from the server; this only shows facts.
 */
export const PlanIterationCheckpoint = ({ iteration, done, calendarOutsideYear = false, readinessCalendarName }: { iteration: Iteration | null; done: boolean; calendarOutsideYear?: boolean; readinessCalendarName?: string | null }) => {
    const { t, i18n } = useTranslation();
    const panels = useIterationPanels();
    // feedback-policy: query loading,error,retry,empty - the calendar row shows its id until the name is known.
    const calendars = useQuery({ queryKey: ['calendars'], queryFn: calendarService.getAll, staleTime: 60_000, enabled: iteration !== null });
    // feedback-policy: query loading,error,retry,empty - All iterations stays until the list is known to be empty.
    const iterations = useQuery({ queryKey: ['iterations'], queryFn: iterationService.getAll, staleTime: 60_000 });
    // With no iteration at all, All iterations has nothing to list: New iteration is the one action.
    const hasIterations = iterations.data === undefined || iterations.data.length > 0;
    const calendarName = iteration
        ? calendars.data?.find(calendar => calendar.id === iteration.calendar_id)?.name
            ?? t('plan.page.calendarFallback', { id: iteration.calendar_id })
        : '';
    const calendarYear = calendars.data?.find(calendar => calendar.id === iteration?.calendar_id)?.year;
    const startYear = iteration?.start_date.slice(0, 4);
    const endYear = iteration?.end_date.slice(0, 4);
    const missingYear = calendarYear && String(calendarYear) === startYear ? endYear : startYear;
    // One primary action per page: the open, incomplete checkpoint's own.
    const primary = !done;

    return (
        <>
            {iteration ? (
                <section className="plan-checkpoint-evidence" aria-labelledby="plan-section-iteration-evidence">
                    <h3 id="plan-section-iteration-evidence">{t('plan.page.evidence')}</h3>
                    <dl>
                        <div><dt>{t('plan.page.iteration')}</dt><dd>{iteration.name}</dd></div>
                        <div>
                            <dt>{t('plan.page.dates')}</dt>
                            <dd>{formatDate(iteration.start_date, i18n.language)} – {formatDate(iteration.end_date, i18n.language)}</dd>
                        </div>
                        <div><dt>{t('plan.master.workingDays')}</dt><dd>{t('plan.master.daysCount', { count: iteration.working_days })}</dd></div>
                        <div><dt>{t('iterations.calendar')}</dt><dd>{calendarName}</dd></div>
                        <div>
                            <dt>{t('plan.page.project')}</dt>
                            <dd>
                                {iteration.project
                                    ? <Link className="plan-evidence-link" to={`/projects/${iteration.project.id}`}>{iteration.project.name}</Link>
                                    : t('iterations.unscopedShort')}
                            </dd>
                        </div>
                    </dl>
                </section>
            ) : (
                <p className="plan-section-waiting">{t('plan.page.noIterationBody')}</p>
            )}
            {calendarOutsideYear && <p>{t('plan.page.calendarOutsideYear', { calendar: readinessCalendarName ?? calendarName })} <Link className="plan-evidence-link" to={`/settings?tab=work_calendar&create=1${missingYear ? `&year=${missingYear}` : ''}`}>{t('plan.page.createCoveringCalendar')}</Link></p>}
            <div className="plan-section-owner flex flex-wrap items-center gap-2">
                {iteration ? (
                    <Button variant="secondary" onClick={() => panels.openEdit(iteration.id)}>{t('iterations.editIteration')}</Button>
                ) : null}
                <Button variant={primary ? 'primary' : 'secondary'} onClick={panels.openCreate}>{t('iterations.newIteration')}</Button>
                {hasIterations && <Button variant="secondary" onClick={panels.openList}>{t('iterations.allIterations')}</Button>}
            </div>
        </>
    );
};
