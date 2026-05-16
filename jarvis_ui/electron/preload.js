const { contextBridge, ipcRenderer } = require('electron');

contextBridge.exposeInMainWorld('jarvisAPI', {
    getState: () => ipcRenderer.invoke('get-state'),
    setState: (state) => ipcRenderer.invoke('set-state', state),
    minimizeToCorner: () => ipcRenderer.invoke('minimize-to-corner'),
    restoreToCenter: () => ipcRenderer.invoke('restore-to-center'),
    onStateChange: (callback) => {
        ipcRenderer.on('state-changed', (event, state) => callback(state));
    },
});