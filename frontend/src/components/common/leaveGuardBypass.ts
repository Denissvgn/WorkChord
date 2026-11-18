let bypassing = false;

/** Runs a navigation that an app action starts itself, so unsaved-leave guards do not ask about it. */
export const navigateWithoutLeaveGuards = (navigate: () => void) => {
    bypassing = true;
    try { navigate(); } finally { bypassing = false; }
};

/** True while a navigation started by navigateWithoutLeaveGuards is being checked by the router. */
export const leaveGuardsBypassed = () => bypassing;
