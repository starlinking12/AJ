import React from 'react';
import './BrowserSurface.css';
const BrowserSurface: React.FC<{data?: any; onClose: () => void}> = ({ data, onClose }) => (
    <div className="browser-surface">
        <button onClick={onClose} className="task-surface-close">Close</button>
        <iframe src={data?.url || 'about:blank'} className="browser-iframe" title="Jarvis Browser" />
    </div>
);
export default BrowserSurface;