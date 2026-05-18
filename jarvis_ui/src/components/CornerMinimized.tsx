import React from 'react';
import GlowCore from './GlowCore';

const CornerMinimized: React.FC = () => {
    return (
        <div className="corner-minimized" style={{ width: 80, height: 80 }}>
            <GlowCore brightness={0.5} pulse={true} />
        </div>
    );
};

export default CornerMinimized;