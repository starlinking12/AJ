import React from 'react';
import './MusicSurface.css';
const MusicSurface: React.FC<{data?: any; onClose: () => void}> = ({ data, onClose }) => (
    <div className="music-surface">
        <button onClick={onClose} className="task-surface-close">Close</button>
        <div className="music-player">
            <div className="music-track">{data?.track || 'No track playing'}</div>
            <div className="music-artist">{data?.artist || ''}</div>
        </div>
    </div>
);
export default MusicSurface;