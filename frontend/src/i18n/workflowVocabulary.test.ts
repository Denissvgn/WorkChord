/// <reference types="node" />

import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { describe, expect, it } from 'vitest';
import { englishResources } from './resources.en';
import { russianResources } from './resources.ru';

type Localized = { en: string; ru: string };
type Entry = { id: string; name: Localized | string; group?: Localized; description?: Localized };
type Vocabulary = Record<'roles' | 'task_states' | 'actions' | 'queues' | 'pipeline_stages', Entry[]>;

// The same vocabulary generates the shared block in every agent role skill.
const vocabulary = JSON.parse(
    readFileSync(resolve(process.cwd(), '../config/workflow-vocabulary.json'), 'utf8'),
) as Vocabulary;

// Interface labels that must use the shared names. When a screen adopts
// another vocabulary term, add its keys here in the same change.
const LABEL_KEYS: Array<{ section: keyof Vocabulary; id: string; field: 'name' | 'group' | 'description'; keys: string[] }> = [
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
    it.each(LABEL_KEYS.flatMap(entry => entry.keys.flatMap(key => (['en', 'ru'] as const).map(language => ({
        ...entry, key, language,
    })))))('$language $key uses the shared name for $section $id', ({ section, id, field, key, language }) => {
        const term = vocabulary[section].find(item => item.id === id);
        expect(term, `${section}.${id} is missing from the vocabulary`).toBeDefined();
        const names = term?.[field] as Localized | undefined;
        expect(lookup(catalogs[language], key)).toBe(names?.[language]);
    });

    it('maps every role, task state, action, queue and pipeline stage to an interface label', () => {
        const mapped = new Set(LABEL_KEYS.map(entry => `${entry.section}.${entry.id}`));
        const required = (['roles', 'task_states', 'actions', 'queues', 'pipeline_stages'] as const)
            .flatMap(section => vocabulary[section].map(item => `${section}.${item.id}`));
        expect(required.filter(item => !mapped.has(item))).toEqual([]);
    });
});
