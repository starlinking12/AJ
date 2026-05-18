import React from 'react';
import './CameraSurface.css';
const CameraSurface: React.FC<{onClose: () => void}> = ({ onClose }) => (
    <div className="camera-surface">
        <button onClick={onClose} className="task-surface-close">Close Camera</button>
        <div className="camera-feed" id="jarvis-camera-feed" />
    </div>
);
export default CameraSurface;