export const ipc = {
    getState: async () => {
        if (window.jarvisAPI) return window.jarvisAPI.getState();
        return 'sleeping';
    },
    setState: async (state: string) => {
        if (window.jarvisAPI) return window.jarvisAPI.setState(state);
        return true;
    },
    minimizeToCorner: async () => {
        if (window.jarvisAPI) return window.jarvisAPI.minimizeToCorner();
        return true;
    },
    restoreToCenter: async () => {
        if (window.jarvisAPI) return window.jarvisAPI.restoreToCenter();
        return true;
    },
};