import { useIdentity } from './identityContext';

/** Server feature that lets a prerequisite's target branch be changed after it is recorded. */
export const PREREQUISITE_RETARGET_FEATURE = 'delivery-prerequisite-retarget-v1';

/**
 * Whether the signed-in person may edit in a project, mirroring the server rule so controls are
 * offered only to people the server will accept. The server remains the authority.
 */
export const useProjectEditAccess = (projectId: number | null | undefined) => {
    const identity = useIdentity()?.identity;
    const features = identity?.features ?? [];
    if (!identity || identity.access === 'observe' || identity.principal?.kind === 'agent') return { canEdit: false, features };
    const operator = identity.workspace_role === 'owner' || identity.workspace_role === 'operator';
    const local = identity.mode === 'trusted_local' && !identity.principal;
    const member = projectId == null
        ? identity.workspace_role === 'member'
        : ['editor', 'manager'].includes(identity.projects?.[String(projectId)] ?? '');
    return { canEdit: operator || local || member, features };
};
