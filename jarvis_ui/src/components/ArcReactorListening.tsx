import React from 'react';
import AudioWaveform from './AudioWaveform';
import PulseRing from './PulseRing';
import GlowCore from './GlowCore';
import ParticleField from './ParticleField';

const ArcReactorListening: React.FC = () => {
    return (
        <div className="arc-reactor-listening">
            <AudioWaveform active={true} />
            <PulseRing count={6} color="rgba(255, 255, 255, 0.6)" />
            <GlowCore brightness={0.9} pulse={true} />
            <ParticleField count={12} />
            <div className="center-text">
                <div className="jarvis-name">J.A.R.V.I.S.</div>
                <div className="jarvis-subtitle">LISTENING</div>
            </div>
        </div>
    );
};

export default ArcReactorListening;