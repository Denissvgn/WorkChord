import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { iterationService } from '../../services/iterationService';
import { projectService } from '../../services/projectService';
import { useWorkScope } from '../../features/scope/useWorkScope';
import type { ScopeIteration, ScopeProject } from '../../features/scope/workScope';
import { formatDate } from '../../utils/formatDate';
import type { Iteration } from '../../types/iteration';
import type { Project } from '../../types/project';
import { ScopePicker, type ScopePickerOption } from './ScopePicker';

const ALL_PROJECTS_KEY = 'project:all';
const BACKLOG_KEY = 'iteration:backlog';
const NEW_ITERATION_KEY = 'action:new-iteration';
const MANAGE_ITERATIONS_KEY = 'action:manage-iterations';

const PLAN_ITERATIONS_PATH = '/plan?panel=iterations';
const PLAN_NEW_ITERATION_PATH = '/plan?create=1';

const todayIso = () => new Date().toISOString().slice(0, 10);

const isCurrent = (iteration: Iteration, today: string) => (
    iteration.start_date.slice(0, 10) <= today && today <= iteration.end_date.slice(0, 10)
);

const byProjectOrder = (a: Project, b: Project) => (
    a.sort_order - b.sort_order || a.name.localeCompare(b.name)
);

/**
 * The top bar's Project and Iteration pickers. They set the scope every scoped page shows.
 * On pages that do not set the scope it is plain text.
 */
export const ScopeBar = () => {
    const { t } = useTranslation();
    const navigate = useNavigate();
    const { project, iteration, isReady, isReadOnly, setProject, setIteration, linkTo } = useWorkScope();

    // feedback-policy: query loading,error,retry,empty - the bar shows a short status; pages own the full states.
    const iterationsQuery = useQuery({ queryKey: ['iterations'], queryFn: iterationService.getAll });
    // feedback-policy: query loading,error,retry,empty - without projects the bar shows project ids; the scope still works.
    const projectsQuery = useQuery({ queryKey: ['projects'], queryFn: projectService.getAll });
    const iterations = iterationsQuery.data;
    const projects = projectsQuery.data;

    const projectName = (id: number) => (
        projects?.find(item => item.id === id)?.name ?? t('scopeBar.projectFallback', { id })
    );

    const projectValueLabel = project === 'all' || project === undefined
        ? t('scopeBar.allProjects')
        : projectName(project);

    const iterationsOfScope = useMemo(() => {
        if (!iterations) return [];
        const inScope = project === undefined || project === 'all'
            ? iterations
            : iterations.filter(item => item.project_id === project);
        return [...inScope].sort((a, b) => b.start_date.localeCompare(a.start_date));
    }, [iterations, project]);

    const iterationLabel = (item: Iteration) => (
        project === 'all' && item.project?.name ? `${item.name} · ${item.project.name}` : item.name
    );

    const iterationValueLabel = iteration === 'backlog' || iteration === undefined
        ? t('scopeBar.backlog')
        : (() => {
            const found = iterations?.find(item => item.id === iteration);
            return found ? iterationLabel(found) : t('scopeBar.iterationFallback', { id: iteration });
        })();

    const projectOptions = useMemo<ScopePickerOption[]>(() => {
        const result: ScopePickerOption[] = [{
            key: ALL_PROJECTS_KEY,
            label: t('scopeBar.allProjects'),
            selected: project === 'all',
        }];
        const groups = new Map<string, Project[]>();
        for (const item of [...(projects ?? [])].sort(byProjectOrder)) {
            const group = item.initiative?.name ?? '';
            groups.set(group, [...(groups.get(group) ?? []), item]);
        }
        const names = [...groups.keys()].sort((a, b) => (
            a === '' ? 1 : b === '' ? -1 : a.localeCompare(b)
        ));
        for (const name of names) {
            for (const item of groups.get(name) ?? []) {
                result.push({
                    key: `project:${item.id}`,
                    label: item.name,
                    group: name === '' ? t('scopeBar.noInitiative') : name,
                    selected: project === item.id,
                });
            }
        }
        return result;
    }, [project, projects, t]);

    const iterationOptions = useMemo<ScopePickerOption[]>(() => {
        const today = todayIso();
        const result: ScopePickerOption[] = [{
            key: BACKLOG_KEY,
            label: t('scopeBar.backlog'),
            detail: t('scopeBar.backlogDetail'),
            selected: iteration === 'backlog',
        }];
        for (const item of iterationsOfScope) {
            result.push({
                key: `iteration:${item.id}`,
                label: iterationLabel(item),
                detail: `${formatDate(item.start_date)} – ${formatDate(item.end_date)}`,
                marker: isCurrent(item, today) ? t('scopeBar.current') : undefined,
                selected: iteration === item.id,
            });
        }
        result.push(
            { key: NEW_ITERATION_KEY, label: t('scopeBar.newIteration'), action: true },
            { key: MANAGE_ITERATIONS_KEY, label: t('scopeBar.manageIterations'), action: true },
        );
        return result;
        // iterationLabel depends on project and the same iterations the list is built from.
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [iteration, iterationsOfScope, project, t]);

    const chooseProject = (option: ScopePickerOption) => {
        const next: ScopeProject = option.key === ALL_PROJECTS_KEY ? 'all' : Number(option.key.slice('project:'.length));
        setProject(next);
    };

    const chooseIteration = (option: ScopePickerOption) => {
        if (option.key === NEW_ITERATION_KEY) {
            navigate(linkTo(PLAN_NEW_ITERATION_PATH));
            return;
        }
        if (option.key === MANAGE_ITERATIONS_KEY) {
            navigate(linkTo(PLAN_ITERATIONS_PATH));
            return;
        }
        const next: ScopeIteration = option.key === BACKLOG_KEY ? 'backlog' : Number(option.key.slice('iteration:'.length));
        setIteration(next);
    };

    if (iterationsQuery.isError) {
        return <p className="scope-bar-status" role="status" data-testid="scope-bar">{t('scopeBar.unavailable')}</p>;
    }

    if (!isReady || project === undefined || iteration === undefined) {
        return <p className="scope-bar-status" role="status" data-testid="scope-bar">{t('scopeBar.loading')}</p>;
    }

    if (isReadOnly) {
        return (
            <p className="scope-bar-readonly" data-testid="scope-bar" data-read-only="true">
                <span className="scope-bar-readonly-item">
                    <span className="scope-bar-readonly-label">{t('scopeBar.project')}</span>
                    <strong title={projectValueLabel}>{projectValueLabel}</strong>
                </span>
                <span aria-hidden="true" className="scope-bar-readonly-sep">·</span>
                <span className="scope-bar-readonly-item">
                    <span className="scope-bar-readonly-label">{t('scopeBar.iteration')}</span>
                    <strong title={iterationValueLabel}>{iterationValueLabel}</strong>
                </span>
            </p>
        );
    }

    return (
        <div className="scope-bar" role="group" aria-label={t('scopeBar.label')} data-testid="scope-bar">
            <ScopePicker
                className="scope-picker-project"
                label={t('scopeBar.project')}
                valueLabel={projectValueLabel}
                options={projectOptions}
                onChoose={chooseProject}
                searchHint={t('scopeBar.searchProjects')}
                noMatches={t('scopeBar.noProjects')}
            />
            <ScopePicker
                className="scope-picker-iteration"
                label={t('scopeBar.iteration')}
                valueLabel={iterationValueLabel}
                options={iterationOptions}
                onChoose={chooseIteration}
                searchHint={t('scopeBar.searchIterations')}
                noMatches={t('scopeBar.noIterations')}
            />
        </div>
    );
};
