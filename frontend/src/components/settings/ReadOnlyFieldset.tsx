import type { ReactNode } from 'react';
import { useSettingsReadOnly } from './sharedUnlock';

/**
 * Wraps editing controls so they are disabled while the surrounding settings
 * are read-only. It adds no box of its own, so the layout is unchanged.
 */
export const ReadOnlyFieldset = ({ children, disabled = false }: { children: ReactNode; disabled?: boolean }) => {
    const readOnly = useSettingsReadOnly();
    return (
        <fieldset
            disabled={disabled || readOnly !== null}
            aria-describedby={readOnly?.noteId}
            className="contents"
        >
            {children}
        </fieldset>
    );
};
