const { app, BrowserWindow, Tray, Menu, ipcMain, nativeImage, screen } = require('electron');
const path = require('path');

let mainWindow = null;
let tray = null;
let isQuitting = false;

function createWindow() {
    const { width, height } = screen.getPrimaryDisplay().workAreaSize;

    mainWindow = new BrowserWindow({
        width: width,
        height: height,
        transparent: true,
        frame: false,
        alwaysOnTop: true,
        skipTaskbar: true,
        resizable: false,
        hasShadow: false,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
        },
    });

    mainWindow.setIgnoreMouseEvents(true, { forward: true });
    mainWindow.loadFile(path.join(__dirname, '..', 'src', 'index.html'));
    mainWindow.setVisibleOnAllWorkspaces(true);
    mainWindow.setAlwaysOnTop(true, 'screen-saver');

    mainWindow.on('close', (event) => {
        if (!isQuitting) {
            event.preventDefault();
            mainWindow.hide();
        }
    });
}

function createTray() {
    const iconPath = path.join(__dirname, '..', 'src', 'assets', 'icons', 'tray_icon.png');
    const icon = nativeImage.createFromPath(iconPath);
    tray = new Tray(icon.resize({ width: 16, height: 16 }));

    const contextMenu = Menu.buildFromTemplate([
        {
            label: 'Show J.A.R.V.I.S.',
            click: () => {
                if (mainWindow) mainWindow.show();
            }
        },
        {
            label: 'Hide J.A.R.V.I.S.',
            click: () => {
                if (mainWindow) mainWindow.hide();
            }
        },
        { type: 'separator' },
        {
            label: 'Quit J.A.R.V.I.S.',
            click: () => {
                isQuitting = true;
                app.quit();
            }
        }
    ]);

    tray.setToolTip('J.A.R.V.I.S.');
    tray.setContextMenu(contextMenu);

    tray.on('click', () => {
        if (mainWindow) {
            mainWindow.isVisible() ? mainWindow.hide() : mainWindow.show();
        }
    });
}

ipcMain.handle('get-state', () => {
    return global.jarvisState || 'sleeping';
});

ipcMain.handle('set-state', (event, state) => {
    global.jarvisState = state;
    return true;
});

ipcMain.handle('minimize-to-corner', () => {
    if (mainWindow) {
        mainWindow.setSize(100, 100);
        const { width, height } = screen.getPrimaryDisplay().workAreaSize;
        mainWindow.setPosition(width - 120, height - 120);
    }
    return true;
});

ipcMain.handle('restore-to-center', () => {
    if (mainWindow) {
        const { width, height } = screen.getPrimaryDisplay().workAreaSize;
        mainWindow.setSize(width, height);
        mainWindow.center();
    }
    return true;
});

app.whenReady().then(() => {
    createWindow();
    createTray();
    global.jarvisState = 'sleeping';
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('before-quit', () => {
    isQuitting = true;
});