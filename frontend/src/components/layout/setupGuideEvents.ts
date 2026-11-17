// The Get started panel on Overview reopens on this event, from any page.
export const OPEN_SETUP_GUIDE_EVENT = 'workchord:open-setup-guide';

export const openSetupGuide = () => {
    window.dispatchEvent(new Event(OPEN_SETUP_GUIDE_EVENT));
};
