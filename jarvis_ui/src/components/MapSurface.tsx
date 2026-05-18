import React from 'react';
import './MapSurface.css';
const MapSurface: React.FC<{data?: any; onClose: () => void}> = ({ data, onClose }) => (
    <div className="map-surface">
        <button onClick={onClose} className="task-surface-close">Close</button>
        <div className="map-container" id="jarvis-map-container" />
    </div>
);
export default MapSurface;