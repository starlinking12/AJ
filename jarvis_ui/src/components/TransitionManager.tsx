import React from 'react';
import './TransitionManager.css';

interface TransitionManagerProps {
    active: boolean;
}

const TransitionManager: React.FC<TransitionManagerProps> = ({ active }) => {
    if (!active) return null;

    return (
        <div className="transition-overlay">
            <div className="transition-circle" />
        </div>
    );
};

export default TransitionManager;