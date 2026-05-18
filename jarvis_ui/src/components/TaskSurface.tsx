import React from 'react';
import MapSurface from '../surfaces/MapSurface';
import NewsSurface from '../surfaces/NewsSurface';
import WeatherSurface from '../surfaces/WeatherSurface';
import CameraSurface from '../surfaces/CameraSurface';
import BrowserSurface from '../surfaces/BrowserSurface';
import MusicSurface from '../surfaces/MusicSurface';
import SystemSurface from '../surfaces/SystemSurface';
import './TaskSurface.css';

interface TaskSurfaceProps {
    taskType: string;
    onClose: () => void;
    taskData?: any;
}

const TaskSurface: React.FC<TaskSurfaceProps> = ({ taskType, onClose, taskData }) => {
    const renderSurface = () => {
        switch (taskType) {
            case 'map': return <MapSurface data={taskData} onClose={onClose} />;
            case 'news': return <NewsSurface data={taskData} onClose={onClose} />;
            case 'weather': return <WeatherSurface data={taskData} onClose={onClose} />;
            case 'camera': return <CameraSurface onClose={onClose} />;
            case 'browser': return <BrowserSurface data={taskData} onClose={onClose} />;
            case 'music': return <MusicSurface data={taskData} onClose={onClose} />;
            case 'system': return <SystemSurface data={taskData} onClose={onClose} />;
            default: return null;
        }
    };

    return (
        <div className="task-surface-overlay">
            <div className="task-surface-content">
                {renderSurface()}
            </div>
        </div>
    );
};

export default TaskSurface;