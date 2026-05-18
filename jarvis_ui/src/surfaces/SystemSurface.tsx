import React from 'react';
import './SystemSurface.css';
const SystemSurface: React.FC<{data?: any; onClose: () => void}> = ({ data, onClose }) => (
    <div className="system-surface">
        <button onClick={onClose} className="task-surface-close">Close</button>
        <pre className="system-output">{data?.output || 'Command executed, Sir.'}</pre>
    </div>
);
export default SystemSurface;