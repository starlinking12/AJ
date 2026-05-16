import React from 'react';
import BreathingAnimation from './BreathingAnimation';
import PulseRing from './PulseRing';
import GlowCore from './GlowCore';
import ParticleField from './ParticleField';

const ArcReactorIdle: React.FC = () => {
    return (
        <div className="arc-reactor-idle">
            <BreathingAnimation />
            <PulseRing count={6} />
            <GlowCore brightness={0.5} pulse={true} />
            <ParticleField count={8} />
            <div className="center-text">
                <div className="jarvis-name">J.A.R.V.I.S.</div>
                <div className="jarvis-subtitle">ONLINE</div>
            </div>
        </div>
    );
};

export default ArcReactorIdle;