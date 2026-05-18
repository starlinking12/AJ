import React from 'react';
import PulseRing from './PulseRing';
import GlowCore from './GlowCore';

const ArcReactorError: React.FC = () => {
    return (
        <div className="arc-reactor-error">
            <PulseRing count={3} color="rgba(255, 50, 50, 0.6)" speed={4} />
            <GlowCore brightness={0.4} pulse={true} color="rgba(255, 80, 80, 0.8)" />
            <div className="center-text">
                <div className="jarvis-name error-text">J.A.R.V.I.S.</div>
                <div className="jarvis-subtitle error-text">ERROR</div>
            </div>
        </div>
    );
};

export default ArcReactorError;