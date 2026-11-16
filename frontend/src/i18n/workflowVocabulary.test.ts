/// <reference types="node" />

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { englishResources } from './resources.en';
import { russianResources } from './resources.ru';

type Localized = { en: string; ru: string };
type Entry = { id: string; name: Localized | string; group?: Localized; description?: Localized };
type Vocabulary = Record<'destinations' | 'checkpoints' | 'terms' | 'roles' | 'task_states' | 'actions' | 'queues' | 'triage_dispositions' | 'pipeline_stages', Entry[]>;

// The same vocabulary generates the shared block in every agent role skill.
const vocabulary = JSON.parse(
    readFileSync(resolve(process.cwd(), '../config/workflow-vocabulary.json'), 'utf8'),
) as Vocabulary;

type WorkflowStep = { id: string; name: string; name_ru?: string };
const workflowSteps = (vocabulary as unknown as { workflow: WorkflowStep[] }).workflow;

// Interface labels that must use the shared names. When a screen adopts
// another vocabulary term, add its keys here in the same change.
const LABEL_KEYS: Array<{ section: keyof Vocabulary; id: string; field: 'name' | 'group' | 'description'; keys: string[] }> = [
    { section: 'destinations', id: 'overview', field: 'name', keys: ['nav.overview', 'documentTitles.overview'] },
    { section: 'destinations', id: 'my_work', field: 'name', keys: ['teamwork.myWork'] },
    { section: 'destinations', id: 'triage', field: 'name', keys: ['nav.triage', 'documentTitles.triage', 'surfaces.triagePage.triageIntake', 'literals.triage_intake'] },
    { section: 'destinations', id: 'projects', field: 'name', keys: ['nav.projects', 'documentTitles.projects'] },
    { section: 'destinations', id: 'plan', field: 'name', keys: ['nav.planWork', 'documentTitles.plan', 'documentTitles.planMaster', 'plan.title', 'plan.hub.planIterationTitle'] },
    { section: 'destinations', id: 'gantt', field: 'name', keys: ['nav.gantt', 'documentTitles.gantt', 'gantt.title'] },
    { section: 'destinations', id: 'tasks', field: 'name', keys: ['nav.tasks', 'documentTitles.tasks'] },
    { section: 'destinations', id: 'analytics', field: 'name', keys: ['nav.analytics', 'documentTitles.analytics'] },
    { section: 'destinations', id: 'team', field: 'name', keys: ['nav.team', 'documentTitles.team'] },
    { section: 'destinations', id: 'settings', field: 'name', keys: ['nav.settings', 'documentTitles.settings'] },
    { section: 'checkpoints', id: 'iteration', field: 'name', keys: ['plan.steps.iteration.title'] },
    { section: 'checkpoints', id: 'capacity', field: 'name', keys: ['plan.steps.team.title'] },
    { section: 'checkpoints', id: 'work', field: 'name', keys: ['plan.steps.work.title'] },
    { section: 'checkpoints', id: 'blockers', field: 'name', keys: ['plan.steps.blockers.title'] },
    { section: 'checkpoints', id: 'schedule', field: 'name', keys: ['plan.steps.schedule.title'] },
    { section: 'checkpoints', id: 'review', field: 'name', keys: ['plan.steps.review.title'] },
    { section: 'terms', id: 'iteration', field: 'name', keys: ['domain.iteration', 'plan.master.planningPeriod'] },
    { section: 'terms', id: 'assignee', field: 'name', keys: ['taskList.assignee', 'surfaces.taskForm.assignee', 'surfaces.triagePage.assignee'] },
    { section: 'terms', id: 'reviewer', field: 'name', keys: ['domain.reviewer'] },
    { section: 'terms', id: 'labels', field: 'name', keys: ['surfaces.taskForm.tags', 'surfaces.triagePage.tags', 'taskFilters.labels'] },
    { section: 'terms', id: 'waits_for', field: 'name', keys: ['taskList.dependsOn', 'surfaces.taskForm.dependencies', 'surfaces.triagePage.dependencies', 'taskFilters.dependencies'] },
    { section: 'terms', id: 'earliest_start', field: 'name', keys: ['gantt.inputEarliestStart', 'surfaces.taskForm.minStartDate'] },
    { section: 'terms', id: 'due_by', field: 'name', keys: ['gantt.inputDueBy', 'surfaces.taskForm.maxEndDate'] },
    { section: 'terms', id: 'request', field: 'name', keys: ['seedDisplay.labels.label_request.name'] },
    { section: 'terms', id: 'notifications', field: 'name', keys: ['teamwork.queue_inbox'] },
    { section: 'roles', id: 'pm', field: 'name', keys: ['agentTeamSetup.roles.pm'] },
    { section: 'roles', id: 'worker', field: 'name', keys: ['agentTeamSetup.roles.worker'] },
    { section: 'roles', id: 'reviewer', field: 'name', keys: ['agentTeamSetup.roles.verifier'] },
    { section: 'roles', id: 'pm', field: 'group', keys: ['agentTeamSetup.steps.controller.title'] },
    { section: 'roles', id: 'worker', field: 'group', keys: ['agentTeamSetup.steps.workers.title'] },
    { section: 'roles', id: 'reviewer', field: 'group', keys: ['agentTeamSetup.steps.verifier.title'] },
    { section: 'task_states', id: 'planned', field: 'name', keys: ['statuses.planned'] },
    { section: 'task_states', id: 'active', field: 'name', keys: ['statuses.active'] },
    { section: 'task_states', id: 'resolved', field: 'name', keys: ['statuses.resolved'] },
    { section: 'task_states', id: 'closed', field: 'name', keys: ['statuses.closed'] },
    { section: 'actions', id: 'start_work', field: 'name', keys: ['domain.action_start_manual'] },
    { section: 'actions', id: 'submit_for_review', field: 'name', keys: ['domain.action_resolve_manual'] },
    { section: 'actions', id: 'report_blocker', field: 'name', keys: ['domain.action_block'] },
    { section: 'actions', id: 'remove_block', field: 'name', keys: ['domain.action_unblock'] },
    { section: 'actions', id: 'accept', field: 'name', keys: ['domain.accept', 'domain.action_accept_review'] },
    { section: 'actions', id: 'request_changes', field: 'name', keys: ['domain.requestRework'] },
    { section: 'actions', id: 'reopen', field: 'name', keys: ['domain.action_reopen'] },
    { section: 'queues', id: 'doing', field: 'name', keys: ['teamwork.queue_active'] },
    { section: 'queues', id: 'up_next', field: 'name', keys: ['teamwork.queue_queued'] },
    { section: 'queues', id: 'blocked', field: 'name', keys: ['teamwork.queue_blocked'] },
    { section: 'queues', id: 'in_review', field: 'name', keys: ['teamwork.queue_awaiting_review'] },
    { section: 'queues', id: 'to_review', field: 'name', keys: ['teamwork.queue_review'] },
    { section: 'queues', id: 'inbox', field: 'name', keys: ['teamwork.queue_inbox'] },
    { section: 'triage_dispositions', id: 'convert', field: 'name', keys: ['surfaces.triagePage.convert'] },
    { section: 'triage_dispositions', id: 'accept', field: 'name', keys: ['surfaces.triagePage.accept'] },
    { section: 'triage_dispositions', id: 'ask_for_clarification', field: 'name', keys: ['surfaces.triagePage.askForClarification'] },
    { section: 'triage_dispositions', id: 'snooze', field: 'name', keys: ['surfaces.triagePage.snooze'] },
    { section: 'triage_dispositions', id: 'mark_duplicate', field: 'name', keys: ['surfaces.triagePage.markDuplicate'] },
    { section: 'triage_dispositions', id: 'decline', field: 'name', keys: ['surfaces.triagePage.decline'] },
    { section: 'pipeline_stages', id: 'needs_definition', field: 'name', keys: ['agentPipeline.columns.needs_definition.title'] },
    { section: 'pipeline_stages', id: 'needs_definition', field: 'description', keys: ['agentPipeline.columns.needs_definition.description'] },
    { section: 'pipeline_stages', id: 'ready_to_assign', field: 'name', keys: ['agentPipeline.columns.ready_to_assign.title'] },
    { section: 'pipeline_stages', id: 'ready_to_assign', field: 'description', keys: ['agentPipeline.columns.ready_to_assign.description'] },
    { section: 'pipeline_stages', id: 'assigned_waiting', field: 'name', keys: ['agentPipeline.columns.assigned_waiting.title'] },
    { section: 'pipeline_stages', id: 'assigned_waiting', field: 'description', keys: ['agentPipeline.columns.assigned_waiting.description'] },
    { section: 'pipeline_stages', id: 'start_ready', field: 'name', keys: ['agentPipeline.columns.start_ready.title'] },
    { section: 'pipeline_stages', id: 'start_ready', field: 'description', keys: ['agentPipeline.columns.start_ready.description'] },
    { section: 'pipeline_stages', id: 'executing', field: 'name', keys: ['agentPipeline.columns.executing.title'] },
    { section: 'pipeline_stages', id: 'executing', field: 'description', keys: ['agentPipeline.columns.executing.description'] },
    { section: 'pipeline_stages', id: 'verification_required', field: 'name', keys: ['agentPipeline.columns.verification_required.title'] },
    { section: 'pipeline_stages', id: 'verification_required', field: 'description', keys: ['agentPipeline.columns.verification_required.description'] },
    { section: 'pipeline_stages', id: 'recovery_required', field: 'name', keys: ['agentPipeline.columns.recovery_required.title'] },
    { section: 'pipeline_stages', id: 'recovery_required', field: 'description', keys: ['agentPipeline.columns.recovery_required.description'] },
];

const lookup = (catalog: unknown, key: string): unknown => key.split('.').reduce<unknown>(
    (value, segment) => (value && typeof value === 'object'
        ? (value as Record<string, unknown>)[segment]
        : undefined),
    catalog,
);

const catalogs = {
    en: englishResources.translation,
    ru: russianResources.translation,
} as const;

describe('shared workflow vocabulary', () => {
    it('keeps English and Russian key sets equal, allowing language-specific plural forms', () => {
        const keys = (value: unknown, prefix = ''): string[] => (
            value && typeof value === 'object'
                ? Object.entries(value).flatMap(([key, child]) => keys(child, prefix ? `${prefix}.${key}` : key))
                : [prefix.replace(/_(zero|one|two|few|many|other)$/, '')]
        );
        expect([...new Set(keys(catalogs.en))].sort()).toEqual([...new Set(keys(catalogs.ru))].sort());
    });

    it.each(LABEL_KEYS.flatMap(entry => entry.keys.flatMap(key => (['en', 'ru'] as const).map(language => ({
        ...entry, key, language,
    })))))('$language $key uses the shared name for $section $id', ({ section, id, field, key, language }) => {
        const term = vocabulary[section].find(item => item.id === id);
        expect(term, `${section}.${id} is missing from the vocabulary`).toBeDefined();
        const names = term?.[field] as Localized | undefined;
        expect(lookup(catalogs[language], key)).toBe(names?.[language]);
    });

    it.each(['capture', 'plan', 'do', 'review'])('uses the vocabulary English name for the landing workflow step %s', stepId => {
        const step = workflowSteps.find(item => item.id === stepId);
        expect(step, `workflow.${stepId} is missing from the vocabulary`).toBeDefined();
        expect(lookup(catalogs.en, `landing.stages.${stepId}.term`)).toBe(step?.name);
    });

    it.each(['capture', 'plan', 'do', 'review'])('uses the vocabulary Russian name for the landing workflow step %s', stepId => {
        const step = workflowSteps.find(item => item.id === stepId);
        expect(step, `workflow.${stepId} is missing from the vocabulary`).toBeDefined();
        expect(step?.name_ru).toEqual(expect.any(String));
        expect(lookup(catalogs.ru, `landing.stages.${stepId}.term`)).toBe(step?.name_ru);
    });

    it('maps every shared destination, checkpoint, localized term and workflow entry to an interface label', () => {
        const mapped = new Set(LABEL_KEYS.map(entry => `${entry.section}.${entry.id}`));
        const required = (['destinations', 'checkpoints', 'roles', 'task_states', 'actions', 'queues', 'triage_dispositions', 'pipeline_stages'] as const)
            .flatMap(section => vocabulary[section].map(item => `${section}.${item.id}`));
        required.push(...vocabulary.terms.filter(item => typeof item.name === 'object').map(item => `terms.${item.id}`));
        expect(required.filter(item => !mapped.has(item))).toEqual([]);
    });
});
