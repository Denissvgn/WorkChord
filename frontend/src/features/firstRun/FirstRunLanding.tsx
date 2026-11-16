import { useEffect, useRef } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useLocation, useNavigate, useNavigationType } from 'react-router-dom';
import { OPEN_SETUP_GUIDE_EVENT } from '../../components/layout/setupGuideEvents';
import { projectService } from '../../services/projectService';
import { useGetStartedVisibility } from './getStartedVisibility';

const OVERVIEW_PATH = '/';

/**
 * Two ways into the Get started panel on Overview. A workspace with no project opens on
 * Overview, whatever page was requested first; later navigation is left alone. Help, Setup
 * guide reopens the panel from any page.
 */
export const FirstRunLanding = () => {
    const location = useLocation();
    const navigate = useNavigate();
    const reopen = useGetStartedVisibility(state => state.reopen);
    const navigationType = useNavigationType();
    const firstLocation = useRef(location.key);
    const movedOn = useRef(false);
    const decided = useRef(false);
    // A page that rewrites its own address (scope parameters, a renamed path) replaces it; only
    // a new entry or Back and Forward mean someone has moved on.
    useEffect(() => {
        if (location.key !== firstLocation.current && navigationType !== 'REPLACE') movedOn.current = true;
    }, [location.key, navigationType]);
    const pathname = useRef(location.pathname);
    useEffect(() => { pathname.current = location.pathname; }, [location.pathname]);
    // feedback-policy: query loading,error,retry,empty - without an answer the requested page stays; each page shows its own states.
    const projects = useQuery({ queryKey: ['projects'], queryFn: () => projectService.getAll(), staleTime: 60000 });

    useEffect(() => {
        if (decided.current) return;
        // Someone already moved on from the first page, or the projects cannot be read: keep the page.
        if (movedOn.current || projects.isError) {
            decided.current = true;
            return;
        }
        if (!projects.data) return;
        decided.current = true;
        if (projects.data.length === 0 && location.pathname !== OVERVIEW_PATH) {
            navigate(OVERVIEW_PATH, { replace: true });
        }
    }, [location.key, location.pathname, navigate, projects.data, projects.isError]);

    useEffect(() => {
        const open = () => {
            reopen();
            if (pathname.current !== OVERVIEW_PATH) navigate(OVERVIEW_PATH);
        };
        window.addEventListener(OPEN_SETUP_GUIDE_EVENT, open);
        return () => window.removeEventListener(OPEN_SETUP_GUIDE_EVENT, open);
    }, [navigate, reopen]);

    return null;
};
