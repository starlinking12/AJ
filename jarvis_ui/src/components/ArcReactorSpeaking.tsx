import React from 'react';
import AudioWaveform from './AudioWaveform';
import PulseRing from './PulseRing';
import GlowCore from './GlowCore';
import ParticleField from './ParticleField';

const ArcReactorSpeaking: React.FC = () => {
    return (
        <div className="arc-reactor-speaking">
            <AudioWaveform active={true} />
            <PulseRing count={6} color="var(--arc-reactor-gold)" />
            <GlowCore brightness={1.0} pulse={true} pulseSpeed={1.5} />
            <ParticleField count={16} speed={1.5} />
            <div className="center-text">
                <div className="jarvis-name">J.A.R.V.I.S.</div>
                <div className="jarvis-subtitle">SPEAKING</div>
            </div>
        </div>
    );
};

export default ArcReactorSpeaking;