import React from 'react';
import PulseRing from './PulseRing';
import GlowCore from './GlowCore';
import ParticleField from './ParticleField';

const ArcReactorThinking: React.FC = () => {
    return (
        <div className="arc-reactor-thinking">
            <PulseRing count={4} speed={3} />
            <GlowCore brightness={0.7} pulse={true} pulseSpeed={2} />
            <ParticleField count={6} speed={2} />
            <div className="center-text">
                <div className="jarvis-name">J.A.R.V.I.S.</div>
                <div className="jarvis-subtitle">THINKING</div>
            </div>
        </div>
    );
};

export default ArcReactorThinking;