// The first-run setup panel will listen for this event. Until it exists, nothing does.
export const OPEN_SETUP_GUIDE_EVENT = 'workchord:open-setup-guide';

export const openSetupGuide = () => {
    window.dispatchEvent(new Event(OPEN_SETUP_GUIDE_EVENT));
};
