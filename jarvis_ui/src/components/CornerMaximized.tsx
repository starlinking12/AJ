import React from 'react';
import GlowCore from './GlowCore';
import PulseRing from './PulseRing';

const CornerMaximized: React.FC = () => {
    return (
        <div className="corner-maximized" style={{ width: 80, height: 80 }}>
            <PulseRing count={3} />
            <GlowCore brightness={0.7} pulse={true} />
        </div>
    );
};

export default CornerMaximized;