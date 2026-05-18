import React from 'react';
import './StatusIndicator.css';
const StatusIndicator: React.FC<{status: 'online' | 'offline' | 'error'; label?: string}> = ({ status, label }) => (
    <div className="status-indicator">
        <span className={`status-dot ${status}`} />
        {label && <span className="status-label">{label}</span>}
    </div>
);
export default StatusIndicator;