export const OPEN_COMMAND_MENU_EVENT = 'workchord:open-command-menu';

export const openCommandMenu = () => {
    window.dispatchEvent(new Event(OPEN_COMMAND_MENU_EVENT));
};
