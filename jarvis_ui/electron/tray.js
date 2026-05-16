const { Tray, Menu, nativeImage } = require('electron');
const path = require('path');

function createTray(mainWindow) {
    const iconPath = path.join(__dirname, '..', 'src', 'assets', 'icons', 'tray_icon.png');
    const icon = nativeImage.createFromPath(iconPath);
    const tray = new Tray(icon.resize({ width: 16, height: 16 }));

    const contextMenu = Menu.buildFromTemplate([
        {
            label: 'Show J.A.R.V.I.S.',
            click: () => mainWindow.show()
        },
        {
            label: 'Hide J.A.R.V.I.S.',
            click: () => mainWindow.hide()
        },
        { type: 'separator' },
        {
            label: 'Quit',
            click: () => {
                app.isQuitting = true;
                app.quit();
            }
        }
    ]);

    tray.setToolTip('J.A.R.V.I.S.');
    tray.setContextMenu(contextMenu);
    return tray;
}

module.exports = { createTray };