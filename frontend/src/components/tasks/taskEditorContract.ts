import type { Task, TaskCreate, TaskStatus, TaskUpdate } from '../../types/task';
import { getApiErrorMessage } from '../../utils/apiError';

export type TaskEditorSection = 'essential' | 'planning' | 'advanced' | 'internal';
export type TaskEditorAvailability =
    | 'all-editors'
    | 'existing-task'
    | 'preserved-metadata';

export interface TaskEditorValues {
    title: string;
    description: string;
    priority: number;
    effort_days: number;
    effort_hours: number;
    assignee_id: number | null;
    project_id: number | null;
    milestone_id: number | null;
    parent_id: number | null;
    depends_on: number[];
    is_optional: boolean;
    is_deferred: boolean;
    tags: string[];
    min_start_date: string | null;
    max_end_date: string | null;
    external_key: string | null;
    source: string | null;
    source_url: string | null;
    status: TaskStatus;
    expected_version: number | null;
}

interface TaskEditorDefaultsContext {
    task?: Task;
    parentId?: number | null;
    parentPriority?: number;
    parentProjectId?: number | null;
    parentMilestoneId?: number | null;
}

interface TaskEditorFieldDefinition<K extends keyof TaskEditorValues> {
    section: TaskEditorSection;
    availability: TaskEditorAvailability;
    defaultValue: (context: TaskEditorDefaultsContext) => TaskEditorValues[K];
}

const effectiveEffortDays = (task?: Task): number => {
    if (!task) return 1;
    if (task.children?.length) {
        return task.children.reduce((total, child) => total + effectiveEffortDays(child), 0);
    }
    return task.effort_days || 1;
};

/**
 * Canonical task-editor contract. Both Tasks and Gantt use these defaults and
 * availability rules; Gantt reuses TaskForm instead of maintaining a second
 * list of fields. Derived schedule dates stay read-only, while description,
 * constraints, labels, and dependencies are editable in direct and sandbox
 * modes. Provider/source fields are preserved until a dedicated UI exists.
 */
export const TASK_EDITOR_FIELD_SCHEMA: {
    [K in keyof TaskEditorValues]: TaskEditorFieldDefinition<K>;
} = {
    title: {
        section: 'essential',
        availability: 'all-editors',
        defaultValue: ({ task }) => task?.title ?? '',
    },
    description: {
        section: 'essential',
        availability: 'all-editors',
        defaultValue: ({ task }) => task?.description ?? '',
    },
    priority: {
        section: 'essential',
        availability: 'all-editors',
        defaultValue: ({ task, parentPriority }) => task?.priority ?? parentPriority ?? 1,
    },
    effort_days: {
        section: 'planning',
        availability: 'all-editors',
        defaultValue: ({ task }) => effectiveEffortDays(task),
    },
    effort_hours: {
        section: 'planning',
        availability: 'all-editors',
        defaultValue: ({ task }) => effectiveEffortDays(task) * 8,
    },
    assignee_id: {
        section: 'essential',
        availability: 'all-editors',
        defaultValue: ({ task }) => task?.assignee?.id ?? null,
    },
    project_id: {
        section: 'essential',
        availability: 'all-editors',
        defaultValue: ({ task, parentProjectId }) => task?.project_id ?? parentProjectId ?? null,
    },
    milestone_id: {
        section: 'planning',
        availability: 'all-editors',
        defaultValue: ({ task, parentId, parentMilestoneId }) => (
            task?.milestone_id ?? (parentId ? parentMilestoneId ?? null : null)
        ),
    },
    parent_id: {
        section: 'internal',
        availability: 'preserved-metadata',
        defaultValue: ({ task, parentId }) => parentId ?? task?.parent_id ?? null,
    },
    depends_on: {
        section: 'advanced',
        availability: 'all-editors',
        defaultValue: ({ task }) => task?.dependencies ?? [],
    },
    is_optional: {
        section: 'advanced',
        availability: 'all-editors',
        defaultValue: ({ task }) => task?.is_optional ?? false,
    },
    is_deferred: {
        section: 'advanced',
        availability: 'all-editors',
        defaultValue: ({ task }) => task?.is_deferred ?? false,
    },
    tags: {
        section: 'advanced',
        availability: 'all-editors',
        defaultValue: ({ task }) => task?.tags ?? [],
    },
    min_start_date: {
        section: 'planning',
        availability: 'all-editors',
        defaultValue: ({ task }) => task?.min_start_date ?? null,
    },
    max_end_date: {
        section: 'planning',
        availability: 'all-editors',
        defaultValue: ({ task }) => task?.max_end_date ?? null,
    },
    external_key: {
        section: 'internal',
        availability: 'preserved-metadata',
        defaultValue: ({ task }) => task?.external_key ?? null,
    },
    source: {
        section: 'internal',
        availability: 'preserved-metadata',
        defaultValue: ({ task }) => task?.source ?? null,
    },
    source_url: {
        section: 'internal',
        availability: 'preserved-metadata',
        defaultValue: ({ task }) => task?.source_url ?? null,
    },
    status: {
        section: 'advanced',
        availability: 'existing-task',
        defaultValue: ({ task }) => task?.status ?? 'planned',
    },
    expected_version: {
        section: 'internal',
        availability: 'existing-task',
        defaultValue: ({ task }) => task?.version ?? null,
    },
};

export const buildTaskEditorDefaults = (
    context: TaskEditorDefaultsContext = {},
): TaskEditorValues => Object.fromEntries(
    Object.entries(TASK_EDITOR_FIELD_SCHEMA).map(([key, definition]) => [
        key,
        definition.defaultValue(context),
    ]),
) as unknown as TaskEditorValues;

export type TaskEditorValidationCode =
    | 'titleRequired'
    | 'priorityRange'
    | 'effortRequired'
    | 'dateOrder'
    | 'assigneeOutsideIteration';

export interface TaskEditorValidationIssue {
    field: keyof TaskEditorValues;
    code: TaskEditorValidationCode;
}

export const validateTaskEditor = (
    values: TaskEditorValues,
    iterationAssigneeIds?: ReadonlySet<number>,
): TaskEditorValidationIssue[] => {
    const issues: TaskEditorValidationIssue[] = [];
    if (!values.title.trim()) issues.push({ field: 'title', code: 'titleRequired' });
    if (!Number.isFinite(values.priority) || values.priority < 1 || values.priority > 10) {
        issues.push({ field: 'priority', code: 'priorityRange' });
    }
    if (!Number.isFinite(values.effort_days) || values.effort_days < 0.1) {
        issues.push({ field: 'effort_days', code: 'effortRequired' });
    }
    if (
        values.min_start_date
        && values.max_end_date
        && values.min_start_date > values.max_end_date
    ) {
        issues.push({ field: 'max_end_date', code: 'dateOrder' });
    }
    if (
        values.assignee_id !== null
        && iterationAssigneeIds
        && !iterationAssigneeIds.has(values.assignee_id)
    ) {
        issues.push({ field: 'assignee_id', code: 'assigneeOutsideIteration' });
    }
    return issues;
};

const mutationFields = (values: TaskEditorValues): TaskCreate => ({
    title: values.title.trim(),
    description: values.description,
    priority: values.priority,
    effort_days: values.effort_days,
    effort_hours: values.effort_hours,
    assignee_id: values.assignee_id,
    project_id: values.project_id,
    milestone_id: values.milestone_id,
    parent_id: values.parent_id,
    depends_on: values.depends_on,
    is_optional: values.is_optional,
    is_deferred: values.is_deferred,
    tags: values.tags,
    min_start_date: values.min_start_date,
    max_end_date: values.max_end_date,
    external_key: values.external_key,
    source: values.source,
    source_url: values.source_url,
});

export const toTaskCreate = (values: TaskEditorValues): TaskCreate => mutationFields(values);

export const toTaskUpdate = (
    values: TaskEditorValues,
    options: { includeStatus?: boolean } = {},
): TaskUpdate => ({
    ...mutationFields(values),
    status: options.includeStatus ? values.status : undefined,
    expected_version: values.expected_version ?? undefined,
});

export interface TaskConflictMetadata {
    id: number;
    version: number;
    title: string;
    status: TaskStatus;
    updated_at: string | null;
}

export type TaskEditorServerError =
    | {
        kind: 'version-conflict';
        expectedVersion: number;
        currentTask: TaskConflictMetadata;
    }
    | { kind: 'generic'; message: string };

export const mapTaskEditorServerError = (
    error: unknown,
    fallback: string,
): TaskEditorServerError => {
    const response = (error as {
        response?: { status?: number; data?: { detail?: unknown } };
    } | null)?.response;
    const detail = response?.data?.detail as {
        code?: string;
        expected_version?: number;
        current_task?: TaskConflictMetadata;
    } | undefined;
    if (
        response?.status === 409
        && detail?.code === 'task_version_conflict'
        && typeof detail.expected_version === 'number'
        && detail.current_task
        && typeof detail.current_task.version === 'number'
    ) {
        return {
            kind: 'version-conflict',
            expectedVersion: detail.expected_version,
            currentTask: detail.current_task,
        };
    }
    return { kind: 'generic', message: getApiErrorMessage(error, fallback) };
};
