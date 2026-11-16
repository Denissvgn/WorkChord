import type { ReactNode } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { mapLegacyPath } from './legacyPaths';
import { legacySwitches } from './legacySwitches';

export function LegacyRedirect({ children }: { children: ReactNode }) {
    const { pathname, search, hash } = useLocation();
    const path = pathname.length > 1 ? pathname.replace(/\/$/, '') : pathname;
    const destination = legacySwitches[path] ? mapLegacyPath(pathname, search) : null;
    return destination ? <Navigate to={`${destination}${hash}`} replace /> : <>{children}</>;
}
