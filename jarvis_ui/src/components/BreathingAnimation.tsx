import React from 'react';

const BreathingAnimation: React.FC = () => {
    return (
        <div className="breathing-animation">
            <div className="breath-ring ring-1" />
            <div className="breath-ring ring-2" />
            <div className="breath-ring ring-3" />
            <div className="breath-aura" />
        </div>
    );
};

export default BreathingAnimation;