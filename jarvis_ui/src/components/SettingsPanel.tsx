import React from 'react';
import './SettingsPanel.css';
const SettingsPanel: React.FC<{onClose: () => void}> = ({ onClose }) => (
    <div className="settings-panel">
        <h2>Settings</h2>
        <button onClick={onClose} className="task-surface-close">Close</button>
    </div>
);
export default SettingsPanel;