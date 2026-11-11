import type { TFunction } from 'i18next';

/** A way back from a write the user just made. */
export interface MutationUndo {
    run: () => Promise<unknown>;
    /** Announced once the undo has been applied. */
    done?: string;
}

/**
 * Put on a mutation's `meta` to announce its result. One listener shows the
 * success toast, so every write ends with the same visible, announced message;
 * errors stay where they happened (inline) and in the error toast.
 */
export interface MutationFeedbackMeta extends Record<string, unknown> {
    success?: string | ((data: unknown, variables: unknown) => string | null | undefined);
    undo?: (data: unknown, variables: unknown) => MutationUndo | null | undefined;
}

export type FeedbackAction = 'created' | 'saved' | 'deleted';
export type FeedbackKind = 'project' | 'release' | 'milestone' | 'task' | 'triageItem' | 'teamMember' | 'profile' | 'initiative' | 'update' | 'absence';

/** "Created task “Fix login”." The object is named so the message stands on its own. */
export const feedbackMessage = (t: TFunction, action: FeedbackAction, kind: FeedbackKind, name?: string | null) => (
    name ? t(`feedback.${action}`, { kind: t(`feedback.kinds.${kind}`), name }) : t(`feedback.${action}Unnamed`, { kind: t(`feedback.kinds.${kind}`) })
);
