import { useCallback, useEffect, useRef, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useLocation, useNavigate } from 'react-router-dom';
import { AllIterationsDrawer } from '../iteration/AllIterationsDrawer';
import { IterationEditorDrawer } from '../iteration/IterationEditorDrawer';
import { useIterationPanels } from '../../features/planningMasters/useIterationPanels';
import { useScopeLink, useLinkScope } from '../../features/scope/useScopeLink';
import { iterationService } from '../../services/iterationService';
import type { Iteration } from '../../types/iteration';

/**
 * The drawers that manage iterations from Plan: every iteration of the scope's project, and the
 * form that creates or edits one. Creating or opening an iteration puts it in scope.
 */
export const PlanIterationDrawers = () => {
    const panels = useIterationPanels();
    const navigate = useNavigate();
    const { pathname, search } = useLocation();
    const scopeLink = useScopeLink();
    const { project } = useLinkScope();
    // feedback-policy: query loading,error,retry,empty - the drawers own their states; a missing iteration shows no form.
    const { data: iterations } = useQuery({ queryKey: ['iterations'], queryFn: iterationService.getAll });

    // The iteration comes with its project unless All projects is chosen, the same rule as choosing it in the scope bar.
    const planLink = useCallback((iteration: Iteration) => scopeLink('/plan', {
        project: project === 'all' ? 'all' : iteration.project_id ?? 'all',
        iteration: iteration.id,
    }), [project, scopeLink]);
    const putInScope = (iteration: Iteration) => navigate(planLink(iteration), { replace: true });

    // A saved iteration is put in scope and the form's parameters leave the link. The form
    // remembers the iteration while the link still carries the form, and the shell then writes
    // that scope into the link it had; so the link is checked until it is the plan's own.
    const [saved, setSaved] = useState<Iteration | null>(null);
    const settled = useRef<Iteration | null>(null);
    useEffect(() => {
        if (!saved || settled.current === saved) return;
        const target = planLink(saved);
        if (`${pathname}${search}` === target) { settled.current = saved; return; }
        navigate(target, { replace: true });
    }, [navigate, pathname, planLink, saved, search]);

    const scopeProjectId = typeof project === 'number' ? project : undefined;
    const editing = panels.editingId === null ? undefined : iterations?.find(item => item.id === panels.editingId);

    if (panels.creating) {
        return (
            <IterationEditorDrawer
                defaultProjectId={scopeProjectId}
                onClose={panels.closeEditor}
                onSaved={iteration => { if (iteration) setSaved(iteration); else panels.closeEditor(); }}
            />
        );
    }
    if (editing) {
        return <IterationEditorDrawer iteration={editing} onClose={panels.closeEditor} onSaved={panels.closeEditor} />;
    }
    if (panels.listOpen && panels.editingId === null) {
        return (
            <AllIterationsDrawer
                projectId={scopeProjectId}
                onOpen={putInScope}
                onEdit={iteration => panels.openEdit(iteration.id)}
                onClose={panels.closeList}
            />
        );
    }
    return null;
};
