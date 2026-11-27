import { useIdentity } from './identityContext';

/** Server feature that lets a prerequisite's target branch be changed after it is recorded. */
export const PREREQUISITE_RETARGET_FEATURE = 'delivery-prerequisite-retarget-v1';

/**
 * Whether the signed-in person may decide in a project (replace or supersede work), mirroring the server rule:
 * an operator, a trusted-local browser, or the project's manager. The server remains the authority.
 */
export const useProjectManageAccess = (projectId: number | null | undefined) => {
    const identity = useIdentity()?.identity;
    if (!identity || identity.access === 'observe' || identity.principal?.kind === 'agent') return false;
    const operator = identity.workspace_role === 'owner' || identity.workspace_role === 'operator';
    const local = identity.mode === 'trusted_local' && !identity.principal;
    return operator || local || (projectId != null && identity.projects?.[String(projectId)] === 'manager');
};

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
