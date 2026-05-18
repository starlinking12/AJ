import React from 'react';
import './BootSplash.css';
const BootSplash: React.FC = () => (
    <div className="boot-splash">
        <div className="boot-reactor">
            <div className="boot-core" />
        </div>
        <div className="boot-text">J.A.R.V.I.S.</div>
        <div className="boot-subtitle">Initializing...</div>
    </div>
);
export default BootSplash;